#!/usr/bin/env python3
"""
Daily Email Summary Script
Reads emails from today, generates summary using Ollama, and sends it as email.
"""

import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import ollama
import os
from dotenv import load_dotenv
import sys

# Load environment variables
load_dotenv()

# Configuration
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'your_email@gmail.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your_app_password')
IMAP_SERVER = os.getenv('IMAP_SERVER', 'imap.gmail.com')
IMAP_PORT = 993
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = 587
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3')
SUMMARY_RECIPIENT = os.getenv('SUMMARY_RECIPIENT', EMAIL_ADDRESS)


def decode_mime_words(s):
    """Decode MIME encoded words in email headers"""
    return email.header.decode_header(s)


def get_email_body(msg):
    """Extract the body text from an email message"""
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    payload = part.get_payload(decode=True)
                    if payload:
                        charset = part.get_content_charset() or 'utf-8'
                        body += payload.decode(charset, errors='ignore')
                except Exception as e:
                    print(f"Error decoding part: {e}")
    else:
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                charset = msg.get_content_charset() or 'utf-8'
                body = payload.decode(charset, errors='ignore')
        except Exception as e:
            print(f"Error decoding body: {e}")
    
    return body.strip()


def get_today_emails(email_address, password, imap_server, imap_port):
    """Fetch all emails received today"""
    try:
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(email_address, password)
        mail.select('inbox')
        
        today = datetime.now().date()
        date_str = today.strftime("%d-%b-%Y")
        
        status, messages = mail.search(None, f'(SINCE {date_str})')
        email_ids = messages[0].split()
        
        emails = []
        
        for email_id in email_ids:
            try:
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                email_body = msg_data[0][1]
                msg = email.message_from_bytes(email_body)
                
                subject = decode_mime_words(msg['Subject'])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode('utf-8', errors='ignore')
                
                from_addr = decode_mime_words(msg['From'])[0][0]
                if isinstance(from_addr, bytes):
                    from_addr = from_addr.decode('utf-8', errors='ignore')
                
                date = msg['Date']
                body = get_email_body(msg)
                
                emails.append({
                    'subject': subject,
                    'from': from_addr,
                    'date': date,
                    'body': body
                })
            except Exception as e:
                print(f"Error processing email {email_id}: {e}")
                continue
        
        mail.close()
        mail.logout()
        
        return emails
    
    except Exception as e:
        print(f"Error connecting to email server: {e}")
        return []


def summarize_emails_with_ollama(emails, model='llama3'):
    """Generate a summary of all emails using Ollama"""
    if not emails:
        return "No emails received today."
    
    email_text = ""
    for i, email_data in enumerate(emails, 1):
        email_text += f"\n--- Email {i} ---\n"
        email_text += f"From: {email_data['from']}\n"
        email_text += f"Subject: {email_data['subject']}\n"
        email_text += f"Date: {email_data['date']}\n"
        body = email_data['body'][:2000] if len(email_data['body']) > 2000 else email_data['body']
        email_text += f"Body: {body}\n"
    
    prompt = f"""Please provide a concise daily email summary. Organize it by:
1. Total number of emails
2. Key topics/themes
3. Important emails (with sender and brief description)
4. Action items if any

Here are today's emails:
{email_text}

Please provide a well-formatted summary:"""

    try:
        response = ollama.chat(model=model, messages=[
            {
                'role': 'system',
                'content': 'You are a helpful assistant that summarizes emails in a clear and organized manner.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ])
        
        summary = response['message']['content']
        return summary
    
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        print("Make sure Ollama is running and the model is available.")
        return f"Error generating summary: {e}"


def send_summary_email(sender_email, sender_password, recipient_email, summary, smtp_server, smtp_port):
    """Send the email summary"""
    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Daily Email Summary - {datetime.now().strftime('%Y-%m-%d')}"
        
        body = f"""
Daily Email Summary
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{summary}

---
This is an automated summary generated using Ollama.
"""
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        
        print(f"Summary email sent successfully to {recipient_email}")
        return True
    
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def main():
    """Main workflow"""
    print("=" * 60)
    print("Starting Daily Email Summary Workflow")
    print("=" * 60)
    
    # Validate configuration
    if EMAIL_ADDRESS == 'your_email@gmail.com' or EMAIL_PASSWORD == 'your_app_password':
        print("ERROR: Please configure your email credentials in .env file")
        print("See SETUP.md for instructions")
        sys.exit(1)
    
    # Step 1: Fetch today's emails
    print("\n[1/3] Fetching today's emails...")
    emails = get_today_emails(EMAIL_ADDRESS, EMAIL_PASSWORD, IMAP_SERVER, IMAP_PORT)
    print(f"Found {len(emails)} email(s) today")
    
    if not emails:
        print("No emails found for today. Exiting.")
        return
    
    # Step 2: Generate summary using Ollama
    print(f"\n[2/3] Generating summary using Ollama ({OLLAMA_MODEL})...")
    summary = summarize_emails_with_ollama(emails, OLLAMA_MODEL)
    print("Summary generated successfully!")
    print("\n" + "=" * 60)
    print("SUMMARY PREVIEW:")
    print("=" * 60)
    print(summary)
    print("=" * 60)
    
    # Step 3: Send summary email
    print(f"\n[3/3] Sending summary email to {SUMMARY_RECIPIENT}...")
    success = send_summary_email(
        EMAIL_ADDRESS, 
        EMAIL_PASSWORD, 
        SUMMARY_RECIPIENT, 
        summary, 
        SMTP_SERVER, 
        SMTP_PORT
    )
    
    if success:
        print("\n✅ Workflow completed successfully!")
    else:
        print("\n❌ Workflow completed with errors. Check the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()

