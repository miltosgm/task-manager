const steps = [
  {
    num: "01",
    label: "Step 1",
    title: "Diagnose",
    desc: "We audit your current growth engine. paid, organic, funnel, messaging. No assumptions. Just data and honest assessment.",
  },
  {
    num: "02",
    label: "Step 2",
    title: "Design",
    desc: "We build a strategy grounded in data, not best guesses. Clear priorities, clear rationale, clear next steps.",
  },
  {
    num: "03",
    label: "Step 3",
    title: "Execute & Optimise",
    desc: "We launch, test, and iterate. constantly improving against the metrics that actually matter to your business.",
  },
  {
    num: "04",
    label: "Step 4",
    title: "Scale What Works",
    desc: "Double down on profitable channels. Kill what doesn't perform. Repeat until growth is predictable and compound.",
  },
];

export default function Process() {
  return (
    <section id="process" className="py-28">
      <div className="max-w-6xl mx-auto px-6">
        <div className="mb-14">
          <p className="text-[11px] font-extrabold text-accent uppercase tracking-[3px] mb-4">
            // How We Work
          </p>
          <h2 className="font-display font-extrabold text-[clamp(36px,5vw,60px)] leading-[1.08] tracking-[-0.04em] mb-4">
            No Onboarding Fog.<br />No 90-Day Discovery.
          </h2>
          <p className="text-[18px] text-gray1 leading-[1.75] max-w-[500px]">
            Just a clear process that delivers outputs before most agencies have
            finished their kickoff deck.
          </p>
        </div>

        {/* Steps */}
        <div className="grid grid-cols-1 md:grid-cols-4 divide-y md:divide-y-0 md:divide-x divide-white/[0.07] border border-white/[0.07] rounded-2xl overflow-hidden">
          {steps.map((step) => (
            <div
              key={step.num}
              className="p-8 hover:bg-accent/[0.03] transition-colors group"
            >
              <div className="font-display font-extrabold text-[52px] text-accent/15 leading-none mb-4">
                {step.num}
              </div>
              <div className="text-[11px] font-bold text-accent uppercase tracking-[2px] mb-3">
                {step.label}
              </div>
              <h3 className="text-[17px] font-bold text-white mb-3 group-hover:text-accent transition-colors">
                {step.title}
              </h3>
              <p className="text-[13px] text-gray1 leading-[1.75]">{step.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
