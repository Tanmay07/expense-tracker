import { useQuery } from '@tanstack/react-query';
import { Target, AlertTriangle, CheckCircle2 } from 'lucide-react';

export function MissionCenter() {
  const { data, isLoading } = useQuery({
    queryKey: ['missions'],
    queryFn: () => fetch('http://localhost:8030/api/bff/missions', { headers: { 'mock_user_123': 'true' } }).then(res => res.json())
  });

  if (isLoading) return <div>Loading missions...</div>;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold tracking-tight">Mission Center</h1>
        <button className="px-4 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors">
          New Mission
        </button>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {(data || []).map((mission: any) => (
          <div key={mission.id} className="p-6 bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800 flex flex-col h-full">
            <div className="flex items-start justify-between mb-4">
              <div className="p-3 bg-blue-100 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 rounded-lg">
                <Target size={24} />
              </div>
              {mission.status === 'ACTIVE' ? (
                <span className="flex items-center text-sm text-green-600 font-medium"><CheckCircle2 size={16} className="mr-1"/> On Track</span>
              ) : (
                <span className="flex items-center text-sm text-yellow-600 font-medium"><AlertTriangle size={16} className="mr-1"/> At Risk</span>
              )}
            </div>
            
            <h2 className="text-xl font-bold mb-2">{mission.name}</h2>
            
            <div className="mt-auto pt-4">
              <div className="flex justify-between text-sm mb-1 text-gray-500">
                <span>Progress</span>
                <span className="font-medium text-gray-900 dark:text-white">{mission.progress}%</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-800 rounded-full h-2">
                <div className="bg-blue-600 h-2 rounded-full" style={{ width: `${mission.progress}%` }}></div>
              </div>
              <p className="text-xs text-gray-400 mt-3 flex items-center justify-between">
                <span>AI Confidence: {mission.confidence}%</span>
                <button className="text-blue-600 hover:underline font-medium">View Details &rarr;</button>
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
