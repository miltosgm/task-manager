"use client";
import { useState, useEffect } from "react";

export default function Nav() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-bg/95 backdrop-blur-xl border-b border-white/[0.06] shadow-2xl"
          : "bg-transparent"
      }`}
    >
      <div className="max-w-6xl mx-auto px-6 h-[72px] flex items-center justify-between">
        {/* Logo */}
        <a href="/" className="flex items-center gap-1">
          <span className="font-display font-extrabold text-[20px] tracking-tight text-white">
            GROW
          </span>
          <span className="font-display font-extrabold text-[20px] tracking-tight text-accent">
            .FINTECH
          </span>
        </a>

        {/* Links */}
        <div className="hidden md:flex items-center gap-8">
          {["Services", "Industries", "Results", "About"].map((l) => (
            <a
              key={l}
              href={`#${l.toLowerCase()}`}
              className="text-[14px] font-medium text-gray1 hover:text-white transition-colors"
            >
              {l}
            </a>
          ))}
        </div>

        {/* CTA */}
        <a
          href="#cta"
          className="bg-accent text-bg font-bold text-[14px] px-5 py-2.5 rounded-lg hover:opacity-90 active:scale-95 transition-all"
        >
          Book a Strategy Call
        </a>
      </div>
    </nav>
  );
}
