import React from 'react';
import Link from 'next/link';

export default function Reproduction() {
  return (
    <div className="max-w-4xl mx-auto px-6 py-20">
      <h1 className="text-4xl font-black mb-4">Reproduction Contract</h1>
      <p className="text-xl text-slate-400 mb-16">
        Transparency, immutability, and complete scientific reproducibility.
      </p>

      {/* REPRODUCTION STATUS CARD */}
      <div className="bg-slate-900 border border-slate-700 rounded-lg overflow-hidden mb-16">
        <div className="bg-slate-950 px-6 py-4 border-b border-slate-800 flex justify-between items-center">
          <h2 className="font-bold text-white tracking-wider">REPRODUCTION STATUS</h2>
          <span className="px-3 py-1 bg-green-900/30 text-green-400 border border-green-500/30 rounded text-xs font-bold">VERIFIED</span>
        </div>
        
        <div className="p-0">
          <table className="w-full text-left text-sm">
            <tbody className="divide-y divide-slate-800">
              <tr>
                <td className="py-4 px-6 text-slate-400 font-medium">Model Artifact</td>
                <td className="py-4 px-6 text-white font-mono">v1.0.0-final</td>
                <td className="py-4 px-6 text-right"><span className="text-slate-500 text-xs">FROZEN</span></td>
              </tr>
              <tr>
                <td className="py-4 px-6 text-slate-400 font-medium">Input Features</td>
                <td className="py-4 px-6 text-white font-mono">5 (Causal only)</td>
                <td className="py-4 px-6 text-right"><span className="text-green-500">PASS</span></td>
              </tr>
              <tr>
                <td className="py-4 px-6 text-slate-400 font-medium">Temporal Split</td>
                <td className="py-4 px-6 text-white font-mono">70% / 15% / 15%</td>
                <td className="py-4 px-6 text-right"><span className="text-green-500">PASS</span></td>
              </tr>
              <tr>
                <td className="py-4 px-6 text-slate-400 font-medium">Leakage Tests</td>
                <td className="py-4 px-6 text-white font-mono">Source, Aggregate, Future</td>
                <td className="py-4 px-6 text-right"><span className="text-green-500">PASS</span></td>
              </tr>
              <tr>
                <td className="py-4 px-6 text-slate-400 font-medium">Adversarial Test</td>
                <td className="py-4 px-6 text-white font-mono">Information Gain Trap</td>
                <td className="py-4 px-6 text-right"><span className="text-green-500">PASS</span></td>
              </tr>
              <tr>
                <td className="py-4 px-6 text-slate-400 font-medium">GitHub CI</td>
                <td className="py-4 px-6 text-white font-mono">pytest test_pipeline.py</td>
                <td className="py-4 px-6 text-right"><span className="text-green-500">PASS</span></td>
              </tr>
              <tr>
                <td className="py-4 px-6 text-slate-400 font-medium">Golden Inference</td>
                <td className="py-4 px-6 text-white font-mono">Scorer 100% Equivalence</td>
                <td className="py-4 px-6 text-right"><span className="text-green-500">PASS</span></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* EXTERNAL LINKS */}
      <h3 className="text-2xl font-bold mb-6">Scientific Artifacts</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        
        <a href="https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction" target="_blank" rel="noopener noreferrer" className="block p-6 bg-slate-900 border border-slate-700 hover:border-slate-500 rounded transition group">
          <div className="font-bold text-white mb-2 group-hover:text-blue-400 transition">GitHub Repository ↗</div>
          <p className="text-sm text-slate-400">Complete source code, CI pipelines, and frozen models.</p>
        </a>

        <a href="https://kaggle.com/competitions/solana-sniper-bot-reverse-engineering/writeups" target="_blank" rel="noopener noreferrer" className="block p-6 bg-slate-900 border border-slate-700 hover:border-slate-500 rounded transition group">
          <div className="font-bold text-white mb-2 group-hover:text-blue-400 transition">Kaggle Writeup & Notebook ↗</div>
          <p className="text-sm text-slate-400">The 10-phase chronological pipeline and execution logs.</p>
        </a>

        <a href="https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction/blob/main/submission/REPRODUCTION_CONTRACT.md" target="_blank" rel="noopener noreferrer" className="block p-6 bg-slate-900 border border-slate-700 hover:border-slate-500 rounded transition group">
          <div className="font-bold text-white mb-2 group-hover:text-blue-400 transition">Reproduction Contract ↗</div>
          <p className="text-sm text-slate-400">Formal guarantees protecting the methodology.</p>
        </a>

        <a href="https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction/blob/main/submission/OBSERVABILITY.md" target="_blank" rel="noopener noreferrer" className="block p-6 bg-slate-900 border border-slate-700 hover:border-slate-500 rounded transition group">
          <div className="font-bold text-white mb-2 group-hover:text-blue-400 transition">Observability Matrix ↗</div>
          <p className="text-sm text-slate-400">Ethical disclosure of unobservable constraints (P&L, Exits).</p>
        </a>

      </div>

    </div>
  );
}
