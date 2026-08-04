const fmt = (n) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(n);

export default function CategorySummary({ summary }) {
  if (!summary) return null;

  return (
    <div className="border border-ink/15 bg-white/60 p-5">
      <div className="mb-4 flex items-baseline justify-between">
        <p className="font-display text-lg text-ink/80">This month</p>
        <p className="font-mono text-xl text-ink">{fmt(summary.total_spent)}</p>
      </div>
      <div className="space-y-3">
        {summary.by_category.map((c) => {
          const pct = c.monthly_budget ? Math.min(100, (c.total_spent / c.monthly_budget) * 100) : null;
          const over = c.monthly_budget && c.total_spent > c.monthly_budget;
          return (
            <div key={c.category_id}>
              <div className="mb-1 flex justify-between text-xs">
                <span className="text-ink/70">{c.category_name}</span>
                <span className="font-mono text-ink/60">
                  {fmt(c.total_spent)}
                  {c.monthly_budget ? ` / ${fmt(c.monthly_budget)}` : ""}
                </span>
              </div>
              {pct !== null && (
                <div className="h-1.5 w-full bg-ink/10">
                  <div
                    className="h-1.5"
                    style={{
                      width: `${pct}%`,
                      backgroundColor: over ? "#b5563c" : c.color,
                    }}
                  />
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
