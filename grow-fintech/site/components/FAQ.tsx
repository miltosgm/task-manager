"use client";
import { useState } from "react";

const faqs = [
  {
    q: "Do you work with early-stage fintechs or only growth-stage?",
    a: "Both. We work with seed-stage fintechs building their first real growth engine and Series B+ companies scaling into new markets. The engagement structure differs, but the depth of focus stays the same.",
  },
  {
    q: "What does GEO (Generative Engine Optimization) actually mean?",
    a: "It's the practice of getting your fintech brand cited and recommended by AI tools. ChatGPT, Perplexity, Google AI Overviews, and others. As buyers increasingly use AI to discover and evaluate products, appearing in those answers is becoming as important as ranking on Google. We build the content, structure, and signals that make that happen.",
  },
  {
    q: "How do you handle financial advertising compliance?",
    a: "It's built into our process from day one. Every campaign asset we produce is reviewed against applicable financial advertising regulations before going live. We've maintained a clean compliance record across all client campaigns.",
  },
  {
    q: "What's your typical engagement model?",
    a: "We work on monthly retainers for ongoing growth partnerships and project-based engagements for specific initiatives. GTM launches, audits, GEO programs. Minimum engagement is typically 3 months.",
  },
  {
    q: "What if I just want an honest view of what's holding us back?",
    a: "That's exactly what our free growth audit is for. We'll look at your current channels, funnel, messaging, and positioning. and tell you honestly what's working, what isn't, and what we'd do about it. Even if the answer isn't 'spend more.'",
  },
];

export default function FAQ() {
  const [open, setOpen] = useState<number | null>(null);

  return (
    <section className="py-28">
      <div className="max-w-6xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-start">
          {/* Left */}
          <div className="sticky top-28">
            <p className="text-[11px] font-extrabold text-accent uppercase tracking-[3px] mb-4">
              // FAQ
            </p>
            <h2 className="font-display font-extrabold text-[clamp(36px,5vw,52px)] leading-[1.08] tracking-[-0.04em] mb-6">
              Common<br />Questions
            </h2>
            <p className="text-[17px] text-gray1 leading-[1.8] mb-8">
              Everything you need to know before working with us. Still have
              something you need answered? Book a call. 30 minutes, no pitch.
            </p>
            <a
              href="#cta"
              className="inline-flex items-center gap-2 border border-accent/30 text-accent font-bold text-[14px] px-6 py-3 rounded-xl hover:bg-accent/10 transition-all"
            >
              Book a Call →
            </a>
          </div>

          {/* Accordion */}
          <div>
            {faqs.map((faq, i) => (
              <div key={i} className="border-b border-white/[0.07]">
                <button
                  onClick={() => setOpen(open === i ? null : i)}
                  className="w-full text-left py-6 flex items-start justify-between gap-6 group"
                >
                  <span className="text-[16px] font-semibold text-white group-hover:text-accent transition-colors leading-snug">
                    {faq.q}
                  </span>
                  <span
                    className={`flex-shrink-0 w-7 h-7 rounded-full border border-white/10 flex items-center justify-center text-accent text-[20px] font-thin mt-0.5 transition-all ${
                      open === i ? "rotate-45 border-accent/40" : ""
                    }`}
                  >
                    +
                  </span>
                </button>
                {open === i && (
                  <p className="text-[14px] text-gray1 leading-[1.8] pb-6 pr-10">
                    {faq.a}
                  </p>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
