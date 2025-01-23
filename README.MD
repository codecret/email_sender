# Email Sender Script

This script automates sending personalized emails to multiple recipients with an optional attachment (e.g., a CV). It uses an SMTP server with SSL for secure email sending and loads environment variables for email credentials.

## Features

- Load email credentials and settings from environment variables.
- Send personalized emails with HTML content and optional attachments (e.g., CV).
- Handle sending to multiple recipients from a file.
- Logs email sending status and errors.
- Delay between emails to avoid rate limiting.

## Prerequisites

Before using the script, ensure you have the following:

- A valid SMTP server (e.g., Gmail, Outlook).
- A `.env` file containing your email credentials.
- Python 3.x installed on your system.

## Installation

1. Clone the repository or download the script file.

   ```bash
   git clone https://github.com/your-repository/email-sender.git
   cd email-sender
   ```

2. Install the required Python dependencies:

   ```bash
   python -m venv myenv
   source myenv/bin/activate # macOS/Linux
   myenv\Scripts\activate # Windows
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory and set the following environment variables:

   ```env
   EMAIL=your_email@example.com
   SMTP=smtp.example.com
   PORT=465
   PASSWORD=your_email_password
   ```

4. Ensure the following files exist and are properly configured:
   - `cvtr.pdf` – the CV or other file to attach to emails.
   - `hr.txt` – a text file containing a list of recipient email addresses (one per line).
   - `template1.html` – an HTML email template for the message body.

## How It Works

1. **Loading Environment Variables**: The script loads SMTP server credentials, email address, and password from the `.env` file.
2. **Reading Recipients**: The script loads the recipient emails from `hr.txt`.
3. **HTML Content**: It loads the HTML email template from `template1.html`.
4. **Sending Emails**: The script sends the email to each recipient in the list, attaching `cvtr.pdf` (if provided).
5. **Logging**: Logs success and failure messages in `email_sender.log`.

## Example Usage

To send emails, simply run the script:

    ```bash
    python email_sender.py
    ```

This will start sending emails one by one with a 5-second delay between each to avoid rate limiting.

## Environment File Example

Create a `.env` file in the root directory with the following content:

    ```env
    EMAIL=your_email@example.com
    SMTP=smtp.example.com
    PORT=465
    PASSWORD=your_email_password
    ```

## Configuration Files

- **hr.txt**: This file should contain the list of recipient email addresses, one per line:

  ```txt
  recipient1@example.com
  recipient2@example.com
  ```

- **template1.html**: The HTML template used for the email content. It can contain placeholders like the recipient’s name.

- **cvtr.pdf**: The PDF file (or other file type) to be attached to each email.

## Logging

The script logs all actions to `email_sender.log`, including errors and successful email sends.

## Troubleshooting

- Ensure that the `.env` file is correctly configured with your email credentials.
- If emails are not being sent, check the log file `email_sender.log` for detailed error messages.
- If using Gmail, you may need to enable "Less Secure Apps" or generate an App Password if you have 2FA enabled.

## License

This project is licensed under the MIT License.
