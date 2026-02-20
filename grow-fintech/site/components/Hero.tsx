export default function Hero() {
  return (
    <section className="relative min-h-screen flex items-center pt-[72px] overflow-hidden">
      {/* Background radial glow */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/2 -translate-x-1/2 w-[700px] h-[700px] bg-accent/[0.06] rounded-full blur-[120px]" />
        <div className="absolute top-0 right-0 bottom-0 w-1/2 opacity-40"
          style={{
            backgroundImage:
              "repeating-linear-gradient(0deg,transparent,transparent 59px,rgba(255,255,255,0.025) 60px),repeating-linear-gradient(90deg,transparent,transparent 59px,rgba(255,255,255,0.025) 60px)",
          }}
        />
      </div>

      <div className="relative z-10 max-w-6xl mx-auto px-6 py-24">
        {/* Badge */}
        <div className="inline-flex items-center gap-2 bg-accent/10 border border-accent/20 text-accent rounded-full px-4 py-2 text-[12px] font-bold uppercase tracking-[2px] mb-8">
          <span className="w-1.5 h-1.5 bg-accent rounded-full pulse" />
          Fintech-Only Marketing Agency
        </div>

        {/* H1 */}
        <h1 className="font-display font-extrabold text-[clamp(52px,8vw,96px)] leading-[1.02] tracking-[-0.05em] mb-6 max-w-[760px]">
          We Grow{" "}
          <span className="text-accent">Fintechs.</span>
          <br />
          Profitably.
        </h1>

        {/* Subhead */}
        <p className="text-[clamp(17px,2vw,21px)] text-gray1 leading-[1.75] max-w-[580px] mb-10">
          Acquisition that scales. Demand that converts. Growth measured in
          revenue. not reports.
        </p>

        {/* CTAs */}
        <div className="flex flex-wrap gap-4 mb-14">
          <a
            href="#cta"
            className="inline-flex items-center gap-2 bg-accent text-bg font-bold text-[15px] px-8 py-4 rounded-xl hover:opacity-90 active:scale-95 transition-all shadow-lg shadow-accent/20"
          >
            Book a Strategy Call
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </a>
          <a
            href="#cta"
            className="inline-flex items-center gap-2 border border-white/10 text-white font-semibold text-[15px] px-8 py-4 rounded-xl hover:border-accent/40 hover:text-accent transition-all"
          >
            Get a Free Growth Audit
          </a>
        </div>

        {/* Trust bar */}
        <div className="flex flex-wrap gap-6">
          {[
            "7+ years fintech-only",
            "CAC-positive or we say so",
            "AI-ready growth strategies",
          ].map((item) => (
            <div key={item} className="flex items-center gap-2.5 text-[13px] text-gray1 font-medium">
              <span className="w-5 h-5 rounded-full bg-accent/10 border border-accent/20 flex items-center justify-center text-accent text-[10px] font-black">
                ✓
              </span>
              {item}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
