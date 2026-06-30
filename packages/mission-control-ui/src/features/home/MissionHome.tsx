import { useQuery } from '@tanstack/react-query';
import { Target, Activity, AlertCircle, Sparkles } from 'lucide-react';

export function MissionHome() {
  const { data, isLoading } = useQuery({
    queryKey: ['dashboard'],
    queryFn: () => fetch('http://localhost:8030/api/bff/dashboard', { headers: { 'mock_user_123': 'true' } }).then(res => res.json())
  });

  if (isLoading) return <div className="animate-pulse flex space-x-4"><div className="flex-1 space-y-4 py-1"><div className="h-4 bg-gray-200 rounded w-3/4"></div><div className="space-y-2"><div className="h-4 bg-gray-200 rounded"></div></div></div></div>;

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Mission Home</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Net Worth Widget */}
        <div className="p-6 bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800">
          <h2 className="text-sm font-medium text-gray-500 mb-2 flex items-center"><Activity size={16} className="mr-2"/> Net Worth</h2>
          <p className="text-3xl font-bold">${data?.net_worth?.toLocaleString() ?? '1,250,000'}</p>
          <div className="mt-4 flex items-center text-sm text-green-600">
            <span className="font-medium">+2.4%</span>
            <span className="ml-2 text-gray-500">vs last month</span>
          </div>
        </div>

        {/* Status Widget */}
        <div className="p-6 bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800">
          <h2 className="text-sm font-medium text-gray-500 mb-2 flex items-center"><Target size={16} className="mr-2"/> Operational Status</h2>
          <div className="flex items-center space-x-3">
            <div className={`w-3 h-3 rounded-full ${data?.mission_status === 'ON_TRACK' ? 'bg-green-500' : 'bg-yellow-500'}`}></div>
            <p className="text-xl font-bold">{data?.mission_status?.replace('_', ' ') || 'ON TRACK'}</p>
          </div>
        </div>

        {/* Risk Widget */}
        <div className="p-6 bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800">
          <h2 className="text-sm font-medium text-gray-500 mb-2 flex items-center"><AlertCircle size={16} className="mr-2"/> Risk Score</h2>
          <p className="text-3xl font-bold text-blue-600">{data?.risk_score ?? 35}<span className="text-sm text-gray-500 ml-1">/ 100</span></p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* AI Insights */}
        <div className="p-6 bg-blue-50 dark:bg-blue-900/20 rounded-xl border border-blue-100 dark:border-blue-800">
          <h2 className="text-lg font-bold text-blue-900 dark:text-blue-100 mb-4 flex items-center"><Sparkles size={20} className="mr-2 text-blue-600 dark:text-blue-400"/> AI Copilot Summary</h2>
          <p className="text-blue-800 dark:text-blue-200">{data?.ai_summary || "Your portfolio is perfectly balanced. No immediate actions required."}</p>
        </div>

        {/* Upcoming Actions */}
        <div className="p-6 bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800">
          <h2 className="text-lg font-bold mb-4">Upcoming Actions</h2>
          <ul className="space-y-3">
            {(data?.upcoming_actions || []).map((action: any) => (
              <li key={action.id} className="flex justify-between items-center p-3 hover:bg-gray-50 dark:hover:bg-gray-800 rounded-lg transition-colors border border-gray-100 dark:border-gray-800">
                <span className="font-medium">{action.title}</span>
                <span className={`text-xs px-2 py-1 rounded-full ${action.urgency === 'HIGH' ? 'bg-red-100 text-red-700' : 'bg-yellow-100 text-yellow-700'}`}>
                  {action.urgency}
                </span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
