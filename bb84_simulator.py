from flask import Flask, render_template_string, request, jsonify, session
import secrets
import hashlib
from datetime import datetime
import socket

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure random secret key

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BB84 Quantum Key Distribution Simulator</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --dark-bg: #0a0a1a;
            --glass-bg: rgba(15, 15, 35, 0.6);
            --glass-bg-hover: rgba(20, 20, 50, 0.8);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glass-border-strong: rgba(255, 255, 255, 0.2);
            --text-color: #e0e8ff;
            --text-secondary: #8892b0;
            --accent-cyan: #00f0ff;
            --accent-green: #39ff14;
            --accent-red: #ff2a6d;
            --accent-yellow: #ffb800;
            --accent-purple: #b44dff;
            --glow-cyan: 0 0 20px rgba(0, 240, 255, 0.4);
            --glow-green: 0 0 20px rgba(57, 255, 20, 0.4);
            --glow-red: 0 0 20px rgba(255, 42, 109, 0.4);
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', system-ui, sans-serif;
            background: radial-gradient(ellipse at top, #1a1a3e 0%, var(--dark-bg) 70%);
            color: var(--text-color);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
            overflow-x: hidden;
        }

        /* Animated background particles */
        body::before {
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-image:
                radial-gradient(2px 2px at 20px 30px, rgba(0, 240, 255, 0.3), rgba(0,0,0,0)),
                radial-gradient(2px 2px at 40px 70px, rgba(57, 255, 20, 0.3), rgba(0,0,0,0)),
                radial-gradient(1px 1px at 90px 40px, rgba(255, 255, 255, 0.3), rgba(0,0,0,0)),
                radial-gradient(1px 1px at 130px 80px, rgba(180, 77, 255, 0.3), rgba(0,0,0,0)),
                radial-gradient(2px 2px at 160px 120px, rgba(0, 240, 255, 0.2), rgba(0,0,0,0));
            background-size: 200px 200px;
            animation: particleMove 20s linear infinite;
            pointer-events: none;
            z-index: 0;
        }

        @keyframes particleMove {
            0% { background-position: 0 0; }
            100% { background-position: 200px 200px; }
        }

        .container {
            max-width: 1440px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }

        header {
            text-align: center;
            margin-bottom: 40px;
        }

        header h1 {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
            text-shadow: none;
            letter-spacing: -1px;
        }

        header .subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
            font-weight: 300;
            max-width: 700px;
            margin: 0 auto;
        }

        .nav {
            display: flex;
            justify-content: center;
            gap: 16px;
            margin: 30px 0;
            flex-wrap: wrap;
        }

        .nav-button {
            padding: 12px 30px;
            background: var(--glass-bg);
            border: 1px solid var(--glass-border-strong);
            border-radius: 50px;
            color: var(--text-color);
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            backdrop-filter: blur(10px);
            letter-spacing: 0.5px;
            font-size: 0.95rem;
        }

        .nav-button:hover {
            background: var(--glass-bg-hover);
            border-color: var(--accent-cyan);
            box-shadow: var(--glow-cyan);
            transform: translateY(-2px);
        }

        .nav-button.active {
            background: linear-gradient(135deg, rgba(0, 240, 255, 0.2), rgba(180, 77, 255, 0.2));
            border-color: var(--accent-cyan);
            box-shadow: var(--glow-cyan);
            color: var(--accent-cyan);
        }

        .main-grid {
            display: grid;
            grid-template-columns: 1fr 2fr 1fr;
            gap: 24px;
        }

        @media (max-width: 1200px) {
            .main-grid {
                grid-template-columns: 1fr;
            }
        }

        .grid-column {
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 28px;
            border: 1px solid var(--glass-border);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            transition: var(--transition);
        }

        .grid-column:hover {
            border-color: var(--glass-border-strong);
            box-shadow: 0 8px 40px rgba(0, 0, 0, 0.6);
        }

        .grid-column h2 {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 24px;
            padding-bottom: 12px;
            border-bottom: 2px solid var(--glass-border);
            color: var(--text-color);
            letter-spacing: -0.5px;
        }

        .control-group {
            margin-bottom: 24px;
        }

        .control-group h3 {
            color: var(--text-secondary);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 12px;
            font-weight: 600;
        }

        button {
            width: 100%;
            padding: 14px 20px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            border: 1px solid var(--accent-cyan);
            border-radius: 12px;
            background: rgba(0, 240, 255, 0.1);
            color: var(--accent-cyan);
            transition: var(--transition);
            text-transform: uppercase;
            letter-spacing: 1px;
            backdrop-filter: blur(10px);
            margin-top: 8px;
        }

        button:hover:not(:disabled) {
            background: rgba(0, 240, 255, 0.2);
            box-shadow: var(--glow-cyan);
            transform: translateY(-2px);
        }

        button:disabled {
            opacity: 0.4;
            cursor: not-allowed;
            border-color: var(--glass-border);
            color: var(--text-secondary);
        }

        .checkbox-container {
            display: flex;
            align-items: center;
            padding: 12px;
            background: rgba(255, 42, 109, 0.05);
            border: 1px solid rgba(255, 42, 109, 0.2);
            border-radius: 12px;
            margin-bottom: 12px;
            transition: var(--transition);
        }

        .checkbox-container:hover {
            background: rgba(255, 42, 109, 0.1);
        }

        .checkbox-container input[type="checkbox"] {
            margin-right: 12px;
            width: 20px;
            height: 20px;
            accent-color: var(--accent-red);
        }

        .checkbox-container label {
            color: var(--accent-red);
            font-weight: 600;
            font-size: 0.9rem;
        }

        .step-status {
            margin-top: 8px;
            padding: 8px 12px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            background: rgba(0, 0, 0, 0.3);
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .status-indicator {
            width: 10px;
            height: 10px;
            border-radius: 50%;
            display: inline-block;
        }

        .status-pending { background: var(--accent-yellow); box-shadow: 0 0 10px var(--accent-yellow); }
        .status-complete { background: var(--accent-green); box-shadow: 0 0 10px var(--accent-green); }
        .status-error { background: var(--accent-red); box-shadow: 0 0 10px var(--accent-red); }

        /* Visualization Column */
        .animation-container {
            position: relative;
            height: 160px;
            margin: 24px 0;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--glass-border);
        }

        .photon-track {
            position: absolute;
            top: 50%;
            left: 80px;
            right: 80px;
            height: 2px;
            background: linear-gradient(90deg,
                transparent,
                rgba(0, 240, 255, 0.3) 20%,
                rgba(0, 240, 255, 0.3) 80%,
                transparent
            );
            transform: translateY(-50%);
        }

        .photon {
            position: absolute;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-cyan);
            box-shadow: 0 0 20px var(--accent-cyan), 0 0 40px var(--accent-cyan);
            animation: photonTravel 2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
        }

        .photon.eve {
            background: var(--accent-red);
            box-shadow: 0 0 20px var(--accent-red), 0 0 40px var(--accent-red);
        }

        @keyframes photonTravel {
            0% { left: 0; opacity: 0; transform: scale(0); }
            20% { opacity: 1; transform: scale(1); }
            80% { opacity: 1; transform: scale(1); }
            100% { left: 100%; opacity: 0; transform: scale(0); }
        }

        .node {
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: var(--glass-bg);
            border: 2px solid var(--glass-border-strong);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.9rem;
            backdrop-filter: blur(10px);
            z-index: 10;
        }

        .node.alice {
            left: 10px;
            border-color: var(--accent-cyan);
            box-shadow: var(--glow-cyan);
            color: var(--accent-cyan);
        }
        .node.bob {
            right: 10px;
            border-color: var(--accent-green);
            box-shadow: var(--glow-green);
            color: var(--accent-green);
        }
        .node.eve {
            left: 50%;
            transform: translate(-50%, -50%);
            border-color: var(--accent-red);
            box-shadow: var(--glow-red);
            color: var(--accent-red);
            display: none;
        }

        .results-grid {
            display: grid;
            grid-template-columns: 140px 1fr;
            gap: 12px;
            align-items: center;
            margin-bottom: 16px;
        }

        .results-grid strong {
            color: var(--text-secondary);
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .bits-bases-display {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }

        .bit, .basis {
            width: 36px;
            height: 36px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 8px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.95rem;
            font-weight: 700;
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: var(--transition);
        }

        .bit {
            background: rgba(0, 0, 0, 0.5);
            color: #fff;
        }

        .basis.Z {
            background: rgba(0, 240, 255, 0.15);
            color: var(--accent-cyan);
            border-color: rgba(0, 240, 255, 0.3);
        }

        .basis.X {
            background: rgba(57, 255, 20, 0.15);
            color: var(--accent-green);
            border-color: rgba(57, 255, 20, 0.3);
        }

        .bit:hover, .basis:hover {
            transform: scale(1.2);
            box-shadow: 0 0 15px currentColor;
        }

        #reconciliation-result {
            padding: 20px;
            border-radius: 12px;
            margin-top: 20px;
            text-align: center;
            font-weight: 700;
            font-size: 1.1rem;
            letter-spacing: 0.5px;
            transition: var(--transition);
        }

        #reconciliation-result.detected {
            background: rgba(255, 42, 109, 0.15);
            border: 1px solid var(--accent-red);
            color: var(--accent-red);
            box-shadow: var(--glow-red);
            animation: alertPulse 2s infinite;
        }

        #reconciliation-result.not-detected {
            background: rgba(57, 255, 20, 0.1);
            border: 1px solid var(--accent-green);
            color: var(--accent-green);
            box-shadow: var(--glow-green);
        }

        @keyframes alertPulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.7; }
        }

        .key-display {
            margin-top: 20px;
            padding: 16px;
            background: rgba(0, 0, 0, 0.5);
            border-radius: 12px;
            border: 1px solid var(--glass-border);
        }

        .key-display .key-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.1rem;
            color: var(--accent-cyan);
            word-break: break-all;
            margin-top: 8px;
        }

        /* Chat Styles */
        .chat-box {
            height: 250px;
            overflow-y: auto;
            background: rgba(0, 0, 0, 0.4);
            border-radius: 12px;
            padding: 16px;
            margin-top: 16px;
            border: 1px solid var(--glass-border);
        }

        .message-input {
            width: 100%;
            padding: 14px;
            background: rgba(0, 0, 0, 0.4);
            border: 1px solid var(--glass-border);
            border-radius: 12px;
            color: var(--text-color);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.95rem;
            margin-bottom: 12px;
            transition: var(--transition);
        }

        .message-input:focus {
            outline: none;
            border-color: var(--accent-cyan);
            box-shadow: var(--glow-cyan);
        }

        .message {
            margin-bottom: 12px;
            padding: 12px;
            border-radius: 10px;
            background: rgba(0, 0, 0, 0.3);
            border-left: 3px solid;
        }

        .message.alice { border-color: var(--accent-cyan); }
        .message.bob { border-color: var(--accent-green); }
        .message.eve { border-color: var(--accent-red); }
        .message.system { border-color: var(--accent-purple); }

        .encrypted-text {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.8rem;
            color: var(--text-secondary);
            margin-top: 4px;
        }

        /* About Page */
        .about-content {
            display: none;
            background: var(--glass-bg);
            backdrop-filter: blur(20px);
            border-radius: 20px;
            padding: 40px;
            margin-top: 20px;
            border: 1px solid var(--glass-border);
        }

        .about-content h2 {
            font-size: 2rem;
            margin-bottom: 24px;
            color: var(--accent-cyan);
        }

        .about-content h3 {
            color: var(--accent-green);
            margin: 24px 0 16px;
            font-size: 1.3rem;
        }

        .protocol-steps {
            display: grid;
            gap: 16px;
            margin: 20px 0;
        }

        .protocol-step {
            padding: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            border-left: 4px solid var(--accent-cyan);
        }

        .security-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            margin: 20px 0;
        }

        @media (max-width: 768px) {
            .security-grid {
                grid-template-columns: 1fr;
            }
            header h1 {
                font-size: 2rem;
            }
        }

        .security-card {
            padding: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            border-top: 3px solid var(--accent-green);
        }

        .basis-cards {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
            margin: 20px 0;
        }

        .basis-card {
            padding: 20px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 12px;
            border: 1px solid var(--glass-border);
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
        }

        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb {
            background: var(--glass-border-strong);
            border-radius: 4px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-cyan);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>BB84 Quantum Key Distribution</h1>
            <p class="subtitle">A quantum-safe protocol simulator demonstrating secure key exchange and eavesdropper detection</p>
            <div class="nav">
                <button id="simulator-btn" class="nav-button active" onclick="showPage('simulator')">⚛️ Simulator</button>
                <button id="about-btn" class="nav-button" onclick="showPage('about')">📚 About BB84</button>
            </div>
        </header>

        <div id="simulator-page">
            <div class="main-grid">
                <!-- Control Panel -->
                <div class="grid-column">
                    <h2>🔬 Protocol Control</h2>
                    <div class="control-group">
                        <h3>Step 1: Alice Prepares</h3>
                        <button id="alice-generate">add some Qubits</button>
                        <div class="step-status" id="alice-status">
                            <span class="status-indicator status-pending"></span>Awaiting generation
                        </div>
                    </div>
                    <div class="control-group">
                        <h3>Step 2: Bob Measures</h3>
                        <div class="checkbox-container">
                            <input type="checkbox" id="eavesdrop-check">
                            <label>⚠️ Enable Eve's Interception</label>
                        </div>
                        <button id="bob-measure" disabled>got some qubits</button>
                        <div class="step-status" id="bob-status">
                            <span class="status-indicator status-pending"></span>Awaiting qubits
                        </div>
                    </div>
                    <div class="control-group">
                        <h3>Step 3: Key Reconciliation</h3>
                        <button id="reconcile" disabled>Compare Bases & Detect Eve</button>
                        <div class="step-status" id="reconcile-status">
                            <span class="status-indicator status-pending"></span>Awaiting measurement
                        </div>
                    </div>
                </div>

                <!-- Visualization Panel -->
                <div class="grid-column">
                    <h2>📡 Quantum Channel Visualization</h2>
                    <div class="animation-container">
                        <div class="photon-track"></div>
                        <div class="node alice">Alice</div>
                        <div class="node bob">Bob</div>
                        <div class="node eve">Eve</div>
                        <div id="photon-stream"></div>
                    </div>

                    <div class="results-grid">
                        <strong>Alice's Bits:</strong>
                        <div id="alice-bits" class="bits-bases-display"></div>
                        <strong>Alice's Bases:</strong>
                        <div id="alice-bases" class="bits-bases-display"></div>
                        <strong>Bob's Bases:</strong>
                        <div id="bob-bases" class="bits-bases-display"></div>
                        <strong>Bob's Results:</strong>
                        <div id="bob-results" class="bits-bases-display"></div>
                    </div>

                    <div id="reconciliation-result">Awaiting key reconciliation...</div>

                    <div class="key-display" id="final-key-section" style="display:none;">
                        <strong>🔑 Final Shared Key (After Privacy Amplification):</strong>
                        <div class="key-value" id="final-key-display"></div>
                    </div>
                </div>

                <!-- Communication Panel -->
                <div class="grid-column">
                    <h2>💬 Secure Communication</h2>
                    <p style="color: var(--text-secondary); margin-bottom: 16px;">Send encrypted messages using the quantum-generated key</p>
                    <input type="text" id="message-input" class="message-input" placeholder="Type your message..." disabled>
                    <button id="encrypt-btn" disabled>🔒 Encrypt & Send</button>
                    <button id="decrypt-btn" disabled style="margin-top: 8px;">🔓 Decrypt Last Message</button>
                    <div id="chat-messages" class="chat-box">
                        <div class="message system">
                            <strong>System:</strong> Welcome to the BB84 Quantum Simulator. Generate qubits to begin.
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- About Page -->
        <div id="about-page" class="about-content">
            <h2>Understanding BB84 Protocol</h2>
            <p>The BB84 protocol, developed by Bennett and Brassard in 1984, uses quantum mechanics to enable secure key distribution. Its security is guaranteed by the laws of physics, not computational complexity.</p>

            <h3>Quantum Bases</h3>
            <div class="basis-cards">
                <div class="basis-card">
                    <h4 style="color: var(--accent-cyan);">Z Basis (Computational)</h4>
                    <p>|0⟩ → Bit 0<br>|1⟩ → Bit 1</p>
                </div>
                <div class="basis-card">
                    <h4 style="color: var(--accent-green);">X Basis (Hadamard)</h4>
                    <p>|+⟩ = (|0⟩+|1⟩)/√2 → Bit 0<br>|-⟩ = (|0⟩-|1⟩)/√2 → Bit 1</p>
                </div>
            </div>

            <h3>Protocol Steps</h3>
            <div class="protocol-steps">
                <div class="protocol-step"><strong>1. Generation:</strong> Alice creates random bits and random bases</div>
                <div class="protocol-step"><strong>2. Transmission:</strong> Alice encodes and sends quantum states</div>
                <div class="protocol-step"><strong>3. Measurement:</strong> Bob measures with random bases</div>
                <div class="protocol-step"><strong>4. Sifting:</strong> They keep only matching basis measurements</div>
                <div class="protocol-step"><strong>5. Error Check:</strong> Compare subset to detect eavesdropping</div>
                <div class="protocol-step"><strong>6. Privacy Amplification:</strong> Hash function strengthens final key</div>
            </div>

            <h3>Security Principles</h3>
            <div class="security-grid">
                <div class="security-card">
                    <h4>No-Cloning Theorem</h4>
                    <p>Quantum states cannot be perfectly copied, preventing undetected interception</p>
                </div>
                <div class="security-card">
                    <h4>Measurement Disturbance</h4>
                    <p>Any measurement inevitably disturbs the quantum state, revealing eavesdroppers</p>
                </div>
                <div class="security-card">
                    <h4>Error Detection</h4>
                    <p>Eve's interference causes ~25% error rate, easily detectable by Alice and Bob</p>
                </div>
                <div class="security-card">
                    <h4>Information-Theoretic Security</h4>
                    <p>Security based on physics, not computational assumptions</p>
                </div>
            </div>
        </div>
    </div style="text-align:center;color:#00f0ff;padding:10px;">🚀 v1.0.1>

    <script>
        function showPage(page) {
            document.getElementById('simulator-page').style.display = page === 'simulator' ? 'grid' : 'none';
            document.getElementById('about-page').style.display = page === 'about' ? 'block' : 'none';
            document.getElementById('simulator-btn').classList.toggle('active', page === 'simulator');
            document.getElementById('about-btn').classList.toggle('active', page === 'about');
        }

        document.addEventListener('DOMContentLoaded', () => {
            // State management
            let protocolState = {
                currentStep: 0,
                encryptedMessages: []
            };

            // DOM Elements
            const elements = {
                aliceGenerate: document.getElementById('alice-generate'),
                bobMeasure: document.getElementById('bob-measure'),
                reconcile: document.getElementById('reconcile'),
                encrypt: document.getElementById('encrypt-btn'),
                decrypt: document.getElementById('decrypt-btn'),
                eavesdropCheck: document.getElementById('eavesdrop-check'),
                messageInput: document.getElementById('message-input'),
                photonStream: document.getElementById('photon-stream'),
                eveNode: document.querySelector('.node.eve'),
                aliceBits: document.getElementById('alice-bits'),
                aliceBases: document.getElementById('alice-bases'),
                bobBases: document.getElementById('bob-bases'),
                bobResults: document.getElementById('bob-results'),
                reconResult: document.getElementById('reconciliation-result'),
                finalKeyDisplay: document.getElementById('final-key-display'),
                finalKeySection: document.getElementById('final-key-section'),
                chat: document.getElementById('chat-messages'),
                statusElements: {
                    alice: document.getElementById('alice-status'),
                    bob: document.getElementById('bob-status'),
                    reconcile: document.getElementById('reconcile-status')
                }
            };

            // Utility functions
            const updateStatus = (element, status, text) => {
                const indicator = element.querySelector('.status-indicator');
                indicator.className = 'status-indicator';
                indicator.classList.add(`status-${status}`);
                element.childNodes[1].textContent = text;
            };

            const renderBitsBases = (container, items, type) => {
                container.innerHTML = items.map(item =>
                    `<div class="${type} ${item}">${item}</div>`
                ).join('');
            };

            const animatePhotons = (count, isEve = false) => {
                for (let i = 0; i < Math.min(count, 10); i++) {
                    setTimeout(() => {
                        const photon = document.createElement('div');
                        photon.className = `photon ${isEve ? 'eve' : ''}`;
                        photon.style.top = `${30 + Math.random() * 100}px`;
                        photon.style.animationDelay = '0s';
                        elements.photonStream.appendChild(photon);

                        setTimeout(() => {
                            if (photon.parentNode) {
                                photon.parentNode.removeChild(photon);
                            }
                        }, 2100);
                    }, i * 150);
                }
            };

            const addChatMessage = (type, sender, message, encrypted = null) => {
                const msgDiv = document.createElement('div');
                msgDiv.className = `message ${type}`;
                msgDiv.innerHTML = `<strong>${sender}:</strong> ${message}`;
                if (encrypted) {
                    msgDiv.innerHTML += `<div class="encrypted-text">Encrypted: ${encrypted}</div>`;
                }
                elements.chat.appendChild(msgDiv);
                elements.chat.scrollTop = elements.chat.scrollHeight;
            };

            // Eve toggle
            elements.eavesdropCheck.addEventListener('change', () => {
                elements.eveNode.style.display = elements.eavesdropCheck.checked ? 'flex' : 'none';
            });

            // Step 1: Alice generates qubits
            elements.aliceGenerate.addEventListener('click', async () => {
                updateStatus(elements.statusElements.alice, 'pending', 'Generating quantum states...');

                try {
                    const response = await fetch('/init_protocol', { method: 'POST' });
                    const data = await response.json();

                    renderBitsBases(elements.aliceBits, data.alice_bits, 'bit');
                    renderBitsBases(elements.aliceBases, data.alice_bases, 'basis');

                    animatePhotons(data.alice_bits.length);

                    updateStatus(elements.statusElements.alice, 'complete', `${data.alice_bits.length} qubits transmitted`);
                    elements.bobMeasure.disabled = false;
                    protocolState.currentStep = 1;

                    addChatMessage('alice', 'Alice', `Generated and sent ${data.alice_bits.length} qubits through quantum channel`);
                } catch (error) {
                    updateStatus(elements.statusElements.alice, 'error', 'Transmission failed');
                    console.error('Error:', error);
                }
            });

            // Step 2: Bob measures qubits
            elements.bobMeasure.addEventListener('click', async () => {
                updateStatus(elements.statusElements.bob, 'pending', 'Measuring quantum states...');
                const isEveActive = elements.eavesdropCheck.checked;

                try {
                    const response = await fetch('/measure_qubits', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ eavesdrop: isEveActive })
                    });
                    const data = await response.json();

                    renderBitsBases(elements.bobBases, data.bob_bases, 'basis');
                    renderBitsBases(elements.bobResults, data.bob_results, 'bit');

                    updateStatus(elements.statusElements.bob, 'complete', 'Measurement complete');
                    elements.reconcile.disabled = false;
                    protocolState.currentStep = 2;

                    if (isEveActive) {
                        setTimeout(() => animatePhotons(data.bob_results.length, true), 500);
                        addChatMessage('eve', 'Eve', 'Intercepted and measured quantum states!');
                    }

                    addChatMessage('bob', 'Bob', 'Received and measured qubits with random bases');
                } catch (error) {
                    updateStatus(elements.statusElements.bob, 'error', 'Measurement failed');
                    console.error('Error:', error);
                }
            });

            // Step 3: Key reconciliation with privacy amplification
            elements.reconcile.addEventListener('click', async () => {
                updateStatus(elements.statusElements.reconcile, 'pending', 'Reconciling keys...');

                try {
                    const response = await fetch('/reconcile', { method: 'POST' });
                    const data = await response.json();

                    if (data.status !== 'success') {
                        updateStatus(elements.statusElements.reconcile, 'error', 'Reconciliation failed');
                        return;
                    }

                    const errorRatePct = (data.error_rate * 100).toFixed(2);

                    if (data.eavesdrop_detected) {
                        elements.reconResult.className = 'detected';
                        elements.reconResult.innerHTML = `⚠️ EAVESDROPPER DETECTED!<br>Error Rate: ${errorRatePct}%`;
                        updateStatus(elements.statusElements.reconcile, 'error', 'Eve detected! Key compromised');
                        addChatMessage('system', 'System', `Eve detected! Error rate: ${errorRatePct}%. Abort communication.`);
                    } else {
                        elements.reconResult.className = 'not-detected';
                        elements.reconResult.innerHTML = `✅ Secure Channel Established<br>Error Rate: ${errorRatePct}%`;
                        updateStatus(elements.statusElements.reconcile, 'complete', 'Secure key ready');

                        // Show final key after privacy amplification
                        elements.finalKeySection.style.display = 'block';
                        elements.finalKeyDisplay.textContent = data.final_key;

                        // Enable communication
                        elements.messageInput.disabled = false;
                        elements.encrypt.disabled = false;
                        elements.decrypt.disabled = false;
                        protocolState.currentStep = 3;

                        addChatMessage('system', 'System', `Secure key established (${data.final_key_length} bits after privacy amplification)`);
                    }

                    // Show sifted keys
                    document.getElementById('alice-bits').innerHTML +=
                        `<div style="width:100%;margin-top:8px;font-size:0.8rem;color:var(--text-secondary);">Sifted: ${data.alice_key}</div>`;
                    document.getElementById('bob-results').innerHTML +=
                        `<div style="width:100%;margin-top:8px;font-size:0.8rem;color:var(--text-secondary);">Sifted: ${data.bob_key}</div>`;

                } catch (error) {
                    updateStatus(elements.statusElements.reconcile, 'error', 'Reconciliation failed');
                    console.error('Error:', error);
                }
            });

            // Encrypt message
            elements.encrypt.addEventListener('click', async () => {
                const message = elements.messageInput.value.trim();
                if (!message) return;

                try {
                    const response = await fetch('/encrypt', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message })
                    });
                    const data = await response.json();

                    protocolState.encryptedMessages.push({
                        original: message,
                        encrypted: data.encrypted,
                        key: data.key
                    });

                    addChatMessage('alice', 'Alice', message, data.encrypted);
                    elements.messageInput.value = '';
                } catch (error) {
                    console.error('Encryption error:', error);
                }
            });

            // Decrypt last message
            elements.decrypt.addEventListener('click', async () => {
                if (protocolState.encryptedMessages.length === 0) {
                    addChatMessage('system', 'System', 'No messages to decrypt');
                    return;
                }

                const lastMessage = protocolState.encryptedMessages[protocolState.encryptedMessages.length - 1];

                try {
                    const response = await fetch('/decrypt', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ encrypted: lastMessage.encrypted, key: lastMessage.key })
                    });
                    const data = await response.json();

                    addChatMessage('bob', 'Bob', `Decrypted: ${data.decrypted}`);
                } catch (error) {
                    console.error('Decryption error:', error);
                }
            });

            // Enter key support
            elements.messageInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') elements.encrypt.click();
            });
        });
    </script>
