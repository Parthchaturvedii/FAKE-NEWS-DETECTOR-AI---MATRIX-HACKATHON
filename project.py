<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Fake News Detector</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
    <div class="container mx-auto px-4 py-8 max-w-4xl">
        <div class="bg-white rounded-2xl shadow-2xl p-8">
            <div class="text-center mb-8">
                <h1 class="text-4xl font-bold text-indigo-600 mb-2">🔍 AI News Verifier</h1>
                <p class="text-gray-600">Verify news articles and claims using AI-powered fact-checking</p>
            </div>

            <!-- Input Section -->
            <div id="inputSection" class="mb-6">
                <label class="block text-gray-700 font-semibold mb-2">Enter News Article URL or Claim:</label>
                <input 
                    type="text" 
                    id="newsInput" 
                    placeholder="https://example.com/news-article or paste a claim here..."
                    class="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-indigo-500 transition"
                />
                <button 
                    onclick="verifyNews()" 
                    class="mt-4 w-full bg-indigo-600 text-white py-3 rounded-lg font-semibold hover:bg-indigo-700 transition shadow-lg hover:shadow-xl"
                >
                    Verify Now
                </button>
            </div>

            <!-- Loading Animation -->
            <div id="loadingSection" class="hidden">
                <div class="text-center py-8">
                    <div class="inline-block animate-spin rounded-full h-16 w-16 border-b-4 border-indigo-600"></div>
                    <p class="mt-4 text-gray-600 font-semibold" id="loadingText">Analyzing claim...</p>
                </div>
            </div>

            <!-- Results Section -->
            <div id="resultsSection" class="hidden">
                <div class="mb-6">
                    <h2 class="text-2xl font-bold text-gray-800 mb-4">Verification Results</h2>
                    
                    <!-- Credibility Score -->
                    <div class="bg-gradient-to-r from-indigo-50 to-blue-50 rounded-lg p-6 mb-6">
                        <div class="flex items-center justify-between mb-3">
                            <span class="text-lg font-semibold text-gray-700">Credibility Score</span>
                            <span id="credibilityScore" class="text-3xl font-bold text-indigo-600">--</span>
                        </div>
                        <div class="w-full bg-gray-200 rounded-full h-3">
                            <div id="credibilityBar" class="h-3 rounded-full transition-all duration-500" style="width: 0%"></div>
                        </div>
                    </div>

                    <!-- Verdict -->
                    <div id="verdictBox" class="rounded-lg p-6 mb-6">
                        <h3 class="text-xl font-bold mb-2" id="verdictTitle">Verdict</h3>
                        <p id="verdictText" class="text-gray-700"></p>
                    </div>

                    <!-- Analysis Details -->
                    <div class="space-y-4">
                        <div class="border-l-4 border-indigo-500 pl-4 py-2">
                            <h4 class="font-bold text-gray-800 mb-2">📊 Key Findings</h4>
                            <p id="keyFindings" class="text-gray-700"></p>
                        </div>

                        <div class="border-l-4 border-green-500 pl-4 py-2">
                            <h4 class="font-bold text-gray-800 mb-2">✅ Supporting Evidence</h4>
                            <p id="supportingEvidence" class="text-gray-700"></p>
                        </div>

                        <div class="border-l-4 border-red-500 pl-4 py-2">
                            <h4 class="font-bold text-gray-800 mb-2">⚠️ Red Flags</h4>
                            <p id="redFlags" class="text-gray-700"></p>
                        </div>

                        <div class="border-l-4 border-blue-500 pl-4 py-2">
                            <h4 class="font-bold text-gray-800 mb-2">🔗 Sources Checked</h4>
                            <ul id="sourcesChecked" class="list-disc list-inside text-gray-700"></ul>
                        </div>
                    </div>

                    <button 
                        onclick="reset()" 
                        class="mt-6 w-full bg-gray-600 text-white py-3 rounded-lg font-semibold hover:bg-gray-700 transition"
                    >
                        Check Another Article
                    </button>
                </div>
            </div>

            <!-- Error Section -->
            <div id="errorSection" class="hidden">
                <div class="bg-red-50 border-l-4 border-red-500 p-4 rounded">
                    <p class="text-red-700 font-semibold">⚠️ Error</p>
                    <p id="errorMessage" class="text-red-600"></p>
                </div>
                <button 
                    onclick="reset()" 
                    class="mt-4 w-full bg-gray-600 text-white py-3 rounded-lg font-semibold hover:bg-gray-700 transition"
                >
                    Try Again
                </button>
            </div>
        </div>

        <!-- Info Footer -->
        <div class="mt-8 text-center text-gray-600 text-sm">
            <p>⚡ Powered by AI | This tool provides guidance but should not replace professional fact-checking</p>
        </div>
    </div>

    <script>
        const loadingMessages = [
            "Analyzing claim...",
            "Searching reliable sources...",
            "Cross-referencing information...",
            "Evaluating credibility...",
            "Checking for misinformation patterns..."
        ];

        async function verifyNews() {
            const input = document.getElementById('newsInput').value.trim();
            
            if (!input) {
                showError('Please enter a URL or claim to verify');
                return;
            }

            // Show loading
            document.getElementById('inputSection').classList.add('hidden');
            document.getElementById('resultsSection').classList.add('hidden');
            document.getElementById('errorSection').classList.add('hidden');
            document.getElementById('loadingSection').classList.remove('hidden');

            // Animate loading messages
            let messageIndex = 0;
            const loadingInterval = setInterval(() => {
                document.getElementById('loadingText').textContent = loadingMessages[messageIndex];
                messageIndex = (messageIndex + 1) % loadingMessages.length;
            }, 2000);

            try {
                // Call Claude API for verification
                const response = await fetch("https://api.anthropic.com/v1/messages", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                    },
                    body: JSON.stringify({
                        model: "claude-sonnet-4-20250514",
                        max_tokens: 1000,
                        messages: [{
                            role: "user",
                            content: `You are a fact-checking AI. Analyze this news claim or article: "${input}"

Please search the web for information about this claim and provide a comprehensive fact-check. Return your response in the following JSON format:

{
  "credibilityScore": <number 0-100>,
  "verdict": "<Verified True|Mostly True|Mixed|Mostly False|False|Unverifiable>",
  "verdictExplanation": "<brief explanation>",
  "keyFindings": "<main findings>",
  "supportingEvidence": "<evidence that supports the claim>",
  "redFlags": "<concerning aspects or contradicting evidence>",
  "sources": ["<source 1>", "<source 2>", "<source 3>"]
}

Be thorough and objective. If you cannot verify, say so.`
                        }],
                        tools: [{
                            type: "web_search_20250305",
                            name: "web_search"
                        }]
                    })
                });

                clearInterval(loadingInterval);

                if (!response.ok) {
                    throw new Error('Failed to verify news. Please try again.');
                }

                const data = await response.json();
                
                // Extract text from response
                let resultText = '';
                for (const block of data.content) {
                    if (block.type === 'text') {
                        resultText += block.text;
                    }
                }

                // Try to parse JSON from the response
                const jsonMatch = resultText.match(/\{[\s\S]*\}/);
                if (!jsonMatch) {
                    throw new Error('Could not parse verification results');
                }

                const results = JSON.parse(jsonMatch[0]);
                displayResults(results);

            } catch (error) {
                clearInterval(loadingInterval);
                showError(error.message || 'An error occurred while verifying the news');
            }
        }

        function displayResults(results) {
            document.getElementById('loadingSection').classList.add('hidden');
            document.getElementById('resultsSection').classList.remove('hidden');

            // Credibility Score
            const score = results.credibilityScore || 0;
            document.getElementById('credibilityScore').textContent = score + '%';
            
            const credibilityBar = document.getElementById('credibilityBar');
            credibilityBar.style.width = score + '%';
            
            if (score >= 70) {
                credibilityBar.className = 'h-3 rounded-full bg-gradient-to-r from-green-400 to-green-600 transition-all duration-500';
            } else if (score >= 40) {
                credibilityBar.className = 'h-3 rounded-full bg-gradient-to-r from-yellow-400 to-orange-500 transition-all duration-500';
            } else {
                credibilityBar.className = 'h-3 rounded-full bg-gradient-to-r from-red-400 to-red-600 transition-all duration-500';
            }

            // Verdict
            const verdictBox = document.getElementById('verdictBox');
            const verdict = results.verdict || 'Unknown';
            
            if (verdict.includes('True') && !verdict.includes('False')) {
                verdictBox.className = 'bg-green-50 border-2 border-green-500 rounded-lg p-6 mb-6';
            } else if (verdict.includes('False')) {
                verdictBox.className = 'bg-red-50 border-2 border-red-500 rounded-lg p-6 mb-6';
            } else {
                verdictBox.className = 'bg-yellow-50 border-2 border-yellow-500 rounded-lg p-6 mb-6';
            }

            document.getElementById('verdictTitle').textContent = '🎯 ' + verdict;
            document.getElementById('verdictText').textContent = results.verdictExplanation || 'No explanation provided';

            // Details
            document.getElementById('keyFindings').textContent = results.keyFindings || 'No key findings available';
            document.getElementById('supportingEvidence').textContent = results.supportingEvidence || 'No supporting evidence found';
            document.getElementById('redFlags').textContent = results.redFlags || 'No red flags identified';

            // Sources
            const sourcesList = document.getElementById('sourcesChecked');
            sourcesList.innerHTML = '';
            if (results.sources && results.sources.length > 0) {
                results.sources.forEach(source => {
                    const li = document.createElement('li');
                    li.textContent = source;
                    li.className = 'mb-1';
                    sourcesList.appendChild(li);
                });
            } else {
                sourcesList.innerHTML = '<li>No sources available</li>';
            }
        }

        function showError(message) {
            document.getElementById('loadingSection').classList.add('hidden');
            document.getElementById('errorSection').classList.remove('hidden');
            document.getElementById('errorMessage').textContent = message;
        }

        function reset() {
            document.getElementById('newsInput').value = '';
            document.getElementById('inputSection').classList.remove('hidden');
            document.getElementById('loadingSection').classList.add('hidden');
            document.getElementById('resultsSection').classList.add('hidden');
            document.getElementById('errorSection').classList.add('hidden');
        }

        // Allow Enter key to submit
        document.getElementById('newsInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                verifyNews();
            }
        });
    </script>
</body>
</html>
