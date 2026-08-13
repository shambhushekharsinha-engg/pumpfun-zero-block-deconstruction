"use client";

import React from 'react';
import { FadeIn, StaggerContainer, StaggerItem } from "@/components/FadeIn";
import { ShieldCheck, Crosshair, HelpCircle } from "lucide-react";

export default function Interpretability() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-20 relative">
      <div className="absolute top-1/4 right-0 w-96 h-96 bg-purple-600/10 rounded-full blur-[120px] pointer-events-none"></div>

      <FadeIn>
        <h1 className="text-4xl md:text-5xl font-black mb-4 tracking-tight">Interpretability & <span className="text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400">Evaluation</span></h1>
        <p className="text-xl text-slate-400 mb-20 max-w-2xl leading-relaxed">
          Rigorous ablation, chronological holdouts, and leakage firewalls proving the scientific validity of the replica.
        </p>
      </FadeIn>

      {/* LEAKAGE FIREWALL */}
      <section className="mb-24">
        <FadeIn delay={0.1}>
          <h2 className="text-2xl font-bold mb-8 flex items-center gap-3"><ShieldCheck className="text-blue-500" /> The Leakage Firewall</h2>
          <div className="bg-slate-900/40 backdrop-blur border border-slate-700/50 rounded-3xl p-8 md:p-12 shadow-xl">
            <div className="font-mono text-sm text-slate-400 mb-12 flex justify-center bg-slate-950/80 p-6 rounded-xl border border-slate-800 overflow-x-auto">
              <pre className="text-blue-300">
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
            
            <StaggerContainer className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center mb-10">
              <StaggerItem className="bg-slate-950/80 border border-slate-800 p-6 rounded-2xl">
                <div className="text-slate-400 text-xs font-bold mb-2 tracking-widest">SOURCE EVENT TEST</div>
                <div className="text-green-400 font-black text-xl flex items-center justify-center gap-2">PASS <ShieldCheck size={20}/></div>
              </StaggerItem>
              <StaggerItem className="bg-slate-950/80 border border-slate-800 p-6 rounded-2xl">
                <div className="text-slate-400 text-xs font-bold mb-2 tracking-widest">AGGREGATE TEST</div>
                <div className="text-green-400 font-black text-xl flex items-center justify-center gap-2">PASS <ShieldCheck size={20}/></div>
              </StaggerItem>
              <StaggerItem className="bg-slate-950/80 border border-slate-800 p-6 rounded-2xl">
                <div className="text-slate-400 text-xs font-bold mb-2 tracking-widest">ADVERSARIAL TEST</div>
                <div className="text-green-400 font-black text-xl flex items-center justify-center gap-2">PASS <ShieldCheck size={20}/></div>
              </StaggerItem>
            </StaggerContainer>

            <div className="text-center bg-blue-900/20 border border-blue-500/20 rounded-2xl p-6">
              <span className="text-blue-300 font-bold uppercase tracking-widest text-sm">Total Leakage Violations Found</span>
              <div className="text-white font-black text-6xl mt-2">0</div>
            </div>
          </div>
        </FadeIn>
      </section>

      {/* MODEL COMPARISON */}
      <section className="mb-24">
        <FadeIn delay={0.2}>
          <h2 className="text-2xl font-bold mb-4 flex items-center gap-3"><Crosshair className="text-purple-500" /> Ablation & Model Comparison (PR-AUC)</h2>
          <p className="text-slate-400 mb-10 leading-relaxed max-w-3xl">
            The model operates substantially above the 4.67% prevalence baseline, and its strongest generalization result occurs on completely unseen deployers.
          </p>
          
          <div className="space-y-8 bg-slate-900/40 backdrop-blur border border-slate-700/50 p-8 md:p-12 rounded-3xl shadow-xl">
            <div>
              <div className="flex justify-between text-sm font-bold mb-3 text-slate-400">
                <span>Baseline (Random Guess)</span>
                <span>0.0467</span>
              </div>
              <div className="w-full h-4 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                <div className="h-full bg-slate-600 w-[10%] rounded-full"></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm font-bold mb-3 text-slate-300">
                <span>Deployment Variables Only</span>
                <span>0.096</span>
              </div>
              <div className="w-full h-4 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                <div className="h-full bg-indigo-900 w-[24%] rounded-full"></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm font-bold mb-3 text-slate-200">
                <span>History Only</span>
                <span>0.238</span>
              </div>
              <div className="w-full h-4 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                <div className="h-full bg-indigo-600 w-[59%] rounded-full"></div>
              </div>
            </div>

            <div>
              <div className="flex justify-between text-sm font-bold mb-3 text-white">
                <span>Full Model (Frozen)</span>
                <span>0.286</span>
              </div>
              <div className="w-full h-5 bg-slate-950 rounded-full overflow-hidden relative border border-slate-800">
                <div className="h-full bg-gradient-to-r from-blue-600 to-indigo-500 w-[71%] rounded-full shadow-[0_0_15px_rgba(99,102,241,0.5)]"></div>
              </div>
            </div>

            <div className="pt-6 border-t border-slate-800/50 mt-8">
              <div className="flex justify-between text-sm font-black mb-3 text-purple-300">
                <span>Unseen Deployers (Generalization)</span>
                <span className="bg-purple-900/40 px-3 py-1 rounded-full border border-purple-500/30">0.396</span>
              </div>
              <div className="w-full h-6 bg-slate-950 rounded-full overflow-hidden relative border border-slate-800 shadow-[0_0_20px_rgba(168,85,247,0.15)]">
                <div className="h-full bg-gradient-to-r from-purple-600 to-pink-500 w-[99%] rounded-full shadow-[0_0_15px_rgba(168,85,247,0.5)]"></div>
              </div>
            </div>
          </div>
        </FadeIn>
      </section>

      {/* RESIDUAL REGIME */}
      <section>
        <FadeIn delay={0.3}>
          <h2 className="text-2xl font-bold mb-4 flex items-center gap-3"><HelpCircle className="text-slate-500" /> The Residual Regime</h2>
          <div className="bg-slate-900/40 backdrop-blur border border-slate-700/50 rounded-3xl p-8 md:p-12 shadow-xl">
            <p className="text-slate-400 mb-10 text-center max-w-2xl mx-auto leading-relaxed">
              The replica successfully reconstructs the dominant observable regime, but cannot fully explain the target&apos;s residual selections based solely on the supplied features.
            </p>

            <div className="flex flex-col md:flex-row gap-6 justify-center items-stretch text-center mb-12">
              <div className="flex-1 bg-slate-950/80 p-8 rounded-2xl border border-green-500/30 shadow-[0_0_20px_rgba(34,197,94,0.05)] relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 bg-green-500/10 rounded-full blur-2xl"></div>
                <div className="text-sm font-bold text-green-400 mb-3 tracking-widest uppercase">Dominant Regime</div>
                <div className="text-slate-400 mb-6 h-12 flex items-center justify-center">Low-history deployers accurately targeted</div>
                <div className="text-2xl font-black text-white flex items-center justify-center gap-2">RECONSTRUCTED <ShieldCheck className="text-green-400" size={24}/></div>
              </div>
              
              <div className="flex-1 bg-slate-950/80 p-8 rounded-2xl border border-slate-700 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 bg-slate-500/10 rounded-full blur-2xl"></div>
                <div className="text-sm font-bold text-slate-400 mb-3 tracking-widest uppercase">Residual Regime</div>
                <div className="text-slate-400 mb-6 h-12 flex items-center justify-center">Serial deployers occasionally selected by bot</div>
                <div className="text-2xl font-black text-white flex items-center justify-center gap-2">UNEXPLAINED <HelpCircle className="text-slate-500" size={24}/></div>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center border-t border-slate-800/50 pt-10">
              <div className="bg-slate-950/50 p-6 rounded-xl border border-slate-800">
                <div className="text-4xl font-black text-white mb-2">1,388</div>
                <div className="text-xs font-bold text-green-500 tracking-widest uppercase">Shared Targets</div>
              </div>
              <div className="bg-slate-950/50 p-6 rounded-xl border border-slate-800">
                <div className="text-4xl font-black text-white mb-2">2,898</div>
                <div className="text-xs font-bold text-blue-400 tracking-widest uppercase">Replica-Only</div>
              </div>
              <div className="bg-slate-950/50 p-6 rounded-xl border border-slate-800">
                <div className="text-4xl font-black text-white mb-2">1,536</div>
                <div className="text-xs font-bold text-slate-500 tracking-widest uppercase">Bot-Only</div>
              </div>
            </div>
          </div>
        </FadeIn>
      </section>

    </div>
  );
}
