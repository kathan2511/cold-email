#!/usr/bin/env python3
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
from config_manager import SecureConfigManager

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Initialize secure config manager
config_manager = SecureConfigManager()

def generate_email_addresses(first, last, company_domain):
    """Generate potential corporate email addresses based on common patterns."""
    first = first.lower()
    last = last.lower()
    f = first[0]
    l = last[0]
    patterns = [
        f"{first}.{last}@{company_domain}",
        f"{first}{last}@{company_domain}",
        f"{first}.{l}@{company_domain}",
        f"{f}{last}@{company_domain}",
        f"{first}@{company_domain}",
        f"{f}.{last}@{company_domain}",
        f"{last}.{first}@{company_domain}",
        f"{last}{first}@{company_domain}",
    ]
    return patterns

def create_email_message(sender, recipient, subject, body, attachment_path):
    """Create a MIME email message with HTML body and PDF attachment."""
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    # Attach the email body as HTML
    msg.attach(MIMEText(body, "html"))

    # Attach the PDF resume
    filename = os.path.basename(attachment_path)
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "pdf")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={filename}")
    msg.attach(part)

    return msg

# Resume paths
RESUME_ENGINEER = "/Users/kathanshah/Downloads/SDE/Hrutwi-Kakadia.pdf"
RESUME_ANALYST = "/Users/kathanshah/Downloads/BIA/Hrutwi-Kakadia.pdf"
RESUME_ML = "/Users/kathanshah/Downloads/ML/Hrutwi-Kakadia.pdf"

# Email templates (same as in your script)
EMAIL_TEMPLATE_ENGINEER = (
    "<p>Hi {first_name},</p>"
    "<p>Hope you're having a great day! I'm <strong>Hrutwi Kakadia</strong>, a driven <strong>Software Engineer</strong> who loves building resilient, high-throughput systems. I'm reaching out because I'm interested in the work your team is doing at <strong>{company}</strong> and would be thrilled to contribute as a <strong>{job_description}</strong>. If there's an opening on your team—or a neighboring team you think might be a fit for my profile—I'd really appreciate being considered (or pointed toward the right person).</p>"
    "<p><strong>A quick snapshot of what I bring</strong></p>"
    "<ul>"
    "<li>Optimized database interaction layers using <strong>Spring Data JPA</strong> and connection pooling, reducing query response times by <strong>42%</strong>.</li>"
    "<li>Developed and maintained high-availability <strong>ETL systems</strong> and <strong>Snowflake APIs</strong> in Python that process <strong>10 M+ records per day</strong></li>"
    "<li>Designed and deployed a <strong>Spring-Boot microservice</strong> on <strong>AWS ECS</strong> ingesting <strong>10 M+ events/day</strong>, cutting data-landing latency by <strong>45%</strong>.</li>"
    "<li>Authored <strong>85% coverage JUnit/Mockito</strong> test‑suite, eliminating regression defects in quarterly releases.</li>"
    "<li>Integrated <strong>Apache Kafka streams</strong> with <strong>SnowPipe</strong> to enable real-time data ingestion into cloud warehouses</li>"
    "</ul>"
    "<p>I'm a quick study who doesn't mind late nights when something really critical is on the line, and I'm happy to close any gaps on the job.</p>"
    "<p>My resume is attached for your reference. Thanks for your time and consideration. I really appreciate it, and I'd love to chat if there's a match.</p>"
    "<p>Best,</p>"
    "<p><strong>Hrutwi Kakadia</strong><br>"
    "+1 (551) 285-8965 | khrutwi@gmail.com | <a href='https://www.linkedin.com/in/hrutwi-kakadia/'>LinkedIn</a></p>"
)

EMAIL_TEMPLATE_ANALYST = (
    "<p>Hi {first_name},</p>"
    "<p>I'm <strong>Hrutwi Kakadia</strong>, a <strong>Business Intelligence Engineer</strong> skilled at turning raw data into dashboards executives actually use to drive key business decisions. I admire how <strong>{company}</strong> leverages analytics, and I'd love to contribute as a <strong>{job_description}</strong>. If your team (or an adjacent one) has any openings I'd be a good fit for, I'd be grateful for a referral or an initial chat.</p>"
    "<p><strong>Highlights that map to your BI stack</strong></p>"
    "<ul>"
    "<li>Built and automated <strong>ETL pipelines</strong> to pull <strong>IICS API</strong> and <strong>Snowflake</strong> data, trimming manual reporting effort by <strong>94%</strong>.</li>"
    "<li>Led cost-optimization deep-dive benchmarking <strong>Snowflake against Databricks</strong>, boosting query efficiency by <strong>35%</strong>.</li>"
    "<li>Crafted <strong>Power BI/Tableau KPI dashboards</strong> that give executives real-time visibility into spend and usage trends.</li>"
    "</ul>"
    "<p>I thrive on steep learning curves, and even if I'm not a perfect fit today, I'm ready to put in the work to upskill on any additional tools you rely on.</p>"
    "<p>My resume is attached for your reference. Thank you for your time and consideration. I look forward to the possibility of working together.</p>"
    "<p>Best,</p>"
    "<p><strong>Hrutwi Kakadia</strong><br>"
    "+1 (551) 285-8965 | khrutwi@gmail.com | <a href='https://www.linkedin.com/in/hrutwi-kakadia/'>LinkedIn</a></p>"
)

