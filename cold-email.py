#!/usr/bin/env python3
import os
import pandas as pd
import argparse
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import getpass

def generate_email_addresses(first, last, company_domain):
    """
    Generate a list of potential corporate email addresses based on common patterns.
    Patterns include:
      - first.last@company.com
      - firstlast@company.com
      - first.[first letter of last]@company.com
      - [first initial][last]@company.com
      - first@company.com
      - [first initial].last@company.com
      - last.first@company.com
      - lastfirst@company.com
    """
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
    """
    Create a MIME email message with a text body and a PDF attachment.
    """
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    # Attach the email body as HTML.
    msg.attach(MIMEText(body, "html"))

    # Attach the PDF resume.
    filename = os.path.basename(attachment_path)
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "pdf")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={filename}")
    msg.attach(part)

    return msg

# === Hardcoded resume paths ===
RESUME_ENGINEER = "/Users/kathanshah/Downloads/SDE/Hrutwi-Kakadia.pdf"
RESUME_ANALYST = "/Users/kathanshah/Downloads/BIA/Hrutwi-Kakadia.pdf"
RESUME_ML = "/Users/kathanshah/Downloads/ML/Hrutwi-Kakadia.pdf"

# === Email templates ===
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

# === Job description classifier ===
def classify_job_description(job_description):
    jd = job_description.lower()
    # Engineer roles (but not if 'business' is present)
    engineer_keywords = ["engineer", "developer", "backend", "frontend", "software"]
    analyst_keywords = ["business analyst", "business intelligence", "bi", "data analyst", "analytics"]
    ml_keywords = ["machine learning", "ml", "data scientist", "data science", "ai", "artificial intelligence"]
    
    if any(k in jd for k in ml_keywords):
        return "ml"
    if any(k in jd for k in analyst_keywords):
        return "analyst"
    if any(k in jd for k in engineer_keywords) and "business" not in jd:
        return "engineer"
    # Default fallback
    return "engineer"

def main():
    # Remove resume argument from parser, since we select it automatically
    parser = argparse.ArgumentParser(
        description="Send personalized cold emails for job referral requests."
    )
    parser.add_argument("input_file", help="Path to Excel or CSV file with columns: first_name, last_name, company, job_description")
    parser.add_argument("--sender", required=True, help="Your sender email address")
    parser.add_argument("--smtp_server", default="smtp.gmail.com", help="SMTP server address (default: smtp.gmail.com)")
    parser.add_argument("--smtp_port", type=int, default=587, help="SMTP server port (default: 587)")
    parser.add_argument("--subject", default="Interested in working at {company} as a {job_description}", help="Subject line for the email")
    args = parser.parse_args()

    # For security, prompt for the sender's email password (or app password)
    password = getpass.getpass(prompt="Enter your email password: ")

    # Read the input file.
    # Supports Excel (.xlsx/.xls) or CSV.
    file_ext = os.path.splitext(args.input_file)[1].lower()
    if file_ext in [".xlsx", ".xls"]:
        df = pd.read_excel(args.input_file)
    elif file_ext == ".csv":
        df = pd.read_csv(args.input_file)
    else:
        print("Unsupported file format. Please provide an Excel (.xlsx/.xls) or CSV file.")
        return

    # Check for the required columns.
    required_columns = ["first_name", "last_name", "company", "job_description"]
    for col in required_columns:
        if col not in df.columns:
            print(f"Missing required column: {col}")
            return

    # Connect to the SMTP server.
    try:
        server = smtplib.SMTP(args.smtp_server, args.smtp_port)
        server.starttls()
        server.login(args.sender, password)
    except Exception as e:
        print(f"Failed to connect or login to the SMTP server: {e}")
        return

    # Process each entry in the DataFrame.
    for idx, row in df.iterrows():
        first_name = str(row["first_name"]).strip()
        last_name = str(row["last_name"]).strip()
        company = str(row["company"]).strip()
        job_description = str(row["job_description"]).strip()

        # Classify job description
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

        # Naively convert the company name into an email domain.
        company_domain = company.lower().replace(" ", "") + ".com"

        # Generate possible recipient email addresses using our common patterns.
        possible_emails = generate_email_addresses(first_name, last_name, company_domain)

        for recipient in possible_emails:
            # Personalize the email body.
            body = email_template.format(
                first_name=first_name,
                company=company,
                job_description=job_description
            )
            # Personalize the subject line.
            subject = args.subject.format(
                company=company,
                job_description=job_description
            )
            # Create the full email message with attachment.
            msg = create_email_message(args.sender, recipient, subject, body, resume_path)
            try:
                server.send_message(msg)
                print(f"Email sent to {recipient}")
            except Exception as e:
                print(f"Failed to send email to {recipient}: {e}")

    server.quit()
    print("All messages processed.")

if __name__ == "__main__":
    main()