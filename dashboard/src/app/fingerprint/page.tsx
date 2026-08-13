"use client";

import React from 'react';
import { FadeIn, StaggerContainer, StaggerItem } from "@/components/FadeIn";
import { Plus, ArrowRight } from "lucide-react";

export default function Fingerprint() {
  return (
    <div className="max-w-5xl mx-auto px-6 py-20 relative">
      <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-[120px] pointer-events-none"></div>

      <FadeIn>
        <h1 className="text-4xl md:text-5xl font-black mb-4 tracking-tight">The Behavioral <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-cyan-300">Fingerprint</span></h1>
        <p className="text-xl text-slate-400 mb-20 max-w-2xl leading-relaxed">
          Our machine learning model isolated the exact decision boundaries defining the target's dominant observable regime.
        </p>
      </FadeIn>

      {/* VISUAL RULE CARD */}
      <FadeIn delay={0.2}>
        <div className="bg-slate-900/50 backdrop-blur-xl border border-slate-700/50 rounded-3xl p-8 md:p-12 mb-20 shadow-[0_0_50px_rgba(0,0,0,0.5)] relative overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-br from-blue-500/5 to-purple-500/5 pointer-events-none"></div>
          
          <div className="flex items-center justify-between mb-12 relative z-10">
            <div className="text-xs font-black tracking-widest text-blue-400 bg-blue-900/20 px-4 py-2 rounded-full border border-blue-500/20">TARGET BOT — DOMINANT REGIME</div>
            <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          </div>
          
          <div className="flex flex-col lg:flex-row items-center justify-center gap-6 lg:gap-8 text-center relative z-10">
            
            <div className="bg-slate-950/80 backdrop-blur border border-slate-700/50 p-8 rounded-2xl w-full lg:w-56 shadow-xl hover:border-blue-500/30 transition-colors">
              <div className="text-sm font-bold text-slate-400 mb-3 uppercase tracking-wider">Past Launches</div>
              <div className="text-4xl font-black text-white">LOW</div>
            </div>

            <div className="text-slate-600">
              <Plus size={32} />
            </div>

            <div className="bg-slate-950/80 backdrop-blur border border-slate-700/50 p-8 rounded-2xl w-full lg:w-56 shadow-xl hover:border-blue-500/30 transition-colors">
              <div className="text-sm font-bold text-slate-400 mb-3 uppercase tracking-wider">Wallet Age</div>
              <div className="text-4xl font-black text-white">AGED</div>
            </div>

            <div className="text-slate-600 hidden lg:block">
              <ArrowRight size={32} />
            </div>
            
            <div className="text-slate-600 block lg:hidden my-2 rotate-90">
              <ArrowRight size={32} />
            </div>

            <div className="bg-gradient-to-br from-blue-900/40 to-cyan-900/40 border border-blue-500/40 p-8 rounded-2xl w-full lg:w-72 shadow-[0_0_40px_rgba(59,130,246,0.2)]">
              <div className="text-lg font-black text-blue-300 leading-tight">HIGHER SELECTION PROBABILITY</div>
            </div>

          </div>
        </div>
      </FadeIn>

      {/* FEATURE IMPORTANCE */}
      <FadeIn delay={0.4}>
        <h3 className="text-2xl font-bold mb-8">Observable Signal Hierarchy</h3>
        <StaggerContainer className="space-y-8 bg-slate-900/30 border border-slate-800/50 rounded-3xl p-8 md:p-12">
          
          <StaggerItem>
            <div className="flex justify-between text-sm font-bold mb-3">
              <span className="text-white text-base">past_launches</span>
              <span className="text-blue-400 bg-blue-900/30 px-3 py-1 rounded-full text-xs">#1 Primary Signal</span>
            </div>
            <div className="w-full h-3 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
              <div className="h-full bg-gradient-to-r from-blue-600 to-cyan-400 w-[100%] shadow-[0_0_10px_rgba(59,130,246,0.5)]"></div>
            </div>
          </StaggerItem>

          <StaggerItem>
            <div className="flex justify-between text-sm font-bold mb-3">
              <span className="text-white text-base">deployer_age_seconds</span>
              <span className="text-blue-400 bg-blue-900/30 px-3 py-1 rounded-full text-xs">#2 Secondary Signal</span>
            </div>
            <div className="w-full h-3 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
              <div className="h-full bg-slate-400 w-[70%]"></div>
            </div>
          </StaggerItem>

          <StaggerItem>
            <div className="flex justify-between text-sm font-bold mb-3">
              <span className="text-slate-300">past_sells</span>
              <span className="text-slate-500 text-xs uppercase tracking-wider mt-1">Minor Signal</span>
            </div>
            <div className="w-full h-2 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
              <div className="h-full bg-slate-600 w-[25%]"></div>
            </div>
          </StaggerItem>

          <StaggerItem>
            <div className="flex justify-between text-sm font-bold mb-3">
              <span className="text-slate-300">past_buys</span>
              <span className="text-slate-500 text-xs uppercase tracking-wider mt-1">Minor Signal</span>
            </div>
            <div className="w-full h-2 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
              <div className="h-full bg-slate-600 w-[20%]"></div>
            </div>
          </StaggerItem>

          <StaggerItem>
            <div className="flex justify-between text-sm font-bold mb-3">
              <span className="text-slate-300">past_burns</span>
              <span className="text-slate-600 text-xs uppercase tracking-wider mt-1">Negligible</span>
            </div>
            <div className="w-full h-2 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
              <div className="h-full bg-slate-700 w-[10%]"></div>
            </div>
          </StaggerItem>

        </StaggerContainer>
      </FadeIn>

    </div>
  );
}
