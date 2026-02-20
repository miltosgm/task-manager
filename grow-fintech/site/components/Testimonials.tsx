const testimonials = [
  {
    quote:
      "We'd tried two agencies before Grow Fintech. Both burned budget. These guys understood our unit economics from the first call. and actually cared about profitability, not just spend.",
    author: "Head of Growth",
    company: "B2B Payments Platform",
  },
  {
    quote:
      "For the first time, our marketing team could actually answer 'what's driving revenue?'. with data. The attribution clarity alone was worth the engagement.",
    author: "CMO",
    company: "Digital Lending Startup",
  },
  {
    quote:
      "The GEO strategy they built has us showing up in AI answers our competitors don't even know exist yet. It's a compounding advantage that keeps growing.",
    author: "Founder",
    company: "Embedded Finance Platform",
  },
];

export default function Testimonials() {
  return (
    <section className="py-28 bg-bg2">
      <div className="max-w-6xl mx-auto px-6">
        <div className="mb-14">
          <p className="text-[11px] font-extrabold text-accent uppercase tracking-[3px] mb-4">
            // What Clients Say
          </p>
          <h2 className="font-display font-extrabold text-[clamp(36px,5vw,60px)] leading-[1.08] tracking-[-0.04em]">
            Straight From<br />Our Clients
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {testimonials.map((t) => (
            <div
              key={t.author}
              className="bg-white/[0.03] border border-white/[0.07] rounded-2xl p-9 hover:border-accent/20 transition-colors flex flex-col"
            >
              <div className="text-accent text-[48px] font-serif leading-[0.6] mb-6 opacity-40">
                "
              </div>
              <p className="text-[15px] text-white/85 leading-[1.85] italic flex-1 mb-8">
                {t.quote}
              </p>
              <div>
                <div className="text-[14px] font-bold text-white">{t.author}</div>
                <div className="text-[13px] text-gray1 mt-1">{t.company}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
