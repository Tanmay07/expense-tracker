import { useQuery } from '@tanstack/react-query';
import { Clock } from 'lucide-react';

export function Timeline() {
  const { data, isLoading } = useQuery({
    queryKey: ['timeline'],
    queryFn: () => fetch('http://localhost:8030/api/bff/timeline', { headers: { 'mock_user_123': 'true' } }).then(res => res.json())
  });

  if (isLoading) return <div>Loading timeline...</div>;

  return (
    <div className="max-w-3xl mx-auto py-8">
      <h1 className="text-3xl font-bold tracking-tight mb-8">Financial Timeline</h1>
      <div className="relative border-l-2 border-gray-200 dark:border-gray-800 ml-4 space-y-8">
        {(data || []).map((event: any) => (
          <div key={event.id} className="relative pl-8">
            <div className="absolute -left-[11px] top-1 p-1 bg-white dark:bg-gray-950 rounded-full border-2 border-blue-500">
              <Clock size={12} className="text-blue-500" />
            </div>
            <div className="p-4 bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800">
              <div className="flex justify-between items-start mb-2">
                <span className="text-xs font-bold text-blue-600 bg-blue-100 dark:bg-blue-900/30 px-2 py-1 rounded">
                  {event.type}
                </span>
                <span className="text-xs text-gray-500">
                  {new Date(event.date).toLocaleString()}
                </span>
              </div>
              <p className="font-medium text-lg">{event.description}</p>
              {event.amount && <p className="text-green-600 font-bold mt-2">+${event.amount}</p>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
