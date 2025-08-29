#!/usr/bin/env python3
"""
Advanced Analytics Dashboard for SnifTern.ai
Provides comprehensive insights, visualizations, and trend analysis
"""

import json
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

class AnalyticsDashboard:
    def __init__(self):
        self.analytics_data = []
        self.fraud_patterns = defaultdict(int)
        self.industry_stats = defaultdict(list)
        self.location_stats = defaultdict(list)
        self.temporal_data = []
        
    def add_analysis_data(self, analysis_result: Dict):
        """Add analysis result to dashboard data"""
        self.analytics_data.append({
            'timestamp': datetime.now().isoformat(),
            'result': analysis_result,
            'is_fraud': 'FAKE' in analysis_result.get('result', ''),
            'confidence_score': analysis_result.get('confidence_score', 0),
            'word_count': analysis_result.get('word_count', 0),
            'pattern_matches': analysis_result.get('pattern_matches', []),
            'source': analysis_result.get('source', 'manual'),
            'company': analysis_result.get('company', 'unknown'),
            'location': analysis_result.get('location', 'unknown'),
            'industry': analysis_result.get('industry', 'unknown')
        })
        
        # Update fraud patterns
        patterns = analysis_result.get('pattern_matches', [])
        for pattern in patterns:
            self.fraud_patterns[pattern] += 1
        
        # Update industry stats
        industry = analysis_result.get('industry', 'unknown')
        self.industry_stats[industry].append({
            'is_fraud': 'FAKE' in analysis_result.get('result', ''),
            'confidence_score': analysis_result.get('confidence_score', 0),
            'timestamp': datetime.now().isoformat()
        })

        # Update location stats
        location = analysis_result.get('location', 'unknown')
        self.location_stats[location].append({
            'is_fraud': 'FAKE' in analysis_result.get('result', ''),
            'confidence_score': analysis_result.get('confidence_score', 0),
            'timestamp': datetime.now().isoformat()
        })

        # Update temporal data
        self.temporal_data.append({
            'timestamp': datetime.now(),
            'is_fraud': 'FAKE' in analysis_result.get('result', ''),
            'confidence_score': analysis_result.get('confidence_score', 0)
        })
    
    def generate_dashboard_report(self) -> Dict:
        """Generate comprehensive dashboard report"""
        report = {
            'summary_metrics': self._calculate_summary_metrics(),
            'fraud_trends': self._analyze_fraud_trends(),
            'pattern_analysis': self._analyze_fraud_patterns(),
            'industry_insights': self._analyze_industry_insights(),
            'location_insights': self._analyze_location_insights(),
            'temporal_analysis': self._analyze_temporal_trends(),
            'source_analysis': self._analyze_source_distribution(),
            'confidence_analysis': self._analyze_confidence_distribution(),
            'recommendations': self._generate_recommendations(),
            'generated_at': datetime.now().isoformat()
        }
        
        return report
    
    def _calculate_summary_metrics(self) -> Dict:
        """Calculate summary metrics"""
        if not self.analytics_data:
            return {}
        
        total_analyses = len(self.analytics_data)
        fraud_count = sum(1 for data in self.analytics_data if data['is_fraud'])
        fraud_rate = (fraud_count / total_analyses) * 100
        
        avg_confidence = sum(data['confidence_score'] for data in self.analytics_data) / total_analyses
        avg_word_count = sum(data['word_count'] for data in self.analytics_data) / total_analyses
        
        return {
            'total_analyses': total_analyses,
            'fraud_detected': fraud_count,
            'fraud_rate_percentage': round(fraud_rate, 2),
            'average_confidence_score': round(avg_confidence, 2),
            'average_word_count': round(avg_word_count, 0),
            'unique_companies': len(set(data['company'] for data in self.analytics_data)),
            'unique_locations': len(set(data['location'] for data in self.analytics_data)),
            'unique_industries': len(set(data['industry'] for data in self.analytics_data))
        }
    
    def _analyze_fraud_trends(self) -> Dict:
        """Analyze fraud trends over time"""
        if not self.temporal_data:
            return {}
        
        # Group by date
        daily_fraud = defaultdict(list)
        for data in self.temporal_data:
            date = data['timestamp'].date()
            daily_fraud[date].append(data['is_fraud'])
        
        # Calculate daily fraud rates
        daily_rates = {}
        for date, fraud_list in daily_fraud.items():
            daily_rates[date.isoformat()] = (sum(fraud_list) / len(fraud_list)) * 100
        
        # Calculate trend
        dates = sorted(daily_rates.keys())
        if len(dates) >= 2:
            recent_rate = daily_rates[dates[-1]]
            previous_rate = daily_rates[dates[-2]]
            trend = 'increasing' if recent_rate > previous_rate else 'decreasing' if recent_rate < previous_rate else 'stable'
        else:
            trend = 'insufficient_data'
        
        return {
            'daily_fraud_rates': daily_rates,
            'trend_direction': trend,
            'average_daily_fraud_rate': round(sum(daily_rates.values()) / len(daily_rates), 2),
            'peak_fraud_rate': round(max(daily_rates.values()), 2),
            'lowest_fraud_rate': round(min(daily_rates.values()), 2)
        }
    
    def _analyze_fraud_patterns(self) -> Dict:
        """Analyze fraud patterns"""
        if not self.fraud_patterns:
            return {}
        
        # Get top patterns
        top_patterns = sorted(self.fraud_patterns.items(), key=lambda x: x[1], reverse=True)
        
        # Categorize patterns
        pattern_categories = {
            'certificate_fraud': 0,
            'urgent_opportunities': 0,
            'suspicious_payments': 0,
            'unrealistic_requirements': 0,
            'other': 0
        }
        
        for pattern, count in self.fraud_patterns.items():
            if 'certificate' in pattern.lower():
                pattern_categories['certificate_fraud'] += count
            elif 'urgent' in pattern.lower():
                pattern_categories['urgent_opportunities'] += count
            elif 'payment' in pattern.lower() or 'money' in pattern.lower():
                pattern_categories['suspicious_payments'] += count
            elif 'experience' in pattern.lower() or 'requirement' in pattern.lower():
                pattern_categories['unrealistic_requirements'] += count
            else:
                pattern_categories['other'] += count
        
        return {
            'top_patterns': top_patterns[:10],
            'pattern_categories': pattern_categories,
            'total_pattern_occurrences': sum(self.fraud_patterns.values()),
            'unique_patterns': len(self.fraud_patterns)
        }
    
    def _analyze_industry_insights(self) -> Dict:
        """Analyze industry-specific insights"""
        if not self.industry_stats:
            return {}
        
        industry_analysis = {}
        for industry, data_list in self.industry_stats.items():
            if not data_list:
                continue
            
            fraud_count = sum(1 for data in data_list if data['is_fraud'])
            total_count = len(data_list)
            fraud_rate = (fraud_count / total_count) * 100
            avg_confidence = sum(data['confidence_score'] for data in data_list) / total_count
            
            industry_analysis[industry] = {
                'total_jobs': total_count,
                'fraud_count': fraud_count,
                'fraud_rate_percentage': round(fraud_rate, 2),
                'average_confidence': round(avg_confidence, 2),
                'risk_level': self._get_risk_level(fraud_rate)
            }
        
        # Sort by fraud rate
        sorted_industries = sorted(industry_analysis.items(), key=lambda x: x[1]['fraud_rate_percentage'], reverse=True)
        
        return {
            'industry_breakdown': dict(sorted_industries),
            'high_risk_industries': [ind for ind, data in sorted_industries if data['risk_level'] in ['HIGH', 'CRITICAL']],
            'safe_industries': [ind for ind, data in sorted_industries if data['risk_level'] == 'SAFE']
        }
    
    def _analyze_location_insights(self) -> Dict:
        """Analyze location-specific insights"""
        if not self.location_stats:
            return {}
        
        location_analysis = {}
        for location, data_list in self.location_stats.items():
            if not data_list:
                continue
            
            fraud_count = sum(1 for data in data_list if data['is_fraud'])
            total_count = len(data_list)
            fraud_rate = (fraud_count / total_count) * 100
            avg_confidence = sum(data['confidence_score'] for data in data_list) / total_count
            
            location_analysis[location] = {
                'total_jobs': total_count,
                'fraud_count': fraud_count,
                'fraud_rate_percentage': round(fraud_rate, 2),
                'average_confidence': round(avg_confidence, 2),
                'risk_level': self._get_risk_level(fraud_rate)
            }
        
        # Sort by fraud rate
        sorted_locations = sorted(location_analysis.items(), key=lambda x: x[1]['fraud_rate_percentage'], reverse=True)
        
        return {
            'location_breakdown': dict(sorted_locations),
            'high_risk_locations': [loc for loc, data in sorted_locations if data['risk_level'] in ['HIGH', 'CRITICAL']],
            'safe_locations': [loc for loc, data in sorted_locations if data['risk_level'] == 'SAFE']
        }
    
    def _analyze_temporal_trends(self) -> Dict:
        """Analyze temporal trends"""
        if not self.temporal_data:
            return {}
        
        # Group by hour of day
        hourly_fraud = defaultdict(list)
        for data in self.temporal_data:
            hour = data['timestamp'].hour
            hourly_fraud[hour].append(data['is_fraud'])
        
        hourly_rates = {}
        for hour, fraud_list in hourly_fraud.items():
            hourly_rates[hour] = (sum(fraud_list) / len(fraud_list)) * 100
        
        # Group by day of week
        daily_fraud = defaultdict(list)
        for data in self.temporal_data:
            day = data['timestamp'].strftime('%A')
            daily_fraud[day].append(data['is_fraud'])
        
        daily_rates = {}
        for day, fraud_list in daily_fraud.items():
            daily_rates[day] = (sum(fraud_list) / len(fraud_list)) * 100
        
        return {
            'hourly_fraud_rates': dict(sorted(hourly_rates.items())),
            'daily_fraud_rates': daily_rates,
            'peak_hour': max(hourly_rates.items(), key=lambda x: x[1])[0] if hourly_rates else None,
            'peak_day': max(daily_rates.items(), key=lambda x: x[1])[0] if daily_rates else None
        }
    
    def _analyze_source_distribution(self) -> Dict:
        """Analyze source distribution"""
        if not self.analytics_data:
            return {}
        
        source_counts = Counter(data['source'] for data in self.analytics_data)
        source_fraud = defaultdict(list)
        
        for data in self.analytics_data:
            source_fraud[data['source']].append(data['is_fraud'])
        
        source_analysis = {}
        for source, fraud_list in source_fraud.items():
            fraud_rate = (sum(fraud_list) / len(fraud_list)) * 100
            source_analysis[source] = {
                'total_analyses': source_counts[source],
                'fraud_rate_percentage': round(fraud_rate, 2),
                'risk_level': self._get_risk_level(fraud_rate)
            }
        
        return {
            'source_breakdown': source_analysis,
            'most_used_source': max(source_counts.items(), key=lambda x: x[1])[0] if source_counts else None,
            'highest_fraud_source': max(source_analysis.items(), key=lambda x: x[1]['fraud_rate_percentage'])[0] if source_analysis else None
        }
    
    def _analyze_confidence_distribution(self) -> Dict:
        """Analyze confidence score distribution"""
        if not self.analytics_data:
            return {}
        
        confidence_scores = [data['confidence_score'] for data in self.analytics_data]
        
        # Create confidence ranges
        ranges = {
            '0-20': 0,
            '21-40': 0,
            '41-60': 0,
            '61-80': 0,
            '81-100': 0
        }
        
        for score in confidence_scores:
            if score <= 20:
                ranges['0-20'] += 1
            elif score <= 40:
                ranges['21-40'] += 1
            elif score <= 60:
                ranges['41-60'] += 1
            elif score <= 80:
                ranges['61-80'] += 1
            else:
                ranges['81-100'] += 1
        
        return {
            'confidence_ranges': ranges,
            'average_confidence': round(sum(confidence_scores) / len(confidence_scores), 2),
            'median_confidence': round(sorted(confidence_scores)[len(confidence_scores)//2], 2),
            'high_confidence_analyses': sum(1 for score in confidence_scores if score >= 80),
            'low_confidence_analyses': sum(1 for score in confidence_scores if score <= 40)
        }
    
    def _get_risk_level(self, percentage: float) -> str:
        """Convert percentage to risk level"""
        if percentage >= 50:
            return 'CRITICAL'
        elif percentage >= 30:
            return 'HIGH'
        elif percentage >= 15:
            return 'MEDIUM'
        elif percentage >= 5:
            return 'LOW'
        else:
            return 'SAFE'
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on analytics"""
        recommendations = []
        
        summary = self._calculate_summary_metrics()
        if not summary:
            return recommendations
        
        # Fraud rate recommendations
        fraud_rate = summary.get('fraud_rate_percentage', 0)
        if fraud_rate > 30:
            recommendations.append("🚨 CRITICAL: Fraud rate is extremely high. Implement additional verification measures immediately.")
        elif fraud_rate > 15:
            recommendations.append("⚠️ HIGH: Fraud rate is concerning. Review job posting sources and verification processes.")
        
        # Industry recommendations
        industry_insights = self._analyze_industry_insights()
        high_risk_industries = industry_insights.get('high_risk_industries', [])
        if high_risk_industries:
            recommendations.append(f"🏭 INDUSTRY RISK: {', '.join(high_risk_industries[:3])} industries show high fraud risk.")
        
        # Location recommendations
        location_insights = self._analyze_location_insights()
        high_risk_locations = location_insights.get('high_risk_locations', [])
        if high_risk_locations:
            recommendations.append(f"📍 LOCATION RISK: {', '.join(high_risk_locations[:3])} locations show high fraud risk.")
        
        # Pattern recommendations
        pattern_analysis = self._analyze_fraud_patterns()
        top_patterns = pattern_analysis.get('top_patterns', [])
        if top_patterns:
            most_common_pattern = top_patterns[0][0]
            recommendations.append(f"🔍 PATTERN ALERT: '{most_common_pattern}' is the most common fraud pattern.")
        
        # Source recommendations
        source_analysis = self._analyze_source_distribution()
        highest_fraud_source = source_analysis.get('highest_fraud_source')
        if highest_fraud_source:
            recommendations.append(f"📊 SOURCE RISK: {highest_fraud_source} shows the highest fraud rate among sources.")
        
        return recommendations
    
    def create_visualizations(self) -> Dict:
        """Create visualization data for dashboard"""
        visualizations = {}
        
        # Fraud rate over time
        fraud_trends = self._analyze_fraud_trends()
        if fraud_trends.get('daily_fraud_rates'):
            visualizations['fraud_trend_chart'] = {
                'type': 'line',
                'data': {
                    'labels': list(fraud_trends['daily_fraud_rates'].keys()),
                    'datasets': [{
                        'label': 'Daily Fraud Rate (%)',
                        'data': list(fraud_trends['daily_fraud_rates'].values()),
                        'borderColor': '#ff6b6b',
                        'backgroundColor': 'rgba(255, 107, 107, 0.1)'
                    }]
                }
            }
        
        # Industry fraud rates
        industry_insights = self._analyze_industry_insights()
        if industry_insights.get('industry_breakdown'):
            industries = list(industry_insights['industry_breakdown'].keys())[:10]
            fraud_rates = [industry_insights['industry_breakdown'][ind]['fraud_rate_percentage'] for ind in industries]
            
            visualizations['industry_chart'] = {
                'type': 'bar',
                'data': {
                    'labels': industries,
                    'datasets': [{
                        'label': 'Fraud Rate (%)',
                        'data': fraud_rates,
                        'backgroundColor': ['#ff6b6b' if rate > 20 else '#4ecdc4' for rate in fraud_rates]
                    }]
                }
            }
        
        # Pattern distribution
        pattern_analysis = self._analyze_fraud_patterns()
        if pattern_analysis.get('pattern_categories'):
            categories = list(pattern_analysis['pattern_categories'].keys())
            counts = list(pattern_analysis['pattern_categories'].values())
            
            visualizations['pattern_chart'] = {
                'type': 'doughnut',
                'data': {
                    'labels': categories,
                    'datasets': [{
                        'data': counts,
                        'backgroundColor': ['#ff6b6b', '#4ecdc4', '#45b7d1', '#96ceb4', '#feca57']
                    }]
                }
            }
        
        return visualizations

# Usage example
if __name__ == "__main__":
    dashboard = AnalyticsDashboard()
    
    # Sample analysis data
    sample_analyses = [
        {
            'result': 'Likely FAKE ❌',
            'confidence_score': 85,
            'word_count': 250,
            'pattern_matches': ['certificate_payment', 'urgent_opportunity'],
            'source': 'LinkedIn',
            'company': 'FakeCorp',
            'location': 'Remote',
            'industry': 'Technology'
        },
        {
            'result': 'Likely REAL ✅',
            'confidence_score': 92,
            'word_count': 400,
            'pattern_matches': [],
            'source': 'Indeed',
            'company': 'Google',
            'location': 'Mountain View, CA',
            'industry': 'Technology'
        }
    ]
    
    # Add data to dashboard
    for analysis in sample_analyses:
        dashboard.add_analysis_data(analysis)
    
    # Generate dashboard report
    report = dashboard.generate_dashboard_report()
    
    print("Analytics Dashboard Report:")
    print(json.dumps(report, indent=2))
    
    # Create visualizations
    visualizations = dashboard.create_visualizations()
    print(f"\nGenerated {len(visualizations)} visualizations") 