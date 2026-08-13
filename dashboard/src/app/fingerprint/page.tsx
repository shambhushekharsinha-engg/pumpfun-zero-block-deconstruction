import React from 'react';

export default function Fingerprint() {
  return (
    <div className="max-w-4xl mx-auto px-6 py-20">
      <h1 className="text-4xl font-black mb-4">The Behavioral Fingerprint</h1>
      <p className="text-xl text-slate-400 mb-16">
        Our machine learning model isolated the exact decision boundaries defining the target's dominant observable regime.
      </p>

      {/* VISUAL RULE CARD */}
      <div className="bg-slate-900 border border-slate-700 rounded-lg p-8 mb-16">
        <div className="text-xs font-black tracking-widest text-slate-500 mb-8">TARGET BOT — DOMINANT OBSERVABLE REGIME</div>
        
        <div className="flex flex-col md:flex-row items-center justify-center gap-8 text-center">
          
          <div className="bg-slate-950 border border-slate-800 p-6 rounded-lg w-48">
            <div className="text-sm font-bold text-slate-400 mb-2">Past Launches</div>
            <div className="text-3xl font-black text-white">LOW</div>
          </div>

          <div className="text-4xl text-slate-600">+</div>

          <div className="bg-slate-950 border border-slate-800 p-6 rounded-lg w-48">
            <div className="text-sm font-bold text-slate-400 mb-2">Wallet Age</div>
            <div className="text-3xl font-black text-white">AGED</div>
          </div>

          <div className="text-4xl text-slate-600">→</div>

          <div className="bg-blue-900/20 border border-blue-500/30 p-6 rounded-lg w-56 shadow-[0_0_30px_rgba(59,130,246,0.15)]">
            <div className="text-lg font-black text-blue-400">HIGHER SELECTION PROBABILITY</div>
          </div>

        </div>
      </div>

      {/* FEATURE IMPORTANCE */}
      <h3 className="text-2xl font-bold mb-8">Observable Signal Hierarchy</h3>
      <div className="space-y-6">
        
        <div>
          <div className="flex justify-between text-sm font-bold mb-2">
            <span className="text-white">past_launches</span>
            <span className="text-blue-400">#1 Primary Signal</span>
          </div>
          <div className="w-full h-4 bg-slate-800 rounded overflow-hidden">
            <div className="h-full bg-blue-500 w-[100%]"></div>
          </div>
        </div>

        <div>
          <div className="flex justify-between text-sm font-bold mb-2">
            <span className="text-white">deployer_age_seconds</span>
            <span className="text-blue-400">#2 Secondary Signal</span>
          </div>
          <div className="w-full h-4 bg-slate-800 rounded overflow-hidden">
            <div className="h-full bg-slate-500 w-[70%]"></div>
          </div>
        </div>

        <div>
          <div className="flex justify-between text-sm font-bold mb-2">
            <span className="text-slate-300">past_sells</span>
            <span className="text-slate-500">Minor Signal</span>
          </div>
          <div className="w-full h-4 bg-slate-800 rounded overflow-hidden">
            <div className="h-full bg-slate-600 w-[25%]"></div>
          </div>
        </div>

        <div>
          <div className="flex justify-between text-sm font-bold mb-2">
            <span className="text-slate-300">past_buys</span>
            <span className="text-slate-500">Minor Signal</span>
          </div>
          <div className="w-full h-4 bg-slate-800 rounded overflow-hidden">
            <div className="h-full bg-slate-600 w-[20%]"></div>
          </div>
        </div>

        <div>
          <div className="flex justify-between text-sm font-bold mb-2">
            <span className="text-slate-300">past_burns</span>
            <span className="text-slate-500">Negligible</span>
          </div>
          <div className="w-full h-4 bg-slate-800 rounded overflow-hidden">
            <div className="h-full bg-slate-600 w-[10%]"></div>
          </div>
        </div>

      </div>

    </div>
  );
}
