import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Zero-Block Deconstruction | Research Dashboard",
  description: "Interactive research artifact reconstructing a Solana sniper's observable decision policy.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.className} bg-slate-950 text-slate-100 min-h-screen flex flex-col`}>
        {/* PREMIUM NAVIGATION */}
        <header className="border-b border-slate-800/50 bg-slate-950/80 backdrop-blur-md sticky top-0 z-50">
          <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
            <Link href="/" className="font-bold tracking-tight text-white flex items-center gap-2">
              <div className="w-4 h-4 bg-blue-500 rounded-sm"></div>
              ZERO-BLOCK DECONSTRUCTION
            </Link>
            <nav className="hidden md:flex gap-8 text-sm font-medium text-slate-400">
              <Link href="/methodology" className="hover:text-white transition">Methodology</Link>
              <Link href="/fingerprint" className="hover:text-white transition">Fingerprint</Link>
              <Link href="/interpretability" className="hover:text-white transition">Interpretability</Link>
              <Link href="/reproduction" className="hover:text-white transition">Reproduction</Link>
            </nav>
          </div>
        </header>

        {/* MAIN CONTENT */}
        <div className="flex-1">
          {children}
        </div>

        {/* REPRODUCIBILITY FOOTER */}
        <footer className="border-t border-slate-800 bg-slate-950 py-12 mt-auto">
          <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center text-sm text-slate-500">
            <div className="flex items-center gap-4 mb-4 md:mb-0">
              <span className="px-2 py-1 bg-blue-900/30 text-blue-400 border border-blue-800/50 rounded font-mono text-xs">v1.0.0-final</span>
              <span className="font-semibold text-slate-400">MODEL STATUS: FROZEN</span>
              <span className="hidden md:inline">|</span>
              <span className="hidden md:inline">Features: 5</span>
              <span className="hidden md:inline">|</span>
              <span className="hidden md:inline flex items-center gap-1">CI: <div className="w-2 h-2 bg-green-500 rounded-full"></div> PASS</span>
            </div>
            <div className="flex gap-6 font-medium">
              <Link href="/methodology" className="hover:text-slate-300 transition">Methodology</Link>
              <Link href="/reproduction" className="hover:text-slate-300 transition">Reproduction Contract</Link>
              <a href="https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction" target="_blank" rel="noopener noreferrer" className="hover:text-slate-300 transition">GitHub</a>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
