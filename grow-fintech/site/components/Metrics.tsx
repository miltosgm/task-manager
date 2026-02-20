const metrics = [
  { num: "7+", label: "Years working exclusively\nwith fintech companies" },
  { num: "$0", label: "Compliance violations\nacross all campaigns to date" },
  { num: "3x", label: "Average CAC reduction\nvia our SEO & GEO programs" },
  { num: "B2B+", label: "Serves both B2B and B2C\nfintechs with dedicated strategies" },
];

export default function Metrics() {
  return (
    <section id="results" className="py-28 bg-accent">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="mb-14 max-w-[600px]">
          <p className="text-[11px] font-extrabold text-bg/50 uppercase tracking-[3px] mb-4">
            // How We Measure Growth
          </p>
          <h2 className="font-display font-extrabold text-[clamp(36px,5vw,60px)] leading-[1.08] tracking-[-0.04em] text-bg mb-5">
            We don't optimise for<br />
            reports nobody reads.
          </h2>
          <p className="text-[17px] text-bg/70 leading-[1.75]">
            We care about CAC, LTV, conversion rates, pipeline quality, and
            revenue contribution. If a channel can't prove its value, it doesn't
            get scaled.{" "}
            <strong className="text-bg font-bold">Simple as that.</strong>
          </p>
        </div>

        {/* Metrics grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-5">
          {metrics.map((m) => (
            <div key={m.num} className="bg-bg/10 rounded-2xl p-8 text-center">
              <div className="font-display font-extrabold text-[clamp(44px,6vw,64px)] text-bg leading-none tracking-[-0.05em] mb-3">
                {m.num}
              </div>
              <div className="text-[13px] text-bg/65 font-medium leading-[1.5] whitespace-pre-line">
                {m.label}
              </div>
            </div>
          ))}
        </div>

        <p className="text-[11px] text-bg/40 italic text-center">
          Results vary by client. Past performance doesn't guarantee future results.
        </p>
      </div>
    </section>
  );
}
