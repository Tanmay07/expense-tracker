import { motion } from 'framer-motion';
import { TrendingUp, DollarSign, Target, Calendar, ArrowRight, Zap, Loader2 } from 'lucide-react';
import { cn } from '../utils/cn';
import { useDashboardMetrics } from '../hooks/useData';

const FADE_UP = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
};

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
              <h2 className="text-lg font-semibold">Today's Mission</h2>
              <button className="text-sm text-blue-400 hover:text-blue-300 flex items-center gap-1 transition-colors">
                View Plan <ArrowRight className="w-4 h-4" />
              </button>
            </div>
            <div className="p-4 rounded-lg bg-secondary/50 border border-border/50 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
              <div>
                <h3 className="font-medium text-foreground flex items-center gap-2">
                  <Zap className="w-4 h-4 text-amber-500" />
                  Optimize Subscriptions
                </h3>
                <p className="text-sm text-muted-foreground mt-1">AI Copilot found $45/mo in unused subscriptions. Review and cancel to achieve your savings goal faster.</p>
              </div>
              <button className="shrink-0 px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white text-sm font-medium rounded-md transition-colors">
                Review Now
              </button>
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
            className="rounded-xl border border-border bg-card p-5 relative overflow-hidden"
            variants={FADE_UP}
          >
            <div className="absolute top-0 right-0 p-32 bg-blue-500/10 blur-[100px] rounded-full pointer-events-none"></div>
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <span className="w-2 h-2 rounded-full bg-blue-500"></span>
              AI Recommendations
            </h2>
            <div className="space-y-3 relative">
              <div className="p-3 rounded-md bg-secondary/30 border border-border/50 text-sm">
                <span className="font-medium block mb-1">Increase Emergency Fund</span>
                Based on your recent spending volatility, consider increasing your target by $1k.
              </div>
              <div className="p-3 rounded-md bg-secondary/30 border border-border/50 text-sm">
                <span className="font-medium block mb-1">Tax Loss Harvesting</span>
                You have $450 in unrealized losses. Execute trades before EOY.
              </div>
            </div>
          </motion.section>

          <motion.section 
            className="rounded-xl border border-border bg-card p-5"
            variants={FADE_UP}
          >
            <h2 className="text-lg font-semibold mb-4">Upcoming Goals</h2>
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium">Italy Trip (Summer)</span>
                  <span className="text-muted-foreground">75%</span>
                </div>
                <div className="w-full h-2 bg-secondary rounded-full overflow-hidden">
                  <div className="h-full bg-blue-500 rounded-full" style={{ width: '75%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-sm mb-1">
                  <span className="font-medium">House Downpayment</span>
                  <span className="text-muted-foreground">42%</span>
                </div>
                <div className="w-full h-2 bg-secondary rounded-full overflow-hidden">
                  <div className="h-full bg-purple-500 rounded-full" style={{ width: '42%' }}></div>
                </div>
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
      className="p-5 rounded-xl border border-border bg-card shadow-sm hover:border-border/80 transition-colors"
    >
      <div className="flex items-center justify-between text-muted-foreground mb-3">
        <span className="text-sm font-medium">{title}</span>
        <Icon className="w-4 h-4" />
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
