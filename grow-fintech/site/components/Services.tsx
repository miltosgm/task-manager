const services = [
  {
    num: "01",
    icon: "🚀",
    title: "Paid Acquisition for Fintech",
    desc: "Performance campaigns across Google, LinkedIn, and Meta. built around your unit economics, not a generic media plan. Every campaign is designed to answer one question: can this scale profitably?",
    tag: null,
  },
  {
    num: "02",
    icon: "🤖",
    title: "GEO. Generative Engine Optimization",
    desc: "Search has changed. Buyers find products through AI answers now. not just search results. We help fintech brands get cited in ChatGPT, Perplexity, and Google AI Overviews, and build signals that influence LLM visibility at scale.",
    tag: "New",
  },
  {
    num: "03",
    icon: "💡",
    title: "Growth Strategy & GTM",
    desc: "Before scaling spend, we align ICP & segmentation, messaging and positioning, funnel design, and channel priorities. Because scaling a broken GTM doesn't fix it. it just burns cash faster.",
    tag: null,
  },
  {
    num: "04",
    icon: "⚡",
    title: "B2B Fintech Demand Generation",
    desc: "If you sell to businesses or institutions, clicks alone won't cut it. We build demand engines that turn attention into qualified conversations, real pipeline, and revenue you can forecast.",
    tag: null,
  },
  {
    num: "05",
    icon: "🧠",
    title: "Fractional CMO / Growth Advisory",
    desc: "Sometimes the problem isn't execution. it's decision-making. We work with founders and leadership teams as a fractional CMO, helping you prioritise the right channels, avoid expensive mistakes, and move faster with confidence.",
    tag: null,
  },
];

export default function Services() {
  return (
    <section id="services" className="py-28">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="mb-14">
          <p className="text-[11px] font-extrabold text-accent uppercase tracking-[3px] mb-4">
            // What We Do
          </p>
          <h2 className="font-display font-extrabold text-[clamp(36px,5vw,64px)] leading-[1.08] tracking-[-0.04em] mb-4">
            What We Do <br />
            And What We Don't
          </h2>
          <p className="text-[18px] text-gray1 leading-[1.75] max-w-[540px]">
            We work on the problems that actually move the needle. Not a long list
            of services. a focused set of things we're genuinely good at.
          </p>
        </div>

        {/* Services grid. 2 col top, 3 bottom */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {services.map((s, i) => (
            <div
              key={s.num}
              className={`relative group bg-white/[0.03] border rounded-2xl p-8 transition-all duration-200 hover:-translate-y-1 cursor-default ${
                s.tag
                  ? "border-accent/30 bg-accent/[0.03] hover:border-accent/50"
                  : "border-white/[0.07] hover:border-accent/25"
              } ${i === 4 ? "md:col-span-2" : ""}`}
            >
              {/* Tag */}
              {s.tag && (
                <span className="absolute top-6 right-6 bg-accent text-bg text-[11px] font-black uppercase px-2.5 py-1 rounded-full tracking-wide">
                  {s.tag}
                </span>
              )}

              {/* Icon + num row */}
              <div className="flex items-center gap-4 mb-6">
                <div
                  className={`w-12 h-12 rounded-xl flex items-center justify-center text-xl ${
                    s.tag
                      ? "bg-accent/20 border border-accent/30"
                      : "bg-white/[0.06] border border-white/[0.08]"
                  }`}
                >
                  {s.icon}
                </div>
                <span
                  className={`text-[11px] font-bold uppercase tracking-[2px] ${
                    s.tag ? "text-accent" : "text-gray2"
                  }`}
                >
                  {s.num}
                </span>
              </div>

              <h3 className="text-[19px] font-bold text-white mb-3 group-hover:text-accent transition-colors">
                {s.title}
              </h3>
              <p className="text-[14px] text-gray1 leading-[1.75]">{s.desc}</p>

              <div className="mt-6 inline-flex items-center gap-2 text-[13px] text-gray2 font-semibold group-hover:text-accent transition-colors">
                Learn more
                <svg width="14" height="14" viewBox="0 0 14 14" fill="none" className="group-hover:translate-x-1 transition-transform">
                  <path d="M2 7h10M8 3l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                </svg>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
