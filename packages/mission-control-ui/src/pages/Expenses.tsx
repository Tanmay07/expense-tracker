import { useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Search, Filter, Download, Plus, MoreHorizontal, Loader2, UploadCloud, Receipt, X } from 'lucide-react';
import { useVirtualizer } from '@tanstack/react-virtual';
import { cn } from '../utils/cn';
import { useExpenses } from '../hooks/useData';

export function Expenses() {
  const [search, setSearch] = useState('');
  const [showUploader, setShowUploader] = useState(false);
  const { data: expenses, isLoading } = useExpenses();
  const parentRef = useRef<HTMLDivElement>(null);

  const filtered = (expenses || []).filter(e => 
    e.merchant.toLowerCase().includes(search.toLowerCase()) || 
    e.category.toLowerCase().includes(search.toLowerCase())
  );

  const rowVirtualizer = useVirtualizer({
    count: filtered.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 64, // estimated row height
    overscan: 5,
  });

  if (isLoading || !expenses) {
    return (
      <div className="flex items-center justify-center h-[50vh]">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6 h-full flex flex-col">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 shrink-0">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Expenses</h1>
          <p className="text-muted-foreground mt-1">Track, filter, and analyze your outgoing cash flow.</p>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 px-4 py-2 bg-secondary text-secondary-foreground text-sm font-medium rounded-md hover:bg-secondary/80 transition-colors">
            <Download className="w-4 h-4" />
            Export CSV
          </button>
          <button 
            onClick={() => setShowUploader(!showUploader)}
            className="flex items-center gap-2 px-4 py-2 bg-primary text-primary-foreground text-sm font-medium rounded-md hover:bg-primary/90 transition-colors"
          >
            <UploadCloud className="w-4 h-4" />
            OCR Upload
          </button>
        </div>
      </div>

      <AnimatePresence>
        {showUploader && (
          <motion.div 
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: 'auto' }}
            exit={{ opacity: 0, height: 0 }}
            className="overflow-hidden shrink-0"
          >
            <div className="p-8 border-2 border-dashed border-border rounded-xl bg-card/50 flex flex-col items-center justify-center relative">
              <button 
                onClick={() => setShowUploader(false)}
                className="absolute top-4 right-4 text-muted-foreground hover:text-foreground"
              >
                <X className="w-4 h-4" />
              </button>
              <Receipt className="w-12 h-12 text-blue-500 mb-4 opacity-80" />
              <h3 className="font-semibold text-lg">Drop receipts here</h3>
              <p className="text-sm text-muted-foreground mt-1 max-w-sm text-center">
                Our AI Vision model will instantly extract merchants, amounts, and auto-categorize your expenses. (Simulated in Dev Mode)
              </p>
              <button className="mt-4 px-4 py-2 bg-secondary text-sm font-medium rounded-md border border-border/50">
                Browse Files
              </button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="flex-1 rounded-xl border border-border bg-card flex flex-col min-h-0">
        <div className="p-4 border-b border-border flex flex-col sm:flex-row items-center justify-between gap-4 bg-secondary/10 shrink-0">
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
          <div className="flex gap-2 w-full sm:w-auto">
             <button className="flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-muted-foreground border border-border rounded-md hover:bg-secondary transition-colors w-full sm:w-auto">
              <Filter className="w-4 h-4" />
              Categories
            </button>
            <button className="flex items-center justify-center gap-2 px-3 py-2 text-sm font-medium text-foreground bg-primary/10 border border-primary/20 rounded-md hover:bg-primary/20 transition-colors w-full sm:w-auto">
              <Plus className="w-4 h-4" />
              Manual Entry
            </button>
          </div>
        </div>

        {/* Virtualized Table Container */}
        <div 
          ref={parentRef}
          className="flex-1 overflow-auto"
        >
          <div
            style={{
              height: `${rowVirtualizer.getTotalSize()}px`,
              width: '100%',
              position: 'relative',
            }}
          >
            {/* Sticky Header */}
            <div className="sticky top-0 z-10 grid grid-cols-[2fr_1fr_1fr_1fr_1.5fr_1fr_50px] text-xs text-muted-foreground uppercase bg-card/80 backdrop-blur-md border-b border-border">
              <div className="px-6 py-4 font-medium">Merchant</div>
              <div className="px-6 py-4 font-medium">Category</div>
              <div className="px-6 py-4 font-medium">Date</div>
              <div className="px-6 py-4 font-medium">Status</div>
              <div className="px-6 py-4 font-medium">Tags</div>
              <div className="px-6 py-4 font-medium text-right">Amount</div>
              <div className="px-6 py-4"></div>
            </div>

            {/* Virtualized Rows */}
            {rowVirtualizer.getVirtualItems().map((virtualRow) => {
              const expense = filtered[virtualRow.index];
              return (
                <div
                  key={expense.id}
                  style={{
                    position: 'absolute',
                    top: 0,
                    left: 0,
                    width: '100%',
                    height: `${virtualRow.size}px`,
                    transform: `translateY(${virtualRow.start}px)`,
                  }}
                  className="grid grid-cols-[2fr_1fr_1fr_1fr_1.5fr_1fr_50px] items-center border-b border-border hover:bg-secondary/20 transition-colors group text-sm"
                >
                  <div className="px-6 font-medium flex items-center gap-3 truncate">
                    <div className="w-8 h-8 rounded bg-secondary flex items-center justify-center text-xs shrink-0">
                      {expense.merchant.charAt(0)}
                    </div>
                    <span className="truncate">{expense.merchant}</span>
                  </div>
                  <div className="px-6 text-muted-foreground truncate">{expense.category}</div>
                  <div className="px-6 text-muted-foreground">{expense.date}</div>
                  <div className="px-6">
                    <span className={cn(
                      "px-2 py-1 text-xs rounded-md whitespace-nowrap",
                      expense.status === 'Cleared' ? "bg-emerald-500/10 text-emerald-500" : "bg-amber-500/10 text-amber-500"
                    )}>
                      {expense.status}
                    </span>
                  </div>
                  <div className="px-6 flex gap-1 flex-wrap overflow-hidden h-6 items-center">
                    {expense.tags.map(tag => (
                      <span key={tag} className="px-2 py-0.5 text-[10px] uppercase tracking-wider bg-secondary text-secondary-foreground rounded shrink-0">
                        {tag}
                      </span>
                    ))}
                  </div>
                  <div className="px-6 text-right font-medium">
                    ${expense.amount.toFixed(2)}
                  </div>
                  <div className="px-6 text-right">
                    <button className="text-muted-foreground hover:text-foreground opacity-0 group-hover:opacity-100 transition-opacity">
                      <MoreHorizontal className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
          
          {filtered.length === 0 && (
            <div className="p-12 text-center text-muted-foreground border-t border-border mt-10">
              No expenses found matching "{search}"
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
