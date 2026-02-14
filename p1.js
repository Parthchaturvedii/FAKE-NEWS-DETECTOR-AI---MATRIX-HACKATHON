// --- CONFIGURATION ---
const SERPER_API_KEY = "e3ca8de43ff318511942c7b2a8d5f121eb3dabca"; 

// Comprehensive Trusted Domains list to avoid the "10% bug"
const TRUSTED_SOURCES = [
    // Global Outlets
    "reuters.com", "apnews.com", "bbc.com", "nytimes.com", "theguardian.com", "npr.org", "wsj.com",
    // Indian Mainstream Media
    "timesofindia.indiatimes.com", "indiatimes.com", "thehindu.com", "ndtv.com", "indianexpress.com", 
    "hindustantimes.com", "business-standard.com", "economictimes.indiatimes.com", "news18.com",
    // Fact-Checkers & Official Govt
    "pib.gov.in", "altnews.in", "boomlive.in", "vishvasnews.com", "factchecker.in", "snopes.com", "politifact.com"
];

async function verifyNews() {
    const input = document.getElementById('newsInput').value.trim();
    if (!input) return alert("Please enter a claim.");

    toggleLoading(true);

    try {
        updateLoadingText("Searching global news...");
        const response = await fetch("https://google.serper.dev/news", {
            method: "POST",
            headers: { "X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json" },
            body: JSON.stringify({ q: input, num: 10 })
        });
        
        const data = await response.json();
        const verification = analyzeResults(input, data);
        displayResults(verification);
    } catch (error) {
        showError("Network error. Please try again.");
    }
}

function analyzeResults(query, data) {
    const news = data.news || [];
    let score = 30; // START AT 30% BASELINE (NEUTRAL)
    let trustedCount = 0;
    let factCheckFlag = false;

    if (news.length === 0) {
        return {
            credibilityScore: 10,
            verdict: "Unverifiable",
            verdictExplanation: "No media coverage found. Be cautious; this might be a isolated rumor.",
            keyFindings: "Total lack of digital footprint for this claim.",
            redFlags: "Information has not reached any indexed news database."
        };
    }

    const detectedSources = [];

    news.forEach(item => {
        const title = item.title.toLowerCase();
        const link = item.link.toLowerCase();
        detectedSources.push(item.source);

        // Check if domain is in our TRUSTED list
        const isTrusted = TRUSTED_SOURCES.some(src => link.includes(src));
        if (isTrusted) {
            trustedCount++;
            score += 20; // Massive boost for high-authority sources
        } else {
            score += 5; // Smaller boost for general media presence
        }

        // Check for debunking keywords
        if (title.includes("fact check") || title.includes("fake") || title.includes("hoax")) {
            factCheckFlag = true;
        }
    });

    // Score Logic & Normalization
    score = Math.min(score, 98); 
    if (factCheckFlag) score = Math.max(15, score - 50); // Penalize if fact-checkers are active
    
    let verdict = "Mixed / Unconfirmed";
    if (score > 70) verdict = "Verified True";
    else if (score < 40) verdict = "Likely False / Suspicious";

    return {
        credibilityScore: score,
        verdict: verdict,
        verdictExplanation: `Found ${news.length} reports. ${trustedCount} from high-authority sources.`,
        keyFindings: `Covered by: ${[...new Set(detectedSources)].slice(0, 3).join(", ")}.`,
        redFlags: factCheckFlag ? "Warning: Professional fact-checking reports found for this topic." : "None detected."
    };
}

// UI & Reset Functions
function displayResults(data) {
    toggleLoading(false);
    document.getElementById('resultsSection').classList.remove('hidden');
    const scoreEl = document.getElementById('credibilityScore');
    scoreEl.textContent = data.credibilityScore + "%";
    scoreEl.style.color = data.credibilityScore > 70 ? "#10b981" : data.credibilityScore > 40 ? "#f59e0b" : "#ef4444";
    document.getElementById('credibilityBar').style.width = data.credibilityScore + "%";
    document.getElementById('credibilityBar').style.backgroundColor = scoreEl.style.color;
    document.getElementById('verdictTitle').textContent = data.verdict;
    document.getElementById('verdictText').textContent = data.verdictExplanation;
    document.getElementById('keyFindings').textContent = data.keyFindings;
    document.getElementById('redFlags').textContent = data.redFlags;
}

function toggleLoading(s) { 
    document.getElementById('inputSection').classList.toggle('hidden', s);
    document.getElementById('loadingSection').classList.toggle('hidden', !s); 
}

function updateLoadingText(t) { document.getElementById('loadingText').textContent = t; }

function showError(m) { 
    toggleLoading(false); 
    document.getElementById('errorSection').classList.remove('hidden'); 
    document.getElementById('errorMessage').textContent = m; 
}

function reset() { location.reload(); }

window.verifyNews = verifyNews;
window.reset = reset;