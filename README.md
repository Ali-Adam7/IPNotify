# IP Monitor and Email Notifier

This Python script monitors the external IP address of a network and sends an email notification whenever it changes.

## Features

- Retrieves current external IP using `ident.me`.
- Supports email notifications via Gmail, Outlook, and Yahoo.
- Uses SMTP for email sending and threading for IP monitoring.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Ali-Adam7/IPNotify.git

2. Install Dependencies:
   ```bash
   pip install smtplib

3. Run the script:
   ```bash
    python main.py

## Configuration
Before running the script, configure your email credentials in the getInputs() function within main.py.

## Usage
Run the script and follow the prompts to enter your email and password.
The script will monitor your IP address and notify you via email if the external IP changes.