EMAIL_TEMPLATE_ML = (
    "<p>Hi {first_name},</p>"
    "<p>Hope you are having a great day! I'm <strong>Hrutwi Kakadia</strong>, a <strong>Data Scientist and Machine Learning Engineer</strong> passionate about translating petabyte-scale data into models that move business metrics. Your team's work at <strong>{company}</strong> is something I am really interested in, and I'd be excited to contribute as a <strong>{job_description}</strong>. If you know of any openings or could point me toward a relevant team, I'd truly appreciate it.</p>"
    "<p><strong>Where I could hit the ground running</strong></p>"
    "<ul>"
    "<li>Built a <strong>Python time-series pipeline</strong> that forecasts <strong>Snowflake credit spend</strong>, improving budget accuracy by <strong>30%</strong></li>"
    "<li>Designed a <strong>causal-impact framework</strong> that quantified query-tuning savings and helped secure a <strong>$2M budget allocation</strong></li>"
    "<li>Trained an <strong>XGBoost model</strong> on <strong>5M marketing events</strong>, raising lead-conversion precision from <strong>0.27 to 0.61</strong></li>"
    "</ul>"
    "<p>I'm relentlessly curious, happy to put in extra hours, and confident I can master any additional domain knowledge your projects require.</p>"
    "<p>My resume is attached for more detail. Thanks so much for your time and consideration—I'd love to discuss how I might contribute at <strong>{company}</strong>.</p>"
    "<p>Best,</p>"
    "<p><strong>Hrutwi Kakadia</strong><br>"
    "+1 (551) 285-8965 | khrutwi@gmail.com | <a href='https://www.linkedin.com/in/hrutwi-kakadia/'>LinkedIn</a></p>"
)

def classify_job_description(job_description):
    """Classify job description to determine email template and resume."""
    jd = job_description.lower()
    engineer_keywords = ["engineer", "developer", "backend", "frontend", "software"]
    analyst_keywords = ["business analyst", "business intelligence", "bi", "data analyst", "analytics"]
    ml_keywords = ["machine learning", "ml", "data scientist", "data science", "ai", "artificial intelligence"]
    
    if any(k in jd for k in ml_keywords):
        return "ml"
    if any(k in jd for k in analyst_keywords):
        return "analyst"
    if any(k in jd for k in engineer_keywords) and "business" not in jd:
        return "engineer"
    return "engineer"

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.json
        
        # Extract form data
        first_name = data.get('firstName', '').strip()
        last_name = data.get('lastName', '').strip()
        company = data.get('company', '').strip()
        job_description = data.get('jobDescription', '').strip()
        sender_email = data.get('senderEmail', '').strip()
        sender_password = data.get('senderPassword', '').strip()
        
        # Try to get credentials from secure storage if not provided
        if not sender_email or not sender_password:
            stored_email, stored_password = config_manager.load_credentials("your_master_password_123")
            if stored_email and stored_password:
                sender_email = stored_email
                sender_password = stored_password
                print(f"✅ Using stored credentials for {sender_email}")
            else:
                return jsonify({'error': 'No email credentials provided and none found in secure storage. Please provide credentials or run setup.'}), 400
        
        # Validate required fields
        if not all([first_name, last_name, company, job_description]):
            return jsonify({'error': 'First name, last name, company, and job description are required'}), 400
        
        # Classify job and select template/resume
        job_type = classify_job_description(job_description)
        if job_type == "engineer":
            resume_path = RESUME_ENGINEER
            email_template = EMAIL_TEMPLATE_ENGINEER
        elif job_type == "analyst":
            resume_path = RESUME_ANALYST
            email_template = EMAIL_TEMPLATE_ANALYST
        elif job_type == "ml":
            resume_path = RESUME_ML
            email_template = EMAIL_TEMPLATE_ML
        else:
            resume_path = RESUME_ENGINEER
            email_template = EMAIL_TEMPLATE_ENGINEER
        
        # Check if resume file exists
        if not os.path.exists(resume_path):
            return jsonify({'error': f'Resume file not found: {resume_path}'}), 400
        
        # Generate company domain and email addresses
        company_domain = company.lower().replace(" ", "") + ".com"
        possible_emails = generate_email_addresses(first_name, last_name, company_domain)
        
        # Connect to SMTP server
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
        except Exception as e:
            return jsonify({'error': f'Failed to connect to email server: {str(e)}'}), 400
        
        sent_emails = []
        failed_emails = []
        
        # Send emails to all possible addresses
        for recipient in possible_emails:
            try:
                # Personalize email body
                body = email_template.format(
                    first_name=first_name,
                    company=company,
                    job_description=job_description
                )
                
                # Create subject
                subject = f"Interested in working at {company} as a {job_description}"
                
                # Create and send email
                msg = create_email_message(sender_email, recipient, subject, body, resume_path)
                server.send_message(msg)
                sent_emails.append(recipient)
                
            except Exception as e:
                failed_emails.append({'email': recipient, 'error': str(e)})
        
        server.quit()
        
        return jsonify({
            'success': True,
            'message': f'Emails sent successfully to {len(sent_emails)} addresses',
            'sent_emails': sent_emails,
            'failed_emails': failed_emails,
            'job_type': job_type
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/credentials-status', methods=['GET'])
def credentials_status():
    """Check if credentials are available in secure storage."""
    # Check environment variables first
    env_email = os.getenv('EMAIL_ADDRESS')
    env_password = os.getenv('EMAIL_PASSWORD')
    
    if env_email and env_password:
        return jsonify({
            'has_credentials': True,
            'email': env_email,
            'source': 'environment'
        })
    
    # Check if encrypted file exists
    if config_manager.credentials_exist():
        # For the status check, we'll assume the encrypted file is valid
        # We don't want to prompt for password in the API
        return jsonify({
            'has_credentials': True,
            'email': 'stored_securely@encrypted.file',
            'source': 'encrypted_file'
        })
    
    return jsonify({'has_credentials': False})

if __name__ == '__main__':
    app.run(debug=True, port=5001) 