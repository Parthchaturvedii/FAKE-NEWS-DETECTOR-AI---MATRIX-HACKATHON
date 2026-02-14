import React, { useState } from 'react';
import axios from 'axios';
import { AlertCircle, CheckCircle2, Shield } from 'lucide-react';

function App() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      const { data } = await axios.post('http://localhost:8000/predict', { text });
      setResult(data.prediction);
    } catch (error) {
      console.error("API Error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white flex flex-col items-center p-8 font-sans">
      <div className="max-w-2xl w-full space-y-6">
        <header className="flex items-center gap-3 mb-8">
          <Shield className="text-blue-400 w-10 h-10" />
          <h1 className="text-3xl font-bold italic">TruthEngine v1.0</h1>
        </header>

        <textarea
          className="w-full h-48 p-4 bg-slate-800 rounded-lg border border-slate-700 focus:ring-2 focus:ring-blue-500 outline-none transition-all"
          placeholder="Paste news content here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />

        <button
          onClick={handleAnalyze}
          disabled={loading || !text}
          className="w-full py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-700 rounded-md font-semibold transition-colors"
        >
          {loading ? 'Analyzing Neural Patterns...' : 'Verify Content'}
        </button>

        {result && (
          <div className={`p-6 rounded-lg border flex items-center gap-4 ${
            result === 'REAL' ? 'bg-emerald-900/20 border-emerald-500' : 'bg-red-900/20 border-red-500'
          }`}>
            {result === 'REAL' ? <CheckCircle2 className="text-emerald-500" /> : <AlertCircle className="text-red-500" />}
            <div>
              <p className="text-lg font-bold">Classification: {result}</p>
              <p className="text-sm opacity-70">Based on trained linguistic patterns.</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
const response = await axios.post('http://127.0.0.1:8000/predict', {
  text: "Scientists discover the moon is made of cheese"
});

console.log(response.data.label); // Outputs: FAKE