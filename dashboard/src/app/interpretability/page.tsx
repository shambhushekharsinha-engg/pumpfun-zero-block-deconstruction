import React from 'react';

export default function Interpretability() {
  return (
    <div className="max-w-4xl mx-auto px-6 py-20">
      <h1 className="text-4xl font-black mb-4">Interpretability & Evaluation</h1>
      <p className="text-xl text-slate-400 mb-16">
        Rigorous ablation, chronological holdouts, and leakage firewalls proving the scientific validity of the replica.
      </p>

      {/* LEAKAGE FIREWALL */}
      <section className="mb-20">
        <h2 className="text-2xl font-bold mb-6">The Leakage Firewall</h2>
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-8">
          <div className="font-mono text-sm text-slate-400 mb-8 flex justify-center">
            <pre>
{`                 t_decision
                     │
                     ▼
───────────────●─────│────────────────────
 historical data     │     future data
       ✓             │          ✗
       ✓             │          ✗
       ✓             │          ✗
                     │
                DECISION`}
            </pre>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
            <div className="bg-slate-950 border border-slate-800 p-4 rounded text-green-400 font-bold tracking-wider text-sm">SOURCE EVENT TEST <span className="ml-2">✓</span></div>
            <div className="bg-slate-950 border border-slate-800 p-4 rounded text-green-400 font-bold tracking-wider text-sm">AGGREGATE TEST <span className="ml-2">✓</span></div>
            <div className="bg-slate-950 border border-slate-800 p-4 rounded text-green-400 font-bold tracking-wider text-sm">ADVERSARIAL TEST <span className="ml-2">✓</span></div>
          </div>
          <div className="mt-8 text-center text-xl text-slate-300 font-medium">
            TOTAL LEAKAGE VIOLATIONS: <span className="text-white font-black text-3xl ml-2">0</span>
          </div>
        </div>
      </section>

      {/* MODEL COMPARISON */}
      <section className="mb-20">
        <h2 className="text-2xl font-bold mb-6">Ablation & Model Comparison (PR-AUC)</h2>
        <p className="text-slate-400 mb-8">
          The model operates substantially above the 4.67% prevalence baseline, and its strongest generalization result occurs on completely unseen deployers.
        </p>
        
        <div className="space-y-6">
          <div>
            <div className="flex justify-between text-sm font-bold mb-2 text-slate-400">
              <span>Baseline (Random Guess)</span>
              <span>0.0467</span>
            </div>
            <div className="w-full h-6 bg-slate-800 rounded overflow-hidden">
              <div className="h-full bg-slate-600 w-[10%]"></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between text-sm font-bold mb-2 text-slate-300">
              <span>Deployment Variables Only</span>
              <span>0.096</span>
            </div>
            <div className="w-full h-6 bg-slate-800 rounded overflow-hidden">
              <div className="h-full bg-blue-900 w-[24%]"></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between text-sm font-bold mb-2 text-slate-200">
              <span>History Only</span>
              <span>0.238</span>
            </div>
            <div className="w-full h-6 bg-slate-800 rounded overflow-hidden">
              <div className="h-full bg-blue-700 w-[59%]"></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between text-sm font-bold mb-2 text-white">
              <span>Full Model (Frozen)</span>
              <span>0.286</span>
            </div>
            <div className="w-full h-6 bg-slate-800 rounded overflow-hidden relative">
              <div className="h-full bg-blue-500 w-[71%]"></div>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 mt-6">
            <div className="flex justify-between text-sm font-bold mb-2 text-blue-300">
              <span>Unseen Deployers (Generalization)</span>
              <span>0.396</span>
            </div>
            <div className="w-full h-6 bg-slate-800 rounded overflow-hidden relative shadow-[0_0_15px_rgba(59,130,246,0.3)]">
              <div className="h-full bg-blue-400 w-[99%]"></div>
            </div>
          </div>
        </div>
      </section>

      {/* RESIDUAL REGIME */}
      <section>
        <h2 className="text-2xl font-bold mb-6">The Residual Regime</h2>
        <div className="bg-slate-900 border border-slate-700 rounded-lg p-8">
          <p className="text-slate-400 mb-8 text-center max-w-xl mx-auto">
            The replica reconstructs the dominant observable regime but cannot fully explain the target's residual selections from the supplied data.
          </p>

          <div className="flex flex-col md:flex-row gap-8 justify-center items-stretch text-center mb-8">
            <div className="flex-1 bg-slate-950 p-6 rounded border border-blue-500/30">
              <div className="text-sm font-bold text-blue-400 mb-2">Dominant Regime</div>
              <div className="text-xs text-slate-500 mb-4 h-10">Low-history deployers</div>
              <div className="text-xl font-black text-white">RECONSTRUCTED <span className="text-green-400">✓</span></div>
            </div>
            
            <div className="flex-1 bg-slate-950 p-6 rounded border border-slate-700">
              <div className="text-sm font-bold text-slate-400 mb-2">Residual Regime</div>
              <div className="text-xs text-slate-500 mb-4 h-10">Serial deployers occasionally selected</div>
              <div className="text-xl font-black text-white">UNEXPLAINED <span className="text-slate-500">?</span></div>
            </div>
          </div>

          <div className="grid grid-cols-3 gap-4 text-center border-t border-slate-800 pt-8">
            <div>
              <div className="text-3xl font-black text-white mb-1">1,388</div>
              <div className="text-xs font-bold text-slate-500 tracking-wider">SHARED TARGETS</div>
            </div>
            <div>
              <div className="text-3xl font-black text-white mb-1">2,898</div>
              <div className="text-xs font-bold text-slate-500 tracking-wider">REPLICA-ONLY</div>
            </div>
            <div>
              <div className="text-3xl font-black text-white mb-1">1,536</div>
              <div className="text-xs font-bold text-slate-500 tracking-wider">BOT-ONLY</div>
            </div>
          </div>
        </div>
      </section>

    </div>
  );
}
