import { useState } from "react";

const today = () => new Date().toISOString().slice(0, 10);

export default function ExpenseForm({ categories, onSubmit }) {
  const [form, setForm] = useState({
    description: "",
    amount: "",
    spent_on: today(),
    category_id: categories[0]?.id || "",
    notes: "",
  });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);

  const update = (field) => (e) => setForm((f) => ({ ...f, [field]: e.target.value }));

  const submit = async (e) => {
    e.preventDefault();
    if (!form.description || !form.amount || !form.category_id) return;
    setBusy(true);
    setError(null);
    try {
      await onSubmit({ ...form, amount: parseFloat(form.amount) });
      setForm((f) => ({ ...f, description: "", amount: "", notes: "" }));
    } catch (err) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <form onSubmit={submit} className="border border-ink/15 bg-white/60 p-5">
      <p className="mb-4 font-display text-lg text-ink/80">Log an entry</p>
      {error && <p className="mb-3 text-sm text-rust">{error}</p>}
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <input
          className="col-span-2 border border-ink/20 bg-paper px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ledger"
          placeholder="What was it for?"
          value={form.description}
          onChange={update("description")}
          required
        />
        <input
          type="number"
          step="0.01"
          min="0"
          className="border border-ink/20 bg-paper px-3 py-2 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-ledger"
          placeholder="Amount"
          value={form.amount}
          onChange={update("amount")}
          required
        />
        <input
          type="date"
          className="border border-ink/20 bg-paper px-3 py-2 font-mono text-sm focus:outline-none focus:ring-2 focus:ring-ledger"
          value={form.spent_on}
          onChange={update("spent_on")}
          required
        />
        <select
          className="col-span-2 border border-ink/20 bg-paper px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ledger sm:col-span-1"
          value={form.category_id}
          onChange={update("category_id")}
          required
        >
          {categories.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>
        <input
          className="col-span-2 border border-ink/20 bg-paper px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ledger sm:col-span-1"
          placeholder="Notes (optional)"
          value={form.notes}
          onChange={update("notes")}
        />
      </div>
      <button
        type="submit"
        disabled={busy || categories.length === 0}
        className="mt-4 bg-ledger px-4 py-2 text-sm font-medium text-paper transition hover:bg-ledger/90 disabled:opacity-50"
      >
        {busy ? "Saving\u2026" : "Add entry"}
      </button>
      {categories.length === 0 && (
        <p className="mt-2 text-xs text-ink/50">Add a category first.</p>
      )}
    </form>
  );
}
