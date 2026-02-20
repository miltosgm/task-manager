const partners = [
  {
    icon: "🚀",
    title: "Fintech founders",
    desc: "Building their first real growth engine and tired of generic agencies that don't understand the product or the buyer.",
  },
  {
    icon: "📊",
    title: "Heads of Growth",
    desc: "Who've inherited broken funnels and need clarity. fast. We audit, diagnose, and prioritise within weeks, not quarters.",
  },
  {
    icon: "🏦",
    title: "B2B fintechs",
    desc: "That sell to banks, businesses, or institutions and need more than clicks. Real demand generation built for long sales cycles.",
  },
  {
    icon: "🎯",
    title: "Growth-stage teams",
    desc: "Who've been burned by generic agencies and want specialists. Teams that care about CAC, LTV, and revenue. not impressions.",
  },
];

export default function WhoWePartnerWith() {
  return (
    <section className="py-28">
      <div className="max-w-6xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-start">
          {/* Left */}
          <div>
            <p className="text-[11px] font-extrabold text-accent uppercase tracking-[3px] mb-4">
              // Who We Partner With
            </p>
            <h2 className="font-display font-extrabold text-[clamp(36px,5vw,56px)] leading-[1.08] tracking-[-0.04em] mb-6">
              We Work With the<br />Teams That Care<br />About Performance
            </h2>
            <p className="text-[17px] text-gray1 leading-[1.8] mb-8">
              Not every fintech is the right fit. We work best with teams that
              have a real product, a clear ICP, and the ambition to scale
              profitably. not just grow headcount.
            </p>
            <a
              href="#cta"
              className="inline-flex items-center gap-2 bg-accent text-bg font-bold text-[15px] px-8 py-4 rounded-xl hover:opacity-90 transition-all"
            >
              See If We're a Fit →
            </a>
          </div>

          {/* Right */}
          <div className="space-y-4">
            {partners.map((p) => (
              <div
                key={p.title}
                className="flex gap-5 items-start p-6 bg-white/[0.03] border border-white/[0.07] rounded-2xl hover:border-accent/30 hover:bg-accent/[0.02] transition-all group"
              >
                <div className="w-11 h-11 flex-shrink-0 bg-accent/10 rounded-xl flex items-center justify-center text-xl">
                  {p.icon}
                </div>
                <div>
                  <h3 className="text-[16px] font-bold text-white mb-2 group-hover:text-accent transition-colors">
                    {p.title}
                  </h3>
                  <p className="text-[13px] text-gray1 leading-[1.7]">{p.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </section>
  );
}
