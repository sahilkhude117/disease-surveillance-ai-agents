"""Reporting plugin for generating disease surveillance reports.

MIGRATED FROM AZURE:
- Replaced Azure Blob Storage with local file storage and optional Supabase Storage
- Removed semantic_kernel dependency
- Uses simple file-based storage for hackathon demo
"""

import json
import uuid
import os
import tempfile
from datetime import datetime
from pathlib import Path

# Optional: Supabase storage support
try:
    from supabase import create_client, Client
    from config.settings import settings
    SUPABASE_STORAGE_AVAILABLE = settings.is_supabase_configured()
except ImportError:
    SUPABASE_STORAGE_AVAILABLE = False
    print("⚠️  Supabase not available. Using local storage only.")


class ReportingPlugin:
    """Plugin for creating and managing surveillance reports."""
    
    def __init__(self, connection_string, storage_type=None):
        """Initialize the reporting plugin.
        
        Args:
            connection_string: Database connection string
            storage_type: Optional storage type ('local' or 'supabase')
        """
        self.connection_string = connection_string
        self.storage_type = storage_type or os.getenv("REPORT_STORAGE_TYPE", "local")
        self.report_directory = os.getenv("REPORT_STORAGE_PATH", "./reports")
        
        # Create report directory if it doesn't exist
        try:
            Path(self.report_directory).mkdir(parents=True, exist_ok=True)
            print(f"✅ Report directory ready: {self.report_directory}")
        except Exception as e:
            print(f"⚠️  Error creating report directory: {e}")
            self.report_directory = "."
        
        # Initialize Supabase client if configured
        self.supabase_client = None
        self.supabase_bucket = None
        if SUPABASE_STORAGE_AVAILABLE and self.storage_type == "supabase":
            try:
                from config.settings import get_supabase_client, settings
                self.supabase_client = get_supabase_client()
                self.supabase_bucket = settings.SUPABASE_STORAGE_BUCKET
                print(f"✅ Supabase storage initialized: {self.supabase_bucket}")
            except Exception as e:
                print(f"⚠️  Supabase storage not available, using local: {e}")
                self.storage_type = "local"
        else:
            print(f"📁 Using local file storage: {self.report_directory}")
    
    def save_surveillance_report(self, report_content: str, session_id: str, 
                                conversation_id: str, report_title: str = None,
                                report_type: str = "comprehensive") -> str:
        """Saves a surveillance report to markdown/PDF and uploads to storage.
        
        Args:
            report_content: The report content in markdown format
            session_id: The session ID
            conversation_id: The conversation ID
            report_title: Optional report title
            report_type: Type of report (comprehensive, anomaly, prediction, alert)
            
        Returns:
            JSON string with result information
        """
        print(f"\n==== SURVEILLANCE REPORT GENERATION STARTED ====")
        print(f"Report length: {len(report_content)} characters")
        print(f"Session ID: {session_id}")
        print(f"Conversation ID: {conversation_id}")
        print(f"Report type: {report_type}")
        
        try:
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            report_id = str(uuid.uuid4())[:8]
            md_filename = f"surveillance_report_{report_type}_{timestamp}_{report_id}.md"
            md_filepath = os.path.join(self.report_directory, md_filename)
            
            # Save markdown file
            print(f"Saving report to file: {md_filepath}")
            with open(md_filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"Successfully saved markdown report: {md_filepath}")
            
            # Upload to Azure Storage
            blob_url = None
            try:
                if self.blob_service_client and AZURE_STORAGE_AVAILABLE:
                    print(f"Uploading to Azure Storage...")
                    blob_url = self._upload_to_storage(md_filepath, md_filename)
                    print(f"Successfully uploaded to storage: {blob_url}")
                else:
                    print("No blob service client available, skipping upload")
                    blob_url = f"file://{os.path.abspath(md_filepath)}"
                    print(f"Using local file URL: {blob_url}")
            except Exception as upload_error:
                print(f"Error uploading to storage: {upload_error}")
                blob_url = f"file://{os.path.abspath(md_filepath)}"
                print(f"Using local file URL as fallback: {blob_url}")
            
            # Log to database
            try:
                print(f"Logging report to database...")
                self._log_report_to_database(
                    session_id, conversation_id, md_filename, 
                    blob_url, report_type
                )
                print("Successfully logged report to database")
            except Exception as db_error:
                print(f"Error logging report to database: {db_error}")
            
            # Return success information
            print(f"==== REPORT GENERATION COMPLETED SUCCESSFULLY ====\n")
            return json.dumps({
                "success": True,
                "filename": md_filename,
                "filepath": md_filepath,
                "blob_url": blob_url,
                "session_id": session_id,
                "conversation_id": conversation_id,
                "report_id": report_id,
                "report_type": report_type
            })
            
        except Exception as e:
            print(f"Error in save_surveillance_report: {e}")
            import traceback
            traceback.print_exc()
            print(f"==== REPORT GENERATION FAILED ====\n")
            return json.dumps({
                "error": str(e),
                "success": False,
                "stage": "overall_process"
            })
    
    def _upload_to_storage(self, filepath: str, filename: str) -> str:
        """Uploads a file to Azure Blob Storage.
        
        Args:
            filepath: Local file path
            filename: File name to use in storage
            
        Returns:
            str: URL of the uploaded blob
        """
        try:
            if not self.blob_service_client or not AZURE_STORAGE_AVAILABLE:
                print("Blob service client not available, cannot upload")
                return f"file://{os.path.abspath(filepath)}"
            
            # Create container if it doesn't exist
            try:
                container_client = self.blob_service_client.get_container_client(self.storage_container)
                if not container_client.exists():
                    container_client.create_container()
                    print(f"Created container: {self.storage_container}")
            except Exception as container_error:
                print(f"Error with container: {container_error}")
                container_client = self.blob_service_client.get_container_client(self.storage_container)
            
            # Generate blob path with folder structure
            year = datetime.now().strftime("%Y")
            month = datetime.now().strftime("%m")
            blob_path = f"{year}/{month}/{filename}"
            
            # Upload file
            blob_client = container_client.get_blob_client(blob_path)
            
            if not os.path.exists(filepath):
                print(f"File not found: {filepath}")
                return f"file_not_found:{filepath}"
            
            with open(filepath, "rb") as data:
                blob_client.upload_blob(
                    data, 
                    overwrite=True,
                    content_settings=ContentSettings(content_type="text/markdown")
                )
            
            print(f"File uploaded successfully: {blob_client.url}")
            return blob_client.url
            
        except Exception as e:
            print(f"Error in _upload_to_storage: {e}")
            import traceback
            traceback.print_exc()
            return f"file://{os.path.abspath(filepath)}"
    
    def _log_report_to_database(self, session_id: str, conversation_id: str, 
                               filename: str, blob_url: str, report_type: str):
        """Logs report metadata to database.
        
        Args:
            session_id: The session ID
            conversation_id: The conversation ID
            filename: The report filename
            blob_url: The report URL
            report_type: The type of report
        """
        try:
            import psycopg2
            conn = psycopg2.connect(self.connection_string)
            cursor = conn.cursor()
            
            # PostgreSQL doesn't use stored procedures the same way
            # Use direct insert
            cursor.execute("""
                INSERT INTO surveillance_reports (
                    session_id, conversation_id, filename,
                    blob_url, report_type, created_date
                )
                VALUES (%s, %s, %s, %s, %s, NOW())
                """, (session_id, conversation_id, filename, blob_url, report_type))
            
            conn.commit()
            print("Successfully inserted report using direct SQL")
            
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error in _log_report_to_database: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_reports(self, session_id: str = None, conversation_id: str = None,
                   report_type: str = None, days: int = 30) -> str:
        """Gets surveillance reports with optional filtering.
        
        Args:
            session_id: Optional session ID to filter by
            conversation_id: Optional conversation ID to filter by
            report_type: Optional report type filter
            days: Number of days to look back (default 30)
            
        Returns:
            JSON string with the reports
        """
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
            
            conn = psycopg2.connect(self.connection_string)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Build query parameters
            params = [days]
            where_clauses = ["created_date >= NOW() - INTERVAL '%s days'"]
            
            if session_id:
                where_clauses.append("session_id = %s")
                params.append(session_id)
                
            if conversation_id:
                where_clauses.append("conversation_id = %s")
                params.append(conversation_id)
            
            if report_type:
                where_clauses.append("report_type = ?")
                params.append(report_type)
            
            # Build query
            query = """
                SELECT 
                    report_id, session_id, conversation_id, filename,
                    blob_url, report_type, created_date
                FROM surveillance_reports
            """
            if where_clauses:
                query += " WHERE " + " AND ".join(where_clauses)
            query += " ORDER BY created_date DESC"
            
            # Execute query
            cursor.execute(query, params)
            
            # Fetch results
            columns = [column[0] for column in cursor.description]
            rows = cursor.fetchall()
            
            # Convert to list of dictionaries
            reports = []
            for row in rows:
                reports.append(dict(zip(columns, row)))
            
            cursor.close()
            conn.close()
            
            # Return as JSON
            return json.dumps({
                "query_timestamp": datetime.now().isoformat(),
                "filters": {
                    "session_id": session_id,
                    "conversation_id": conversation_id,
                    "report_type": report_type,
                    "days": days
                },
                "total_reports": len(reports),
                "reports": reports
            }, default=str)
            
        except Exception as e:
            print(f"Error getting reports: {e}")
            import traceback
            traceback.print_exc()
            return json.dumps({"error": str(e)})
    
    def generate_report_from_conversation(self, conversation_id: str, 
                                         session_id: str,
                                         report_type: str = "comprehensive") -> str:
        """Generates a report from conversation history.
        
        Args:
            conversation_id: The conversation ID
            session_id: The session ID
            report_type: Type of report to generate
            
        Returns:
            JSON string with result information
        """
        try:
            # Retrieve thinking logs from database
            import psycopg2
            from psycopg2.extras import RealDictCursor
            
            conn = psycopg2.connect(self.connection_string)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT 
                    agent_name, thinking_stage, thought_content,
                    agent_output, user_query, created_date
                FROM agent_thinking_logs
                WHERE conversation_id = %s
                ORDER BY created_date
            """, (conversation_id,))
            
            rows = cursor.fetchall()
            cursor.close()
            conn.close()
            
            if not rows:
                return json.dumps({
                    "error": "No conversation history found",
                    "success": False
                })
            
            # Build report from conversation
            report_content = f"# Disease Surveillance Report\n\n"
            report_content += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            report_content += f"**Conversation ID:** {conversation_id}\n\n"
            
            report_content += "## Executive Summary\n\n"
            report_content += "This report was automatically generated from a disease surveillance conversation.\n\n"
            
            # Extract and organize content by agent
            agent_outputs = {}
            for row in rows:
                agent_name = row[0]
                agent_output = row[3]
                
                if agent_output and agent_name:
                    if agent_name not in agent_outputs:
                        agent_outputs[agent_name] = []
                    agent_outputs[agent_name].append(agent_output)
            
            # Add sections for each agent
            for agent_name, outputs in agent_outputs.items():
                report_content += f"## {agent_name} Analysis\n\n"
                # Use the most comprehensive output
                best_output = max(outputs, key=len)
                # Clean up the output
                best_output = best_output.replace(f"{agent_name} > ", "")
                report_content += f"{best_output}\n\n"
            
            # Save the report
            result = self.save_surveillance_report(
                report_content=report_content,
                session_id=session_id,
                conversation_id=conversation_id,
                report_title=f"Surveillance Report - {datetime.now().strftime('%Y-%m-%d')}",
                report_type=report_type
            )
            
            return result
            
        except Exception as e:
            print(f"Error generating report from conversation: {e}")
            import traceback
            traceback.print_exc()
            return json.dumps({
                "error": str(e),
                "success": False
            })
