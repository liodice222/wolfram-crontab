# Daily Questions System

A Python-based system that sends daily practice questions via email using a cron job. The system tracks sent questions in a database and automatically moves them to a separate "sent" database once they've been emailed.

## Features

- **Database Tracking**: Automatically tracks which questions have been sent
- **Dual Database System**: 
  - `unsent_questions.db`: Contains questions that haven't been sent yet
  - `sent_questions.db`: Contains questions that have been sent
- **Automatic Question Cycling**: When all questions are sent, the system automatically resets
- **Email Integration**: Sends formatted HTML emails with questions
- **Cron Job Support**: Easy setup for automated daily execution
- **Database Management**: Utility scripts for managing and viewing question status

## Files

- `script.py`: Main script that sends daily questions
- `db.py`: Database management system
- `questions.py`: Question bank with chemistry, biochemistry, and physics questions
- `manage_db.py`: Database management utility
- `setup_cron.py`: Cron job setup utility
- `README.md`: This documentation

## Setup Instructions

### 1. Prerequisites

Make sure you have Python 3 installed and the required packages:

```bash
pip install requests
```

### 2. Email Configuration

The system uses Gmail SMTP. You'll need to:

1. Enable 2-factor authentication on your Gmail account
2. Generate an App Password
3. Store the password in macOS Keychain:

```bash
security add-generic-password -a "iodice.pt@gmail.com" -s "iodice.pt@gmail.com" -w
```

When prompted, enter your Gmail App Password.

### 3. Database Setup

The database will be automatically created when you first run the script. To initialize it with your questions:

```bash
python3 script.py
```

This will:
- Create the database files
- Populate them with questions from `questions.py`
- Send the first question as a test

### 4. Setting Up the Cron Job

Use the setup script to easily configure the cron job:

```bash
python3 setup_cron.py
```

This will guide you through:
- Testing the script
- Adding a daily cron job (default: 9:00 AM)
- Setting a custom time
- Managing existing cron jobs

### 5. Manual Cron Setup (Alternative)

If you prefer to set up the cron job manually:

```bash
# Edit your crontab
crontab -e

# Add this line to run daily at 9:00 AM
0 9 * * * /usr/bin/python3 /path/to/your/script.py
```

## Usage

### Running the Script Manually

```bash
python3 script.py
```

This will:
1. Initialize the database if needed
2. Select a random unsent question
3. Send it via email
4. Mark the question as sent and move it to the sent database
5. Display database statistics

### Database Management

Use the management utility to view and manage your questions:

```bash
python3 manage_db.py
```

Options include:
- View database statistics
- View recently sent questions
- View unsent questions
- Reset all questions to unsent status
- Export sent questions to JSON

### Adding New Questions

To add new questions, edit the `questions.py` file. The format is:

```python
questions = {
    "subject_name": [
        {
            "question": "Your question text?",
            "options": ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"],
            "answer": "B. Option 2",
            "explanation": "Explanation of the answer",
            "resource": "Reference book or source"
        }
    ]
}
```

After adding questions, run the script once to populate the database:

```bash
python3 script.py
```

## Database Schema

### Unsent Questions Database (`unsent_questions.db`)

```sql
CREATE TABLE practice_problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT NOT NULL,
    question TEXT NOT NULL,
    options TEXT NOT NULL,
    answer TEXT NOT NULL,
    explanation TEXT NOT NULL,
    resource TEXT NOT NULL,
    sent BOOLEAN DEFAULT FALSE,
    created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Sent Questions Database (`sent_questions.db`)

```sql
CREATE TABLE sent_problems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_id INTEGER,
    subject TEXT NOT NULL,
    question TEXT NOT NULL,
    options TEXT NOT NULL,
    answer TEXT NOT NULL,
    explanation TEXT NOT NULL,
    resource TEXT NOT NULL,
    sent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## How It Works

1. **Question Selection**: The system randomly selects an unsent question from the database
2. **Email Sending**: Formats the question as HTML and sends it via Gmail SMTP
3. **Database Update**: Marks the question as sent and moves it to the sent database
4. **Auto-Reset**: When no unsent questions remain, the system automatically resets all questions

## Troubleshooting

### Email Issues

- Check that your Gmail App Password is correctly stored in Keychain
- Ensure 2-factor authentication is enabled on your Gmail account
- Verify the email addresses in `script.py` are correct

### Database Issues

- If the database gets corrupted, delete the `.db` files and run the script again
- Use `manage_db.py` to reset all questions if needed

### Cron Job Issues

- Check that the script path in the cron job is absolute
- Ensure the script has execute permissions: `chmod +x script.py`
- Check cron logs: `grep CRON /var/log/syslog`

## Security Notes

- Email passwords are stored securely in macOS Keychain
- Database files contain question data but no sensitive information
- The script runs with your user permissions

## Customization

You can customize:
- Email template in the `send_html_email()` function
- Question format in the `get_practice_problem()` function
- Database file locations in the `QuestionDatabase` class
- Email timing by modifying the cron job

## Support

If you encounter issues:
1. Check the console output for error messages
2. Verify all prerequisites are installed
3. Test the script manually before setting up the cron job
4. Use the management utilities to diagnose database issues
