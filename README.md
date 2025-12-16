# Daily Email Summary System

A Jupyter notebook system that reads all your emails from the day, generates an AI-powered summary using Ollama (local LLM), and sends the summary as a new email.

## Features

- 📧 **Email Reading**: Fetches all emails received today via IMAP
- 🤖 **AI Summarization**: Uses Ollama (free, local LLM) to generate intelligent summaries
- 📨 **Auto Email**: Sends the summary as a new email automatically
- 🔒 **Privacy-First**: All processing happens locally with Ollama
- ⚙️ **Configurable**: Easy setup with environment variables

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Ollama**:
   ```bash
   # Install Ollama from https://ollama.ai
   ollama pull llama3
   ```

3. **Configure email credentials** (see `SETUP.md` for detailed instructions)

4. **Launch Jupyter Notebook**:
   ```bash
   jupyter notebook
   ```

5. **Open `main.ipynb`** and run the workflow!

## Detailed Setup

See [SETUP.md](SETUP.md) for complete setup instructions including:
- Gmail App Password configuration
- Ollama installation and model setup
- Environment variable configuration
- Troubleshooting guide

## Dependencies

- **jupyter**: Core Jupyter notebook environment
- **ollama**: Python client for Ollama LLM
- **python-dotenv**: Environment variable management
- **pandas, numpy**: Data manipulation
- **requests, beautifulsoup4**: Web scraping utilities
- Built-in libraries: `imaplib`, `smtplib`, `email`

## How It Works

1. **Fetch Emails**: Connects to your email via IMAP and retrieves all emails from today
2. **Generate Summary**: Sends email content to Ollama (local LLM) for intelligent summarization
3. **Send Summary**: Emails the generated summary back to you

## Privacy & Security

- All AI processing happens **locally** using Ollama
- No data is sent to external AI services
- Email credentials stored securely in `.env` file (not committed to git)
- Uses Gmail App Passwords for secure authentication

## Usage

1. Configure your email credentials in the notebook or `.env` file
2. Run all cells to load functions
3. Execute `daily_email_summary_workflow()` to run the complete process

For automation, see the SETUP.md guide for scheduling options.

