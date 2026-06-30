import ReactFlow, { MiniMap, Controls, Background } from 'reactflow';
import 'reactflow/dist/style.css';
import { useQuery } from '@tanstack/react-query';

export function GraphExp() {
  const { data, isLoading } = useQuery({
    queryKey: ['graph'],
    queryFn: () => fetch('http://localhost:8030/api/bff/graph', { headers: { 'mock_user_123': 'true' } }).then(res => res.json())
  });

  if (isLoading) return <div>Loading graph...</div>;

  const initialNodes = (data?.nodes || []).map((n: any, i: number) => ({
    id: n.id,
    position: { x: (i % 2) * 200, y: Math.floor(i / 2) * 150 },
    data: { label: `${n.label} (${n.type})` },
    style: { 
      background: n.type === 'person' ? '#3b82f6' : '#fff',
      color: n.type === 'person' ? '#fff' : '#000',
      border: '1px solid #e5e7eb',
      borderRadius: '8px',
      padding: '10px'
    }
  }));
  
  const initialEdges = (data?.edges || []).map((e: any, i: number) => ({
    id: `e${i}`,
    source: e.source,
    target: e.target,
    animated: true,
  }));

  return (
    <div className="h-[calc(100vh-10rem)] bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-800">
      <div className="p-4 border-b border-gray-200 dark:border-gray-800">
        <h2 className="font-bold text-lg">Financial Graph Explorer</h2>
      </div>
      <div className="h-full w-full">
        <ReactFlow nodes={initialNodes} edges={initialEdges} fitView>
          <Controls />
          <MiniMap />
          <Background gap={12} size={1} />
        </ReactFlow>
      </div>
    </div>
  );
}
