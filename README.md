Stock Predictor
A cloud-based stock tracking and analysis application built with AWS services and vanilla JavaScript. This application allows users to view real-time stock data, analyze historical price trends, and track their investment budget across multiple stocks.
Live Website
Website URL: http://stock-predictor-frontend.s3-website-us-east-1.amazonaws.com
Author
Abdullah Navaid
Table of Contents

Features
Architecture
Technologies Used
Project Structure
AWS Services
Setup and Deployment
Usage
API Documentation
Future Enhancements
Contributing

Features

Real-Time Stock Data: View current stock prices, daily gains/losses, and trading volumes
Interactive Stock List: Sortable table displaying multiple stocks with key metrics
Historical Analysis: 60-day price charts showing close, high, and low prices
Ticker Search: Search and filter specific stocks from the available list
Responsive Design: Clean, professional interface with elegant serif typography
Visual Indicators: Color-coded gains (green) and losses (red) for quick analysis
Data Validation: Input validation and error handling for seamless user experience

Architecture
This application follows a serverless architecture pattern using AWS cloud services:
User Browser
    |
CloudFront Distribution
    |
S3 Static Website Hosting (Frontend)
    |
API Gateway (REST API)
    |
Lambda Function (Backend Logic - Python)
    |
S3 Bucket (Stock Data Storage - ZIP files)
    |
CloudWatch (Monitoring & Logging)
Technologies Used
Frontend

HTML5: Semantic markup and structure
CSS3: Custom styling with Google Fonts (Lora)
JavaScript (ES6+): Vanilla JS for application logic
Chart.js: Interactive price charts and data visualization
Responsive Design: Mobile-friendly layout

Backend & Infrastructure

Python 3.x: Lambda function runtime
AWS Lambda: Serverless compute for API logic

Static website hosting for frontend files
Storage for stock data (ZIP files)


AWS API Gateway: RESTful API endpoint management
AWS CloudWatch: Error monitoring and application logging
AWS CloudFront: Content delivery network (CDN)

Project Structure
stock-predictor/
├── frontend/
│   ├── start.html          # Budget input page (entry point)
│   ├── index.html          # Stock list and search interface
│   ├── results.html        # Individual stock details and charts
|   ├── error.html          # Redirects to error page if wrong stock ticker
├── lambda_package/
│   └── lambda_function.py     # Python Lambda function code
├── local_server.py         # Runs the site locally
└── requirements.txt        # Contains all needed packages
Frontend Files Description
start.html
The initial entry point of the application where users input their investment budget. This page validates the budget input and passes it to the stock list page via URL parameters.
index.html
The main stock tracker interface that displays a sortable table of all available stocks. Features include:

Real-time stock data display
Sortable columns (Ticker, Date, Gain/Loss, High, Low, Volume)
Color-coded daily gains and losses
Ticker search functionality
Budget display carried over from start page

results.html
Individual stock detail page showing comprehensive information for a selected ticker:

Latest stock prices (Open, High, Low, Close)
Trading volume
Interactive 60-day price chart with Chart.js
Historical price trends visualization

AWS Services
1. Amazon S3

Frontend Hosting: Hosts all HTML, CSS, and JavaScript files
Data Storage: Stores stock data ZIP files for Lambda processing
Static Website: Configured for public read access with index document
Bucket Configuration: Enabled static website hosting with start.html as index

2. AWS Lambda

Runtime: Python 3.x
Function: Processes stock data requests from ZIP files and returns JSON responses
Trigger: API Gateway invocation
Permissions: IAM role with S3 read access to stock data bucket
Handler: Extracts and parses stock data from S3-hosted ZIP files

3. API Gateway

Type: REST API
Endpoint: https://a3gp55veoh.execute-api.us-east-1.amazonaws.com/prod/stocks
Method: GET
Integration: Lambda proxy integration
CORS: Enabled for cross-origin requests from S3-hosted frontend

4. CloudWatch

Logs: Lambda function execution logs with detailed error tracking
Metrics: API request counts, error rates, latency measurements
Alarms: Error threshold monitoring for server issues
Retention: Log groups for debugging and performance analysis

5. CloudFront

Distribution: CDN for faster global content delivery
Origin: S3 static website endpoint
Caching: Optimized cache policies for static assets
SSL/TLS: HTTPS support for secure connections

Setup and Deployment
Prerequisites

AWS Account with appropriate permissions
AWS CLI configured with credentials
Python 3.x installed locally
Basic knowledge of AWS services

Frontend Deployment

Create S3 Bucket for Frontend

bashaws s3 mb s3://stock-predictor-frontend
aws s3 website s3://stock-predictor-frontend --index-document start.html

Upload Frontend Files

bashaws s3 sync ./frontend s3://stock-predictor-frontend --acl public-read

Configure Bucket Policy for Public Access

