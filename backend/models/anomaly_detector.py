"""Anomaly detection models for disease surveillance.

This module implements various anomaly detection algorithms inspired by
statistical methods and machine learning approaches.
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Optional
from scipy import stats
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from datetime import datetime


class AnomalyDetector:
    """Multi-method anomaly detection for disease surveillance data."""
    
    def __init__(self, threshold: float = 0.75):
        """Initialize anomaly detector.
        
        Args:
            threshold: Confidence threshold for anomaly detection (0-1)
        """
        self.threshold = threshold
        self.scaler = StandardScaler()
        self.isolation_forest = IsolationForest(contamination=0.1, random_state=42)
        self.baseline_stats = {}
    
    def fit_baseline(self, data: Dict[str, pd.DataFrame]):
        """Fit baseline statistics from historical data.
        
        Args:
            data: Dictionary of DataFrames by source type
        """
        for source_type, df in data.items():
            if df.empty or 'timestamp' not in df.columns:
                continue
            
            # Calculate daily counts
            daily_counts = df.groupby(df['timestamp'].dt.date).size().values
            
            self.baseline_stats[source_type] = {
                'mean': np.mean(daily_counts),
                'std': np.std(daily_counts),
                'median': np.median(daily_counts),
                'q1': np.percentile(daily_counts, 25),
                'q3': np.percentile(daily_counts, 75),
                'iqr': np.percentile(daily_counts, 75) - np.percentile(daily_counts, 25)
            }
    
    def detect_statistical_anomalies(self, 
                                     data: Dict[str, pd.DataFrame],
                                     method: str = 'zscore') -> List[Dict]:
        """Detect anomalies using statistical methods.
        
        Args:
            data: Dictionary of DataFrames by source type
            method: 'zscore', 'iqr', or 'modified_zscore'
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        for source_type, df in data.items():
            if df.empty or 'timestamp' not in df.columns:
                continue
            
            # Get baseline stats
            baseline = self.baseline_stats.get(source_type)
            if not baseline:
                continue
            
            # Calculate daily counts for recent data
            daily_counts = df.groupby(df['timestamp'].dt.date).size()
            
            for date, count in daily_counts.items():
                anomaly_score = 0.0
                is_anomaly = False
                detection_method = method
                
                if method == 'zscore':
                    # Z-score method
                    if baseline['std'] > 0:
                        z_score = (count - baseline['mean']) / baseline['std']
                        is_anomaly = abs(z_score) > 2.5
                        anomaly_score = min(abs(z_score) / 3.0, 1.0)
                
                elif method == 'iqr':
                    # IQR method
                    lower_bound = baseline['q1'] - 1.5 * baseline['iqr']
                    upper_bound = baseline['q3'] + 1.5 * baseline['iqr']
                    is_anomaly = count < lower_bound or count > upper_bound
                    
                    if count > baseline['median']:
                        anomaly_score = min((count - upper_bound) / baseline['iqr'], 1.0)
                    else:
                        anomaly_score = min((lower_bound - count) / baseline['iqr'], 1.0)
                
                elif method == 'modified_zscore':
                    # Modified Z-score using median absolute deviation
                    median = baseline['median']
                    mad = np.median(np.abs(daily_counts.values - median))
                    if mad > 0:
                        modified_z = 0.6745 * (count - median) / mad
                        is_anomaly = abs(modified_z) > 3.5
                        anomaly_score = min(abs(modified_z) / 4.0, 1.0)
                
                if is_anomaly and anomaly_score >= self.threshold:
                    anomalies.append({
                        'id': f"{source_type}_{date}_{np.random.randint(1000, 9999)}",
                        'timestamp': datetime.combine(date, datetime.min.time()),
                        'type': f'{source_type}_spike',
                        'data_source': source_type,
                        'severity': self._calculate_severity(anomaly_score),
                        'confidence': float(anomaly_score),
                        'baseline_value': baseline['mean'],
                        'current_value': int(count),
                        'deviation_percent': ((count - baseline['mean']) / baseline['mean'] * 100) if baseline['mean'] > 0 else 0,
                        'detection_method': detection_method,
                        'location': 'aggregated'  # Can be refined with location data
                    })
        
        return anomalies
    
    def detect_ml_anomalies(self, data: Dict[str, pd.DataFrame]) -> List[Dict]:
        """Detect anomalies using machine learning (Isolation Forest).
        
        Args:
            data: Dictionary of DataFrames by source type
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        # Prepare feature matrix
        features_list = []
        metadata_list = []
        
        for source_type, df in data.items():
            if df.empty or 'timestamp' not in df.columns:
                continue
            
            daily_data = df.groupby(df['timestamp'].dt.date)
            
            for date, group in daily_data:
                # Extract features
                features = [
                    len(group),  # Daily count
                    group['timestamp'].dt.hour.mean() if 'timestamp' in group.columns else 12,  # Average hour
                    len(group) / max(1, group['timestamp'].dt.hour.nunique()) if 'timestamp' in group.columns else 0,  # Hourly rate
                ]
                
                features_list.append(features)
                metadata_list.append({
                    'date': date,
                    'source_type': source_type,
                    'count': len(group)
                })
        
        if len(features_list) < 10:  # Need minimum samples
            return anomalies
        
        # Fit and predict
        features_array = np.array(features_list)
        features_scaled = self.scaler.fit_transform(features_array)
        
        predictions = self.isolation_forest.fit_predict(features_scaled)
        scores = self.isolation_forest.score_samples(features_scaled)
        
        # Extract anomalies
        for i, (pred, score, metadata) in enumerate(zip(predictions, scores, metadata_list)):
            if pred == -1:  # Anomaly detected
                anomaly_score = 1.0 - (score + 0.5)  # Convert to 0-1 range
                
                if anomaly_score >= self.threshold:
                    anomalies.append({
                        'id': f"{metadata['source_type']}_{metadata['date']}_{np.random.randint(1000, 9999)}",
                        'timestamp': datetime.combine(metadata['date'], datetime.min.time()),
                        'type': f"{metadata['source_type']}_ml_anomaly",
                        'data_source': metadata['source_type'],
                        'severity': self._calculate_severity(anomaly_score),
                        'confidence': float(anomaly_score),
                        'current_value': metadata['count'],
                        'detection_method': 'isolation_forest',
                        'location': 'aggregated'
                    })
        
        return anomalies
    
    def detect_temporal_anomalies(self, data: Dict[str, pd.DataFrame]) -> List[Dict]:
        """Detect temporal anomalies (unusual patterns over time).
        
        Args:
            data: Dictionary of DataFrames by source type
            
        Returns:
            List of detected anomalies
        """
        anomalies = []
        
        for source_type, df in data.items():
            if df.empty or 'timestamp' not in df.columns:
                continue
            
            # Sort by timestamp
            df_sorted = df.sort_values('timestamp')
            daily_counts = df_sorted.groupby(df_sorted['timestamp'].dt.date).size()
            
            if len(daily_counts) < 7:  # Need at least a week of data
                continue
            
            # Calculate rate of change
            daily_changes = daily_counts.pct_change().fillna(0)
            
            # Detect rapid increases (potential outbreak signal)
            for i in range(len(daily_changes)):
                if i < 3:  # Skip first few days
                    continue
                
                # Check for sustained increase
                recent_changes = daily_changes.iloc[i-3:i+1]
                if (recent_changes > 0.2).sum() >= 3:  # 20% increase for 3+ consecutive days
                    avg_increase = recent_changes.mean()
                    anomaly_score = min(avg_increase, 1.0)
                    
                    if anomaly_score >= self.threshold:
                        date = daily_counts.index[i]
                        anomalies.append({
                            'id': f"{source_type}_temporal_{date}_{np.random.randint(1000, 9999)}",
                            'timestamp': datetime.combine(date, datetime.min.time()),
                            'type': f'{source_type}_rapid_increase',
                            'data_source': source_type,
                            'severity': 'high',  # Rapid increases are always concerning
                            'confidence': float(anomaly_score),
                            'current_value': int(daily_counts.iloc[i]),
                            'detection_method': 'temporal_pattern',
                            'pattern': 'sustained_increase',
                            'location': 'aggregated'
                        })
        
        return anomalies
    
    def detect_all_anomalies(self, data: Dict[str, pd.DataFrame]) -> List[Dict]:
        """Detect anomalies using all available methods.
        
        Args:
            data: Dictionary of DataFrames by source type
            
        Returns:
            Combined list of detected anomalies
        """
        # Fit baseline if not already done
        if not self.baseline_stats:
            self.fit_baseline(data)
        
        # Collect anomalies from all methods
        all_anomalies = []
        
        # Statistical methods
        all_anomalies.extend(self.detect_statistical_anomalies(data, method='zscore'))
        all_anomalies.extend(self.detect_statistical_anomalies(data, method='iqr'))
        
        # ML method
        all_anomalies.extend(self.detect_ml_anomalies(data))
        
        # Temporal patterns
        all_anomalies.extend(self.detect_temporal_anomalies(data))
        
        # Deduplicate and sort by confidence
        unique_anomalies = self._deduplicate_anomalies(all_anomalies)
        unique_anomalies.sort(key=lambda x: x['confidence'], reverse=True)
        
        return unique_anomalies
    
    def _calculate_severity(self, confidence: float) -> str:
        """Calculate severity level based on confidence score.
        
        Args:
            confidence: Anomaly confidence score (0-1)
            
        Returns:
            Severity level string
        """
        if confidence >= 0.9:
            return 'critical'
        elif confidence >= 0.8:
            return 'high'
        elif confidence >= 0.65:
            return 'medium'
        else:
            return 'low'
    
    def _deduplicate_anomalies(self, anomalies: List[Dict]) -> List[Dict]:
        """Remove duplicate anomalies from the same source and time.
        
        Args:
            anomalies: List of anomalies
            
        Returns:
            Deduplicated list
        """
        seen = set()
        unique = []
        
        for anomaly in anomalies:
            key = (
                anomaly['data_source'],
                anomaly['timestamp'].date() if isinstance(anomaly['timestamp'], datetime) else anomaly['timestamp']
            )
            
            if key not in seen:
                seen.add(key)
                unique.append(anomaly)
        
        return unique
