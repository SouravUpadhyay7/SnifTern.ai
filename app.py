from flask import Flask, render_template, request, jsonify, send_file
import os
from enhanced_prediction_utils import EnhancedFakeInternshipPredictor
from ocr_utils import extract_text_from_image, is_valid_image, get_ocr_status
from scraping_utils import extract_text_from_url, is_valid_url
import json
from datetime import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import requests
from bs4 import BeautifulSoup
import re

# Import the new analytics modules
from analytics_dashboard import AnalyticsDashboard
from market_intelligence import JobMarketIntelligence, RealTimeAlertSystem
from blockchain_verification import BlockchainVerification

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Initialize enhanced predictor
predictor = EnhancedFakeInternshipPredictor()

# Initialize analytics components
analytics_dashboard = AnalyticsDashboard()
market_intelligence = JobMarketIntelligence()
alert_system = RealTimeAlertSystem()
blockchain_verifier = BlockchainVerification()

# Enhanced company database with more comprehensive information
ENHANCED_COMPANY_DATABASE = {
    # Fraudulent Companies
    "fakecorp": {
        "name": "FakeCorp Inc",
        "fraud_score": 95,
        "reports": 150,
        "last_updated": "2024-01-15",
        "domain_age": "2 months",
        "social_media": "Limited/None",
        "contact_verification": "Failed",
        "industry": "Technology",
        "location": "Unknown",
        "website": "fakecorp-scam.com",
        "red_flags": ["No physical address", "Fake testimonials", "Payment required upfront"]
    },
    "scamtech": {
        "name": "ScamTech Solutions",
        "fraud_score": 88,
        "reports": 89,
        "last_updated": "2024-01-10",
        "domain_age": "3 months",
        "social_media": "None",
        "contact_verification": "Failed",
        "industry": "IT Services",
        "location": "Virtual",
        "website": "scamtech-fake.net",
        "red_flags": ["Virtual office only", "No employee reviews", "Suspicious payment methods"]
    },
    "phishco": {
        "name": "PhishCo Ltd",
        "fraud_score": 92,
        "reports": 234,
        "last_updated": "2024-01-12",
        "domain_age": "1 month",
        "social_media": "Fake profiles",
        "contact_verification": "Failed",
        "industry": "Consulting",
        "location": "International",
        "website": "phishco-scam.org",
        "red_flags": ["International scam", "Fake social media", "Data harvesting"]
    },
    "certscam": {
        "name": "CertScam Academy",
        "fraud_score": 98,
        "reports": 445,
        "last_updated": "2024-01-25",
        "domain_age": "1 month",
        "social_media": "None",
        "contact_verification": "Failed",
        "industry": "Education",
        "location": "Unknown",
        "website": "certscam-academy.biz",
        "red_flags": ["Certificate payment scam", "Fake credentials", "No accreditation"]
    },
    "workfromhomescam": {
        "name": "WorkFromHome Solutions",
        "fraud_score": 93,
        "reports": 267,
        "last_updated": "2024-01-19",
        "domain_age": "6 weeks",
        "social_media": "Fake profiles",
        "contact_verification": "Failed",
        "industry": "Remote Work",
        "location": "Virtual",
        "website": "workfromhome-scam.net",
        "red_flags": ["Work from home scam", "Upfront payments", "Fake testimonials"]
    },
    "fastmoney": {
        "name": "FastMoney Opportunities",
        "fraud_score": 96,
        "reports": 389,
        "last_updated": "2024-01-21",
        "domain_age": "3 weeks",
        "social_media": "None",
        "contact_verification": "Failed",
        "industry": "Financial",
        "location": "Unknown",
        "website": "fastmoney-scam.org",
        "red_flags": ["Get rich quick scheme", "No legitimate business", "Payment required"]
    },
    "internshipscam": {
        "name": "Internship Masters",
        "fraud_score": 90,
        "reports": 198,
        "last_updated": "2024-01-17",
        "domain_age": "2 months",
        "social_media": "Limited",
        "contact_verification": "Failed",
        "industry": "Education",
        "location": "Virtual",
        "website": "internshipmasters-fake.com",
        "red_flags": ["Fake internship certificates", "Payment for placement", "No real mentorship"]
    },
    "digitaldreams": {
        "name": "Digital Dreams Corp",
        "fraud_score": 87,
        "reports": 134,
        "last_updated": "2024-01-13",
        "domain_age": "4 months",
        "social_media": "Fake",
        "contact_verification": "Failed",
        "industry": "Digital Marketing",
        "location": "Unknown",
        "website": "digitaldreams-scam.biz",
        "red_flags": ["Virtual company", "No real clients", "Suspicious payment methods"]
    },
    "onlinescamjobs": {
        "name": "Online Jobs Hub",
        "fraud_score": 94,
        "reports": 356,
        "last_updated": "2024-01-23",
        "domain_age": "2 weeks",
        "social_media": "None",
        "contact_verification": "Failed",
        "industry": "Job Portal",
        "location": "Unknown",
        "website": "onlinejobshub-scam.com",
        "red_flags": ["Registration fees", "Fake job listings", "No legitimate employers"]
    },
    "homebasedwork": {
        "name": "HomeBased Work Solutions",
        "fraud_score": 92,
        "reports": 223,
        "last_updated": "2024-01-20",
        "domain_age": "5 weeks",
        "social_media": "Fake",
        "contact_verification": "Failed",
        "industry": "Remote Work",
        "location": "Virtual",
        "website": "homebasedwork-scam.org",
        "red_flags": ["Work from home scam", "Equipment fees", "No real work provided"]
    },
    "dataentryscam": {
        "name": "DataEntry Masters",
        "fraud_score": 89,
        "reports": 178,
        "last_updated": "2024-01-18",
        "domain_age": "3 months",
        "social_media": "Limited",
        "contact_verification": "Failed",
        "industry": "Data Processing",
        "location": "Unknown",
        "website": "dataentrymasters-fake.net",
        "red_flags": ["Data entry scam", "Training fees", "No legitimate clients"]
    },
    "mlmscam": {
        "name": "MLM Success Network",
        "fraud_score": 95,
        "reports": 412,
        "last_updated": "2024-01-24",
        "domain_age": "4 weeks",
        "social_media": "Fake profiles",
        "contact_verification": "Failed",
        "industry": "Marketing",
        "location": "Virtual",
        "website": "mlmsuccess-scam.biz",
        "red_flags": ["MLM pyramid scheme", "Recruitment fees", "Fake income promises"]
    },
    "surveyscam": {
        "name": "Survey Rewards Pro",
        "fraud_score": 91,
        "reports": 234,
        "last_updated": "2024-01-16",
        "domain_age": "2 months",
        "social_media": "None",
        "contact_verification": "Failed",
        "industry": "Market Research",
        "location": "Unknown",
        "website": "surveyrewards-fake.com",
        "red_flags": ["Survey scam", "Personal data harvesting", "No real rewards"]
    },
    "cryptoscam": {
        "name": "CryptoJobs Global",
        "fraud_score": 97,
        "reports": 567,
        "last_updated": "2024-01-26",
        "domain_age": "3 weeks",
        "social_media": "Fake",
        "contact_verification": "Failed",
        "industry": "Cryptocurrency",
        "location": "International",
        "website": "cryptojobs-scam.org",
        "red_flags": ["Cryptocurrency scam", "Investment required", "Fake trading platform"]
    },
    "tutorscam": {
        "name": "Online Tutor Academy",
        "fraud_score": 88,
        "reports": 145,
        "last_updated": "2024-01-15",
        "domain_age": "3 months",
        "social_media": "Limited",
        "contact_verification": "Failed",
        "industry": "Education",
        "location": "Virtual",
        "website": "onlinetutor-scam.net",
        "red_flags": ["Fake tutoring jobs", "Training material fees", "No real students"]
    },
    "quickcash": {
        "name": "QuickCash Enterprises",
        "fraud_score": 97,
        "reports": 312,
        "last_updated": "2024-01-20",
        "domain_age": "6 weeks",
        "social_media": "None",
        "contact_verification": "Failed",
        "industry": "Financial Services",
        "location": "Unknown",
        "website": "quickcash-money.biz",
        "red_flags": ["Certificate payment required", "Unrealistic salary promises", "No company verification"]
    },
    "easyintern": {
        "name": "EasyIntern Global",
        "fraud_score": 91,
        "reports": 187,
        "last_updated": "2024-01-18",
        "domain_age": "3 months",
        "social_media": "Fake profiles",
        "contact_verification": "Failed",
        "industry": "Education",
        "location": "Virtual",
        "website": "easyintern-fake.org",
        "red_flags": ["Virtual internships with fees", "No real office", "Fake employee testimonials"]
    },
    "instantjobs": {
        "name": "InstantJobs Pro",
        "fraud_score": 89,
        "reports": 156,
        "last_updated": "2024-01-16",
        "domain_age": "2 months",
        "social_media": "Limited",
        "contact_verification": "Failed",
        "industry": "Recruitment",
        "location": "Unknown",
        "website": "instantjobs-scam.net",
        "red_flags": ["Immediate hiring promises", "No interview process", "Payment for job placement"]
    },
    "dreamcareers": {
        "name": "Dream Careers Ltd",
        "fraud_score": 94,
        "reports": 278,
        "last_updated": "2024-01-22",
        "domain_age": "5 weeks",
        "social_media": "None",
        "contact_verification": "Failed",
        "industry": "Career Services",
        "location": "International",
        "website": "dreamcareers-fake.com",
        "red_flags": ["Certificate fees", "Work from home scam", "No legitimate contact info"]
    },
    "globalinternships": {
        "name": "Global Internships Inc",
        "fraud_score": 86,
        "reports": 143,
        "last_updated": "2024-01-14",
        "domain_age": "4 months",
        "social_media": "Fake",
        "contact_verification": "Failed",
        "industry": "Education",
        "location": "Virtual",
        "website": "globalinternships-scam.org",
        "red_flags": ["International internship scam", "Payment required", "No physical presence"]
    },

    # Legitimate Companies
    "google": {
        "name": "Google",
        "fraud_score": 5,
        "reports": 2,
        "last_updated": "2024-01-15",
        "domain_age": "25+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Technology",
        "location": "Mountain View, CA",
        "website": "google.com",
        "green_flags": ["Established company", "Verified contact info", "Positive reviews"]
    },
    "microsoft": {
        "name": "Microsoft",
        "fraud_score": 3,
        "reports": 1,
        "last_updated": "2024-01-15",
        "domain_age": "30+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Technology",
        "location": "Redmond, WA",
        "website": "microsoft.com",
        "green_flags": ["Fortune 500 company", "Verified contact info", "Excellent reputation"]
    },
    "amazon": {
        "name": "Amazon",
        "fraud_score": 6,
        "reports": 5,
        "last_updated": "2024-01-15",
        "domain_age": "25+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "E-commerce",
        "location": "Seattle, WA",
        "website": "amazon.com",
        "green_flags": ["Global company", "Verified contact info", "Established reputation"]
    },
    "apple": {
        "name": "Apple Inc",
        "fraud_score": 4,
        "reports": 1,
        "last_updated": "2024-01-15",
        "domain_age": "30+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Technology",
        "location": "Cupertino, CA",
        "website": "apple.com",
        "green_flags": ["Fortune 500 company", "Global brand", "Excellent employee reviews"]
    },
    "meta": {
        "name": "Meta (Facebook)",
        "fraud_score": 7,
        "reports": 3,
        "last_updated": "2024-01-15",
        "domain_age": "20+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Technology",
        "location": "Menlo Park, CA",
        "website": "meta.com",
        "green_flags": ["Major tech company", "Verified offices", "Strong online presence"]
    },
    "netflix": {
        "name": "Netflix",
        "fraud_score": 8,
        "reports": 4,
        "last_updated": "2024-01-15",
        "domain_age": "25+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Entertainment",
        "location": "Los Gatos, CA",
        "website": "netflix.com",
        "green_flags": ["Global streaming leader", "Public company", "Verified offices worldwide"]
    },
    "tesla": {
        "name": "Tesla Inc",
        "fraud_score": 9,
        "reports": 6,
        "last_updated": "2024-01-15",
        "domain_age": "20+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Automotive",
        "location": "Austin, TX",
        "website": "tesla.com",
        "green_flags": ["Public company", "Global manufacturing", "Innovative technology leader"]
    },
    "spotify": {
        "name": "Spotify",
        "fraud_score": 7,
        "reports": 2,
        "last_updated": "2024-01-15",
        "domain_age": "15+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Music/Technology",
        "location": "Stockholm, Sweden",
        "website": "spotify.com",
        "green_flags": ["Public company", "Global music platform", "Strong brand recognition"]
    },
    "uber": {
        "name": "Uber Technologies",
        "fraud_score": 12,
        "reports": 8,
        "last_updated": "2024-01-15",
        "domain_age": "15+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Transportation",
        "location": "San Francisco, CA",
        "website": "uber.com",
        "green_flags": ["Public company", "Global operations", "Established platform"]
    },
    "airbnb": {
        "name": "Airbnb Inc",
        "fraud_score": 10,
        "reports": 7,
        "last_updated": "2024-01-15",
        "domain_age": "15+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Hospitality",
        "location": "San Francisco, CA",
        "website": "airbnb.com",
        "green_flags": ["Public company", "Global platform", "Verified business model"]
    },
    "salesforce": {
        "name": "Salesforce",
        "fraud_score": 5,
        "reports": 1,
        "last_updated": "2024-01-15",
        "domain_age": "25+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Software",
        "location": "San Francisco, CA",
        "website": "salesforce.com",
        "green_flags": ["Fortune 500 company", "CRM leader", "Strong corporate reputation"]
    },
    "adobe": {
        "name": "Adobe Inc",
        "fraud_score": 6,
        "reports": 2,
        "last_updated": "2024-01-15",
        "domain_age": "30+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Software",
        "location": "San Jose, CA",
        "website": "adobe.com",
        "green_flags": ["Creative software leader", "Public company", "Global presence"]
    },
    "ibm": {
        "name": "IBM",
        "fraud_score": 4,
        "reports": 1,
        "last_updated": "2024-01-15",
        "domain_age": "30+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Technology",
        "location": "Armonk, NY",
        "website": "ibm.com",
        "green_flags": ["Century-old company", "Global technology leader", "Strong corporate governance"]
    },
    "oracle": {
        "name": "Oracle Corporation",
        "fraud_score": 5,
        "reports": 2,
        "last_updated": "2024-01-15",
        "domain_age": "25+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Software",
        "location": "Austin, TX",
        "website": "oracle.com",
        "green_flags": ["Database technology leader", "Fortune 500", "Global enterprise solutions"]
    },
    "intel": {
        "name": "Intel Corporation",
        "fraud_score": 6,
        "reports": 3,
        "last_updated": "2024-01-15",
        "domain_age": "30+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Semiconductors",
        "location": "Santa Clara, CA",
        "website": "intel.com",
        "green_flags": ["Semiconductor leader", "Public company", "Global manufacturing"]
    },
    "nvidia": {
        "name": "NVIDIA Corporation",
        "fraud_score": 7,
        "reports": 2,
        "last_updated": "2024-01-15",
        "domain_age": "30+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Technology",
        "location": "Santa Clara, CA",
        "website": "nvidia.com",
        "green_flags": ["AI technology leader", "Public company", "Innovation leader"]
    },
    "linkedin": {
        "name": "LinkedIn Corporation",
        "fraud_score": 8,
        "reports": 4,
        "last_updated": "2024-01-15",
        "domain_age": "20+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Professional Network",
        "location": "Sunnyvale, CA",
        "website": "linkedin.com",
        "green_flags": ["Professional networking leader", "Microsoft subsidiary", "Verified platform"]
    },
    "tcs": {
        "name": "Tata Consultancy Services",
        "fraud_score": 5,
        "reports": 2,
        "last_updated": "2024-01-15",
        "domain_age": "25+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "IT Services",
        "location": "Mumbai, India",
        "website": "tcs.com",
        "green_flags": ["Global IT services leader", "Public company", "Tata Group subsidiary"]
    },
    "infosys": {
        "name": "Infosys Limited",
        "fraud_score": 6,
        "reports": 3,
        "last_updated": "2024-01-15",
        "domain_age": "25+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "IT Services",
        "location": "Bangalore, India",
        "website": "infosys.com",
        "green_flags": ["IT consulting leader", "Public company", "Global delivery model"]
    },
    "wipro": {
        "name": "Wipro Limited",
        "fraud_score": 7,
        "reports": 3,
        "last_updated": "2024-01-15",
        "domain_age": "25+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "IT Services",
        "location": "Bangalore, India",
        "website": "wipro.com",
        "green_flags": ["IT services provider", "Public company", "Global operations"]
    },
    "accenture": {
        "name": "Accenture",
        "fraud_score": 8,
        "reports": 4,
        "last_updated": "2024-01-15",
        "domain_age": "20+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Consulting",
        "location": "Dublin, Ireland",
        "website": "accenture.com",
        "green_flags": ["Global consulting leader", "Public company", "Fortune 500"]
    },
    "deloitte": {
        "name": "Deloitte",
        "fraud_score": 6,
        "reports": 2,
        "last_updated": "2024-01-15",
        "domain_age": "30+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Consulting",
        "location": "London, UK",
        "website": "deloitte.com",
        "green_flags": ["Big Four consulting", "Global presence", "Professional services leader"]
    },
    "jpmorgan": {
        "name": "JPMorgan Chase",
        "fraud_score": 8,
        "reports": 5,
        "last_updated": "2024-01-15",
        "domain_age": "25+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Banking",
        "location": "New York, NY",
        "website": "jpmorganchase.com",
        "green_flags": ["Major bank", "Fortune 500", "Regulated financial institution"]
    },
    "goldman": {
        "name": "Goldman Sachs",
        "fraud_score": 9,
        "reports": 4,
        "last_updated": "2024-01-15",
        "domain_age": "25+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Investment Banking",
        "location": "New York, NY",
        "website": "goldmansachs.com",
        "green_flags": ["Investment banking leader", "Public company", "Global financial services"]
    },
    "mckinsey": {
        "name": "McKinsey & Company",
        "fraud_score": 7,
        "reports": 3,
        "last_updated": "2024-01-15",
        "domain_age": "30+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Management Consulting",
        "location": "New York, NY",
        "website": "mckinsey.com",
        "green_flags": ["Top consulting firm", "Global presence", "Elite reputation"]
    },
    "pwc": {
        "name": "PricewaterhouseCoopers",
        "fraud_score": 6,
        "reports": 2,
        "last_updated": "2024-01-15",
        "domain_age": "30+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Professional Services",
        "location": "London, UK",
        "website": "pwc.com",
        "green_flags": ["Big Four accounting", "Global network", "Professional services leader"]
    },
    "ey": {
        "name": "Ernst & Young",
        "fraud_score": 7,
        "reports": 3,
        "last_updated": "2024-01-15",
        "domain_age": "30+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Professional Services",
        "location": "London, UK",
        "website": "ey.com",
        "green_flags": ["Big Four accounting", "Global operations", "Professional excellence"]
    },
    "kpmg": {
        "name": "KPMG",
        "fraud_score": 6,
        "reports": 2,
        "last_updated": "2024-01-15",
        "domain_age": "30+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Professional Services",
        "location": "Amstelveen, Netherlands",
        "website": "kpmg.com",
        "green_flags": ["Big Four accounting", "Global network", "Audit and advisory leader"]
    },
    "cisco": {
        "name": "Cisco Systems",
        "fraud_score": 5,
        "reports": 1,
        "last_updated": "2024-01-15",
        "domain_age": "30+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Networking",
        "location": "San Jose, CA",
        "website": "cisco.com",
        "green_flags": ["Networking technology leader", "Public company", "Global infrastructure"]
    },
    "vmware": {
        "name": "VMware",
        "fraud_score": 8,
        "reports": 3,
        "last_updated": "2024-01-15",
        "domain_age": "25+ years",
        "social_media": "Extensive presence",
        "contact_verification": "Verified",
        "industry": "Software",
        "location": "Palo Alto, CA",
        "website": "vmware.com",
        "green_flags": ["Virtualization leader", "Enterprise software", "Strong technology focus"]
    }
}

