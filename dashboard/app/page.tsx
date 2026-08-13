import PolicyExplorer from "@/components/PolicyExplorer";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 font-sans">
      <main className="max-w-5xl mx-auto px-6 py-16">
        
        {/* HERO */}
        <div className="mb-16">
          <h1 className="text-5xl font-black tracking-tight mb-4 text-white">
            ZERO-BLOCK <br/> DECONSTRUCTION
          </h1>
          <p className="text-xl text-slate-400 mb-8 max-w-2xl">
            Can we reconstruct the dominant observable decision policy of a Solana sniper using only point-in-time on-chain evidence?
          </p>
          <div className="flex gap-4">
            <Link href="#explorer" className="bg-blue-600 hover:bg-blue-500 text-white px-6 py-2 rounded font-semibold transition">
              Explore the Replica
            </Link>
            <Link href="/methodology" className="border border-slate-700 hover:border-slate-500 text-slate-300 px-6 py-2 rounded font-semibold transition">
              View Methodology
            </Link>
          </div>
        </div>

        {/* STATS */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-20">
          <div className="p-4 bg-slate-900 rounded border border-slate-800">
            <div className="text-3xl font-bold text-white mb-1">411,137</div>
            <div className="text-xs font-semibold text-slate-500 tracking-wider">DEPLOYMENTS</div>
          </div>
          <div className="p-4 bg-slate-900 rounded border border-slate-800">
            <div className="text-3xl font-bold text-white mb-1">13,818</div>
            <div className="text-xs font-semibold text-slate-500 tracking-wider">KNOWN POSITIVES</div>
          </div>
          <div className="p-4 bg-slate-900 rounded border border-slate-800">
            <div className="text-3xl font-bold text-white mb-1">0</div>
            <div className="text-xs font-semibold text-slate-500 tracking-wider">LEAKAGE VIOLATIONS</div>
          </div>
          <div className="p-4 bg-slate-900 rounded border border-slate-800">
            <div className="text-3xl font-bold text-white mb-1">0.2861</div>
            <div className="text-xs font-semibold text-slate-500 tracking-wider">TEST PR-AUC</div>
          </div>
        </div>

        {/* EXPLORER */}
        <section id="explorer" className="mb-20">
          <PolicyExplorer />
        </section>

      </main>

      {/* FOOTER */}
      <footer className="border-t border-slate-800 bg-slate-950 py-8">
        <div className="max-w-5xl mx-auto px-6 flex justify-between items-center text-sm text-slate-500">
          <div>
            <strong>MODEL STATUS:</strong> v1.0.0-final FROZEN
            <span className="mx-4">|</span>
            Features: 5
            <span className="mx-4">|</span>
            CI: <span className="text-green-500">PASS</span>
          </div>
          <div className="flex gap-4">
            <Link href="/methodology" className="hover:text-slate-300">Methodology</Link>
            <Link href="/reproduction" className="hover:text-slate-300">Reproduction Contract</Link>
            <a href="https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction" target="_blank" className="hover:text-slate-300">GitHub</a>
          </div>
        </div>
      </footer>
    </div>
  );
}
