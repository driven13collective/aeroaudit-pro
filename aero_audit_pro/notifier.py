import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_audit_log(tester_name, detections_count):
    # Your verified credentials
    sender_email = "mb350ellc@gmail.com"
    # Note: Spaces are removed from the password for the script
    app_password = "qrhrpxnpletgwpzk"
    receiver_email = "mb350ellc@gmail.com"

    subject = f"🏎️ AeroAudit-Pro: Beta Detection Alert ({tester_name})"
    
    body = f"""
    AeroAudit-Pro Cloud Briefing
    -----------------------------
    A tester has just completed an F1 sponsorship audit.
    
    Tester Name: {tester_name}
    Logos Identified: {detections_count}
    Server: Lightning.ai Cloud
    
    This log confirms your tool is running 24/7 while you are away.
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Port 465 is the modern secure standard for Gmail SSL
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.send_message(msg)
            print("Business Log: Email sent to mb350ellc@gmail.com")
    except Exception as e:
        print(f"Logging Error: {e}")
