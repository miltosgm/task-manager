const industries = [
  { icon: "🏦", name: "Neobanks & Digital Banking" },
  { icon: "💳", name: "Payments & Money Movement" },
  { icon: "🏠", name: "Lending & Credit Platforms" },
  { icon: "₿", name: "Crypto & Web3" },
  { icon: "🔌", name: "Embedded Finance & BaaS" },
  { icon: "🛡️", name: "Insurtech" },
  { icon: "📈", name: "Wealthtech & Investment" },
  { icon: "🏗️", name: "B2B Fintech Infrastructure" },
];

export default function Industries() {
  return (
    <section id="industries" className="py-28 bg-bg2">
      <div className="max-w-6xl mx-auto px-6">
        <div className="mb-14">
          <p className="text-[11px] font-extrabold text-accent uppercase tracking-[3px] mb-4">
            // Industries
          </p>
          <h2 className="font-display font-extrabold text-[clamp(36px,5vw,60px)] leading-[1.08] tracking-[-0.04em] mb-4">
            We Know Your Category
          </h2>
          <p className="text-[18px] text-gray1 leading-[1.75] max-w-[500px]">
            We've built campaigns inside every major fintech vertical. B2B and
            B2C, regulated and emerging.
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {industries.map((ind) => (
            <div
              key={ind.name}
              className="bg-white/[0.03] border border-white/[0.07] rounded-2xl p-6 hover:border-accent/35 hover:bg-accent/[0.03] transition-all cursor-default group"
            >
              <div className="text-[28px] mb-3">{ind.icon}</div>
              <div className="text-[14px] font-semibold text-white group-hover:text-accent transition-colors leading-snug">
                {ind.name}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
