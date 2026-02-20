const pains = [
  {
    icon: "🔥",
    title: "Burning paid budget without CAC guardrails",
    desc: "Spending aggressively on paid media with no clear cost-per-acquisition control. and wondering why growth stalls quarter after quarter.",
  },
  {
    icon: "📉",
    title: "Running SEO playbooks built for 2019",
    desc: "While your buyers increasingly find products through AI answers. channels most fintechs aren't showing up in yet.",
  },
  {
    icon: "🎯",
    title: "Scaling channels without a real demand engine",
    desc: "Throwing paid media at unclear positioning is the fastest way to burn budget. Channels don't fix broken GTMs.",
  },
  {
    icon: "🤷",
    title: "Working with agencies who don't know fintech",
    desc: "Optimising for clicks when you need qualified pipeline, unit economics, and revenue you can actually forecast.",
  },
];

export default function Problem() {
  return (
    <section id="problem" className="py-28 bg-bg2">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="mb-14">
          <p className="text-[11px] font-extrabold text-accent uppercase tracking-[3px] mb-4">
            // The Problem
          </p>
          <h2 className="font-display font-extrabold text-[clamp(36px,5vw,64px)] leading-[1.08] tracking-[-0.04em] mb-4">
            Sound familiar?
          </h2>
          <p className="text-[18px] text-gray1 leading-[1.75] max-w-[540px]">
            Too many fintechs are burning budget on the wrong channels, with
            agencies that don't understand fintech economics or buyer journeys.
          </p>
        </div>

        {/* Pain cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-10">
          {pains.map((p) => (
            <div
              key={p.title}
              className="bg-white/[0.03] border border-white/[0.07] rounded-2xl p-8 hover:border-accent/30 transition-colors group"
            >
              <div className="text-3xl mb-5">{p.icon}</div>
              <h3 className="text-[17px] font-bold text-white mb-3 group-hover:text-accent transition-colors">
                {p.title}
              </h3>
              <p className="text-[14px] text-gray1 leading-[1.75]">{p.desc}</p>
            </div>
          ))}
        </div>

        {/* Bridge */}
        <div className="rounded-2xl p-10 md:p-12 text-center bg-gradient-to-br from-accent/[0.08] to-accent2/[0.05] border border-accent/20">
          <p className="text-[20px] md:text-[24px] font-bold text-white leading-[1.5]">
            We fix that.{" "}
            <span className="text-accent">Without the excuses.</span>{" "}
            <span className="text-gray1 font-normal">
              7+ years working exclusively with fintech teams. from early
              traction to Series B scale.
            </span>
          </p>
        </div>
      </div>
    </section>
  );
}
