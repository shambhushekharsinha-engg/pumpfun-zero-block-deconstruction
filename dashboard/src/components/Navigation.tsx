"use client";

import { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Menu, X, Hexagon, Terminal, Activity, FileCode2 } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function Navigation() {
  const [isOpen, setIsOpen] = useState(false);
  const pathname = usePathname();

  const links = [
    { href: "/methodology", label: "Methodology", icon: <Terminal size={16} /> },
    { href: "/fingerprint", label: "Fingerprint", icon: <Hexagon size={16} /> },
    { href: "/interpretability", label: "Interpretability", icon: <Activity size={16} /> },
    { href: "/reproduction", label: "Reproduction", icon: <FileCode2 size={16} /> },
  ];

  return (
    <header className="border-b border-slate-800/80 bg-slate-950/80 backdrop-blur-xl fixed top-0 left-0 w-full z-50">
      <div className="max-w-6xl mx-auto px-6 h-16 flex items-center justify-between">
        <Link href="/" className="font-black tracking-tight text-white flex items-center gap-3 group">
          <div className="w-5 h-5 bg-gradient-to-tr from-blue-600 to-cyan-400 rounded-sm shadow-[0_0_15px_rgba(59,130,246,0.5)] group-hover:shadow-[0_0_25px_rgba(59,130,246,0.8)] transition-shadow duration-300"></div>
          <span className="bg-clip-text text-transparent bg-gradient-to-r from-white to-slate-400 text-sm sm:text-base truncate max-w-[200px] sm:max-w-none">
            ZERO-BLOCK DECONSTRUCTION
          </span>
        </Link>
        
        {/* Desktop Nav */}
        <nav className="hidden md:flex gap-1 text-sm font-medium">
          {links.map((link) => {
            const isActive = pathname === link.href;
            return (
              <Link 
                key={link.href} 
                href={link.href} 
                className={`flex items-center gap-2 px-4 py-2 rounded-full transition-all duration-300 ${
                  isActive 
                    ? "bg-slate-800/50 text-blue-400 shadow-[inset_0_1px_0_rgba(255,255,255,0.1)]" 
                    : "text-slate-400 hover:text-white hover:bg-slate-800/30"
                }`}
              >
                {link.icon}
                {link.label}
              </Link>
            );
          })}
        </nav>

        {/* Mobile Toggle */}
        <button 
          className="md:hidden text-slate-400 hover:text-white p-2"
          onClick={() => setIsOpen(!isOpen)}
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Mobile Nav */}
      <AnimatePresence>
        {isOpen && (
          <motion.nav 
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="md:hidden border-t border-slate-800 bg-slate-900/95 backdrop-blur overflow-hidden"
          >
            <div className="flex flex-col p-4 gap-2">
              {links.map((link) => (
                <Link 
                  key={link.href} 
                  href={link.href} 
                  onClick={() => setIsOpen(false)}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                    pathname === link.href 
                      ? "bg-blue-900/20 text-blue-400" 
                      : "text-slate-400 hover:text-white hover:bg-slate-800/50"
                  }`}
                >
                  {link.icon}
                  <span className="font-medium">{link.label}</span>
                </Link>
              ))}
            </div>
          </motion.nav>
        )}
      </AnimatePresence>
    </header>
  );
}
