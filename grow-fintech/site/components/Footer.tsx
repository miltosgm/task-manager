const services = [
  "Paid Acquisition",
  "GEO / AI Optimization",
  "Growth Strategy & GTM",
  "B2B Demand Generation",
  "Fractional CMO",
];

const industries = [
  "Neobanks",
  "Payments",
  "Lending",
  "Crypto & Web3",
  "Embedded Finance",
  "Insurtech",
];

const company = ["About", "Work", "Blog", "Careers", "Contact"];

export default function Footer() {
  return (
    <footer className="bg-bg border-t border-white/[0.06] pt-16 pb-10">
      <div className="max-w-6xl mx-auto px-6">
        {/* Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-10 md:gap-16 mb-14">
          {/* Brand */}
          <div className="col-span-2 md:col-span-1">
            <div className="font-display font-extrabold text-[22px] tracking-tight mb-4">
              <span className="text-white">GROW</span>
              <span className="text-accent">.FINTECH</span>
            </div>
            <p className="text-[14px] text-gray1 leading-[1.75] max-w-[220px]">
              The growth agency for fintech. Revenue-obsessed, fintech-native,
              AI-ready.
            </p>
          </div>

          {/* Services */}
          <div>
            <h4 className="text-[11px] font-bold text-gray2 uppercase tracking-[2px] mb-5">
              Services
            </h4>
            <ul className="space-y-3">
              {services.map((s) => (
                <li key={s}>
                  <a
                    href="#services"
                    className="text-[14px] text-gray1 hover:text-accent transition-colors"
                  >
                    {s}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Industries */}
          <div>
            <h4 className="text-[11px] font-bold text-gray2 uppercase tracking-[2px] mb-5">
              Industries
            </h4>
            <ul className="space-y-3">
              {industries.map((i) => (
                <li key={i}>
                  <a
                    href="#industries"
                    className="text-[14px] text-gray1 hover:text-accent transition-colors"
                  >
                    {i}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Company */}
          <div>
            <h4 className="text-[11px] font-bold text-gray2 uppercase tracking-[2px] mb-5">
              Company
            </h4>
            <ul className="space-y-3">
              {company.map((c) => (
                <li key={c}>
                  <a
                    href="#"
                    className="text-[14px] text-gray1 hover:text-accent transition-colors"
                  >
                    {c}
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="border-t border-white/[0.06] pt-8 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <p className="text-[13px] text-gray2">
            © 2025 Grow Fintech Ltd. All rights reserved.{" "}
            <span className="text-accent">grow-fintech.io</span>
          </p>
          <p className="text-[11px] text-gray2/60 italic max-w-[440px] text-right">
            Marketing results vary by client. Past performance doesn't guarantee
            future results. Nothing on this site constitutes financial advice.
          </p>
        </div>
      </div>
    </footer>
  );
}