# Multi-language support
LANGUAGES = {
    'en': {
        'title': 'Sniftern - Advanced Internship Fraud Detection',
        'tagline': 'Advanced AI-Powered Internship Fraud Detection & Company Verification',
        'job_detection': 'Internship Detection',
        'company_search': 'Company Search',
        'job_analysis': 'Internship Posting Analysis',
        'analysis_desc': 'Analyze internship postings for potential fraud using advanced AI and pattern recognition.',
        'direct_text': 'Direct Text',
        'url_extraction': 'URL Extraction',
        'paste_placeholder': 'Paste the internship posting text here...',
        'analyze_btn': 'Analyze Internship Posting',
        'url_placeholder': 'Enter internship posting URL...',
        'extract_btn': 'Extract & Analyze',
        'company_database': 'Company Fraud Database',
        'company_desc': 'Search our comprehensive database to check if a company has been reported for fraud.',
        'company_placeholder': 'Enter company name...',
        'search_btn': 'Search',
        'results': 'Analysis Results',
        'company_info': 'Company Information',
        'footer_copyright': '© 2024 Sniftern. Built with advanced AI and machine learning.',
        'disclaimer': '⚠️ This tool is for educational purposes. Always verify internship postings through official channels.',
        'analyzing': 'Analyzing...',
        'likely_fake': 'Likely FAKE ❌',
        'likely_real': 'Likely REAL ✅',
        'confidence': 'Confidence',
        'words_analyzed': 'Words Analyzed',
        'suspicious_patterns': 'Suspicious Patterns Detected',
        'fraud_detected': 'FRAUD DETECTED',
        'legitimate_company': 'LEGITIMATE COMPANY',
        'fraud_score': 'Fraud Score',
        'reports': 'Reports',
        'last_updated': 'Last Updated',
        'domain_age': 'Domain Age',
        'social_media': 'Social Media',
        'contact_verification': 'Contact Verification',
        'industry': 'Industry',
        'location': 'Location',
        'website': 'Website',
        'red_flags': 'Red Flags',
        'green_flags': 'Green Flags',
        'export_pdf': 'Export PDF Report',
        'salary_analysis': 'Salary Analysis',
        'job_quality': 'Internship Description Quality',
        'interview_analysis': 'Interview Process Analysis',
        'document_analysis': 'Document Analysis',
        'linkedin_integration': 'LinkedIn Integration',
        'indeed_integration': 'Indeed Integration',
        'glassdoor_integration': 'Glassdoor Integration'
    },
    'hi': {
        'title': 'जॉबगार्डियन प्रो - उन्नत नौकरी धोखाधड़ी पहचान',
        'tagline': 'उन्नत AI-संचालित नौकरी धोखाधड़ी पहचान और कंपनी सत्यापन',
        'job_detection': 'इंटर्नशिप पहचान',
        'company_search': 'कंपनी खोज',
        'job_analysis': 'इंटर्नशिप पोस्टिंग विश्लेषण',
        'analysis_desc': 'उन्नत AI और पैटर्न पहचान का उपयोग करके नौकरी पोस्टिंग का विश्लेषण करें।',
        'direct_text': 'सीधा टेक्स्ट',
        'url_extraction': 'URL निष्कर्षण',
        'paste_placeholder': 'नौकरी पोस्टिंग टेक्स्ट यहाँ पेस्ट करें...',
        'analyze_btn': 'नौकरी पोस्टिंग विश्लेषण करें',
        'url_placeholder': 'नौकरी पोस्टिंग URL दर्ज करें...',
        'extract_btn': 'निष्कर्षण और विश्लेषण',
        'company_database': 'कंपनी धोखाधड़ी डेटाबेस',
        'company_desc': 'जांचें कि क्या कंपनी को धोखाधड़ी के लिए रिपोर्ट किया गया है।',
        'company_placeholder': 'कंपनी का नाम दर्ज करें...',
        'search_btn': 'खोजें',
        'results': 'विश्लेषण परिणाम',
        'company_info': 'कंपनी की जानकारी',
        'footer_copyright': '© 2024 जॉबगार्डियन प्रो। उन्नत AI और मशीन लर्निंग के साथ बनाया गया।',
        'disclaimer': '⚠️ यह उपकरण शैक्षिक उद्देश्यों के लिए है। हमेशा आधिकारिक चैनलों के माध्यम से नौकरी पोस्टिंग की जांच करें।',
        'analyzing': 'विश्लेषण कर रहा है...',
        'likely_fake': 'संभवतः नकली ❌',
        'likely_real': 'संभवतः वास्तविक ✅',
        'confidence': 'विश्वास',
        'words_analyzed': 'विश्लेषित शब्द',
        'suspicious_patterns': 'संदिग्ध पैटर्न पाए गए',
        'fraud_detected': 'धोखाधड़ी पाई गई',
        'legitimate_company': 'वैध कंपनी',
        'fraud_score': 'धोखाधड़ी स्कोर',
        'reports': 'रिपोर्ट',
        'last_updated': 'अंतिम अपडेट',
        'domain_age': 'डोमेन आयु',
        'social_media': 'सोशल मीडिया',
        'contact_verification': 'संपर्क सत्यापन',
        'industry': 'उद्योग',
        'location': 'स्थान',
        'website': 'वेबसाइट',
        'red_flags': 'लाल झंडे',
        'green_flags': 'हरे झंडे',
        'export_pdf': 'PDF रिपोर्ट निर्यात करें',
        'salary_analysis': 'वेतन विश्लेषण',
        'job_quality': 'इंटर्नशिप विवरण गुणवत्ता',
        'interview_analysis': 'साक्षात्कार प्रक्रिया विश्लेषण',
        'document_analysis': 'दस्तावेज़ विश्लेषण',
        'linkedin_integration': 'LinkedIn एकीकरण',
        'indeed_integration': 'Indeed एकीकरण',
        'glassdoor_integration': 'Glassdoor एकीकरण'
    },
    'bn': {
        'title': 'জবগার্ডিয়ান প্রো - উন্নত চাকরি প্রতারণা সনাক্তকরণ',
        'tagline': 'উন্নত AI-চালিত চাকরি প্রতারণা সনাক্তকরণ এবং কোম্পানি যাচাইকরণ',
        'job_detection': 'ইন্টার্নশিপ সনাক্তকরণ',
        'company_search': 'কোম্পানি অনুসন্ধান',
        'job_analysis': 'ইন্টার্নশিপ পোস্টিং বিশ্লেষণ',
        'analysis_desc': 'উন্নত AI এবং প্যাটার্ন সনাক্তকরণ ব্যবহার করে চাকরি পোস্টিং বিশ্লেষণ করুন।',
        'direct_text': 'সরাসরি টেক্সট',
        'url_extraction': 'URL নিষ্কর্ষণ',
        'paste_placeholder': 'চাকরি পোস্টিং টেক্সট এখানে পেস্ট করুন...',
        'analyze_btn': 'চাকরি পোস্টিং বিশ্লেষণ করুন',
        'url_placeholder': 'চাকরি পোস্টিং URL লিখুন...',
        'extract_btn': 'নিষ্কর্ষণ এবং বিশ্লেষণ',
        'company_database': 'কোম্পানি প্রতারণা ডেটাবেস',
        'company_desc': 'কোম্পানিকে প্রতারণার জন্য রিপোর্ট করা হয়েছে কিনা তা যাচাই করুন।',
        'company_placeholder': 'কোম্পানির নাম লিখুন...',
        'search_btn': 'অনুসন্ধান করুন',
        'results': 'বিশ্লেষণ ফলাফল',
        'company_info': 'কোম্পানির তথ্য',
        'footer_copyright': '© 2024 জবগার্ডিয়ান প্রো। উন্নত AI এবং মেশিন লার্নিং দিয়ে তৈরি।',
        'disclaimer': '⚠️ এই টুলটি শিক্ষামূলক উদ্দেশ্যে। সর্বদা সরকারি চ্যানেলের মাধ্যমে চাকরি পোস্টিং যাচাই করুন।',
        'analyzing': 'বিশ্লেষণ করছে...',
        'likely_fake': 'সম্ভবত জাল ❌',
        'likely_real': 'সম্ভবত আসল ✅',
        'confidence': 'আত্মবিশ্বাস',
        'words_analyzed': 'বিশ্লেষিত শব্দ',
        'suspicious_patterns': 'সন্দেহজনক প্যাটার্ন পাওয়া গেছে',
        'fraud_detected': 'প্রতারণা সনাক্ত হয়েছে',
        'legitimate_company': 'বৈধ কোম্পানি',
        'fraud_score': 'প্রতারণা স্কোর',
        'reports': 'রিপোর্ট',
        'last_updated': 'সর্বশেষ আপডেট',
        'domain_age': 'ডোমেন বয়স',
        'social_media': 'সামাজিক মাধ্যম',
        'contact_verification': 'যোগাযোগ যাচাইকরণ',
        'industry': 'শিল্প',
        'location': 'অবস্থান',
        'website': 'ওয়েবসাইট',
        'red_flags': 'লাল পতাকা',
        'green_flags': 'সবুজ পতাকা',
        'export_pdf': 'PDF রিপোর্ট রপ্তানি করুন',
        'salary_analysis': 'বেতন বিশ্লেষণ',
        'job_quality': 'ইন্টার্নশিপের বিবরণ গুণমান',
        'interview_analysis': 'সাক্ষাত্কার প্রক্রিয়া বিশ্লেষণ',
        'document_analysis': 'নথি বিশ্লেষণ',
        'linkedin_integration': 'LinkedIn ইন্টিগ্রেশন',
        'indeed_integration': 'Indeed ইন্টিগ্রেশন',
        'glassdoor_integration': 'Glassdoor ইন্টিগ্রেশন'
    }
}

