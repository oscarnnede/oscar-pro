import { useEffect, useState, useCallback } from "react";
import { api } from "./api";
import ExpenseForm from "./components/ExpenseForm";
import ExpenseTable from "./components/ExpenseTable";
import CategorySummary from "./components/CategorySummary";

const now = new Date();

export default function App() {
  const [categories, setCategories] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [summary, setSummary] = useState(null);
  const [newCategory, setNewCategory] = useState("");
  const [loading, setLoading] = useState(true);
  const [err, setErr] = useState(null);

  const month = now.getMonth() + 1;
  const year = now.getFullYear();

  const refresh = useCallback(async () => {
    try {
      const [cats, exp, sum] = await Promise.all([
        api.listCategories(),
        api.listExpenses({ month, year }),
        api.monthlySummary(month, year),
      ]);
      setCategories(cats);
      setExpenses(exp);
      setSummary(sum);
      setErr(null);
    } catch (e) {
      setErr(e.message);
    } finally {
      setLoading(false);
    }
  }, [month, year]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const addExpense = async (data) => {
    await api.createExpense(data);
    await refresh();
  };

  const removeExpense = async (id) => {
    await api.deleteExpense(id);
    await refresh();
  };

  const addCategory = async (e) => {
    e.preventDefault();
    if (!newCategory.trim()) return;
    const palette = ["#2f6f5e", "#b5563c", "#c99a3d", "#3b5a8a", "#7a5a9c"];
    await api.createCategory({
      name: newCategory.trim(),
      color: palette[categories.length % palette.length],
    });
    setNewCategory("");
    await refresh();
  };

  const monthLabel = now.toLocaleDateString("en-US", { month: "long", year: "numeric" });

  return (
    <div className="mx-auto min-h-screen max-w-5xl px-4 py-10 sm:px-8">
      <header className="mb-10 border-b border-ink/15 pb-6">
        <p className="font-mono text-xs uppercase tracking-widest text-ink/40">{monthLabel}</p>
        <h1 className="font-display text-4xl font-semibold text-ink">Ledger</h1>
        <p className="mt-1 text-sm text-ink/50">A quiet place to keep track of where it goes.</p>
      </header>

      {loading && <p className="text-sm text-ink/40">Loading\u2026</p>}
      {err && (
        <p className="mb-6 border border-rust/30 bg-rust/5 p-3 text-sm text-rust">
          Couldn't reach the API: {err}
        </p>
      )}

      {!loading && !err && (
        <div className="grid grid-cols-1 gap-8 lg:grid-cols-[1.1fr_1.4fr]">
          <div className="space-y-6">
            <ExpenseForm categories={categories} onSubmit={addExpense} />

            <form onSubmit={addCategory} className="flex gap-2 border border-ink/15 bg-white/60 p-4">
              <input
                className="flex-1 border border-ink/20 bg-paper px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-ledger"
                placeholder="New category (e.g. Groceries)"
                value={newCategory}
                onChange={(e) => setNewCategory(e.target.value)}
              />
              <button
                type="submit"
                className="border border-ink/20 px-3 py-2 text-sm text-ink/70 hover:bg-ink/5"
              >
                Add
              </button>
            </form>

            <CategorySummary summary={summary} />
          </div>

          <div className="border border-ink/15 bg-white/60 p-5">
            <p className="mb-4 font-display text-lg text-ink/80">Entries</p>
            <ExpenseTable expenses={expenses} onDelete={removeExpense} />
          </div>
        </div>
      )}
    </div>
  );
}
