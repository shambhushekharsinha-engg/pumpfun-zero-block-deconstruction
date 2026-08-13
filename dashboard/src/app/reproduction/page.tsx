"use client";

import React from 'react';
import { FadeIn, StaggerContainer, StaggerItem } from "@/components/FadeIn";
import { CheckCircle2, FileText, Code, FileLock2, ShieldAlert } from "lucide-react";

export default function Reproduction() {
  return (
    <div key="reproduction-page" className="max-w-5xl mx-auto px-6 py-20 relative">
      <div className="absolute top-1/3 left-0 w-96 h-96 bg-emerald-600/10 rounded-full blur-[120px] pointer-events-none"></div>

      <FadeIn>
        <h1 className="text-4xl md:text-5xl font-black mb-4 tracking-tight">Reproduction <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-400">Contract</span></h1>
        <p className="text-xl text-slate-400 mb-20 max-w-2xl leading-relaxed">
          Transparency, immutability, and complete scientific reproducibility.
        </p>
      </FadeIn>

      {/* REPRODUCTION STATUS CARD */}
      <FadeIn delay={0.2}>
        <div className="bg-slate-900/40 backdrop-blur-xl border border-slate-700/50 rounded-3xl overflow-hidden mb-24 shadow-[0_0_50px_rgba(0,0,0,0.5)]">
          <div className="bg-slate-950/80 px-8 py-6 border-b border-slate-800/80 flex flex-col md:flex-row justify-between items-center gap-4">
            <h2 className="font-black text-white tracking-widest text-lg flex items-center gap-3">
              <FileLock2 className="text-emerald-500" /> REPRODUCTION STATUS
            </h2>
            <div className="px-4 py-2 bg-emerald-900/20 text-emerald-400 border border-emerald-500/30 rounded-full text-xs font-black tracking-widest shadow-[0_0_15px_rgba(16,185,129,0.2)] flex items-center gap-2">
              <CheckCircle2 size={16}/> VERIFIED
            </div>
          </div>
          
          <div className="p-0">
            <table className="w-full text-left text-sm md:text-base">
              <tbody className="divide-y divide-slate-800/50">
                <tr className="hover:bg-slate-800/20 transition-colors">
                  <td className="py-5 px-8 text-slate-400 font-bold">Model Artifact</td>
                  <td className="py-5 px-8 text-white font-mono bg-slate-950/30">v1.0.0-final</td>
                  <td className="py-5 px-8 text-right"><span className="text-blue-400 text-xs font-black tracking-widest bg-blue-900/20 px-3 py-1 rounded-full border border-blue-500/20">FROZEN</span></td>
                </tr>
                <tr className="hover:bg-slate-800/20 transition-colors">
                  <td className="py-5 px-8 text-slate-400 font-bold">Input Features</td>
                  <td className="py-5 px-8 text-white font-mono bg-slate-950/30">5 (Causal only)</td>
                  <td className="py-5 px-8 text-right flex justify-end items-center"><CheckCircle2 className="text-emerald-500" size={20}/></td>
                </tr>
                <tr className="hover:bg-slate-800/20 transition-colors">
                  <td className="py-5 px-8 text-slate-400 font-bold">Temporal Split</td>
                  <td className="py-5 px-8 text-white font-mono bg-slate-950/30">70% / 15% / 15%</td>
                  <td className="py-5 px-8 text-right flex justify-end items-center"><CheckCircle2 className="text-emerald-500" size={20}/></td>
                </tr>
                <tr className="hover:bg-slate-800/20 transition-colors">
                  <td className="py-5 px-8 text-slate-400 font-bold">Leakage Tests</td>
                  <td className="py-5 px-8 text-white font-mono bg-slate-950/30">Source, Aggregate, Future</td>
                  <td className="py-5 px-8 text-right flex justify-end items-center"><CheckCircle2 className="text-emerald-500" size={20}/></td>
                </tr>
                <tr className="hover:bg-slate-800/20 transition-colors">
                  <td className="py-5 px-8 text-slate-400 font-bold">Adversarial Test</td>
                  <td className="py-5 px-8 text-white font-mono bg-slate-950/30">Information Gain Trap</td>
                  <td className="py-5 px-8 text-right flex justify-end items-center"><CheckCircle2 className="text-emerald-500" size={20}/></td>
                </tr>
                <tr className="hover:bg-slate-800/20 transition-colors">
                  <td className="py-5 px-8 text-slate-400 font-bold">GitHub CI</td>
                  <td className="py-5 px-8 text-white font-mono bg-slate-950/30">pytest test_pipeline.py</td>
                  <td className="py-5 px-8 text-right flex justify-end items-center"><CheckCircle2 className="text-emerald-500" size={20}/></td>
                </tr>
                <tr className="hover:bg-slate-800/20 transition-colors">
                  <td className="py-5 px-8 text-slate-400 font-bold">Golden Inference</td>
                  <td className="py-5 px-8 text-white font-mono bg-slate-950/30">Scorer 100% Equivalence</td>
                  <td className="py-5 px-8 text-right flex justify-end items-center"><CheckCircle2 className="text-emerald-500" size={20}/></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </FadeIn>

      {/* EXTERNAL LINKS */}
      <FadeIn delay={0.4}>
        <h3 className="text-2xl font-bold mb-8">Scientific Artifacts</h3>
        <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          <StaggerItem>
            <a href="https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction" target="_blank" rel="noopener noreferrer" className="block p-8 bg-slate-900/40 backdrop-blur border border-slate-700/50 hover:border-blue-500/50 rounded-2xl transition-all duration-300 hover:shadow-[0_0_30px_rgba(59,130,246,0.15)] hover:-translate-y-1 group">
              <div className="flex items-center gap-3 font-black text-white mb-3 text-lg group-hover:text-blue-400 transition-colors">
                <Code size={24}/> GitHub Repository
              </div>
              <p className="text-slate-400 leading-relaxed">Complete source code, CI pipelines, automated tests, and frozen model artifacts.</p>
            </a>
          </StaggerItem>

          <StaggerItem>
            <a href="https://kaggle.com/competitions/solana-sniper-bot-reverse-engineering/writeups" target="_blank" rel="noopener noreferrer" className="block p-8 bg-slate-900/40 backdrop-blur border border-slate-700/50 hover:border-indigo-500/50 rounded-2xl transition-all duration-300 hover:shadow-[0_0_30px_rgba(99,102,241,0.15)] hover:-translate-y-1 group">
              <div className="flex items-center gap-3 font-black text-white mb-3 text-lg group-hover:text-indigo-400 transition-colors">
                <FileText size={24}/> Kaggle Writeup & Notebook
              </div>
              <p className="text-slate-400 leading-relaxed">The 10-phase chronological ML pipeline, comprehensive EDA, and execution logs.</p>
            </a>
          </StaggerItem>

          <StaggerItem>
            <a href="https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction/blob/main/submission/REPRODUCTION_CONTRACT.md" target="_blank" rel="noopener noreferrer" className="block p-8 bg-slate-900/40 backdrop-blur border border-slate-700/50 hover:border-emerald-500/50 rounded-2xl transition-all duration-300 hover:shadow-[0_0_30px_rgba(16,185,129,0.15)] hover:-translate-y-1 group">
              <div className="flex items-center gap-3 font-black text-white mb-3 text-lg group-hover:text-emerald-400 transition-colors">
                <FileLock2 size={24}/> Reproduction Contract
              </div>
              <p className="text-slate-400 leading-relaxed">Formal guarantees protecting the methodology, model weights, and environment.</p>
            </a>
          </StaggerItem>

          <StaggerItem>
            <a href="https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction/blob/main/submission/OBSERVABILITY.md" target="_blank" rel="noopener noreferrer" className="block p-8 bg-slate-900/40 backdrop-blur border border-slate-700/50 hover:border-purple-500/50 rounded-2xl transition-all duration-300 hover:shadow-[0_0_30px_rgba(168,85,247,0.15)] hover:-translate-y-1 group">
              <div className="flex items-center gap-3 font-black text-white mb-3 text-lg group-hover:text-purple-400 transition-colors">
                <ShieldAlert size={24}/> Observability Matrix
              </div>
              <p className="text-slate-400 leading-relaxed">Ethical disclosure of unobservable constraints, missing P&L, and hidden latency.</p>
            </a>
          </StaggerItem>

        </StaggerContainer>
      </FadeIn>

    </div>
  );
}
