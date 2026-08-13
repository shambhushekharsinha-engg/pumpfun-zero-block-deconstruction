import React from 'react';

export default function Methodology() {
  const steps = [
    { number: '01', title: 'Data Ingestion', desc: '4.9M raw blockchain activities parsed', color: 'border-slate-700' },
    { number: '02', title: 'Universe Definition', desc: '411,137 valid Solana token launches identified', color: 'border-slate-700' },
    { number: '03', title: 'Target Acquisition', desc: '13,818 known positive selections extracted via transaction graph', color: 'border-slate-700' },
    { number: '04', title: 'Causal Features', desc: 'Strictly point-in-time features (past_launches, age, buys/sells/burns)', color: 'border-blue-500' },
    { number: '05', title: 'Leakage Firewall', desc: 'Pre-deployment isolation. No future lookahead allowed.', color: 'border-blue-500' },
    { number: '06', title: 'Temporal ML', desc: 'Time-aware validation splits trained on LightGBM', color: 'border-blue-500' },
    { number: '07', title: 'Interpretability', desc: 'SHAP values and recursive ablation testing', color: 'border-purple-500' },
    { number: '08', title: 'Behavioral Fingerprint', desc: 'Final dominant rule extraction (The Zero-Block Deconstruction)', color: 'border-purple-500' },
  ];

  return (
    <div className="max-w-4xl mx-auto px-6 py-20">
      <h1 className="text-4xl font-black mb-4">How We Reverse-Engineered the Policy</h1>
      <p className="text-xl text-slate-400 mb-16">
        From 4.9 million raw activities to a singular behavioral fingerprint.
      </p>

      <div className="relative">
        {/* Vertical Line */}
        <div className="absolute left-6 top-0 bottom-0 w-0.5 bg-slate-800"></div>

        <div className="space-y-12">
          {steps.map((step, idx) => (
            <div key={idx} className="relative flex items-start gap-8">
              <div className={`relative z-10 w-12 h-12 rounded-full bg-slate-900 border-2 ${step.color} flex items-center justify-center font-bold text-slate-300`}>
                {step.number}
              </div>
              <div className="pt-2">
                <h3 className="text-2xl font-bold mb-2">{step.title}</h3>
                <p className="text-slate-400 text-lg">{step.desc}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
