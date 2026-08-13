"use client";

import React from 'react';
import { FadeIn, StaggerContainer, StaggerItem } from "@/components/FadeIn";
import { Database, Search, Target, ShieldAlert, GitMerge, BrainCircuit, Activity, Hexagon } from "lucide-react";

export default function Methodology() {
  const steps = [
    { icon: <Database/>, number: '01', title: 'Data Ingestion', desc: '4.9M raw blockchain activities parsed from Solana mainnet RPCs.', color: 'text-slate-400 border-slate-700' },
    { icon: <Search/>, number: '02', title: 'Universe Definition', desc: '411,137 valid Solana token launches identified and categorized.', color: 'text-slate-400 border-slate-700' },
    { icon: <Target/>, number: '03', title: 'Target Acquisition', desc: '13,818 known positive selections extracted via graph analysis of the target wallet.', color: 'text-blue-400 border-blue-500/50 shadow-[0_0_15px_rgba(59,130,246,0.2)]' },
    { icon: <Activity/>, number: '04', title: 'Causal Features', desc: 'Strictly point-in-time features isolated (past_launches, age, buys/sells/burns).', color: 'text-blue-400 border-blue-500/50 shadow-[0_0_15px_rgba(59,130,246,0.2)]' },
    { icon: <ShieldAlert/>, number: '05', title: 'Leakage Firewall', desc: 'Pre-deployment isolation applied. Absolutely no future lookahead allowed.', color: 'text-blue-400 border-blue-500/50 shadow-[0_0_15px_rgba(59,130,246,0.2)]' },
    { icon: <GitMerge/>, number: '06', title: 'Temporal ML', desc: 'Time-aware validation splits generated and trained on LightGBM.', color: 'text-blue-400 border-blue-500/50 shadow-[0_0_15px_rgba(59,130,246,0.2)]' },
    { icon: <BrainCircuit/>, number: '07', title: 'Interpretability', desc: 'SHAP values and recursive ablation testing applied to the frozen model.', color: 'text-purple-400 border-purple-500/50 shadow-[0_0_15px_rgba(168,85,247,0.2)]' },
    { icon: <Hexagon/>, number: '08', title: 'Behavioral Fingerprint', desc: 'Final dominant rule extraction (The Zero-Block Deconstruction).', color: 'text-purple-400 border-purple-500/50 shadow-[0_0_15px_rgba(168,85,247,0.2)]' },
  ];

  return (
    <div className="max-w-4xl mx-auto px-6 py-20 relative">
      <div className="absolute top-0 right-0 w-96 h-96 bg-blue-900/10 rounded-full blur-[100px] pointer-events-none"></div>

      <FadeIn>
        <h1 className="text-4xl md:text-5xl font-black mb-4 tracking-tight">How We Reverse-Engineered <br/><span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">The Policy</span></h1>
        <p className="text-xl text-slate-400 mb-20 max-w-2xl leading-relaxed">
          From 4.9 million raw activities to a singular behavioral fingerprint.
        </p>
      </FadeIn>

      <div className="relative pl-4 md:pl-8">
        {/* Vertical Line */}
        <div className="absolute left-[39px] md:left-[55px] top-6 bottom-0 w-0.5 bg-gradient-to-b from-slate-800 via-blue-900/50 to-purple-900/50"></div>

        <StaggerContainer className="space-y-16">
          {steps.map((step, idx) => (
            <StaggerItem key={idx} className="relative flex items-start gap-6 md:gap-10 group">
              <div className={`relative z-10 w-12 h-12 md:w-16 md:h-16 rounded-2xl bg-slate-900/80 backdrop-blur border-2 flex items-center justify-center font-bold transition-transform duration-500 group-hover:scale-110 ${step.color}`}>
                {step.icon}
              </div>
              <div className="pt-2 md:pt-4">
                <div className="text-sm font-bold tracking-widest text-slate-500 mb-1 opacity-70">PHASE {step.number}</div>
                <h3 className="text-2xl font-bold mb-2 text-white group-hover:text-blue-300 transition-colors">{step.title}</h3>
                <p className="text-slate-400 text-lg leading-relaxed max-w-lg">{step.desc}</p>
              </div>
            </StaggerItem>
          ))}
        </StaggerContainer>
      </div>
    </div>
  );
}
