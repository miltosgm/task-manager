export default function FinalCTA() {
  return (
    <section id="cta" className="py-28 bg-bg2">
      <div className="max-w-6xl mx-auto px-6">
        <div className="relative rounded-3xl p-12 md:p-20 text-center overflow-hidden border border-accent/20 bg-gradient-to-br from-accent/[0.07] to-accent2/[0.04]">
          {/* Glow */}
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[500px] h-[300px] bg-accent/10 blur-[80px] rounded-full pointer-events-none" />

          <div className="relative z-10">
            <p className="text-[11px] font-extrabold text-accent uppercase tracking-[3px] mb-6 inline-block">
              // Get Started
            </p>
            <h2 className="font-display font-extrabold text-[clamp(38px,6vw,72px)] leading-[1.05] tracking-[-0.05em] mb-5">
              Want an Honest View of<br />
              What's Holding You Back?
            </h2>
            <p className="text-[18px] text-gray1 leading-[1.75] max-w-[540px] mx-auto mb-3">
              Book a 30-minute strategy call. We'll tell you exactly what's
              working, what isn't, and what to do about it.
            </p>
            <p className="text-[22px] md:text-[26px] font-bold text-accent mb-10">
              Even if the answer isn't "spend more."
            </p>

            <div className="flex flex-wrap gap-4 justify-center mb-5">
              <a
                href="https://calendly.com"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-accent text-bg font-bold text-[16px] px-10 py-4 rounded-xl hover:opacity-90 active:scale-95 transition-all shadow-lg shadow-accent/25"
              >
                Book a Strategy Call →
              </a>
              <a
                href="#cta"
                className="inline-flex items-center gap-2 border border-white/15 text-white font-semibold text-[16px] px-10 py-4 rounded-xl hover:border-accent/40 hover:text-accent transition-all"
              >
                Get a Free Growth Audit
              </a>
            </div>

            <p className="text-[13px] text-gray2">
              30 minutes. No pitch deck. Just straight talk about your growth.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}
