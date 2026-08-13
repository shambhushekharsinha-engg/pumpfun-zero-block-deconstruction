import { PolicyExplorer } from "@/components/PolicyExplorer";
import EvidenceBadge from "@/components/EvidenceBadge";
import { FadeIn, StaggerContainer, StaggerItem } from "@/components/FadeIn";
import Link from "next/link";
import { ArrowRight, ShieldCheck, Zap, Activity } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col min-h-screen">
      {/* HEADER SECTION */}
      <header className="pb-16 pt-24 relative overflow-hidden">
        {/* Subtle background grid */}
        <div className="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 mix-blend-overlay pointer-events-none"></div>
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#4f4f4f2e_1px,transparent_1px),linear-gradient(to_bottom,#4f4f4f2e_1px,transparent_1px)] bg-[size:14px_24px] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)] pointer-events-none z-[-1]"></div>

        <FadeIn className="max-w-5xl mx-auto px-6 text-center relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-900/30 border border-blue-500/30 text-blue-400 text-xs font-bold mb-8">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
            </span>
            MODEL v1.0.0-final (FROZEN)
          </div>
          
          <h1 className="text-5xl md:text-7xl font-black mb-6 tracking-tight text-white leading-tight drop-shadow-lg">
            Reconstructing a Sniper's <br className="hidden md:block"/>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-300 to-emerald-400 drop-shadow-sm">
              Observable Decision Policy
            </span>
          </h1>
          
          <p className="text-xl md:text-2xl text-slate-400 max-w-3xl mx-auto leading-relaxed mb-10">
            A purely mathematical deconstruction of a highly successful Solana target, using strictly point-in-time features and rigorous leakage firewalls.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <Link href="#explorer" className="group flex items-center gap-2 bg-white text-slate-950 px-8 py-3 rounded-full font-bold transition hover:bg-blue-50 hover:scale-105 shadow-[0_0_20px_rgba(255,255,255,0.2)]">
              Test The Replica
              <ArrowRight size={18} className="group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link href="/methodology" className="flex items-center gap-2 border border-slate-700 bg-slate-900/50 hover:bg-slate-800 text-slate-300 px-8 py-3 rounded-full font-bold transition hover:border-slate-500">
              View Methodology
            </Link>
          </div>
        </FadeIn>
      </header>

      {/* MAIN PIPELINE */}
      <main className="flex-1 max-w-6xl mx-auto px-6 py-16 w-full space-y-24">
        
        {/* EXECUTIVE SUMMARY */}
        <section>
          <FadeIn delay={0.2}>
            <div className="flex items-center gap-2 text-slate-400 mb-6 font-bold tracking-widest text-sm uppercase">
              <Zap size={16} className="text-blue-500" /> Executive Metrics
            </div>
          </FadeIn>
          
          <StaggerContainer className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <StaggerItem className="bg-slate-900/50 backdrop-blur border border-slate-800 p-6 rounded-2xl hover:border-blue-500/50 transition-colors">
              <div className="text-slate-400 text-sm font-bold mb-2">Dominant Regime Accuracy</div>
              <div className="text-4xl font-black text-white">0.2861</div>
              <div className="text-sm text-green-400 mt-2 font-medium">PR-AUC (+6.1x over baseline)</div>
            </StaggerItem>

            <StaggerItem className="bg-slate-900/50 backdrop-blur border border-slate-800 p-6 rounded-2xl hover:border-emerald-500/50 transition-colors">
              <div className="text-slate-400 text-sm font-bold mb-2">Leakage Violations</div>
              <div className="text-4xl font-black text-white">0</div>
              <div className="text-sm text-emerald-400 mt-2 font-medium">100% Strict Point-in-time</div>
            </StaggerItem>

            <StaggerItem className="bg-slate-900/50 backdrop-blur border border-slate-800 p-6 rounded-2xl hover:border-purple-500/50 transition-colors">
              <div className="text-slate-400 text-sm font-bold mb-2">Generalization Factor</div>
              <div className="text-4xl font-black text-white">0.3963</div>
              <div className="text-sm text-purple-400 mt-2 font-medium">Unseen deployer cohort</div>
            </StaggerItem>
          </StaggerContainer>
        </section>

        {/* EVIDENCE ALIGNMENT */}
        <section>
          <FadeIn delay={0.3}>
            <div className="flex items-center gap-2 text-slate-400 mb-6 font-bold tracking-widest text-sm uppercase">
              <ShieldCheck size={16} className="text-blue-500" /> Epistemological Framework
            </div>
            
            <div className="bg-slate-900/50 backdrop-blur border border-slate-800 p-8 rounded-3xl grid grid-cols-1 md:grid-cols-2 gap-12 items-center relative overflow-hidden">
              <div className="absolute top-0 right-0 w-64 h-64 bg-blue-900/10 rounded-full blur-3xl"></div>
              
              <div className="relative z-10">
                <h2 className="text-3xl font-black mb-4">The Observability Constraint</h2>
                <p className="text-slate-400 leading-relaxed mb-6">
                  We cannot know the target&apos;s true P&L. We cannot know their internal latency. 
                  We can only mathematically map their <strong>observable selections</strong> to the 
                  <strong> observable point-in-time features</strong> of the tokens they selected.
                </p>
                <Link href="/interpretability" className="text-blue-400 hover:text-blue-300 font-bold inline-flex items-center gap-1">
                  Read our methodology <ArrowRight size={16}/>
                </Link>
              </div>

              <div className="space-y-4 relative z-10">
                <EvidenceBadge title="Point-in-Time Features" status="observable" description="Raw on-chain telemetry available prior to deployment." />
                <EvidenceBadge title="Target's Purchase Events" status="observable" description="Known selections extracted from the target's public wallet." />
                <EvidenceBadge title="Target's Exit Timing" status="unobservable" description="We cannot predict when the target will sell." />
                <EvidenceBadge title="Target's True Profitability" status="unobservable" description="Latency and MEV obscure the true P&L." />
              </div>
            </div>
          </FadeIn>
        </section>

        {/* INTERACTIVE DEMO */}
        <section id="explorer" className="scroll-mt-32">
          <FadeIn delay={0.4}>
            <div className="flex items-center gap-2 text-slate-400 mb-6 font-bold tracking-widest text-sm uppercase">
              <Activity size={16} className="text-blue-500" /> Behavioral Simulator
            </div>
            <PolicyExplorer />
          </FadeIn>
        </section>

      </main>
    </div>
  );
}
