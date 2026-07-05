import { motion } from 'framer-motion';
import { TrendingUp, DollarSign, Target, Calendar, ArrowRight, Zap, Loader2 } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { cn } from '../utils/cn';
import { useDashboardMetrics } from '../hooks/useData';

const FADE_UP = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
};

const MOCK_CHART_DATA = [
  { name: 'Jan', value: 4000 },
  { name: 'Feb', value: 3000 },
  { name: 'Mar', value: 5000 },
  { name: 'Apr', value: 4500 },
  { name: 'May', value: 6000 },
  { name: 'Jun', value: 5500 },
  { name: 'Jul', value: 7000 },
];

export function Home() {
  const { data: metrics, isLoading } = useDashboardMetrics();

  if (isLoading || !metrics) {
    return (
      <div className="flex items-center justify-center h-[50vh]">
        <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Mission Control</h1>
          <p className="text-muted-foreground mt-1">Here's your financial operating system at a glance.</p>
        </div>
        <div className="flex items-center gap-2">
          <span className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium bg-emerald-500/10 text-emerald-500 rounded-full border border-emerald-500/20">
            <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
            System Healthy
          </span>
          <button className="px-4 py-2 bg-primary text-primary-foreground text-sm font-medium rounded-md hover:bg-primary/90 transition-colors">
            New Mission
          </button>
        </div>
      </div>

      <motion.div 
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
        initial="initial" animate="animate"
        transition={{ staggerChildren: 0.1 }}
      >
        <MetricCard title="Net Worth" value={metrics.netWorth.toLocaleString('en-US', { style: 'currency', currency: 'USD' })} trend={`${metrics.netWorthTrend}%`} isPositive={metrics.netWorthTrend > 0} icon={DollarSign} delay={0} />
        <MetricCard title="Monthly Cash Flow" value={metrics.cashFlow.toLocaleString('en-US', { style: 'currency', currency: 'USD' })} trend={`${metrics.cashFlowTrend}%`} isPositive={metrics.cashFlowTrend > 0} icon={TrendingUp} delay={0.1} />
        <MetricCard title="Active Goals" value={`${metrics.activeGoals} On Track`} trend={`${metrics.atRiskGoals} At Risk`} isPositive={metrics.atRiskGoals === 0} icon={Target} delay={0.2} />
        <MetricCard title="Pending Bills" value={metrics.pendingBills.toLocaleString('en-US', { style: 'currency', currency: 'USD' })} trend={`Due in ${metrics.billsDueDays} days`} isPositive={metrics.billsDueDays > 5} icon={Calendar} delay={0.3} />
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-6">
          <motion.section 
            className="rounded-xl border border-border bg-card p-5"
            variants={FADE_UP}
          >
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Cash Flow Trends</h2>
              <div className="flex gap-2">
                <button className="px-3 py-1 text-xs font-medium bg-secondary rounded">1M</button>
                <button className="px-3 py-1 text-xs font-medium hover:bg-secondary rounded text-muted-foreground">3M</button>
                <button className="px-3 py-1 text-xs font-medium hover:bg-secondary rounded text-muted-foreground">YTD</button>
              </div>
            </div>
            <div className="h-[250px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={MOCK_CHART_DATA} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#888' }} dy={10} />
                  <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 12, fill: '#888' }} tickFormatter={(v) => `$${v/1000}k`} />
                  <Tooltip 
                    contentStyle={{ backgroundColor: 'rgba(0,0,0,0.8)', border: 'none', borderRadius: '8px', color: '#fff' }}
                    itemStyle={{ color: '#fff' }}
                    formatter={(value: any) => [`$${value}`, 'Cash Flow']}
                  />
                  <Area type="monotone" dataKey="value" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorValue)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </motion.section>

          <motion.section 
            className="rounded-xl border border-border bg-card p-5"
            variants={FADE_UP}
          >
             <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold">Recent Transactions</h2>
              <button className="text-sm text-muted-foreground hover:text-foreground transition-colors">View All</button>
            </div>
            <div className="space-y-4">
              {[
                { name: 'Whole Foods Market', category: 'Groceries', amount: -142.50, date: 'Today, 2:30 PM' },
                { name: 'Salary Deposit', category: 'Income', amount: 4250.00, date: 'Yesterday', isPositive: true },
                { name: 'Netflix Subscription', category: 'Entertainment', amount: -15.99, date: 'Oct 24' },
                { name: 'Vanguard S&P 500', category: 'Investment', amount: -500.00, date: 'Oct 23' },
              ].map((txn, i) => (
                <div key={i} className="flex items-center justify-between group">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-secondary flex items-center justify-center text-muted-foreground">
                      {txn.name.charAt(0)}
                    </div>
                    <div>
                      <p className="font-medium text-sm group-hover:text-blue-400 transition-colors">{txn.name}</p>
                      <p className="text-xs text-muted-foreground">{txn.category} • {txn.date}</p>
                    </div>
                  </div>
                  <span className={cn("font-medium text-sm", txn.isPositive ? "text-emerald-500" : "")}>
                    {txn.isPositive ? '+' : ''}{txn.amount.toLocaleString('en-US', { style: 'currency', currency: 'USD' })}
                  </span>
                </div>
              ))}
            </div>
          </motion.section>
        </div>

        <div className="space-y-6">
           <motion.section 
            className="rounded-xl border border-border bg-card p-5 border-blue-500/30 relative overflow-hidden shadow-[0_0_20px_rgba(59,130,246,0.1)]"
            variants={FADE_UP}
          >
            <div className="absolute top-0 right-0 p-32 bg-blue-500/10 blur-[100px] rounded-full pointer-events-none"></div>
            <div className="flex items-center justify-between mb-4 relative">
              <h2 className="text-lg font-semibold flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-blue-500 animate-pulse"></span>
                Active Mission
              </h2>
            </div>
            <div className="relative">
              <h3 className="font-medium text-foreground text-lg">Tax Loss Harvesting</h3>
              <p className="text-sm text-muted-foreground mt-1 mb-4">Execute trades to harvest $4,500 in unrealized losses before EOY.</p>
              
              <div className="space-y-3">
                <div className="flex items-center gap-3 text-sm">
                  <div className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-500 flex items-center justify-center shrink-0">✓</div>
                  <span className="text-muted-foreground line-through">Identify losing positions</span>
                </div>
                <div className="flex items-center gap-3 text-sm">
                   <div className="w-5 h-5 rounded-full bg-emerald-500/20 text-emerald-500 flex items-center justify-center shrink-0">✓</div>
                  <span className="text-muted-foreground line-through">Analyze wash sale rules</span>
                </div>
                <div className="flex items-center gap-3 text-sm font-medium">
                  <div className="relative flex items-center justify-center w-5 h-5 shrink-0">
                    <span className="absolute w-full h-full bg-blue-500/20 rounded-full animate-ping"></span>
                    <div className="w-2 h-2 bg-blue-500 rounded-full relative z-10"></div>
                  </div>
                  <span className="text-blue-400">Execute sell orders</span>
                </div>
              </div>

              <button className="w-full mt-6 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white text-sm font-medium rounded-md transition-colors flex items-center justify-center gap-2">
                Authorize Execution <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </motion.section>

          <motion.section 
            className="rounded-xl border border-border bg-card p-5"
            variants={FADE_UP}
          >
            <h2 className="text-lg font-semibold mb-4">AI Recommendations</h2>
            <div className="space-y-3 relative">
              <div className="p-3 rounded-md bg-secondary/30 border border-border/50 text-sm hover:border-border transition-colors cursor-pointer group">
                <span className="font-medium flex items-center gap-2 mb-1 group-hover:text-blue-400 transition-colors">
                  <Zap className="w-4 h-4 text-amber-500" />
                  Optimize Subscriptions
                </span>
                Found $45/mo in unused subscriptions. Review and cancel.
              </div>
              <div className="p-3 rounded-md bg-secondary/30 border border-border/50 text-sm hover:border-border transition-colors cursor-pointer group">
                <span className="font-medium block mb-1 group-hover:text-blue-400 transition-colors">Increase Emergency Fund</span>
                Based on your recent spending volatility, consider increasing your target by $1k.
              </div>
            </div>
          </motion.section>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ title, value, trend, isPositive, icon: Icon, delay }: any) {
  return (
    <motion.div 
      variants={FADE_UP}
      transition={{ delay }}
      className="p-5 rounded-xl border border-border bg-card shadow-sm hover:border-border/80 transition-colors group cursor-default"
    >
      <div className="flex items-center justify-between text-muted-foreground mb-3">
        <span className="text-sm font-medium">{title}</span>
        <Icon className="w-4 h-4 group-hover:text-foreground transition-colors" />
      </div>
      <div className="text-2xl font-bold tracking-tight">{value}</div>
      <div className="mt-1 flex items-center text-xs">
        <span className={cn("font-medium", isPositive ? "text-emerald-500" : "text-rose-500")}>
          {trend}
        </span>
        <span className="text-muted-foreground ml-1.5">vs last month</span>
      </div>
    </motion.div>
  );
}