@app.route('/')
def index():
    lang = request.args.get('lang', 'en')
    return render_template('index.html', lang=lang, translations=LANGUAGES.get(lang, LANGUAGES['en']))

@app.route('/detect', methods=['POST'])
def detect_fraud():
    """Detect fraud in job posting text"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Perform fraud detection
        result = predictor.enhanced_predict(text)
        
        # Add to analytics dashboard
        analytics_dashboard.add_analysis_data({
            'result': result['result'],
            'confidence_score': result['confidence_score'],
            'word_count': result['word_count'],
            'pattern_matches': result.get('pattern_matches', []),
            'source': 'manual',
            'company': 'unknown',
            'location': 'unknown',
            'industry': 'unknown'
        })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/search_company', methods=['POST'])
def search_company():
    try:
        data = request.get_json()
        company_name = data.get('company_name', '').lower().strip()
        
        if not company_name:
            return jsonify({'error': 'No company name provided'}), 400
        
        # Search in enhanced company database
        if company_name in ENHANCED_COMPANY_DATABASE:
            company_data = ENHANCED_COMPANY_DATABASE[company_name]
            return jsonify({
                'found': True,
                'is_fraud': company_data['fraud_score'] > 50,
                'company_data': company_data
            })
        
        # Search for partial matches
        matches = {k: v for k, v in ENHANCED_COMPANY_DATABASE.items() 
                  if company_name in k or company_name in v['name'].lower()}
        
        if matches:
            first_match = list(matches.items())[0]
            return jsonify({
                'found': True,
                'is_fraud': first_match[1]['fraud_score'] > 50,
                'company_data': first_match[1],
                'partial_match': True
            })
        
        # Company not found
        return jsonify({
            'found': False,
            'message': 'Company not found in our database. This could be a new company or the name might be misspelled.'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/extract_url', methods=['POST'])
def extract_url():
    try:
        data = request.get_json()
        url = data.get('url', '')
        
        if not url:
            return jsonify({'error': 'No URL provided'}), 400
        
        if not is_valid_url(url):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        extracted_text = extract_text_from_url(url)
        
        if extracted_text:
            return jsonify({
                'success': True,
                'text': extracted_text,
                'word_count': len(extracted_text.split())
            })
        else:
            return jsonify({'error': 'Could not extract text from URL'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_linkedin', methods=['POST'])
def analyze_linkedin():
    """Analyze LinkedIn job posting"""
    try:
        data = request.get_json()
        linkedin_url = data.get('linkedin_url', '').strip()

        if not linkedin_url:
            return jsonify({'error': 'No LinkedIn URL provided'}), 400

        # Validate LinkedIn URL
        if 'linkedin.com/jobs' not in linkedin_url:
            return jsonify({'error': 'Invalid LinkedIn job URL. Please provide a valid LinkedIn job posting URL.'}), 400

        # Extract content from LinkedIn using enhanced scraping
        from scraping_utils import extract_job_content_enhanced

        # Try enhanced extraction first
        extracted_text = extract_job_content_enhanced(linkedin_url)

        # Fallback to original method if enhanced fails
        if not extracted_text:
            extracted_text = extract_linkedin_job_content(linkedin_url)

        if not extracted_text:
            return jsonify({
                'error': 'LinkedIn Anti-Bot Protection Detected',
                'message': 'LinkedIn has sophisticated anti-bot protection that prevents automated content extraction.',
                'suggestions': [
                    'Copy the job description text manually and paste it in the main text analysis box',
                    'Use the "Paste Job Description" option instead',
                    'Try again later as LinkedIn may temporarily block automated requests'
                ],
                'alternative': 'Use the main text analysis feature by copying and pasting the job description directly'
            }), 400

        # Perform prediction
        result = predictor.enhanced_predict(extracted_text)

        # Add AI analysis
        result['salary_analysis'] = predictor.analyze_salary_range(extracted_text)
        result['internship_quality_score'] = predictor.analyze_internship_description_quality(extracted_text)
        result['interview_analysis'] = predictor.analyze_interview_process(extracted_text)

        # Add to analytics dashboard
        analytics_dashboard.add_analysis_data({
            'result': result['result'],
            'confidence_score': result['confidence_score'],
            'word_count': result['word_count'],
            'pattern_matches': result.get('pattern_matches', []),
            'source': 'LinkedIn',
            'company': 'unknown',  # Could extract from URL
            'location': 'unknown',  # Could extract from URL
            'industry': 'unknown'   # Could extract from URL
        })

        return jsonify(result)
    except Exception as e:
        print(f"LinkedIn analysis error: {str(e)}")
        return jsonify({'error': f'Network error: {str(e)}. Please check your connection and try again.'}), 500

@app.route('/test_linkedin_extraction', methods=['POST'])
def test_linkedin_extraction():
    """Test LinkedIn URL extraction without full analysis"""
    try:
        data = request.get_json()
        linkedin_url = data.get('linkedin_url', '').strip()

        if not linkedin_url:
            return jsonify({'error': 'No LinkedIn URL provided'}), 400

        # Validate LinkedIn URL
        if 'linkedin.com/jobs' not in linkedin_url:
            return jsonify({'error': 'Invalid LinkedIn job URL. Please provide a valid LinkedIn job posting URL.'}), 400

        # Test extraction
        from scraping_utils import extract_job_content_enhanced
        enhanced_text = extract_job_content_enhanced(linkedin_url)
        fallback_text = extract_linkedin_job_content(linkedin_url)

        return jsonify({
            'url': linkedin_url,
            'enhanced_extraction_length': len(enhanced_text) if enhanced_text else 0,
            'enhanced_preview': enhanced_text[:200] + '...' if enhanced_text and len(enhanced_text) > 200 else enhanced_text,
            'fallback_extraction_length': len(fallback_text) if fallback_text else 0,
            'fallback_preview': fallback_text[:200] + '...' if fallback_text and len(fallback_text) > 200 else fallback_text,
            'success': bool(enhanced_text or fallback_text)
        })

    except Exception as e:
        print(f"LinkedIn test error: {str(e)}")
        return jsonify({'error': f'Test failed: {str(e)}'}), 500

@app.route('/analyze_indeed', methods=['POST'])
def analyze_indeed():
    try:
        data = request.get_json()
        indeed_url = data.get('indeed_url', '')
        
        if not indeed_url:
            return jsonify({'error': 'No Indeed URL provided'}), 400
        
        # Validate Indeed URL
        if 'indeed.com' not in indeed_url:
            return jsonify({'error': 'Please provide a valid Indeed job posting URL'}), 400
        
        # Extract text from Indeed job posting
        extracted_text = extract_indeed_job_content(indeed_url)
        
        if extracted_text:
            # Get prediction with pattern analysis
            result, confidence_score, icon, pattern_matches = predictor.get_prediction_result(extracted_text)
            
            # AI-Powered Features
            salary_analysis = predictor.analyze_salary_range(extracted_text)
            job_quality_score = predictor.analyze_internship_description_quality(extracted_text)
            interview_analysis = predictor.analyze_interview_process(extracted_text)
            
            return jsonify({
                'success': True,
                'result': result,
                'confidence_score': round(min(100, max(0, confidence_score)), 1),
                'icon': icon,
                'pattern_matches': pattern_matches,
                'word_count': len(extracted_text.split()),
                'salary_analysis': salary_analysis,
                'internship_quality_score': job_quality_score,
                'interview_analysis': interview_analysis,
                'source': 'Indeed'
            })
        else:
            return jsonify({'error': 'Could not extract text from Indeed URL. Indeed may have blocked automated access.'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Indeed analysis failed: {str(e)}'}), 500

@app.route('/analyze_glassdoor', methods=['POST'])
def analyze_glassdoor():
    try:
        data = request.get_json()
        glassdoor_url = data.get('glassdoor_url', '')
        
        if not glassdoor_url:
            return jsonify({'error': 'No Glassdoor URL provided'}), 400
        
        # Validate Glassdoor URL
        if 'glassdoor.com' not in glassdoor_url:
            return jsonify({'error': 'Please provide a valid Glassdoor job posting URL'}), 400
        
        # Extract text from Glassdoor job posting
        extracted_text = extract_glassdoor_job_content(glassdoor_url)
        
        if extracted_text:
            # Get prediction with pattern analysis
            result, confidence_score, icon, pattern_matches = predictor.get_prediction_result(extracted_text)
            
            # AI-Powered Features
            salary_analysis = predictor.analyze_salary_range(extracted_text)
            job_quality_score = predictor.analyze_internship_description_quality(extracted_text)
            interview_analysis = predictor.analyze_interview_process(extracted_text)
            
            return jsonify({
                'success': True,
                'result': result,
                'confidence_score': round(min(100, max(0, confidence_score)), 1),
                'icon': icon,
                'pattern_matches': pattern_matches,
                'word_count': len(extracted_text.split()),
                'salary_analysis': salary_analysis,
                'internship_quality_score': job_quality_score,
                'interview_analysis': interview_analysis,
                'source': 'Glassdoor'
            })
        else:
            return jsonify({'error': 'Could not extract text from Glassdoor URL. Glassdoor may have blocked automated access.'}), 400
    
    except Exception as e:
        return jsonify({'error': f'Glassdoor analysis failed: {str(e)}'}), 500

@app.route('/export_pdf', methods=['POST'])
def export_pdf():
    try:
        data = request.get_json()
        analysis_data = data.get('analysis_data', {})
        
        # Create PDF report
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                              leftMargin=50, rightMargin=50,
                              topMargin=50, bottomMargin=50)
        styles = getSampleStyleSheet()
        story = []

        # Enhanced Title with branding
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=28,
            spaceAfter=10,
            alignment=1,
            textColor=colors.HexColor('#2563eb'),
            fontName='Helvetica-Bold'
        )

        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=14,
            spaceAfter=30,
            alignment=1,
            textColor=colors.HexColor('#64748b'),
            fontName='Helvetica'
        )

        story.append(Paragraph("🔍 Sniftern", title_style))
        story.append(Paragraph("Advanced Internship Fraud Detection Report", subtitle_style))
        story.append(Spacer(1, 20))
        
        # Enhanced Analysis Results Section
        section_style = ParagraphStyle(
            'SectionHeader',
            parent=styles['Heading2'],
            fontSize=18,
            spaceAfter=15,
            textColor=colors.HexColor('#1e40af'),
            fontName='Helvetica-Bold'
        )

        story.append(Paragraph("📊 Analysis Results", section_style))
        story.append(Spacer(1, 12))

        # Determine result color based on analysis
        result_text = analysis_data.get('result', 'N/A')
        result_color = colors.HexColor('#dc2626') if 'FAKE' in result_text.upper() else colors.HexColor('#16a34a')

        result_data = [
            ['Metric', 'Value'],
            ['Detection Result', analysis_data.get('result', 'N/A')],
            ['Confidence Score', f"{analysis_data.get('confidence_score', 0)}%"],
            ['Words Analyzed', str(analysis_data.get('word_count', 0))],
            ['Suspicious Patterns', str(len(analysis_data.get('pattern_matches', [])))]
        ]

        result_table = Table(result_data, colWidths=[200, 200])
        result_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563eb')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f8fafc')),
            ('TEXTCOLOR', (1, 1), (1, 1), result_color),  # Color the result cell
            ('FONTNAME', (1, 1), (1, 1), 'Helvetica-Bold'),  # Bold the result
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
        ]))
        story.append(result_table)
        story.append(Spacer(1, 25))
        
        # Enhanced AI Analysis Section
        if 'salary_analysis' in analysis_data:
            story.append(Paragraph("🤖 AI-Powered Deep Analysis", section_style))
            story.append(Spacer(1, 12))

            ai_data = [
                ['Analysis Category', 'Assessment'],
                ['Salary Analysis', analysis_data.get('salary_analysis', 'N/A')],
                ['Internship Quality Score', analysis_data.get('internship_quality_score', 'N/A')],
                ['Interview Process Analysis', analysis_data.get('interview_analysis', 'N/A')]
            ]

            ai_table = Table(ai_data, colWidths=[200, 300])
            ai_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#059669')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#f0fdf4')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#d1fae5')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP')
            ]))
            story.append(ai_table)
            story.append(Spacer(1, 25))
        
        # Enhanced Patterns Section
        if analysis_data.get('pattern_matches'):
            story.append(Paragraph("⚠️ Suspicious Patterns Detected", section_style))
            story.append(Spacer(1, 12))

            pattern_style = ParagraphStyle(
                'PatternStyle',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=8,
                leftIndent=20,
                textColor=colors.HexColor('#dc2626'),
                fontName='Helvetica'
            )

            for i, pattern in enumerate(analysis_data['pattern_matches'], 1):
                story.append(Paragraph(f"{i}. {pattern}", pattern_style))

            story.append(Spacer(1, 25))
        
        # Enhanced Footer
        story.append(Spacer(1, 30))

        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=10,
            alignment=1,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=5
        )

        story.append(Paragraph("Generated by Sniftern - Advanced Fraud Detection System", footer_style))
        story.append(Paragraph(f"Report Date: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", footer_style))
        story.append(Paragraph("⚠️ This report is for educational and informational purposes only.", footer_style))
        story.append(Paragraph("Always verify internship postings through official company channels.", footer_style))

        doc.build(story)
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name=f"sniftern_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            mimetype='application/pdf'
        )
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Platform-specific scraping functions
def extract_linkedin_job_content(url):
    """Enhanced LinkedIn job content extraction with better error handling"""
    try:
        import time
        import random

        # More comprehensive headers to avoid detection
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://www.linkedin.com/'
        }

        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(1, 3))

        # Make request with longer timeout
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Updated LinkedIn job posting selectors
        job_selectors = [
            '.job-description',
            '.show-more-less-html__markup',
            '.job-description__content',
            '[data-job-description]',
            '.job-description__text',
            '.description__text',
            '.job-description-content',
            '.job-description__content--rich-text',
            '.jobs-description__content',
            '.jobs-description-content__text',
            '.jobs-box__html-content'
        ]

        job_text = ""
        for selector in job_selectors:
            elements = soup.select(selector)
            if elements:
                job_text = ' '.join([elem.get_text(strip=True) for elem in elements])
                if len(job_text) > 50:  # Ensure we got meaningful content
                    break

        # Enhanced fallback: try multiple content extraction strategies
        if not job_text or len(job_text) < 50:
            # Strategy 1: Look for job-related divs
            job_divs = soup.find_all('div', class_=lambda x: x and ('job' in x.lower() or 'description' in x.lower()))
            if job_divs:
                job_text = ' '.join([div.get_text(strip=True) for div in job_divs[:3]])

            # Strategy 2: Look for main content areas
            if not job_text or len(job_text) < 50:
                main_selectors = ['main', 'article', '[role="main"]', '.main-content', '#main-content']
                for selector in main_selectors:
                    main_content = soup.select_one(selector)
                    if main_content:
                        # Remove unwanted elements
                        for element in main_content(['nav', 'footer', 'header', 'script', 'style', 'aside', '.ad']):
                            element.decompose()
                        job_text = main_content.get_text(strip=True)
                        if len(job_text) > 50:
                            break

        # Clean and return text
        if job_text and len(job_text) > 20:
            return clean_extracted_text(job_text)
        else:
            return ""

    except requests.exceptions.RequestException as e:
        print(f"LinkedIn network error: {str(e)}")
        return ""
    except Exception as e:
        print(f"LinkedIn extraction error: {str(e)}")
        return ""

def extract_indeed_job_content(url):
    """Enhanced Indeed job content extraction"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Indeed job posting selectors
        job_selectors = [
            '#jobDescriptionText',
            '.job-description',
            '[data-testid="job-description"]',
            '.jobsearch-jobDescriptionText',
            '.job-description-container'
        ]
        
        job_text = ""
        for selector in job_selectors:
            elements = soup.select(selector)
            if elements:
                job_text = ' '.join([elem.get_text(strip=True) for elem in elements])
                break
        
        # Fallback: try to find any text content
        if not job_text:
            # Remove navigation, footer, and other non-content elements
            for element in soup(['nav', 'footer', 'header', 'script', 'style', 'aside']):
                element.decompose()
            
            # Try to extract main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='main')
            if main_content:
                job_text = main_content.get_text(strip=True)
            else:
                job_text = soup.get_text(strip=True)
        
        # Clean and return text
        if job_text:
            return clean_extracted_text(job_text)
        else:
            return ""
            
    except Exception as e:
        print(f"Indeed extraction error: {str(e)}")
        return ""