json{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "PublicReadGetObject",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::stock-predictor-frontend/*"
    }
  ]
}
Backend Deployment

Create Lambda function via AWS Console
Select Python 3.x runtime
Upload function code as ZIP or paste inline
Set environment variables (S3_BUCKET_NAME, ZIP_FILE_KEY)
Configure execution role with S3 read permissions
Set timeout to 30 seconds (for ZIP processing)
Allocate sufficient memory (256MB minimum)


Configure API Gateway


Create new REST API
Create resource and GET method
Set Lambda proxy integration
Enable CORS with allowed origins
Deploy to production stage
Note the invoke URL for frontend integration


Set Up CloudWatch Monitoring


Lambda automatically creates log groups
Create custom CloudWatch alarms for error rates
Set up SNS notifications for critical errors
Configure log retention policies


Configure CloudFront Distribution (Optional)


Create distribution with S3 origin
Configure custom domain if needed
Set up SSL certificate
Configure cache behaviors for optimal performance

Usage
Step 1: Set Budget

Navigate to http://stock-predictor-frontend.s3-website-us-east-1.amazonaws.com
Enter your investment budget on the start.html page
Click Continue to proceed to the stock list

Step 2: Browse Stocks

View the complete list of available stocks on index.html
Sort by clicking column headers (Ticker, Date, Gain/Loss, High, Low, Volume)
Review daily performance metrics with color-coded indicators
Green indicates positive gains, red indicates losses

Step 3: Search Specific Ticker

Enter a stock ticker symbol in the search box
Click Search Ticker button
System validates ticker exists in database
Navigate to detailed view if ticker is valid

Step 4: Analyze Historical Data

On results.html, view latest stock metrics
Review open, close, high, low prices and volume
Analyze the interactive 60-day price chart
Compare close price, high price, and low price trends
Use Back to Stock List link to return or Change Budget to restart

API Documentation
Get All Stocks
Endpoint: GET /prod/stocks
Description: Returns all available stock data with 60-day historical prices
Request: No parameters required
Response Format:
json{
  "stocks": [
    {
      "ticker": "AAPL",
      "history": [
        {
          "date": "2025-10-20",
          "open": 175.50,
          "close": 178.20,
          "high": 179.00,
          "low": 174.80,
          "volume": 52000000
        }
      ]
    }
  ]
}



Lambda Function Implementation
The backend uses a Python Lambda function that:

Reads ZIP file from S3 bucket
Extracts and parses stock data
Formats data into JSON structure
Returns response to API Gateway
Handles errors and logs to CloudWatch

Key Python libraries used:

boto3: AWS SDK for S3 interactions
zipfile: Extract data from ZIP archives
json: Format response data

Future Enhancements

User Authentication: Implement AWS Cognito for user accounts and saved preferences
Portfolio Tracking: Save and track multiple stock portfolios with DynamoDB
Real-Time Updates: WebSocket integration via API Gateway for live price updates
Advanced Analytics: Technical indicators (RSI, MACD, Moving Averages)
Price Alerts: SNS/SES notifications for price threshold alerts
Mobile App: React Native mobile application
Database Integration: DynamoDB for persistent user data and preferences
AI Predictions: SageMaker integration for ML-based price forecasting
News Integration: Display relevant financial news per stock using external APIs
Export Functionality: Generate and download reports as PDF/CSV
Multi-Currency Support: Display prices in different currencies
Dark Mode: Theme toggle for better user experience
Performance Optimization: Implement caching strategies with ElastiCache

Known Issues

Budget is passed via URL parameters (consider session storage for production)
No persistent storage for user preferences across sessions
Limited to 60 days of historical data per stock
Single-page navigation without routing library
ZIP file processing may have cold start latency

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository
Create a feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a Pull Request with detailed description

License
This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

Chart.js for excellent charting library and documentation
Google Fonts for Lora typography
AWS for comprehensive cloud infrastructure and documentation
Financial data providers for stock market data

Contact
Abdullah Navaid
GitHub: github.com/your-username
Email: anavaidwork@gmail.com
Security Notes

All API endpoints use HTTPS encryption
CloudWatch monitors for suspicious activity and errors
S3 buckets follow least-privilege access principles
No sensitive data stored in frontend code
Input validation prevents XSS and injection attacks
Lambda function has minimal IAM permissions (S3 read only)
CORS configured to allow only necessary origins

Performance Considerations

CloudFront CDN reduces latency for global users
Lambda function optimized for fast ZIP extraction
Chart.js configured for efficient rendering
Minimal external dependencies for faster load times
S3 static hosting provides high availability

Troubleshooting
Issue: Stock data not loading

Check CloudWatch logs for Lambda errors
Verify API Gateway endpoint is accessible
Ensure S3 bucket has correct permissions
Confirm ZIP file exists in S3 bucket

Issue: Charts not rendering

Verify Chart.js CDN is accessible
Check browser console for JavaScript errors
Ensure stock history data is properly formatted

Issue: Budget not passing between pages

Verify URL parameters are being set correctly
Check browser console for navigation errors
Ensure start.html form is submitting properly

Built with AWS Cloud Services and JavaScript
