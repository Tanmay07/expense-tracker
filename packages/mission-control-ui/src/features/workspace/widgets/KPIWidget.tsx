import { TrendingUp, TrendingDown } from 'lucide-react';
import type { WidgetConfig } from '../../../store/useWorkspaceStore';

interface KPIWidgetProps {
  config: WidgetConfig;
}

export function KPIWidget({ config }: KPIWidgetProps) {
  // Mock data for the KPI based on config.data_source
  const isPositive = true;
  const value = config.data_source.includes('total') ? '$12,450.00' : '42';
  const trend = '+5.2%';

  return (
    <div className="flex flex-col justify-center h-full">
      <div className="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
        {value}
      </div>
      <div className="mt-2 flex items-center text-sm">
        <span className={`font-medium flex items-center gap-1 ${isPositive ? 'text-emerald-600 dark:text-emerald-500' : 'text-red-600 dark:text-red-500'}`}>
          {isPositive ? <TrendingUp size={14} /> : <TrendingDown size={14} />}
          {trend}
        </span>
        <span className="text-gray-500 ml-2">vs last month</span>
      </div>
    </div>
  );
}
