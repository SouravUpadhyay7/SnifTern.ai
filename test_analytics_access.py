#!/usr/bin/env python3
"""
Test script to demonstrate how to access the Analytics Dashboard
Shows different ways to interact with the analytics features
"""

import requests
import json
import time
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"

def test_analytics_access():
    """Test different ways to access analytics dashboard"""
    print("🚀 Testing Analytics Dashboard Access")
    print("=" * 50)
    
    # Test 1: Access analytics page
    print("\n1. 📊 Testing Analytics Page Access")
    try:
        response = requests.get(f"{BASE_URL}/analytics")
        if response.status_code == 200:
            print("✅ Analytics page accessible")
            print(f"   Status: {response.status_code}")
            print(f"   Content length: {len(response.text)} characters")
        else:
            print(f"❌ Analytics page not accessible: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing analytics page: {str(e)}")
    
    # Test 2: Get dashboard data via API
    print("\n2. 📈 Testing Dashboard API")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/dashboard")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Dashboard API working")
                dashboard_data = data.get('dashboard_data', {})
                summary = dashboard_data.get('summary_metrics', {})
                print(f"   Total analyses: {summary.get('total_analyses', 0)}")
                print(f"   Fraud detected: {summary.get('fraud_detected', 0)}")
                print(f"   Fraud rate: {summary.get('fraud_rate_percentage', 0)}%")
            else:
                print(f"❌ Dashboard API error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Dashboard API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing dashboard API: {str(e)}")
    
    # Test 3: Get market intelligence
    print("\n3. 🔍 Testing Market Intelligence API")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/market-intelligence")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Market Intelligence API working")
                market_data = data.get('market_intelligence', {})
                summary = market_data.get('summary', {})
                print(f"   Total jobs analyzed: {summary.get('total_jobs_analyzed', 0)}")
                print(f"   Fraud rate: {summary.get('fraud_rate_percentage', 0)}%")
                print(f"   Critical threats: {summary.get('critical_threats', 0)}")
                
                alerts = data.get('alerts', [])
                if alerts:
                    print(f"   Active alerts: {len(alerts)}")
                    for alert in alerts[:2]:  # Show first 2 alerts
                        print(f"     - {alert.get('severity')}: {alert.get('message')}")
                else:
                    print("   No active alerts")
            else:
                print(f"❌ Market Intelligence API error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Market Intelligence API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error accessing market intelligence API: {str(e)}")
    
    # Test 4: Test blockchain verification
    print("\n4. 🔐 Testing Blockchain Verification")
    try:
        # Test job posting verification
        job_data = {
            'id': 'test_job_123',
            'title': 'Software Engineer',
            'company': 'TestCorp',
            'location': 'San Francisco, CA',
            'salary': '$80,000 - $120,000',
            'domain': 'testcorp.com',
            'contact_info': {
                'email': 'hr@testcorp.com',
                'phone': '(555) 123-4567'
            },
            'fraud_score': 15,
            'pattern_matches': []
        }
        
        response = requests.post(
            f"{BASE_URL}/api/analytics/blockchain-verification",
            headers={'Content-Type': 'application/json'},
            json={'type': 'job_posting', 'job_data': job_data}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Blockchain verification working")
                verification_result = data.get('verification_result', {})
                print(f"   Verification score: {verification_result.get('verification_score', 0)}%")
                print(f"   Verified: {verification_result.get('verified', False)}")
                print(f"   Block hash: {verification_result.get('block_hash', 'N/A')[:20]}...")
            else:
                print(f"❌ Blockchain verification error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Blockchain verification failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing blockchain verification: {str(e)}")
    
    # Test 5: Get verification history
    print("\n5. 📜 Testing Verification History")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/verification-history/TestCorp")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                history = data.get('verification_history', [])
                print(f"✅ Verification history working")
                print(f"   History entries: {len(history)}")
                if history:
                    latest = history[0]
                    print(f"   Latest verification: {latest.get('timestamp', 'N/A')}")
                    print(f"   Verification score: {latest.get('verification_score', 0)}%")
            else:
                print(f"❌ Verification history error: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ Verification history failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing verification history: {str(e)}")

def add_sample_data():
    """Add sample data to the analytics dashboard"""
    print("\n📊 Adding Sample Data to Analytics Dashboard")
    print("=" * 50)
    
    # Sample job postings to analyze
    sample_jobs = [
        {
            'text': 'We are looking for a remote data entry specialist. No experience required. You can work from home and earn $50-100 per hour. Immediate start available. Please send your personal information including bank details and credit card information.',
            'source': 'manual'
        },
        {
            'text': 'Software Engineer Intern at Google. Join our team in Mountain View, CA. Competitive salary, great benefits, and mentorship opportunities. Must have strong programming skills in Python, Java, or C++.',
            'source': 'manual'
        },
        {
            'text': 'URGENT: Make money fast! No experience needed. Send $50 for training certificate. Earn $200 per day working from home. Limited time offer!',
            'source': 'manual'
        }
    ]
    
    for i, job in enumerate(sample_jobs, 1):
        print(f"\nAnalyzing sample job {i}...")
        try:
            response = requests.post(
                f"{BASE_URL}/detect",
                headers={'Content-Type': 'application/json'},
                json={'text': job['text']}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Job {i} analyzed successfully")
                print(f"   Result: {result.get('result', 'N/A')}")
                print(f"   Confidence: {result.get('confidence_score', 0)}%")
                print(f"   Source: {job['source']}")
            else:
                print(f"❌ Failed to analyze job {i}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Error analyzing job {i}: {str(e)}")
        
        time.sleep(1)  # Small delay between requests

def show_usage_instructions():
    """Show how to use the analytics dashboard"""
    print("\n📖 How to Access Analytics Dashboard")
    print("=" * 50)
    
    print("\n🌐 Web Interface:")
    print("1. Start the Flask app: python app.py")
    print("2. Open browser and go to: http://localhost:5000")
    print("3. Click on 'Analytics Dashboard' in the navigation")
    print("4. View real-time analytics and insights")
    
    print("\n🔌 API Endpoints:")
    print("• GET /analytics - Analytics dashboard page")
    print("• GET /api/analytics/dashboard - Dashboard data")
    print("• GET /api/analytics/market-intelligence - Market intelligence")
    print("• POST /api/analytics/blockchain-verification - Verify with blockchain")
    print("• GET /api/analytics/verification-history/<id> - Verification history")
    
    print("\n📊 Features Available:")
    print("• Real-time fraud trend analysis")
    print("• Industry and location risk insights")
    print("• Market intelligence and alerts")
    print("• Blockchain verification records")
    print("• Interactive charts and visualizations")
    print("• Actionable recommendations")
    
    print("\n💡 Tips:")
    print("• The dashboard gets better with more data")
    print("• Analyze different types of jobs for comprehensive insights")
    print("• Check the market intelligence for emerging threats")
    print("• Use blockchain verification for high-value job postings")

def main():
    """Main test function"""
    print("🎯 SnifTern.ai Analytics Dashboard Access Test")
    print("=" * 60)
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code != 200:
            print("❌ Server is not responding properly")
            return
    except:
        print("❌ Server is not running. Please start the Flask app first:")
        print("   python app.py")
        return
    
    print("✅ Server is running")
    
    # Run tests
    test_analytics_access()
    
    # Add sample data
    add_sample_data()
    
    # Show usage instructions
    show_usage_instructions()
    
    print("\n" + "=" * 60)
    print("🎉 Analytics Dashboard Access Test Complete!")
    print("\nNext steps:")
    print("1. Visit http://localhost:5000/analytics in your browser")
    print("2. Explore the different analytics features")
    print("3. Analyze more jobs to see richer insights")
    print("4. Check the market intelligence for trends")

if __name__ == "__main__":
    main() 