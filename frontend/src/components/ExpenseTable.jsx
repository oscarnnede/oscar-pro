const fmt = (n) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD" }).format(n);

export default function ExpenseTable({ expenses, onDelete }) {
  if (expenses.length === 0) {
    return (
      <p className="border border-dashed border-ink/20 p-6 text-center text-sm text-ink/50">
        No entries yet this month. Add one on the left to start the ledger.
      </p>
    );
  }

  return (
    <table className="w-full border-collapse text-sm">
      <thead>
        <tr className="border-b border-ink/20 text-left text-xs uppercase tracking-wide text-ink/50">
          <th className="py-2">Date</th>
          <th className="py-2">Description</th>
          <th className="py-2">Category</th>
          <th className="py-2 text-right">Amount</th>
          <th className="py-2"></th>
        </tr>
      </thead>
      <tbody>
        {expenses.map((e) => (
          <tr key={e.id} className="border-b border-ink/10 hover:bg-ink/[0.03]">
            <td className="py-2 font-mono text-xs text-ink/60">{e.spent_on}</td>
            <td className="py-2">
              {e.description}
              {e.notes && <span className="ml-2 text-xs text-ink/40">{e.notes}</span>}
            </td>
            <td className="py-2">
              <span
                className="inline-block h-2 w-2 rounded-full align-middle"
                style={{ backgroundColor: e.category.color }}
              />
              <span className="ml-1.5 align-middle text-ink/70">{e.category.name}</span>
            </td>
            <td className="py-2 text-right font-mono">{fmt(e.amount)}</td>
            <td className="py-2 text-right">
              <button
                onClick={() => onDelete(e.id)}
                className="text-xs text-ink/30 hover:text-rust"
                aria-label={`Delete ${e.description}`}
              >
                remove
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
