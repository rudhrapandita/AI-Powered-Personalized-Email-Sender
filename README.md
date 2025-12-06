# AI-Powered-Personalized-Email-Sender
A Python script that automates sending personalized, AI-generated emails to a list of recipients. Uses xAI's Grok API to craft natural, human-like email bodies based on a simple topic description. Perfect for newsletters, follow-ups, or outreach campaigns.


Features

Bulk Personalization: Reads recipients from a CSV (email + name).
AI-Generated Content: Grok writes unique, engaging emails per recipient using a topic prompt.
Human-Like Variations: Random greetings/closings for authenticity.
Secure Credentials: Environment variables for email/API keys.
Fallback Mode: Simple templates if AI fails.
Easy Automation: Schedule via cron/Task Scheduler.

Repository Structure
textai-email-sender/
├── README.md                 # This file
├── requirements.txt          # Dependencies
├── .env.example              # Environment variable template
├── .gitignore                # Standard ignores
├── src/
│   └── email_sender.py       # Main script
└── example/
    ├── recipients.csv        # Sample recipient list
    └── sample_output.txt     # Example generated email
Quick Start
1. Clone the Repo
Bashgit clone https://github.com/yourusername/ai-email-sender.git
cd ai-email-sender
2. Install Dependencies
Bashpip install -r requirements.txt
3. Set Up Environment
Copy the example env file:
Bashcp .env.example .env
Edit .env with your credentials:
textSENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
XAI_API_KEY=your_xai_api_key

Gmail Setup: Enable 2FA, generate App Password.
xAI API: Sign up at console.x.ai, add credits, generate key.

4. Prepare Recipients
Edit example/recipients.csv (or your own):
csvemail,name
alice@example.com,Alice
bob@work.com,Bob
charlie@home.com,Charlie
5. Run the Script
Bashpython src/email_sender.py

Prompts for: CSV path, subject template (e.g., "Update for {name}"), topic (e.g., "Exciting AI project news").
Sends emails via Gmail SMTP.

Example Output
A sample AI-generated email (from example/sample_output.txt):
textHi Alice,

I hope this email finds you well. Regarding exciting AI project news, our latest Grok integration is revolutionizing how teams collaborate—imagine drafting reports in seconds! I'd love your thoughts on piloting it next quarter.

Let's hop on a quick call?

Best regards,
Your Name
Customization

AI Prompts: Edit system_prompt in src/email_sender.py for tone (e.g., "Make it humorous").
Other Providers: Swap SMTP settings (e.g., Outlook: smtp-mail.outlook.com).
Advanced: Add attachments or HTML via MIMEText(..., 'html').
Scheduling: Use cron: 0 9 * * 1 python src/email_sender.py (Mondays at 9 AM).

Limitations & Costs

Gmail Limits: ~500 emails/day; use for testing.
xAI Costs: ~$0.01–0.10 per email (token-based); monitor at console.x.ai.
Rate Limits: Add import time; time.sleep(1) between sends if needed.
Privacy: Recipient data sent to xAI API—use ethically.
