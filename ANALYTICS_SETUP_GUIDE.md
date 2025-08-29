# 📊 Analytics Dashboard Setup & Access Guide

This guide shows you how to access and use the SnifTern.ai Analytics Dashboard.

## 🚀 **Quick Start**

### 1. **Start the Application**
```bash
python app.py
```

### 2. **Access the Dashboard**
- **Web Interface**: Go to `http://localhost:5000/analytics`
- **Navigation**: Click "Analytics Dashboard" in the main navigation
- **Direct URL**: `http://localhost:5000/analytics`

## 🌐 **Web Interface Access**

### **Method 1: Through Main Navigation**
1. Open `http://localhost:5000`
2. Look for "Analytics Dashboard" in the navigation tabs
3. Click to access the dashboard

### **Method 2: Direct URL**
- Navigate directly to: `http://localhost:5000/analytics`

### **Method 3: API Access**
- Dashboard data: `GET http://localhost:5000/api/analytics/dashboard`
- Market intelligence: `GET http://localhost:5000/api/analytics/market-intelligence`

## 📊 **What You'll See**

### **1. Summary Metrics**
- **Total Analyses**: Number of jobs analyzed
- **Fraud Detected**: Number of fake jobs found
- **Fraud Rate**: Percentage of fake jobs
- **Average Confidence**: Detection confidence score

### **2. Interactive Charts**
- **Fraud Trends**: Daily fraud rate over time
- **Industry Analysis**: Fraud rates by industry
- **Pattern Distribution**: Types of fraud patterns

### **3. Market Intelligence**
- **High-Risk Industries**: Industries with high fraud rates
- **High-Risk Locations**: Locations with high fraud rates
- **Emerging Threats**: New fraud patterns detected
- **Real-Time Alerts**: Critical security alerts

### **4. Recommendations**
- Actionable advice based on current data
- Security recommendations
- Best practices for job seekers

## 🔧 **API Endpoints**

### **Dashboard Data**
```bash
GET /api/analytics/dashboard
```
Returns comprehensive dashboard data including metrics, trends, and visualizations.

### **Market Intelligence**
```bash
GET /api/analytics/market-intelligence
```
Returns market intelligence report with fraud trends and alerts.

### **Blockchain Verification**
```bash
POST /api/analytics/blockchain-verification
Content-Type: application/json

{
  "type": "job_posting",
  "job_data": {
    "id": "job_123",
    "title": "Software Engineer",
    "company": "TechCorp",
    "location": "San Francisco, CA",
    "salary": "$80,000 - $120,000",
    "domain": "techcorp.com",
    "contact_info": {
      "email": "hr@techcorp.com",
      "phone": "(555) 123-4567"
    },
    "fraud_score": 15,
    "pattern_matches": []
  }
}
```

### **Verification History**
```bash
GET /api/analytics/verification-history/{identifier}
```
Returns verification history for a specific company or job posting.

## 🧪 **Testing the Dashboard**

### **Run the Test Script**
```bash
python test_analytics_access.py
```

This script will:
- Test all analytics endpoints
- Add sample data to the dashboard
- Show you how to access different features

### **Manual Testing**
1. **Add Sample Data**:
   ```bash
   curl -X POST http://localhost:5000/detect \
     -H "Content-Type: application/json" \
     -d '{"text": "We are looking for a remote data entry specialist. No experience required. You can work from home and earn $50-100 per hour."}'
   ```

2. **Check Dashboard**:
   ```bash
   curl http://localhost:5000/api/analytics/dashboard
   ```

3. **Get Market Intelligence**:
   ```bash
   curl http://localhost:5000/api/analytics/market-intelligence
   ```

## 📈 **Dashboard Features**

### **Real-Time Analytics**
- Live fraud trend analysis
- Industry risk assessment
- Location-based insights
- Pattern recognition

