#!/usr/bin/env python3
"""
Blockchain Verification System for SnifTern.ai
Provides immutable verification of job postings and company credentials
"""

import hashlib
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
import requests

class BlockchainVerification:
    def __init__(self):
        self.verification_chain = []
        self.pending_verifications = []
        self.company_registry = {}
        
    def create_verification_block(self, job_data: Dict, verification_type: str) -> Dict:
        """Create a new verification block"""
        block = {
            'index': len(self.verification_chain),
            'timestamp': datetime.now().isoformat(),
            'verification_type': verification_type,
            'data': job_data,
            'previous_hash': self._get_latest_hash(),
            'hash': None,
            'verified_by': 'SnifTern.ai',
            'verification_score': 0
        }
        
        # Calculate hash
        block['hash'] = self._calculate_hash(block)
        
        return block
    
    def verify_job_posting(self, job_data: Dict) -> Dict:
        """Verify a job posting and add to blockchain"""
        verification_result = {
            'verified': False,
            'verification_score': 0,
            'verification_details': {},
            'block_hash': None,
            'timestamp': datetime.now().isoformat()
        }
        
        # Perform verification checks
        checks = self._perform_verification_checks(job_data)
        verification_result['verification_details'] = checks
        
        # Calculate verification score
        score = self._calculate_verification_score(checks)
        verification_result['verification_score'] = score
        verification_result['verified'] = score >= 70  # 70% threshold
        
        # Create verification block
        block = self.create_verification_block(job_data, 'job_posting_verification')
        block['verification_score'] = score
        
        # Add to chain
        self.verification_chain.append(block)
        verification_result['block_hash'] = block['hash']
        
        return verification_result
    
    def verify_company_credentials(self, company_data: Dict) -> Dict:
        """Verify company credentials and add to blockchain"""
        verification_result = {
            'verified': False,
            'verification_score': 0,
            'verification_details': {},
            'block_hash': None,
            'timestamp': datetime.now().isoformat()
        }
        
        # Perform company verification checks
        checks = self._perform_company_verification_checks(company_data)
        verification_result['verification_details'] = checks
        
        # Calculate verification score
        score = self._calculate_company_verification_score(checks)
        verification_result['verification_score'] = score
        verification_result['verified'] = score >= 80  # 80% threshold for companies
        
        # Create verification block
        block = self.create_verification_block(company_data, 'company_verification')
        block['verification_score'] = score
        
        # Add to chain
        self.verification_chain.append(block)
        verification_result['block_hash'] = block['hash']
        
        # Update company registry
        self.company_registry[company_data.get('name', '')] = {
            'verification_score': score,
            'verified': verification_result['verified'],
            'last_verified': datetime.now().isoformat(),
            'block_hash': block['hash']
        }
        
        return verification_result
    
    def _perform_verification_checks(self, job_data: Dict) -> Dict:
        """Perform comprehensive verification checks on job posting"""
        checks = {
            'company_verification': False,
            'domain_verification': False,
            'contact_verification': False,
            'salary_verification': False,
            'location_verification': False,
            'ai_fraud_detection': False,
            'pattern_analysis': False
        }
        
        # Company verification
        company_name = job_data.get('company', '')
        if company_name in self.company_registry:
            checks['company_verification'] = self.company_registry[company_name]['verified']
        else:
            # Check if company exists in external databases
            checks['company_verification'] = self._verify_company_external(company_name)
        
        # Domain verification
        domain = job_data.get('domain', '')
        if domain:
            checks['domain_verification'] = self._verify_domain(domain)
        
        # Contact verification
        contact_info = job_data.get('contact_info', {})
        if contact_info:
            checks['contact_verification'] = self._verify_contact_info(contact_info)
        
        # Salary verification
        salary_info = job_data.get('salary', '')
        if salary_info:
            checks['salary_verification'] = self._verify_salary(salary_info, job_data.get('title', ''))
        
        # Location verification
        location = job_data.get('location', '')
        if location:
            checks['location_verification'] = self._verify_location(location)
        
        # AI fraud detection
        fraud_score = job_data.get('fraud_score', 0)
        checks['ai_fraud_detection'] = fraud_score < 30  # Low fraud score
        
        # Pattern analysis
        patterns = job_data.get('pattern_matches', [])
        checks['pattern_analysis'] = len(patterns) < 3  # Few suspicious patterns
        
        return checks
    
    def _perform_company_verification_checks(self, company_data: Dict) -> Dict:
        """Perform verification checks on company"""
        checks = {
            'business_registration': False,
            'domain_age': False,
            'social_media_presence': False,
            'employee_count': False,
            'financial_stability': False,
            'legal_compliance': False,
            'reputation_score': False
        }
        
        # Business registration
        company_name = company_data.get('name', '')
        checks['business_registration'] = self._verify_business_registration(company_name)
        
        # Domain age
        domain = company_data.get('website', '')
        if domain:
            checks['domain_age'] = self._verify_domain_age(domain)
        
        # Social media presence
        social_media = company_data.get('social_media', {})
        checks['social_media_presence'] = self._verify_social_media_presence(social_media)
        
        # Employee count
        employee_count = company_data.get('employee_count', 0)
        checks['employee_count'] = employee_count > 10  # At least 10 employees
        
        # Financial stability (simplified check)
        checks['financial_stability'] = True  # Would integrate with financial APIs
        
        # Legal compliance
        checks['legal_compliance'] = self._verify_legal_compliance(company_name)
        
        # Reputation score
        reputation_score = company_data.get('reputation_score', 0)
        checks['reputation_score'] = reputation_score > 60
        
        return checks
    
    def _calculate_verification_score(self, checks: Dict) -> float:
        """Calculate verification score based on checks"""
        weights = {
            'company_verification': 0.25,
            'domain_verification': 0.20,
            'contact_verification': 0.15,
            'salary_verification': 0.15,
            'location_verification': 0.10,
            'ai_fraud_detection': 0.10,
            'pattern_analysis': 0.05
        }
        
        score = 0
        for check, weight in weights.items():
            if checks.get(check, False):
                score += weight * 100
        
        return score
    
    def _calculate_company_verification_score(self, checks: Dict) -> float:
        """Calculate company verification score"""
        weights = {
            'business_registration': 0.25,
            'domain_age': 0.20,
            'social_media_presence': 0.15,
            'employee_count': 0.15,
            'financial_stability': 0.10,
            'legal_compliance': 0.10,
            'reputation_score': 0.05
        }
        
        score = 0
        for check, weight in weights.items():
            if checks.get(check, False):
                score += weight * 100
        
        return score
    
    def _verify_company_external(self, company_name: str) -> bool:
        """Verify company in external databases"""
        # This would integrate with real business databases
        # For now, return True for demonstration
        return True
    
    def _verify_domain(self, domain: str) -> bool:
        """Verify domain legitimacy"""
        try:
            # Check if domain is accessible
            response = requests.get(f"https://{domain}", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _verify_contact_info(self, contact_info: Dict) -> bool:
        """Verify contact information"""
        # Check if email format is valid
        email = contact_info.get('email', '')
        if email and '@' in email and '.' in email.split('@')[1]:
            return True
        return False
    
    def _verify_salary(self, salary_info: str, job_title: str) -> bool:
        """Verify salary information"""
        # Check if salary is within reasonable range for job title
        # This would integrate with salary databases
        return True
    
    def _verify_location(self, location: str) -> bool:
        """Verify location information"""
        # Check if location is valid
        valid_locations = ['remote', 'san francisco', 'new york', 'london', 'tokyo']
        return any(valid_loc in location.lower() for valid_loc in valid_locations)
    
    def _verify_business_registration(self, company_name: str) -> bool:
        """Verify business registration"""
        # This would integrate with government business registries
        return True
    
    def _verify_domain_age(self, domain: str) -> bool:
        """Verify domain age"""
        # This would integrate with WHOIS data
        return True
    
    def _verify_social_media_presence(self, social_media: Dict) -> bool:
        """Verify social media presence"""
        # Check if company has social media accounts
        return len(social_media) > 0
    
    def _verify_legal_compliance(self, company_name: str) -> bool:
        """Verify legal compliance"""
        # This would integrate with legal databases
        return True
    
    def _calculate_hash(self, block: Dict) -> str:
        """Calculate hash of block"""
        block_string = json.dumps(block, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def _get_latest_hash(self) -> str:
        """Get hash of latest block"""
        if not self.verification_chain:
            return "0"
        return self.verification_chain[-1]['hash']
    
    def get_verification_history(self, identifier: str) -> List[Dict]:
        """Get verification history for a specific identifier"""
        history = []
        
        for block in self.verification_chain:
            data = block.get('data', {})
            if (data.get('company', '') == identifier or 
                data.get('name', '') == identifier or
                data.get('id', '') == identifier):
                history.append({
                    'timestamp': block['timestamp'],
                    'verification_type': block['verification_type'],
                    'verification_score': block['verification_score'],
                    'block_hash': block['hash'],
                    'verified': block['verification_score'] >= 70
                })
        
        return history
    
    def verify_chain_integrity(self) -> bool:
        """Verify blockchain integrity"""
        for i in range(1, len(self.verification_chain)):
            current_block = self.verification_chain[i]
            previous_block = self.verification_chain[i-1]
            
            # Check if current block's previous_hash matches previous block's hash
            if current_block['previous_hash'] != previous_block['hash']:
                return False
            
            # Check if current block's hash is valid
            expected_hash = self._calculate_hash({
                'index': current_block['index'],
                'timestamp': current_block['timestamp'],
                'verification_type': current_block['verification_type'],
                'data': current_block['data'],
                'previous_hash': current_block['previous_hash'],
                'verified_by': current_block['verified_by'],
                'verification_score': current_block['verification_score']
            })
            
            if current_block['hash'] != expected_hash:
                return False
        
        return True

# Usage example
if __name__ == "__main__":
    blockchain = BlockchainVerification()
    
    # Sample job posting
    job_posting = {
        'id': 'job_123',
        'title': 'Software Engineer',
        'company': 'TechCorp',
        'location': 'San Francisco, CA',
        'salary': '$80,000 - $120,000',
        'domain': 'techcorp.com',
        'contact_info': {
            'email': 'hr@techcorp.com',
            'phone': '(555) 123-4567'
        },
        'fraud_score': 15,
        'pattern_matches': []
    }
    
    # Verify job posting
    verification_result = blockchain.verify_job_posting(job_posting)
    print("Job Posting Verification Result:")
    print(json.dumps(verification_result, indent=2))
    
    # Sample company data
    company_data = {
        'name': 'TechCorp',
        'website': 'techcorp.com',
        'employee_count': 150,
        'social_media': {
            'linkedin': 'linkedin.com/company/techcorp',
            'twitter': '@techcorp'
        },
        'reputation_score': 85
    }
    
    # Verify company
    company_verification = blockchain.verify_company_credentials(company_data)
    print("\nCompany Verification Result:")
    print(json.dumps(company_verification, indent=2))
    
    # Check chain integrity
    integrity = blockchain.verify_chain_integrity()
    print(f"\nBlockchain Integrity: {integrity}")
    
    # Get verification history
    history = blockchain.get_verification_history('TechCorp')
    print(f"\nVerification History for TechCorp:")
    print(json.dumps(history, indent=2)) 