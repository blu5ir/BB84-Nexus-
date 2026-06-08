# 🔐 BB84 Quantum Key Distribution Simulator

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A futuristic, interactive web-based simulator demonstrating the **BB84 Quantum Key Distribution (QKD) protocol** — the first quantum cryptography protocol that enables two parties to produce a shared random secret key, with security guaranteed by the fundamental laws of quantum mechanics.

![BB84 Simulator Screenshot]
<img width="1572" height="743" alt="image" src="https://github.com/user-attachments/assets/ab618017-6bad-4241-afc2-6e127d39957d" />


## ✨ Features

### 🎯 Core Protocol Implementation
- **Complete BB84 Protocol**: All 6 steps including privacy amplification
- **Quantum State Preparation**: Alice generates random bits and bases
- **Quantum Measurement**: Bob measures with random bases
- **Basis Reconciliation**: Public comparison of bases (sifting)
- **Eavesdropper Detection**: Eve's interference creates detectable errors
- **Privacy Amplification**: SHA-256 hashing for final key strengthening

### 🔬 Security Features
- **No-Cloning Theorem**: Visual demonstration of quantum state uniqueness
- **Measurement Disturbance**: Eve's interception causes ~25% error rate
- **Real-time Error Detection**: Immediate feedback on eavesdropping attempts
- **Information-Theoretic Security**: Physics-based, not computation-based security

### 🎨 Visual Design
- **Glassmorphism UI**: Frosted glass panels with modern aesthetics
- **Animated Particle Background**: Dynamic quantum particle visualization
- **Photon Animation**: Visual representation of quantum state transmission
- **Neon Accent Colors**: Cyan (Alice), Green (Bob), Red (Eve)
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dark Theme**: Eye-friendly deep space color scheme

### 💬 Communication Features
- **End-to-End Encryption**: XOR-based encryption using quantum-generated keys
- **Message Exchange**: Send encrypted messages between Alice and Bob
- **Decryption Verification**: Verify message integrity with decryption
- **Chat Interface**: Real-time communication log

## 📋 Requirements

- Python 3.8 or higher
- Flask 3.0+
- Modern web browser (Chrome, Firefox, Safari, Edge)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/bb84-quantum-simulator.git
cd bb84-quantum-simulator
