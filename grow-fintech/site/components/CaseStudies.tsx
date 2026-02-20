const cases = [
  {
    tag: "Payments · B2B",
    stat: "+38%",
    statDesc: "Qualified demo requests in 90 days",
    title: "Payments Startup. B2B",
    strategy: "LinkedIn ABM + compliance-reviewed landing pages + full-funnel conversion rate optimisation.",
    featured: true,
  },
  {
    tag: "Neobank · B2C",
    stat: "3.2x",
    statDesc: "CAC reduction via SEO & GEO program",
    title: "Neobank. Consumer",
    strategy: "Long-form fintech content + GEO signals + landing page conversion optimisation.",
    featured: false,
  },
  {
    tag: "Embedded Finance · B2B",
    stat: "1,200",
    statDesc: "MQL/month from 0 in 6 months",
    title: "Embedded Finance Platform",
    strategy: "Full-funnel paid media + lifecycle nurture + revenue attribution modeling.",
    featured: false,
  },
];

export default function CaseStudies() {
  return (
    <section id="cases" className="py-28 bg-bg2">
      <div className="max-w-6xl mx-auto px-6">
        <div className="mb-14">
          <p className="text-[11px] font-extrabold text-accent uppercase tracking-[3px] mb-4">
            // Results
          </p>
          <h2 className="font-display font-extrabold text-[clamp(36px,5vw,60px)] leading-[1.08] tracking-[-0.04em] mb-4">
            Work That Speaks<br />for Itself
          </h2>
          <p className="text-[14px] text-gray2 italic">
            Placeholder results. real client metrics added on engagement.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
          {cases.map((c) => (
            <div
              key={c.title}
              className="bg-white/[0.03] border border-white/[0.07] rounded-2xl overflow-hidden hover:border-accent/30 transition-all hover:-translate-y-1 group"
            >
              {/* Header */}
              <div className="p-8 bg-gradient-to-br from-accent/[0.06] to-accent2/[0.04] border-b border-white/[0.07]">
                <div className="text-[11px] font-bold text-accent uppercase tracking-[2px] mb-3">
                  {c.tag}
                </div>
                <div className="font-display font-extrabold text-[clamp(44px,7vw,56px)] text-white leading-none tracking-[-0.05em]">
                  {c.stat}
                </div>
                <div className="text-[13px] text-gray1 mt-2">{c.statDesc}</div>
              </div>

              {/* Body */}
              <div className="p-8">
                <h3 className="text-[17px] font-bold text-white mb-3 group-hover:text-accent transition-colors">
                  {c.title}
                </h3>
                <p className="text-[13px] text-gray1 leading-[1.7] mb-5">
                  {c.strategy}
                </p>
                <a
                  href="#"
                  className="inline-flex items-center gap-2 text-[13px] text-accent font-bold hover:gap-3 transition-all"
                >
                  Read Case Study
                  <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                    <path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                  </svg>
                </a>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
