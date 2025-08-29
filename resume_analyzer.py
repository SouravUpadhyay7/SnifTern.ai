#!/usr/bin/env python3
"""
AI-Powered Resume Analyzer for SnifTern.ai
Analyzes resumes for job compatibility and potential red flags
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import spacy
from collections import Counter

class ResumeAnalyzer:
    def __init__(self):
        self.skill_keywords = {
            'programming': ['python', 'java', 'javascript', 'c++', 'sql', 'html', 'css', 'react', 'node.js'],
            'data_science': ['machine learning', 'data analysis', 'statistics', 'pandas', 'numpy', 'tensorflow'],
            'design': ['photoshop', 'illustrator', 'figma', 'ui/ux', 'graphic design', 'web design'],
            'marketing': ['social media', 'content creation', 'seo', 'google ads', 'email marketing'],
            'business': ['project management', 'leadership', 'strategy', 'analytics', 'sales']
        }
        
        self.red_flags = {
            'suspicious_skills': ['expert in everything', 'master of all technologies', '100% success rate'],
            'unrealistic_experience': ['10 years experience at age 20', 'ceo at 18', 'founded 50 companies'],
            'grammar_issues': ['poor grammar', 'spelling mistakes', 'inconsistent formatting'],
            'missing_info': ['no contact information', 'no education details', 'no work history'],
            'suspicious_dates': ['future dates', 'overlapping employment', 'gaps too long']
        }
        
    def analyze_resume(self, resume_text: str, job_requirements: str) -> Dict:
        """
        Comprehensive resume analysis
        """
        analysis = {
            'compatibility_score': 0,
            'skill_match': {},
            'experience_match': {},
            'education_match': {},
            'red_flags': [],
            'recommendations': [],
            'overall_assessment': '',
            'detailed_analysis': {}
        }
        
        # Extract information from resume
        resume_info = self._extract_resume_info(resume_text)
        
        # Extract job requirements
        job_info = self._extract_job_requirements(job_requirements)
        
        # Analyze skill compatibility
        skill_analysis = self._analyze_skill_compatibility(resume_info, job_info)
        analysis['skill_match'] = skill_analysis
        
        # Analyze experience compatibility
        experience_analysis = self._analyze_experience_compatibility(resume_info, job_info)
        analysis['experience_match'] = experience_analysis
        
        # Analyze education compatibility
        education_analysis = self._analyze_education_compatibility(resume_info, job_info)
        analysis['education_match'] = education_analysis
        
        # Check for red flags
        red_flags = self._check_red_flags(resume_text, resume_info)
        analysis['red_flags'] = red_flags
        
        # Calculate overall compatibility score
        compatibility_score = self._calculate_compatibility_score(
            skill_analysis, experience_analysis, education_analysis, red_flags
        )
        analysis['compatibility_score'] = compatibility_score
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            skill_analysis, experience_analysis, education_analysis, red_flags
        )
        analysis['recommendations'] = recommendations
        
        # Overall assessment
        analysis['overall_assessment'] = self._generate_overall_assessment(compatibility_score, red_flags)
        
        # Detailed analysis
        analysis['detailed_analysis'] = {
            'resume_info': resume_info,
            'job_info': job_info,
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        return analysis
    
    def _extract_resume_info(self, resume_text: str) -> Dict:
        """Extract key information from resume"""
        info = {
            'skills': [],
            'experience': [],
            'education': [],
            'contact_info': {},
            'summary': '',
            'languages': [],
            'certifications': []
        }
        
        # Extract skills
        info['skills'] = self._extract_skills(resume_text)
        
        # Extract experience
        info['experience'] = self._extract_experience(resume_text)
        
        # Extract education
        info['education'] = self._extract_education(resume_text)
        
        # Extract contact information
        info['contact_info'] = self._extract_contact_info(resume_text)
        
        # Extract summary
        info['summary'] = self._extract_summary(resume_text)
        
        # Extract languages
        info['languages'] = self._extract_languages(resume_text)
        
        # Extract certifications
        info['certifications'] = self._extract_certifications(resume_text)
        
        return info
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract skills from resume text"""
        skills = []
        text_lower = text.lower()
        
        # Extract skills from all categories
        for category, keywords in self.skill_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    skills.append(keyword)
        
        # Extract additional skills using regex patterns
        skill_patterns = [
            r'\b(?:proficient in|skilled in|experience with|knowledge of)\s+([^,\n]+)',
            r'\b(?:expertise in|specialized in|certified in)\s+([^,\n]+)',
            r'\b(?:programming languages?|technologies?|tools?|frameworks?):\s*([^.\n]+)'
        ]
        
        for pattern in skill_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                skills.extend([skill.strip() for skill in match.split(',')])
        
        return list(set(skills))  # Remove duplicates
    
    def _extract_experience(self, text: str) -> List[Dict]:
        """Extract work experience from resume"""
        experience = []
        
        # Look for experience patterns
        experience_patterns = [
            r'(\w+\s+\d{4})\s*[-–—]\s*(\w+\s+\d{4}|\bpresent\b)',
            r'(\d{4})\s*[-–—]\s*(\d{4}|\bpresent\b)',
            r'(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\s*[-–—]\s*(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}'
        ]
        
        # Extract job titles
        job_title_patterns = [
            r'\b(?:software engineer|developer|analyst|manager|director|coordinator|specialist|assistant|intern)\b',
            r'\b(?:senior|junior|lead|principal|associate)\s+\w+',
            r'\b(?:full stack|front end|back end|data|machine learning|ai|devops)\s+\w+'
        ]
        
        # This is a simplified extraction - in a real implementation, you'd use more sophisticated NLP
        lines = text.split('\n')
        current_job = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for job titles
            for pattern in job_title_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    if current_job:
                        experience.append(current_job)
                    current_job = {'title': match.group(), 'company': '', 'duration': '', 'description': ''}
                    break
            
            # Look for company names
            if current_job and not current_job.get('company'):
                company_patterns = [
                    r'\b(?:at|with|for)\s+([A-Z][A-Za-z\s&]+(?:Inc|Corp|LLC|Ltd|Company))',
                    r'\b([A-Z][A-Za-z\s&]+(?:Inc|Corp|LLC|Ltd|Company))\b'
                ]
                for pattern in company_patterns:
                    match = re.search(pattern, line)
                    if match:
                        current_job['company'] = match.group(1) if match.groups() else match.group()
                        break
        
        if current_job:
            experience.append(current_job)
        
        return experience
    
    def _extract_education(self, text: str) -> List[Dict]:
        """Extract education information"""
        education = []
        
        # Look for degree patterns
        degree_patterns = [
            r'\b(?:bachelor|master|phd|doctorate|associate)\s+(?:of|in)\s+([^,\n]+)',
            r'\b(?:bs|ba|ms|ma|phd|mba)\s+(?:in\s+)?([^,\n]+)',
            r'\b(?:degree|diploma|certificate)\s+(?:in\s+)?([^,\n]+)'
        ]
        
        # Look for university patterns
        university_patterns = [
            r'\b(?:university|college|institute|school)\s+of\s+([^,\n]+)',
            r'\b([A-Z][A-Za-z\s&]+(?:University|College|Institute|School))\b'
        ]
        
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            degree_match = None
            university_match = None
            
            for pattern in degree_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    degree_match = match.group()
                    break
            
            for pattern in university_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    university_match = match.group()
                    break
            
            if degree_match or university_match:
                education.append({
                    'degree': degree_match or '',
                    'university': university_match or '',
                    'year': self._extract_year(line)
                })
        
        return education
    
    def _extract_contact_info(self, text: str) -> Dict:
        """Extract contact information"""
        contact = {}
        
        # Email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact['email'] = email_match.group()
        
        # Phone
        phone_patterns = [
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\b\+\d{1,3}[-.]?\d{3}[-.]?\d{3}[-.]?\d{4}\b'
        ]
        for pattern in phone_patterns:
            phone_match = re.search(pattern, text)
            if phone_match:
                contact['phone'] = phone_match.group()
                break
        
        # LinkedIn
        linkedin_pattern = r'linkedin\.com/in/[A-Za-z0-9-]+'
        linkedin_match = re.search(linkedin_pattern, text)
        if linkedin_match:
            contact['linkedin'] = linkedin_match.group()
        
        return contact
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary"""
        summary_patterns = [
            r'\b(?:summary|objective|profile|about)\s*:?\s*([^.\n]+)',
            r'\b(?:experienced|skilled|passionate|dedicated)\s+([^.\n]+)'
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_languages(self, text: str) -> List[str]:
        """Extract language skills"""
        languages = []
        language_patterns = [
            r'\b(?:languages?|fluent in|speak)\s*:?\s*([^.\n]+)',
            r'\b(?:english|spanish|french|german|chinese|japanese|arabic|hindi|portuguese|russian)\b'
        ]
        
        for pattern in language_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    languages.extend([lang.strip() for lang in match[0].split(',')])
                else:
                    languages.append(match)
        
        return list(set(languages))
    
    def _extract_certifications(self, text: str) -> List[str]:
        """Extract certifications"""
        certifications = []
        cert_patterns = [
            r'\b(?:certified|certification|certificate)\s+(?:in\s+)?([^,\n]+)',
            r'\b(?:aws|azure|google|cisco|microsoft|oracle)\s+(?:certified|certification)\b',
            r'\b(?:pmp|scrum|agile|six sigma|lean)\s+(?:certified|certification)\b'
        ]
        
        for pattern in cert_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            certifications.extend(matches)
        
        return list(set(certifications))
    
    def _extract_job_requirements(self, requirements: str) -> Dict:
        """Extract job requirements"""
        job_info = {
            'required_skills': [],
            'preferred_skills': [],
            'experience_level': '',
            'education_requirements': [],
            'responsibilities': []
        }
        
        text_lower = requirements.lower()
        
        # Extract required skills
        required_patterns = [
            r'\b(?:required|must have|essential)\s+(?:skills?|experience?|knowledge?)\s*:?\s*([^.\n]+)',
            r'\b(?:proficiency in|experience with|knowledge of)\s+([^.\n]+)'
        ]
        
        for pattern in required_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                job_info['required_skills'].extend([skill.strip() for skill in match.split(',')])
        
        # Extract preferred skills
        preferred_patterns = [
            r'\b(?:preferred|nice to have|bonus|plus)\s+(?:skills?|experience?)\s*:?\s*([^.\n]+)',
            r'\b(?:familiarity with|understanding of)\s+([^.\n]+)'
        ]
        
        for pattern in preferred_patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                job_info['preferred_skills'].extend([skill.strip() for skill in match.split(',')])
        
        # Extract experience level
        experience_patterns = [
            r'\b(?:entry level|junior|senior|lead|principal|expert)\s+\w+',
            r'\b(\d+)\s+(?:years?|yrs?)\s+(?:of\s+)?experience\b'
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, text_lower)
            if match:
                job_info['experience_level'] = match.group()
                break
        
        return job_info
    
    def _analyze_skill_compatibility(self, resume_info: Dict, job_info: Dict) -> Dict:
        """Analyze skill compatibility between resume and job requirements"""
        analysis = {
            'required_skills_match': 0,
            'preferred_skills_match': 0,
            'missing_required_skills': [],
            'matching_skills': [],
            'score': 0
        }
        
        resume_skills = set(skill.lower() for skill in resume_info['skills'])
        required_skills = set(skill.lower() for skill in job_info['required_skills'])
        preferred_skills = set(skill.lower() for skill in job_info['preferred_skills'])
        
        # Check required skills
        matching_required = resume_skills.intersection(required_skills)
        missing_required = required_skills - resume_skills
        
        analysis['required_skills_match'] = len(matching_required)
        analysis['missing_required_skills'] = list(missing_required)
        analysis['matching_skills'].extend(list(matching_required))
        
        # Check preferred skills
        matching_preferred = resume_skills.intersection(preferred_skills)
        analysis['preferred_skills_match'] = len(matching_preferred)
        analysis['matching_skills'].extend(list(matching_preferred))
        
        # Calculate score
        total_required = len(required_skills)
        total_preferred = len(preferred_skills)
        
        if total_required > 0:
            required_score = len(matching_required) / total_required * 70  # 70% weight for required
        else:
            required_score = 0
        
        if total_preferred > 0:
            preferred_score = len(matching_preferred) / total_preferred * 30  # 30% weight for preferred
        else:
            preferred_score = 0
        
        analysis['score'] = required_score + preferred_score
        
        return analysis
    
    def _analyze_experience_compatibility(self, resume_info: Dict, job_info: Dict) -> Dict:
        """Analyze experience compatibility"""
        analysis = {
            'experience_level_match': False,
            'years_experience': 0,
            'relevant_experience': [],
            'score': 0
        }
        
        # Extract years of experience from resume
        total_years = 0
        for exp in resume_info['experience']:
            if 'duration' in exp and exp['duration']:
                # Simple duration parsing - in real implementation, use more sophisticated parsing
                duration = exp['duration']
                years_match = re.search(r'(\d+)\s*(?:years?|yrs?)', duration)
                if years_match:
                    total_years += int(years_match.group(1))
        
        analysis['years_experience'] = total_years
        
        # Check if experience level matches
        job_level = job_info['experience_level'].lower()
        if 'entry' in job_level or 'junior' in job_level:
            analysis['experience_level_match'] = total_years <= 3
        elif 'senior' in job_level or 'lead' in job_level:
            analysis['experience_level_match'] = total_years >= 5
        elif 'principal' in job_level or 'expert' in job_level:
            analysis['experience_level_match'] = total_years >= 8
        else:
            analysis['experience_level_match'] = True
        
        # Calculate score based on experience level match
        if analysis['experience_level_match']:
            analysis['score'] = 100
        else:
            analysis['score'] = max(0, 100 - abs(total_years - 5) * 10)
        
        return analysis
    
    def _analyze_education_compatibility(self, resume_info: Dict, job_info: Dict) -> Dict:
        """Analyze education compatibility"""
        analysis = {
            'education_level_match': False,
            'relevant_degrees': [],
            'score': 0
        }
        
        # Check if education requirements are met
        job_education = job_info['education_requirements']
        resume_education = resume_info['education']
        
        if not job_education:  # No specific education requirements
            analysis['education_level_match'] = True
            analysis['score'] = 100
        else:
            # Check if any degree matches requirements
            for degree in resume_education:
                degree_text = degree.get('degree', '').lower()
                for req in job_education:
                    if req.lower() in degree_text:
                        analysis['education_level_match'] = True
                        analysis['relevant_degrees'].append(degree)
                        break
            
            analysis['score'] = 100 if analysis['education_level_match'] else 50
        
        return analysis
    
    def _check_red_flags(self, text: str, resume_info: Dict) -> List[Dict]:
        """Check for red flags in resume"""
        red_flags = []
        text_lower = text.lower()
        
        # Check for suspicious skills
        for flag in self.red_flags['suspicious_skills']:
            if flag in text_lower:
                red_flags.append({
                    'type': 'suspicious_skills',
                    'description': f'Unrealistic skill claim: "{flag}"',
                    'severity': 'high'
                })
        
        # Check for unrealistic experience
        for flag in self.red_flags['unrealistic_experience']:
            if flag in text_lower:
                red_flags.append({
                    'type': 'unrealistic_experience',
                    'description': f'Unrealistic experience claim: "{flag}"',
                    'severity': 'critical'
                })
        
        # Check for grammar issues
        grammar_issues = self._check_grammar(text)
        if grammar_issues:
            red_flags.append({
                'type': 'grammar_issues',
                'description': f'Grammar/spelling issues detected: {grammar_issues}',
                'severity': 'medium'
            })
        
        # Check for missing information
        missing_info = []
        if not resume_info['contact_info']:
            missing_info.append('contact information')
        if not resume_info['education']:
            missing_info.append('education details')
        if not resume_info['experience']:
            missing_info.append('work experience')
        
        if missing_info:
            red_flags.append({
                'type': 'missing_info',
                'description': f'Missing important information: {", ".join(missing_info)}',
                'severity': 'high'
            })
        
        return red_flags
    
    def _check_grammar(self, text: str) -> str:
        """Simple grammar check - in real implementation, use proper NLP libraries"""
        issues = []
        
        # Check for common spelling mistakes
        common_mistakes = {
            'recieve': 'receive',
            'seperate': 'separate',
            'definately': 'definitely',
            'occassion': 'occasion',
            'accomodate': 'accommodate'
        }
        
        for mistake, correction in common_mistakes.items():
            if mistake in text.lower():
                issues.append(f'"{mistake}" should be "{correction}"')
        
        # Check for excessive capitalization
        words = text.split()
        excessive_caps = sum(1 for word in words if word.isupper() and len(word) > 2)
        if excessive_caps > len(words) * 0.1:  # More than 10% of words are all caps
            issues.append('Excessive use of capitalization')
        
        return '; '.join(issues) if issues else ''
    
    def _calculate_compatibility_score(self, skill_analysis: Dict, experience_analysis: Dict, 
                                     education_analysis: Dict, red_flags: List[Dict]) -> float:
        """Calculate overall compatibility score"""
        # Weighted scoring
        skill_score = skill_analysis['score'] * 0.4  # 40% weight
        experience_score = experience_analysis['score'] * 0.3  # 30% weight
        education_score = education_analysis['score'] * 0.2  # 20% weight
        red_flag_penalty = len(red_flags) * 10  # 10 points penalty per red flag
        
        total_score = skill_score + experience_score + education_score - red_flag_penalty
        
        return max(0, min(100, total_score))  # Clamp between 0 and 100
    
    def _generate_recommendations(self, skill_analysis: Dict, experience_analysis: Dict,
                                education_analysis: Dict, red_flags: List[Dict]) -> List[str]:
        """Generate recommendations for improvement"""
        recommendations = []
        
        # Skill recommendations
        missing_skills = skill_analysis.get('missing_required_skills', [])
        if missing_skills:
            recommendations.append(f"🔧 Develop skills in: {', '.join(missing_skills[:3])}")
        
        # Experience recommendations
        if not experience_analysis['experience_level_match']:
            years_needed = experience_analysis['years_experience']
            if years_needed < 3:
                recommendations.append("📈 Gain more work experience to meet job requirements")
            elif years_needed > 10:
                recommendations.append("🎯 Consider applying for senior-level positions")
        
        # Education recommendations
        if not education_analysis['education_level_match']:
            recommendations.append("🎓 Consider additional education or certifications")
        
        # Red flag recommendations
        for flag in red_flags:
            if flag['type'] == 'grammar_issues':
                recommendations.append("✍️ Review and fix grammar/spelling issues")
            elif flag['type'] == 'missing_info':
                recommendations.append("📝 Add missing information to resume")
            elif flag['type'] == 'suspicious_skills':
                recommendations.append("⚠️ Be more specific about skills and avoid unrealistic claims")
        
        return recommendations
    
    def _generate_overall_assessment(self, compatibility_score: float, red_flags: List[Dict]) -> str:
        """Generate overall assessment"""
        if compatibility_score >= 90:
            assessment = "Excellent match! Strong candidate for the position."
        elif compatibility_score >= 75:
            assessment = "Good match with some areas for improvement."
        elif compatibility_score >= 60:
            assessment = "Moderate match. Consider addressing key gaps."
        elif compatibility_score >= 40:
            assessment = "Weak match. Significant improvements needed."
        else:
            assessment = "Poor match. Consider different opportunities."
        
        if red_flags:
            critical_flags = [f for f in red_flags if f['severity'] == 'critical']
            if critical_flags:
                assessment += " ⚠️ Critical red flags detected."
            else:
                assessment += " ⚠️ Some concerns identified."
        
        return assessment
    
    def _extract_year(self, text: str) -> str:
        """Extract year from text"""
        year_match = re.search(r'\b(19|20)\d{2}\b', text)
        return year_match.group() if year_match else ''

# Usage example
if __name__ == "__main__":
    analyzer = ResumeAnalyzer()
    
    # Sample resume text
    resume_text = """
    JOHN DOE
    Software Engineer
    john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe
    
    SUMMARY
    Experienced software engineer with 3 years of experience in Python, JavaScript, and React.
    
    EXPERIENCE
    Software Engineer | TechCorp | 2021 - Present
    - Developed web applications using React and Node.js
    - Collaborated with cross-functional teams
    
    EDUCATION
    Bachelor of Science in Computer Science | University of Technology | 2021
    
    SKILLS
    Python, JavaScript, React, Node.js, SQL, Git, AWS
    """
    
    # Sample job requirements
    job_requirements = """
    Required Skills: Python, JavaScript, React, SQL
    Preferred Skills: AWS, Node.js, Git
    Experience Level: 2-4 years
    Education: Bachelor's degree in Computer Science or related field
    """
    
    # Analyze resume
    analysis = analyzer.analyze_resume(resume_text, job_requirements)
    
    print("Resume Analysis Results:")
    print(json.dumps(analysis, indent=2)) 