### **Interactive Visualizations**
- Line charts for fraud trends
- Bar charts for industry analysis
- Doughnut charts for pattern distribution
- Responsive design for all devices

### **Market Intelligence**
- Fraud pattern analysis
- Emerging threat detection
- Risk level assessment
- Actionable recommendations

### **Blockchain Integration**
- Immutable verification records
- Trust score calculation
- Verification history tracking
- Data integrity assurance

## 🔍 **Understanding the Data**

### **Fraud Rate Calculation**
```
Fraud Rate = (Number of Fake Jobs / Total Jobs Analyzed) × 100
```

### **Confidence Score**
- **90-100%**: Very high confidence
- **70-89%**: High confidence
- **50-69%**: Medium confidence
- **Below 50%**: Low confidence

### **Risk Levels**
- **CRITICAL**: 50%+ fraud rate
- **HIGH**: 30-49% fraud rate
- **MEDIUM**: 15-29% fraud rate
- **LOW**: 5-14% fraud rate
- **SAFE**: Below 5% fraud rate

## 🛠️ **Troubleshooting**

### **Dashboard Not Loading**
1. Check if Flask app is running: `python app.py`
2. Verify the URL: `http://localhost:5000/analytics`
3. Check browser console for errors
4. Ensure all dependencies are installed

### **No Data Showing**
1. Analyze some jobs first to generate data
2. Run the test script: `python test_analytics_access.py`
3. Check if the analytics modules are imported correctly

### **API Errors**
1. Check server logs for error messages
2. Verify API endpoint URLs
3. Ensure proper JSON format for POST requests
4. Check if all required modules are installed

### **Charts Not Displaying**
1. Check if Chart.js is loading properly
2. Verify internet connection for CDN resources
3. Check browser console for JavaScript errors
4. Ensure data is in the correct format

## 📱 **Mobile Access**

The analytics dashboard is fully responsive and works on:
- **Desktop**: Full feature access
- **Tablet**: Optimized layout
- **Mobile**: Touch-friendly interface

## 🔄 **Data Refresh**

### **Automatic Refresh**
- Dashboard loads fresh data on each visit
- Real-time updates for new analyses

### **Manual Refresh**
- Click the "🔄 Refresh Data" button
- Use browser refresh (F5)

### **API Refresh**
```bash
curl http://localhost:5000/api/analytics/dashboard
```

## 📊 **Data Sources**

The dashboard aggregates data from:
- **Manual job analysis**: Direct text input
- **LinkedIn integration**: LinkedIn job postings
- **Indeed integration**: Indeed job postings
- **Glassdoor integration**: Glassdoor job postings
- **URL extraction**: Generic job posting URLs

## 🎯 **Best Practices**

### **For Users**
1. **Regular Monitoring**: Check dashboard regularly for trends
2. **Data Quality**: Analyze diverse job types for better insights
3. **Alert Response**: Pay attention to real-time alerts
4. **Recommendations**: Follow provided security recommendations

### **For Developers**
1. **Data Collection**: Ensure all job analyses are logged
2. **Error Handling**: Implement proper error handling for API calls
3. **Performance**: Monitor dashboard performance with large datasets
4. **Security**: Implement proper authentication for sensitive data

## 🚀 **Advanced Usage**

### **Custom Analytics**
You can extend the dashboard by:
- Adding new metrics
- Creating custom visualizations
- Implementing additional data sources
- Building custom reports

### **Integration**
The dashboard can be integrated with:
- **Business Intelligence tools**: Tableau, Power BI
- **Monitoring systems**: Grafana, Kibana
- **Alert systems**: Email, SMS, Slack
- **Data warehouses**: For long-term storage

---

## 🎉 **You're Ready!**

Now you can access the SnifTern.ai Analytics Dashboard and explore:
- Real-time fraud insights
- Market intelligence
- Interactive visualizations
- Blockchain verification
- Actionable recommendations

**Start exploring**: `http://localhost:5000/analytics` 