</body>
</html>
"""

class BB84Protocol:
    def __init__(self):
        self.basis_map = {0: 'Z', 1: 'X'}
        self.bit_map = {0: '0', 1: '1'}

    def generate_random_sequence(self, length=64):  # Increased from 16 to 64 for robust key
        return [secrets.randbelow(2) for _ in range(length)]

    def prepare_qubits(self, bits, bases):
        return [(self.basis_map[basis], bit) for bit, basis in zip(bits, bases)]

    def measure_qubit(self, qubit, basis_str):
        qubit_basis, qubit_value = qubit
        return qubit_value if qubit_basis == basis_str else secrets.randbelow(2)

    def measure_qubits(self, qubits, bases):
        return [self.measure_qubit(qubit, self.basis_map[basis]) for qubit, basis in zip(qubits, bases)]

    def simulate_eavesdropping(self, qubits):
        eaves_bases = self.generate_random_sequence(len(qubits))
        tampered_qubits = []
        for qubit, basis in zip(qubits, eaves_bases):
            basis_str = self.basis_map[basis]
            eve_result = self.measure_qubit(qubit, basis_str)
            tampered_qubits.append((basis_str, eve_result))
        return tampered_qubits

    def reconcile_keys(self, alice_bits, alice_bases, bob_bases, bob_results):
        matching_indices = [i for i, (a_b, b_b) in enumerate(zip(alice_bases, bob_bases)) if a_b == b_b]
        if not matching_indices:
            return {'error_rate': 0, 'alice_key': '', 'bob_key': ''}

        alice_key = [alice_bits[i] for i in matching_indices]
        bob_key = [bob_results[i] for i in matching_indices]

        error_count = sum(1 for a, b in zip(alice_key, bob_key) if a != b)
        error_rate = error_count / len(alice_key) if alice_key else 0

        return {
            'error_rate': error_rate,
            'alice_key': "".join(map(str, alice_key)),
            'bob_key': "".join(map(str, bob_key))
        }

    def privacy_amplification(self, key_string):
        """Apply SHA-256 hash for privacy amplification"""
        if not key_string:
            return ""
        # Hash the key to produce a shorter, more secure key
        hash_obj = hashlib.sha256(key_string.encode())
        # Convert to binary string
        hash_bits = bin(int(hash_obj.hexdigest(), 16))[2:].zfill(256)
        # Take first 32 bits for manageable key
        return hash_bits[:32]

    def encrypt_message(self, message, key):
        """XOR encryption with the key"""
        if not key:
            return ""
        encrypted = []
        key_bits = key
        for i, char in enumerate(message):
            key_index = i % len(key_bits)
            char_code = ord(char) ^ int(key_bits[key_index])
            encrypted.append(f"{char_code:02x}")
        return " ".join(encrypted)

    def decrypt_message(self, encrypted_hex, key):
        """XOR decryption with the key"""
        if not key or not encrypted_hex:
            return ""
        hex_values = encrypted_hex.split()
        decrypted = []
        key_bits = key
        for i, hex_val in enumerate(hex_values):
            key_index = i % len(key_bits)
            char_code = int(hex_val, 16) ^ int(key_bits[key_index])
            decrypted.append(chr(char_code))
        return "".join(decrypted)

# Initialize protocol
protocol = BB84Protocol()

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/init_protocol', methods=['POST'])
def init_protocol():
    # Use session for per-user state instead of global dictionary
    alice_bits = protocol.generate_random_sequence(length=64)
    alice_bases = protocol.generate_random_sequence(length=64)

    session['alice_bits'] = alice_bits
    session['alice_bases'] = alice_bases

    return jsonify({
        'alice_bits': [protocol.bit_map[b] for b in alice_bits],
        'alice_bases': [protocol.basis_map[b] for b in alice_bases]
    })

@app.route('/measure_qubits', methods=['POST'])
def measure_qubits():
    data = request.get_json(silent=True) or {}

    if 'alice_bits' not in session:
        return jsonify({'status': 'error', 'message': 'Alice must generate qubits first'})

    alice_bits = session['alice_bits']
    alice_bases = session['alice_bases']

    qubits = protocol.prepare_qubits(alice_bits, alice_bases)

    if data.get('eavesdrop'):
        qubits = protocol.simulate_eavesdropping(qubits)

    bob_bases = protocol.generate_random_sequence(len(qubits))
    bob_results = protocol.measure_qubits(qubits, bob_bases)

    session['bob_bases'] = bob_bases
    session['bob_results'] = bob_results

    return jsonify({
        'bob_bases': [protocol.basis_map[b] for b in bob_bases],
        'bob_results': [protocol.bit_map[b] for b in bob_results]
    })

@app.route('/reconcile', methods=['POST'])
def reconcile():
    if 'alice_bits' not in session or 'bob_results' not in session:
        return jsonify({'status': 'error', 'message': 'Both parties must complete their steps'})

    result = protocol.reconcile_keys(
        session['alice_bits'], session['alice_bases'],
        session['bob_bases'], session['bob_results']
    )

    # Privacy amplification
    alice_final_key = protocol.privacy_amplification(result['alice_key'])
    bob_final_key = protocol.privacy_amplification(result['bob_key'])

    session['final_key'] = alice_final_key

    result['final_key'] = alice_final_key
    result['final_key_length'] = len(alice_final_key)
    result['eavesdrop_detected'] = result['error_rate'] > 0.1
    result['status'] = 'success'

    return jsonify(result)

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    message = data.get('message', '')

    if 'final_key' not in session:
        return jsonify({'status': 'error', 'message': 'No key established'})

    final_key = session['final_key']
    encrypted = protocol.encrypt_message(message, final_key)

    return jsonify({
        'encrypted': encrypted,
        'key': final_key,
        'status': 'success'
    })

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    encrypted = data.get('encrypted', '')
    key = data.get('key', '')

    if not encrypted or not key:
        return jsonify({'status': 'error', 'message': 'Missing data'})

    decrypted = protocol.decrypt_message(encrypted, key)

    return jsonify({
        'decrypted': decrypted,
        'status': 'success'
    })

def find_free_port(start_port=5000):
    """Find a free port starting from start_port"""
    port = start_port
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.bind(('127.0.0.1', port))
            sock.close()
            return port
        except OSError:
            port += 1
            sock.close()

if __name__ == '__main__':
    port = find_free_port(5000)
    print(f"Starting BB84 Simulator on http://127.0.0.1:{port}")
    app.run(debug=True, threaded=True, port=port)
