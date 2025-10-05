import time
from gmail_client import get_gmail_service, get_job_emails, mark_as_read
from summarizer import summarize_email
from whatsapp_client import send_whatsapp_message

def is_job_related(subject, body):
    """Check if the email is job-related based on keywords."""
    job_keywords = [
        'job', 'career', 'position', 'vacancy', 'hiring', 'opportunity',
        'recruitment', 'opening', 'employment', 'role', 'apply', 'interview',
        'job posting', 'job description', 'work'
    ]
    
    text = (subject + ' ' + body).lower()
    return any(keyword in text for keyword in job_keywords)

def main():
    """The main function that runs the agent's workflow."""
    print("🤖 AI Job Alert Agent is now active...")
    gmail_service = get_gmail_service()
    
    while True:
        try:
            print("\nChecking for new job emails...")
            emails = get_job_emails(gmail_service)
            
            if emails:
                for email in emails:
                    print(f"Processing new email with subject: '{email['subject']}'")
                    
                    # 1. Summarize the email
                    summary = summarize_email(email['subject'], email['body'])
                    
                    # 2. Format the message for WhatsApp
                    whatsapp_msg = f"🔔 *New Job Alert!* 🔔\n\n*Subject:* {email['subject']}\n\n*Summary:* \n{summary}"
                    
                    # 3. Send the summary via WhatsApp
                    send_whatsapp_message(whatsapp_msg)
                    
                    # 4. Mark the email as read
                    mark_as_read(gmail_service, email['id'])
            
            # Wait for 24 hours before checking again
            print("Sleeping for 24 hours...")
            time.sleep(86400)

        except Exception as e:
            print(f"An error occurred in the main loop: {e}")
            # Wait a bit longer before retrying in case of a persistent error
            time.sleep(60)

if __name__ == '__main__':
    main()