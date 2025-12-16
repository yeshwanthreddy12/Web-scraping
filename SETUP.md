# Setup Guide for Daily Email Summary System

## Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed and running (https://ollama.ai)
3. **Gmail account** with 2-Step Verification enabled

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Ollama

1. **Install Ollama** (if not already installed):
   - Visit https://ollama.ai and download for your OS
   - Or use: `curl -fsSL https://ollama.ai/install.sh | sh`

2. **Start Ollama** (if not running):
   ```bash
   ollama serve
   ```

3. **Download a model** (choose one):
   ```bash
   ollama pull llama3        # Recommended: Fast and efficient
   # or
   ollama pull mistral       # Alternative option
   # or
   ollama pull gemma         # Google's model
   ```

4. **Test Ollama**:
   ```bash
   ollama run llama3 "Hello, how are you?"
   ```

## Step 3: Configure Gmail App Password

Since Gmail requires app-specific passwords for IMAP/SMTP access:

1. Go to your **Google Account** (https://myaccount.google.com)
2. Navigate to **Security** → **2-Step Verification** (enable if not already)
3. Scroll down to **App passwords**
4. Click **Select app** → Choose "Mail"
5. Click **Select device** → Choose "Other" and type "Email Summary"
6. Click **Generate**
7. **Copy the 16-character password** (you'll need this)

## Step 4: Configure Email Credentials

### Option A: Using Environment Variables (Recommended)

1. Create a `.env` file in the project directory:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your credentials:
   ```
   EMAIL_ADDRESS=your_email@gmail.com
   EMAIL_PASSWORD=your_16_char_app_password
   IMAP_SERVER=imap.gmail.com
   SMTP_SERVER=smtp.gmail.com
   OLLAMA_MODEL=llama3
   SUMMARY_RECIPIENT=your_email@gmail.com
   ```

### Option B: Direct Configuration in Notebook

Edit the configuration cell in `main.ipynb` and replace the placeholder values with your actual credentials.

## Step 5: Test the Setup

1. Open `main.ipynb` in Jupyter Notebook
2. Run all cells up to the test section
3. Uncomment and run the test cells to verify:
   - Email connection works
   - Ollama is accessible

## Step 6: Run the Workflow

1. In the notebook, go to the "Main Workflow" section
2. Uncomment the line: `daily_email_summary_workflow()`
3. Run the cell

The system will:
- Fetch all emails from today
- Generate a summary using Ollama
- Send the summary as a new email

## Troubleshooting

### Email Connection Issues

- **"Authentication failed"**: Make sure you're using an App Password, not your regular Gmail password
- **"IMAP not enabled"**: Go to Gmail Settings → Forwarding and POP/IMAP → Enable IMAP
- **"Less secure app access"**: Use App Passwords instead (recommended)

### Ollama Issues

- **"Connection refused"**: Make sure Ollama is running (`ollama serve`)
- **"Model not found"**: Pull the model first (`ollama pull llama3`)
- **"Timeout"**: The model might be too large or slow. Try a smaller model like `gemma:2b`

### Other Email Providers

For non-Gmail providers, update the IMAP/SMTP settings:

- **Outlook/Hotmail**:
  - IMAP: `outlook.office365.com:993`
  - SMTP: `smtp.office365.com:587`

- **Yahoo**:
  - IMAP: `imap.mail.yahoo.com:993`
  - SMTP: `smtp.mail.yahoo.com:587`

## Automation (Optional)

To run this daily automatically, you can:

1. **Use cron (Linux/Mac)**:
   ```bash
   crontab -e
   # Add: 0 20 * * * cd /path/to/project && jupyter nbconvert --to notebook --execute main.ipynb
   ```

2. **Use Task Scheduler (Windows)**:
   - Create a batch file that runs the notebook
   - Schedule it in Task Scheduler

3. **Use Python script**:
   - Convert the notebook functions to a `.py` file
   - Run it with a scheduler

## Security Notes

- **Never commit `.env` file** to git (it's already in `.gitignore`)
- **Keep your App Password secure**
- **Consider using environment variables** instead of hardcoding credentials

