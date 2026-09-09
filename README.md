# JAMB-Style Mathematics CBT Web App

Converted from the uploaded Tkinter CBT program.

## Run locally

1. Install Python 3.10+.
2. Open Command Prompt/Terminal in this folder.
3. Install Flask:

   pip install -r requirements.txt

4. Start the server:

   python app.py

5. Open:

   http://127.0.0.1:5000

## Important

This is a practice/CBT-style system, not an official JAMB system.

The app keeps the original 30 Mathematics questions from the uploaded Python program, randomizes question and option order for each new exam, saves answers on navigation, has a 30-minute timer, automatically submits after expiry, and calculates the score.