def extract_glassdoor_job_content(url):
    """Enhanced Glassdoor job content extraction"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Glassdoor job posting selectors
        job_selectors = [
            '.jobDescriptionContent',
            '.job-description',
            '[data-testid="job-description"]',
            '.desc',
            '.job-description-content'
        ]
        
        job_text = ""
        for selector in job_selectors:
            elements = soup.select(selector)
            if elements:
                job_text = ' '.join([elem.get_text(strip=True) for elem in elements])
                break
        
        # Fallback: try to find any text content
        if not job_text:
            # Remove navigation, footer, and other non-content elements
            for element in soup(['nav', 'footer', 'header', 'script', 'style', 'aside']):
                element.decompose()
            
            # Try to extract main content
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='main')
            if main_content:
                job_text = main_content.get_text(strip=True)
            else:
                job_text = soup.get_text(strip=True)
        
        # Clean and return text
        if job_text:
            return clean_extracted_text(job_text)
        else:
            return ""
            
    except Exception as e:
        print(f"Glassdoor extraction error: {str(e)}")
        return ""

def clean_extracted_text(text):
    """Clean extracted text from job postings"""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove common job site elements
    remove_patterns = [
        r'cookie|privacy|terms|conditions',
        r'sign in|sign up|login|register',
        r'apply now|apply for this job',
        r'share|save|bookmark',
        r'related jobs|similar jobs',
        r'company reviews|employee reviews',
        r'salary estimates|salary information',
        r'job alerts|email alerts',
        r'feedback|report|flag'
    ]
    
    for pattern in remove_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Clean up extra whitespace again
    text = ' '.join(text.split())
    
    return text

@app.route('/analytics')
def analytics_page():
    """Analytics dashboard page"""
    return render_template('analytics.html')

@app.route('/api/analytics/dashboard', methods=['GET'])
def get_analytics_dashboard():
    """Get analytics dashboard data"""
    try:
        # Generate dashboard report
        dashboard_report = analytics_dashboard.generate_dashboard_report()
        
        # Create visualizations
        visualizations = analytics_dashboard.create_visualizations()
        
        return jsonify({
            'success': True,
            'dashboard_data': dashboard_report,
            'visualizations': visualizations
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analytics/market-intelligence', methods=['GET'])
def get_market_intelligence():
    """Get market intelligence report"""
    try:
        # Convert analytics data to job data format for market intelligence
        job_data = []
        for data in analytics_dashboard.analytics_data:
            job_data.append({
                'title': data.get('result', {}).get('title', 'Unknown'),
                'company': data.get('result', {}).get('company', 'Unknown'),
                'location': data.get('result', {}).get('location', 'Unknown'),
                'industry': data.get('result', {}).get('industry', 'Unknown'),
                'is_fraud': data.get('is_fraud', False),
                'pattern_matches': data.get('pattern_matches', []),
                'posted_date': data.get('timestamp', ''),
                'salary_analysis': data.get('result', {}).get('salary_analysis', ''),
                'description': data.get('result', {}).get('description', '')
            })
        
        # Generate market intelligence report
        market_report = market_intelligence.generate_market_report(job_data)
        
        # Check for alerts
        alerts = alert_system.check_alerts(market_report)
        
        return jsonify({
            'success': True,
            'market_intelligence': market_report,
            'alerts': alerts
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analytics/blockchain-verification', methods=['POST'])
def verify_with_blockchain():
    """Verify job posting or company with blockchain"""
    try:
        data = request.get_json()
        verification_type = data.get('type', 'job_posting')
        
        if verification_type == 'job_posting':
            verification_result = blockchain_verifier.verify_job_posting(data.get('job_data', {}))
        elif verification_type == 'company':
            verification_result = blockchain_verifier.verify_company_credentials(data.get('company_data', {}))
        else:
            return jsonify({
                'success': False,
                'error': 'Invalid verification type'
            }), 400
        
        return jsonify({
            'success': True,
            'verification_result': verification_result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/analytics/verification-history/<identifier>', methods=['GET'])
def get_verification_history(identifier):
    """Get verification history for a specific identifier"""
    try:
        history = blockchain_verifier.get_verification_history(identifier)
        
        return jsonify({
            'success': True,
            'verification_history': history
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 