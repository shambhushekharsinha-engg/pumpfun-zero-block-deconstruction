"use client";

import { useState, useEffect } from "react";
import { Activity, Zap, ShieldCheck, AlertTriangle } from "lucide-react";

export function PolicyExplorer() {
  const [features, setFeatures] = useState({
    past_launches: 2,
    past_buys: 1,
    past_sells: 4,
    past_burns: 0,
    deployer_age_seconds: 518400, // 6 days
  });

  const [score, setScore] = useState<number | null>(null);
  const [isTop5, setIsTop5] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchPrediction = async () => {
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

    // Debounce the prediction request for smooth slider interaction
    const timeoutId = setTimeout(() => {
      fetchPrediction();
    }, 150);

    return () => clearTimeout(timeoutId);
  }, [features]);

  return (
    <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-700/50 rounded-3xl p-8 shadow-[0_0_50px_rgba(0,0,0,0.3)] relative overflow-hidden">
      <div className="absolute top-0 right-0 w-64 h-64 bg-blue-600/10 rounded-full blur-[100px] pointer-events-none"></div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 relative z-10">
        
        {/* INPUTS */}
        <div className="space-y-8">
          <div>
            <h3 className="text-xl font-bold text-white flex items-center gap-2 mb-2">
              <Zap className="text-blue-400" size={20} /> Hypothetical Deployer
            </h3>
            <p className="text-slate-400 text-sm">
              Explore the two dominant observable signals. Other causal-in-time features remain fixed at the reference deployer profile.
            </p>
          </div>
          
          <div className="space-y-6 bg-slate-950/50 p-6 rounded-2xl border border-slate-800">
            <div>
              <div className="flex justify-between text-sm mb-2 font-bold">
                <span className="text-slate-300">Past Launches (Primary Signal)</span>
                <span className="text-blue-400 bg-blue-900/30 px-2 py-0.5 rounded">{features.past_launches}</span>
              </div>
              <input 
                type="range" min="0" max="20" value={features.past_launches}
                onChange={(e) => setFeatures({...features, past_launches: parseInt(e.target.value)})}
                className="w-full accent-blue-500 h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer"
              />
            </div>

            <div>
              <div className="flex justify-between text-sm mb-2 font-bold">
                <span className="text-slate-300">Wallet Age (Secondary Signal)</span>
                <span className="text-blue-400 bg-blue-900/30 px-2 py-0.5 rounded">{Math.floor(features.deployer_age_seconds / 86400)} Days</span>
              </div>
              <input 
                type="range" min="0" max="30" value={Math.floor(features.deployer_age_seconds / 86400)}
                onChange={(e) => setFeatures({...features, deployer_age_seconds: parseInt(e.target.value) * 86400})}
                className="w-full accent-blue-500 h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer"
              />
            </div>
          </div>
        </div>

        {/* OUTPUT */}
        <div className="flex flex-col justify-center items-center p-8 bg-slate-950/80 rounded-2xl border border-slate-800 shadow-inner relative">
          
          <div className="absolute top-4 left-4">
            {loading ? (
              <span className="flex h-3 w-3 relative">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-slate-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-3 w-3 bg-slate-500"></span>
              </span>
            ) : (
              <span className="flex h-3 w-3 relative">
                <span className="relative inline-flex rounded-full h-3 w-3 bg-blue-500"></span>
              </span>
            )}
          </div>

          <h3 className="text-slate-500 text-xs font-black tracking-widest uppercase mb-4">Inference Engine Output</h3>
          
          <div className="text-7xl font-black mb-6 text-transparent bg-clip-text bg-gradient-to-br from-white to-slate-400 tabular-nums transition-all duration-300">
            {score !== null ? `${score.toFixed(1)}%` : "--.-%"}
          </div>
          
          <div className="h-16 flex items-center justify-center w-full">
            {isTop5 ? (
              <div className="flex items-center gap-2 text-green-400 font-black tracking-widest text-sm border border-green-500/30 bg-green-500/10 px-6 py-2 rounded-full shadow-[0_0_20px_rgba(34,197,94,0.15)] animate-in fade-in zoom-in duration-300">
                <ShieldCheck size={18}/> HIGH-CONFIDENCE OBSERVABLE REPLICA REGIME
              </div>
            ) : (
              <div className="flex items-center gap-2 text-slate-400 font-bold tracking-widest text-sm border border-slate-700/50 bg-slate-800/30 px-6 py-2 rounded-full animate-in fade-in zoom-in duration-300">
                <AlertTriangle size={18}/> UNEXPLAINED / RESIDUAL REGIME
              </div>
            )}
          </div>

          <div className="mt-8 pt-6 border-t border-slate-800 w-full text-center">
            <p className="text-sm text-slate-400 leading-relaxed font-medium">
              {features.past_launches < 3 ? (
                <span className="text-blue-300">Low past launches strongly correlate with selection. </span>
              ) : (
                <span className="text-slate-500">High past launches severely degrade probability. </span>
              )}
              
              {features.deployer_age_seconds > 86400 * 5 ? (
                <span className="text-blue-300">Aged wallets further amplify the signal.</span>
              ) : (
                <span className="text-slate-500">Fresh wallets introduce noise into the regime.</span>
              )}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
