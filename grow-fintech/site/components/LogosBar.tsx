export default function LogosBar() {
  const logos = Array.from({ length: 6 });

  return (
    <div className="border-t border-b border-white/[0.06] bg-bg2 py-10">
      <div className="max-w-6xl mx-auto px-6">
        <p className="text-center text-[11px] font-bold text-gray2 uppercase tracking-[3px] mb-8">
          Trusted by fintech teams across payments, lending, crypto & embedded finance
        </p>
        <div className="flex flex-wrap justify-center items-center gap-10">
          {logos.map((_, i) => (
            <div
              key={i}
              className="h-7 w-[100px] bg-white/[0.06] rounded"
            />
          ))}
        </div>
      </div>
    </div>
  );
}
