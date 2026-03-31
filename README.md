🦯 Shravan: AI-Powered Smart Navigational Assistant
Shravan is an advanced, edge-computing-based assistive device engineered to provide "digital sight" and spatial awareness for the visually impaired. Built on the high-performance Raspberry Pi 5 platform, it replaces traditional passive sticks with a proactive, multi-modal sensing system that identifies obstacles, recognizes objects, and provides real-time voice guidance.

🌟 Key Features
Real-time AI Vision: Leverages YOLOv8 Nano to identify 80+ object classes (People, Cars, Stairs, Chairs) at 20+ FPS.

180° Safety Corridor: A tri-angular array of HC-SR04 Ultrasonic Sensors provides high-precision distance data, ensuring collision avoidance even in low-light.

Inverted Camera Logic: Optimized for hardware-level image normalization using libcamera (rpicam-apps) flags (--hflip, --vflip) to handle inverted mounting with zero CPU overhead.

Deterministic Priority Logic: A custom-built controller that manages three execution layers: Manual Scan, Reactive Safety Reflex, and Ambient Awareness.

🛠️ Tech Stack
Processor: Raspberry Pi 5 (8GB RAM, Broadcom BCM2712 SoC)

Vision: Sony IMX708 / OV5647 Camera Module (Night Vision Enabled)

Sensing: 3x HC-SR04 Ultrasonic Sensors + Tactile GPIO Interrupt Button

OS/Language: Raspberry Pi OS (64-bit) | Python 3.11

AI Framework: Ultralytics YOLOv8, OpenCV (cv2)

Audio: pyttsx3 (Offline TTS) via Bluetooth A2DP

📂 Project Structure
Plaintext
🧠 Operational Logic
Priority 1 (Manual): Triggered by a physical button for high-resolution on-demand object identification.

Priority 2 (Reactive): Activates when distance < 100cm. Throttles AI to prioritize immediate directional cues (e.g., "Obstacle Ahead, Move Left").

Priority 3 (Ambient): Standard mode for continuous background scanning in clear paths (>100cm).

🚀 Getting Started
Clone the repository:

Bash
git clone https://github.com/yourusername/shravan-smart-stick.git
Install dependencies:

Bash
pip install -r requirements.txt
Run the application:

Bash
python main.py
