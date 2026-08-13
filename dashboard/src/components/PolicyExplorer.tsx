"use client";

import { useState } from "react";

export default function PolicyExplorer() {
  const [features, setFeatures] = useState({
    past_launches: 2,
    past_buys: 1,
    past_sells: 4,
    past_burns: 0,
    deployer_age_seconds: 518400, // 6 days
  });

  const [score, setScore] = useState<number | null>(87.4);
  const [isTop5, setIsTop5] = useState<boolean>(true);
  const [loading, setLoading] = useState<boolean>(false);

  const handlePredict = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(features),
      });
      const data = await res.json();
      setScore(data.probability * 100);
      setIsTop5(data.top_5_percent);
    } catch (err) {
      console.error(err);
    }
    setLoading(false);
  };

  return (
    <div className="bg-slate-900 text-white p-6 rounded-lg shadow-lg border border-slate-700">
      <h2 className="text-2xl font-bold mb-4">Behavioral Policy Explorer</h2>
      <p className="text-sm text-slate-400 mb-6">
        Explore how the frozen replica responds to hypothetical point-in-time feature vectors.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h3 className="text-lg font-semibold mb-4 text-slate-300">HYPOTHETICAL DEPLOYER</h3>
          
          <div className="mb-4">
            <label className="block text-sm mb-1">Past launches: {features.past_launches}</label>
            <input 
              type="range" min="0" max="100" value={features.past_launches}
              onChange={(e) => setFeatures({...features, past_launches: parseInt(e.target.value)})}
              className="w-full accent-blue-500"
            />
          </div>

          <div className="mb-4">
            <label className="block text-sm mb-1">Deployer age (days): {Math.floor(features.deployer_age_seconds / 86400)}</label>
            <input 
              type="range" min="0" max="30" value={Math.floor(features.deployer_age_seconds / 86400)}
              onChange={(e) => setFeatures({...features, deployer_age_seconds: parseInt(e.target.value) * 86400})}
              className="w-full accent-blue-500"
            />
          </div>

          <button 
            onClick={handlePredict}
            className="mt-4 px-6 py-2 bg-blue-600 hover:bg-blue-500 rounded text-white font-semibold transition"
          >
            {loading ? "Simulating..." : "Run Frozen Inference"}
          </button>
        </div>

        <div className="flex flex-col justify-center items-center p-6 border-l border-slate-700">
          <h3 className="text-slate-400 text-sm tracking-wider mb-2">REPLICA PROBABILITY</h3>
          <div className="text-6xl font-black text-blue-400 mb-4">
            {score !== null ? `${score.toFixed(1)}%` : "--"}
          </div>
          
          {isTop5 && (
            <div className="text-green-400 font-bold tracking-wide border border-green-500/30 bg-green-500/10 px-4 py-1 rounded">
              HIGH-CONFIDENCE BEHAVIORAL MATCH
            </div>
          )}
          {!isTop5 && (
            <div className="text-slate-400 font-bold tracking-wide border border-slate-500/30 bg-slate-500/10 px-4 py-1 rounded">
              RESIDUAL / UNEXPLAINED REGIME
            </div>
          )}

          <div className="mt-8 text-sm text-slate-400">
            <p><strong>Primary driver:</strong> past_launches</p>
            <p><strong>Secondary driver:</strong> deployer_age_seconds</p>
          </div>
        </div>
      </div>
    </div>
  );
}
