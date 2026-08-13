import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Link from "next/link";

import { Navigation } from "@/components/Navigation";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Zero-Block Deconstruction | Research Dashboard",
  description: "Interactive research artifact reconstructing a Solana sniper's observable decision policy.",
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="scroll-smooth">
      <body className={`${inter.className} bg-slate-950 text-slate-100 min-h-screen flex flex-col relative`}>
        {/* AMBIENT BACKGROUND GLOWS */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none z-[-1]">
          <div className="absolute -top-[20%] -left-[10%] w-[50%] h-[50%] rounded-full bg-blue-900/20 blur-[120px]"></div>
          <div className="absolute top-[40%] -right-[10%] w-[40%] h-[60%] rounded-full bg-indigo-900/10 blur-[120px]"></div>
        </div>

        <Navigation />

        {/* MAIN CONTENT */}
        <div className="flex-1 pt-16">
          {children}
        </div>

        {/* REPRODUCIBILITY FOOTER */}
        <footer className="border-t border-slate-800 bg-slate-950 py-12 mt-auto">
          <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center text-sm text-slate-500">
            <div className="flex items-center gap-4 mb-4 md:mb-0">
              <span className="px-2 py-1 bg-blue-900/30 text-blue-400 border border-blue-800/50 rounded font-mono text-xs">v1.1.1-final</span>
              <span className="font-semibold text-slate-400">MODEL STATUS: FROZEN</span>
              <span className="hidden md:inline">|</span>
              <span className="hidden md:inline">Features: 5</span>
              <span className="hidden md:inline">|</span>
              <div className="hidden md:flex items-center gap-1">CI: <div className="w-2 h-2 bg-green-500 rounded-full"></div> PASS</div>
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
