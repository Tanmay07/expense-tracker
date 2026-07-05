import { useState } from 'react';
import { motion } from 'framer-motion';
import { Search, Filter, Download, Plus, MoreHorizontal, Loader2 } from 'lucide-react';
import { cn } from '../utils/cn';
import { useExpenses } from '../hooks/useData';

export function Expenses() {
  const [search, setSearch] = useState('');
  const { data: expenses, isLoading } = useExpenses();

  if (isLoading || !expenses) {
    return (
      <div className="flex items-center justify-center h-[50vh]">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    );
  }
  
  const filtered = expenses.filter(e => 
    e.merchant.toLowerCase().includes(search.toLowerCase()) || 
    e.category.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="max-w-7xl mx-auto space-y-6 h-full flex flex-col">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Expenses</h1>
          <p className="text-muted-foreground mt-1">Track, filter, and analyze your outgoing cash flow.</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 px-4 py-2 bg-secondary text-secondary-foreground text-sm font-medium rounded-md hover:bg-secondary/80 transition-colors">
            <Download className="w-4 h-4" />
            Export
          </button>
          <button className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground text-sm font-medium rounded-md hover:bg-primary/90 transition-colors">
            <Plus className="w-4 h-4" />
            Add Record
          </button>
        </div>
      </div>

      <div className="flex-1 rounded-xl border border-border bg-card flex flex-col overflow-hidden">
        <div className="p-4 border-b border-border flex flex-col sm:flex-row items-center justify-between gap-4 bg-secondary/10">
          <div className="relative w-full sm:w-72">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input 
              type="text"
              placeholder="Search merchants, categories..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-background border border-border rounded-md text-sm outline-none focus:border-blue-500 transition-colors"
            />
          </div>
          <button className="flex items-center gap-2 px-3 py-2 text-sm font-medium text-muted-foreground border border-border rounded-md hover:bg-secondary transition-colors w-full sm:w-auto justify-center">
            <Filter className="w-4 h-4" />
            Filters
          </button>
        </div>

        <div className="flex-1 overflow-auto">
          <table className="w-full text-sm text-left">
            <thead className="text-xs text-muted-foreground uppercase bg-secondary/30 sticky top-0 z-10 backdrop-blur-md">
              <tr>
                <th className="px-6 py-4 font-medium">Merchant</th>
                <th className="px-6 py-4 font-medium">Category</th>
                <th className="px-6 py-4 font-medium">Date</th>
                <th className="px-6 py-4 font-medium">Status</th>
                <th className="px-6 py-4 font-medium">Tags</th>
                <th className="px-6 py-4 font-medium text-right">Amount</th>
                <th className="px-6 py-4"></th>
              </tr>
            </thead>
            <tbody className="divide-y divide-border">
              {filtered.map((expense) => (
                <motion.tr 
                  key={expense.id}
                  initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                  className="hover:bg-secondary/20 transition-colors group"
                >
                  <td className="px-6 py-4 font-medium flex items-center gap-3">
                    <div className="w-8 h-8 rounded bg-secondary flex items-center justify-center text-xs">
                      {expense.merchant.charAt(0)}
                    </div>
                    {expense.merchant}
                  </td>
                  <td className="px-6 py-4 text-muted-foreground">{expense.category}</td>
                  <td className="px-6 py-4 text-muted-foreground">{expense.date}</td>
                  <td className="px-6 py-4">
                    <span className={cn(
                      "px-2 py-1 text-xs rounded-md",
                      expense.status === 'Cleared' ? "bg-emerald-500/10 text-emerald-500" : "bg-amber-500/10 text-amber-500"
                    )}>
                      {expense.status}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex gap-1 flex-wrap">
                      {expense.tags.map(tag => (
                        <span key={tag} className="px-2 py-0.5 text-[10px] uppercase tracking-wider bg-secondary text-secondary-foreground rounded">
                          {tag}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td className="px-6 py-4 text-right font-medium">
                    ${expense.amount.toFixed(2)}
                  </td>
                  <td className="px-6 py-4 text-right">
                    <button className="text-muted-foreground hover:text-foreground opacity-0 group-hover:opacity-100 transition-opacity">
                      <MoreHorizontal className="w-4 h-4" />
                    </button>
                  </td>
                </motion.tr>
              ))}
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={7} className="px-6 py-12 text-center text-muted-foreground">
                    No expenses found matching "{search}"
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
