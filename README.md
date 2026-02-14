# FAKE-NEWS-DETECTOR-AI---MATRIX-HACKATHON
AI Fake News Detector is a full-stack web app that uses Machine Learning and NLP to classify news as real or fake. Built with HTML, CSS, JavaScript, Python (Flask), and MongoDB, it analyzes user input text and returns predictions with confidence scores, helping combat online misinformation.


AI News Verifier
This project is a high-performance, real-time news verification tool designed to combat misinformation and rumors. It allows users to input a news claim or a direct URL to receive an instant credibility assessment based on live web data.

Initially developed to use the Gemini 2.0 API with Google Search Grounding, the project evolved into a robust, logic-based system utilizing the Serper API to ensure high availability and bypass API quota limitations.

🚀 Key Features
Real-Time Verification: Scans global and regional news databases instantly using the Serper API.

Credibility Scoring Algorithm: Uses a custom-built point system that evaluates claims based on source authority, media presence, and the existence of professional fact-checks.

Extensive Trusted Source Database: Features a comprehensive list of high-authority international and Indian news domains (e.g., BBC, Reuters, Times of India, PIB) to ensure accurate localized results.

Fact-Check Detection: Automatically identifies if professional fact-checking organizations (like AltNews or Snopes) have already debunked a specific claim.

Responsive UI: A clean, modern interface built with Tailwind CSS that provides clear visual feedback, including a credibility progress bar and detailed verdicts.

🛠️ Technology Stack
Frontend: HTML5, Tailwind CSS.

Logic: JavaScript (ES6 Modules).

API: Serper News API (Google Search results).

Previous Iteration: Gemini 2.0 Flash (AI-powered analysis).

📖 How It Works
Search: The system fetches the top 10 most relevant news articles for the user's input.

Analyze: It iterates through the results to check if the URLs match a predefined list of trusted "High-Authority" domains.

Cross-Reference: It scans article titles for "debunking" keywords like "Fake," "Hoax," or "Fact Check".

Score: A credibility percentage is calculated: starting from a neutral baseline and increasing with trusted hits or decreasing with red flags.

Verdict: The final result is categorized as "Verified True," "Mixed," or "Likely False".
