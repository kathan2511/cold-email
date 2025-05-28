# Cold Email Sender

A web-based application for sending personalized cold emails for job referrals with automatic template selection based on job type.

## Features

- **Web UI**: Clean React interface for easy email sending
- **Automatic Template Selection**: Detects job type (Engineer/Analyst/ML) and selects appropriate email template
- **HTML Emails**: Sends formatted emails with bold text and clickable links
- **Multiple Email Patterns**: Generates various email address patterns for better reach
- **Resume Attachment**: Automatically attaches the appropriate resume based on job type

## Setup Instructions

### Prerequisites

- Python 3.7+
- Node.js 14+
- Gmail account with App Password enabled

### Backend Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Update resume paths in `email_api.py`:**
   ```python
   RESUME_ENGINEER = "/path/to/your/engineer-resume.pdf"
   RESUME_ANALYST = "/path/to/your/analyst-resume.pdf"
   RESUME_ML = "/path/to/your/ml-resume.pdf"
   ```

3. **Start the Flask API server:**
   ```bash
   python email_api.py
   ```
   The API will run on `http://localhost:5000`

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd email-frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the React development server:**
   ```bash
   npm start
   ```
   The web app will open at `http://localhost:3000`

## Usage

1. **Open the web application** at `http://localhost:3000`

2. **Fill in the form:**
   - **First Name**: Recipient's first name
   - **Last Name**: Recipient's last name
   - **Company**: Target company name
   - **Job Description**: Role you're interested in (e.g., "Software Engineer", "Data Scientist")
   - **Your Email**: Your Gmail address
   - **Email Password**: Your Gmail App Password (not regular password)

3. **Click "Send Emails"** - The system will:
   - Detect the job type from the description
   - Select the appropriate email template and resume
   - Generate multiple potential email addresses
   - Send personalized HTML emails to all generated addresses

## Gmail App Password Setup

For security, Gmail requires App Passwords for third-party applications:

1. Enable 2-Factor Authentication on your Google account
2. Go to Google Account settings → Security → App passwords
3. Generate a new app password for "Mail"
4. Use this 16-character password in the web form

## Email Templates

The system includes three specialized templates:

- **Software Engineer**: Highlights technical skills, frameworks, and system design
- **Business Analyst**: Focuses on data analysis, dashboards, and business intelligence
- **Machine Learning**: Emphasizes ML models, data science, and AI projects

## File Structure

```
├── cold-email.py          # Original command-line script
├── email_api.py           # Flask API backend
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── email-frontend/       # React frontend
    ├── package.json
    ├── public/
    │   └── index.html
    └── src/
        ├── App.js        # Main React component
        ├── App.css       # Styling
        ├── index.js      # React entry point
        └── index.css     # Base styles
```

## Security Notes

- Never commit your email credentials to version control
- Use Gmail App Passwords instead of regular passwords
- The password field in the web form is not stored anywhere
- All email sending happens locally on your machine

## Troubleshooting

**"Resume file not found" error:**
- Update the resume paths in `email_api.py` to match your actual file locations

**"Failed to connect to email server" error:**
- Verify your Gmail credentials
- Ensure you're using an App Password, not your regular password
- Check that 2FA is enabled on your Google account

**CORS errors:**
- Make sure both the Flask API (port 5000) and React app (port 3000) are running
- The Flask app includes CORS headers for local development

## Original Command-Line Version

The original `cold-email.py` script can still be used with Excel/CSV files:

```bash
python cold-email.py input.xlsx --sender your.email@gmail.com
``` 