import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import csv
import random
from openai import OpenAI  # Requires: pip install openai

def generate_email_body(topic, recipient_name, api_key):
    """
    Uses xAI Grok API to generate a personalized, human-like email body based on a topic.
    
    Args:
    topic (str): The main topic for the email.
    recipient_name (str): Name of the recipient for personalization.
    api_key (str): xAI API key.
    
    Returns:
    str: Generated email body.
    """
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )
    
    system_prompt = "You are a helpful, professional email assistant. Write concise, natural, and engaging emails that sound human-written. Include a warm greeting, relevant content based on the topic, a call to action if appropriate, and a friendly closing. Use casual yet polite language."
    
    user_prompt = f"Topic: {topic}. Personalize for {recipient_name}. Structure: Greeting with name, body discussing the topic, closing."
    
    try:
        response = client.chat.completions.create(
            model="grok-4-0709",  # Use latest Grok model; check docs for updates
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=300,  # Adjust for length
            temperature=0.7  # For natural variation
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"AI generation failed: {e}")
        return f"Hi {recipient_name},\n\nRegarding {topic}, let's discuss soon.\n\nBest,\nYour Name"

def send_personalized_emails(sender_email, sender_password, xai_api_key, csv_file_path, subject_template, topic):
    """
    Sends AI-generated personalized emails to recipients from a CSV file.
    CSV should have columns: 'email' and 'name'.
    AI generates unique body for each based on topic.
    
    Args:
    sender_email (str): Your email address.
    sender_password (str): Your email password or app-specific password.
    xai_api_key (str): xAI API key (get from https://console.x.ai/).
    csv_file_path (str): Path to CSV file with 'email' and 'name' columns.
    subject_template (str): Subject with optional {name} placeholder.
    topic (str): The email topic for AI to base the body on.
    """
    # Human-like variations for subject/greeting if needed
    greetings = ["Hi", "Hello", "Hey"]  # But AI handles most
    closings = ["Best regards,", "Cheers,", "Warmly,"]
    
    try:
        # Gmail SMTP setup
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                recipient_email = row['email']
                recipient_name = row['name']
                
                # Personalize subject
                subject = subject_template.format(name=recipient_name)
                
                # Generate AI body for this recipient
                body = generate_email_body(topic, recipient_name, xai_api_key)
                
                # Add random closing variation if not in AI output
                closing = random.choice(closings)
                if not body.endswith(('regards,', 'cheers,', 'warmly,', 'best,')):
                    body += f"\n\n{closing}\nYour Name"
                
                # Set up message
                message = MIMEMultipart()
                message['From'] = sender_email
                message['To'] = recipient_email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                
                # Send
                text = message.as_string()
                server.sendmail(sender_email, recipient_email, text)
                print(f"AI-generated email sent to {recipient_name} ({recipient_email}) on topic: {topic}")
        
        server.quit()
        print("All AI-personalized emails sent successfully!")
        
    except Exception as e:
        print(f"Failed to send emails. Error: {e}")

# Example usage
if __name__ == "__main__":
    # Set environment variables for credentials
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')
    xai_api_key = os.getenv('XAI_API_KEY')  # Get from https://console.x.ai/
    
    if not sender_email or not sender_password or not xai_api_key:
        print("Please set SENDER_EMAIL, SENDER_PASSWORD, and XAI_API_KEY environment variables.")
        print("For xAI API: Sign up at https://x.ai/api/ and generate key at https://console.x.ai/")
    else:
        csv_file = input("Enter path to CSV file (e.g., recipients.csv): ")
        subject_template = input("Enter subject template (use {name} for personalization, e.g., 'Update on {name}\'s Project'): ")
        topic = input("Enter the email topic (e.g., 'Follow-up on our recent meeting'): ")
        
        send_personalized_emails(sender_email, sender_password, xai_api_key, csv_file, subject_template, topic)
