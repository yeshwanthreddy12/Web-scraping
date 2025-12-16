# How to Get Gmail App Password

**IMPORTANT**: Gmail requires an "App Password" for IMAP/SMTP access. You cannot use your regular Gmail password.

## Step-by-Step Instructions

1. **Go to your Google Account**
   - Visit: https://myaccount.google.com
   - Sign in with: yeshwanthreddy.bunny@gmail.com

2. **Enable 2-Step Verification** (if not already enabled)
   - Click on **Security** in the left sidebar
   - Under "How you sign in to Google", click **2-Step Verification**
   - Follow the prompts to enable it (if not already enabled)

3. **Create App Password**
   - Go back to **Security** page
   - Scroll down to "How you sign in to Google"
   - Click on **App passwords** (you may need to search for it)
   - If you don't see "App passwords", make sure 2-Step Verification is enabled first

4. **Generate the Password**
   - Select app: Choose **Mail**
   - Select device: Choose **Other (Custom name)**
   - Type: "Email Summary System"
   - Click **Generate**

5. **Copy the 16-Character Password**
   - Google will show you a 16-character password (looks like: `abcd efgh ijkl mnop`)
   - **Copy this password** (remove spaces if any)

6. **Add to .env file**
   - Open the `.env` file in this project
   - Replace `YOUR_APP_PASSWORD_HERE` with the 16-character password
   - Save the file

## Quick Link

Direct link to App Passwords: https://myaccount.google.com/apppasswords

## Example .env file

After setup, your `.env` should look like:
```
EMAIL_ADDRESS=yeshwanthreddy.bunny@gmail.com
EMAIL_PASSWORD=abcdefghijklmnop
IMAP_SERVER=imap.gmail.com
SMTP_SERVER=smtp.gmail.com
OLLAMA_MODEL=llama3
SUMMARY_RECIPIENT=yeshwanthreddy.bunny@gmail.com
```

## Troubleshooting

- **"App passwords" option not showing**: Make sure 2-Step Verification is enabled
- **"Invalid credentials"**: Make sure you're using the App Password, not your regular password
- **Password has spaces**: Remove all spaces when copying to .env file

