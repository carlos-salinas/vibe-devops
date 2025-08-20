#!/usr/bin/env python3
from flask import Flask
import os

app = Flask(__name__)

def generate_html():
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Happy Vibe DevOps</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 50px;
            margin: 0;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .container {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 20px;
            padding: 40px;
            backdrop-filter: blur(10px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        h1 {
            font-size: 3.5rem;
            margin: 0;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        }
        
        .strikethrough {
            text-decoration: line-through;
            color: #ff6b6b;
        }
        
        .emoji {
            animation: blink 1s infinite;
            font-size: 4rem;
            display: inline-block;
        }
        
        @keyframes blink {
            0%, 50% { opacity: 1; }
            51%, 100% { opacity: 0; }
        }
        
        .subtitle {
            font-size: 1.2rem;
            margin-top: 20px;
            opacity: 0.8;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Happy Vibe <span class="strikethrough">Code</span> DevOps! <span class="emoji">😃</span></h1>
        <p class="subtitle">Powered by Flask, Docker, and Tekton</p>
    </div>
</body>
</html>"""
    
    with open('/tmp/index.html', 'w') as f:
        f.write(html_content)
    
    return html_content

@app.route('/')
def home():
    return generate_html()

if __name__ == '__main__':
    os.makedirs('/tmp', exist_ok=True)
    generate_html()
    print("Static HTML generated at /tmp/index.html")