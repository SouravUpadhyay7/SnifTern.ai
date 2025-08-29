#!/usr/bin/env python3
"""
Market Intelligence Module for SnifTern.ai
Provides real-time job market insights and fraud trend analysis
"""

import requests
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import re
from typing import Dict, List, Tuple, Optional

class JobMarketIntelligence:
    def __init__(self):
        self.fraud_trends = defaultdict(list)
        self.market_stats = {}
        self.industry_risks = {}
        self.location_risks = {}
        self.salary_anomalies = []
        
    def analyze_fraud_trends(self, job_data: List[Dict]) -> Dict:
        """
        Analyze fraud patterns and trends over time
        """
        trends = {
            'total_jobs': len(job_data),
            'fraud_rate': 0,
            'top_fraud_indicators': [],
            'industry_risk_levels': {},
            'location_risk_levels': {},
            'salary_anomalies': [],
            'emerging_threats': [],
            'seasonal_patterns': {}
        }
        
        if not job_data:
            return trends
            
        # Calculate fraud rate
        fraud_count = sum(1 for job in job_data if job.get('is_fraud', False))
        trends['fraud_rate'] = (fraud_count / len(job_data)) * 100
        
        # Analyze fraud indicators
        fraud_indicators = []
        for job in job_data:
            if job.get('is_fraud', False):
                patterns = job.get('pattern_matches', [])
                fraud_indicators.extend(patterns)
        
        # Count most common fraud indicators
        indicator_counts = Counter(fraud_indicators)
        trends['top_fraud_indicators'] = indicator_counts.most_common(10)
        
        # Industry risk analysis
        industry_fraud = defaultdict(list)
        for job in job_data:
            industry = job.get('industry', 'Unknown')
            industry_fraud[industry].append(job.get('is_fraud', False))
        
        for industry, fraud_list in industry_fraud.items():
            risk_level = (sum(fraud_list) / len(fraud_list)) * 100
            trends['industry_risk_levels'][industry] = {
                'risk_percentage': risk_level,
                'total_jobs': len(fraud_list),
                'fraud_count': sum(fraud_list),
                'risk_level': self._get_risk_level(risk_level)
            }
        
        # Location risk analysis
        location_fraud = defaultdict(list)
        for job in job_data:
            location = job.get('location', 'Unknown')
            location_fraud[location].append(job.get('is_fraud', False))
        
        for location, fraud_list in location_fraud.items():
            risk_level = (sum(fraud_list) / len(fraud_list)) * 100
            trends['location_risk_levels'][location] = {
                'risk_percentage': risk_level,
                'total_jobs': len(fraud_list),
                'fraud_count': sum(fraud_list),
                'risk_level': self._get_risk_level(risk_level)
            }
        
        return trends
    
    def detect_salary_anomalies(self, job_data: List[Dict]) -> List[Dict]:
        """
        Detect unrealistic salary promises and anomalies
        """
        anomalies = []
        
        for job in job_data:
            salary_info = job.get('salary_analysis', '')
            if 'HIGH RISK' in salary_info or 'MEDIUM RISK' in salary_info:
                anomalies.append({
                    'job_title': job.get('title', 'Unknown'),
                    'company': job.get('company', 'Unknown'),
                    'location': job.get('location', 'Unknown'),
                    'salary_analysis': salary_info,
                    'risk_level': 'HIGH' if 'HIGH RISK' in salary_info else 'MEDIUM',
                    'detected_at': datetime.now().isoformat()
                })
        
        return anomalies
    
    def identify_emerging_threats(self, job_data: List[Dict]) -> List[Dict]:
        """
        Identify new and emerging fraud patterns
        """
        threats = []
        
        # Analyze recent patterns (last 30 days)
        recent_jobs = [
            job for job in job_data 
            if self._is_recent(job.get('posted_date', ''))
        ]
        
        # Find new fraud patterns
        all_patterns = []
        for job in recent_jobs:
            if job.get('is_fraud', False):
                patterns = job.get('pattern_matches', [])
                all_patterns.extend(patterns)
        
        # Identify patterns that are increasing
        pattern_counts = Counter(all_patterns)
        emerging_patterns = [
            pattern for pattern, count in pattern_counts.items()
            if count >= 3  # Pattern appears in at least 3 recent fraud cases
        ]
        
        for pattern in emerging_patterns:
            threats.append({
                'pattern': pattern,
                'frequency': pattern_counts[pattern],
                'first_seen': self._get_first_seen_date(pattern, job_data),
                'threat_level': 'HIGH' if pattern_counts[pattern] >= 5 else 'MEDIUM',
                'description': self._describe_threat(pattern)
            })
        
        return threats
    
    def generate_market_report(self, job_data: List[Dict]) -> Dict:
        """
        Generate comprehensive market intelligence report
        """
        report = {
            'report_date': datetime.now().isoformat(),
            'summary': {},
            'fraud_trends': self.analyze_fraud_trends(job_data),
            'salary_anomalies': self.detect_salary_anomalies(job_data),
            'emerging_threats': self.identify_emerging_threats(job_data),
            'recommendations': [],
            'market_insights': {}
        }
        
        # Generate summary
        total_jobs = len(job_data)
        fraud_count = sum(1 for job in job_data if job.get('is_fraud', False))
        
        report['summary'] = {
            'total_jobs_analyzed': total_jobs,
            'fraud_detected': fraud_count,
            'fraud_rate_percentage': (fraud_count / total_jobs * 100) if total_jobs > 0 else 0,
            'high_risk_industries': self._get_high_risk_industries(report['fraud_trends']),
            'high_risk_locations': self._get_high_risk_locations(report['fraud_trends']),
            'critical_threats': len([t for t in report['emerging_threats'] if t['threat_level'] == 'HIGH'])
        }
        
        # Generate recommendations
        report['recommendations'] = self._generate_recommendations(report)
        
        # Market insights
        report['market_insights'] = self._generate_market_insights(job_data)
        
        return report
    
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
    
    def _is_recent(self, date_str: str, days: int = 30) -> bool:
        """Check if date is within specified days"""
        try:
            if not date_str:
                return False
            job_date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return (datetime.now() - job_date).days <= days
        except:
            return False
    
    def _get_first_seen_date(self, pattern: str, job_data: List[Dict]) -> str:
        """Get the first date a pattern was seen"""
        for job in job_data:
            if job.get('is_fraud', False):
                patterns = job.get('pattern_matches', [])
                if pattern in patterns:
                    return job.get('posted_date', datetime.now().isoformat())
        return datetime.now().isoformat()
    
    def _describe_threat(self, pattern: str) -> str:
        """Generate description for threat pattern"""
        threat_descriptions = {
            'certificate_payment': 'Scammers charging fees for fake certificates',
            'urgent_opportunity': 'Pressure tactics to rush decisions',
            'no_experience_required': 'Unrealistic job requirements',
            'suspicious_payment': 'Requests for personal financial information',
            'commission_based': 'No guaranteed salary, commission-only scams',
            'virtual_internship_suspicious': 'Fake remote internship opportunities'
        }
        
        for key, description in threat_descriptions.items():
            if key in pattern.lower():
                return description
        
        return f'New fraud pattern detected: {pattern}'
    
    def _get_high_risk_industries(self, fraud_trends: Dict) -> List[str]:
        """Get industries with high fraud risk"""
        high_risk = []
        for industry, data in fraud_trends.get('industry_risk_levels', {}).items():
            if data.get('risk_level') in ['HIGH', 'CRITICAL']:
                high_risk.append(industry)
        return high_risk
    
    def _get_high_risk_locations(self, fraud_trends: Dict) -> List[str]:
        """Get locations with high fraud risk"""
        high_risk = []
        for location, data in fraud_trends.get('location_risk_levels', {}).items():
            if data.get('risk_level') in ['HIGH', 'CRITICAL']:
                high_risk.append(location)
        return high_risk
    
    def _generate_recommendations(self, report: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Based on fraud rate
        fraud_rate = report['summary']['fraud_rate_percentage']
        if fraud_rate > 30:
            recommendations.append("🚨 CRITICAL: Fraud rate is extremely high. Consider implementing additional verification measures.")
        elif fraud_rate > 15:
            recommendations.append("⚠️ HIGH: Fraud rate is concerning. Review job posting sources and verification processes.")
        
        # Based on emerging threats
        high_threats = [t for t in report['emerging_threats'] if t['threat_level'] == 'HIGH']
        if high_threats:
            recommendations.append(f"🔍 NEW THREATS: {len(high_threats)} new high-risk fraud patterns detected. Update detection algorithms.")
        
        # Based on industry risks
        critical_industries = report['summary']['high_risk_industries']
        if critical_industries:
            recommendations.append(f"🏭 INDUSTRY RISK: {', '.join(critical_industries[:3])} industries show critical fraud risk.")
        
        # Based on salary anomalies
        salary_anomalies = len(report['salary_anomalies'])
        if salary_anomalies > 10:
            recommendations.append(f"💰 SALARY FRAUD: {salary_anomalies} jobs with suspicious salary promises detected.")
        
        return recommendations
    
    def _generate_market_insights(self, job_data: List[Dict]) -> Dict:
        """Generate market insights and trends"""
        insights = {
            'popular_job_titles': [],
            'salary_trends': {},
            'remote_work_trends': {},
            'skill_demand': {},
            'company_trust_scores': {}
        }
        
        # Analyze job titles
        titles = [job.get('title', '') for job in job_data if job.get('title')]
        title_counts = Counter(titles)
        insights['popular_job_titles'] = title_counts.most_common(10)
        
        # Analyze remote work trends
        remote_jobs = sum(1 for job in job_data if 'remote' in job.get('description', '').lower())
        total_jobs = len(job_data)
        insights['remote_work_trends'] = {
            'remote_percentage': (remote_jobs / total_jobs * 100) if total_jobs > 0 else 0,
            'total_remote_jobs': remote_jobs,
            'total_jobs': total_jobs
        }
        
        return insights

class RealTimeAlertSystem:
    def __init__(self):
        self.alert_thresholds = {
            'fraud_rate': 20.0,  # Alert if fraud rate exceeds 20%
            'new_threats': 3,    # Alert if 3+ new threats detected
            'salary_anomalies': 5,  # Alert if 5+ salary anomalies
            'critical_industries': 2  # Alert if 2+ industries at critical risk
        }
    
    def check_alerts(self, market_report: Dict) -> List[Dict]:
        """Check if any alerts should be triggered"""
        alerts = []
        
        # Fraud rate alert
        fraud_rate = market_report['summary']['fraud_rate_percentage']
        if fraud_rate > self.alert_thresholds['fraud_rate']:
            alerts.append({
                'type': 'FRAUD_RATE_HIGH',
                'severity': 'CRITICAL',
                'message': f'Fraud rate has reached {fraud_rate:.1f}% - significantly above normal levels',
                'timestamp': datetime.now().isoformat(),
                'recommendation': 'Immediately review job posting sources and implement additional verification'
            })
        
        # New threats alert
        new_threats = len(market_report['emerging_threats'])
        if new_threats >= self.alert_thresholds['new_threats']:
            alerts.append({
                'type': 'NEW_THREATS_DETECTED',
                'severity': 'HIGH',
                'message': f'{new_threats} new fraud patterns detected',
                'timestamp': datetime.now().isoformat(),
                'recommendation': 'Update fraud detection algorithms and review recent job postings'
            })
        
        # Salary anomalies alert
        salary_anomalies = len(market_report['salary_anomalies'])
        if salary_anomalies >= self.alert_thresholds['salary_anomalies']:
            alerts.append({
                'type': 'SALARY_FRAUD_SPIKE',
                'severity': 'MEDIUM',
                'message': f'{salary_anomalies} jobs with suspicious salary promises detected',
                'timestamp': datetime.now().isoformat(),
                'recommendation': 'Review salary verification processes and flag unrealistic promises'
            })
        
        return alerts

# Usage example
if __name__ == "__main__":
    # Initialize market intelligence
    market_intel = JobMarketIntelligence()
    alert_system = RealTimeAlertSystem()
    
    # Sample job data (replace with real data)
    sample_jobs = [
        {
            'title': 'Software Engineer Intern',
            'company': 'TechCorp',
            'location': 'San Francisco, CA',
            'industry': 'Technology',
            'is_fraud': False,
            'posted_date': '2024-01-15T10:00:00Z',
            'description': 'Remote software engineering internship...'
        },
        {
            'title': 'Data Entry Specialist',
            'company': 'FakeCorp',
            'location': 'Remote',
            'industry': 'Technology',
            'is_fraud': True,
            'pattern_matches': ['certificate_payment', 'urgent_opportunity'],
            'posted_date': '2024-01-16T10:00:00Z',
            'description': 'No experience required, earn $50-100 per hour...'
        }
    ]
    
    # Generate market report
    report = market_intel.generate_market_report(sample_jobs)
    
    # Check for alerts
    alerts = alert_system.check_alerts(report)
    
    print("Market Intelligence Report:")
    print(json.dumps(report, indent=2))
    
    if alerts:
        print("\n🚨 ALERTS:")
        for alert in alerts:
            print(f"- {alert['severity']}: {alert['message']}") 