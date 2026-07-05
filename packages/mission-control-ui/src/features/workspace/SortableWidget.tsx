import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { GripHorizontal, Settings, X } from 'lucide-react';
import type { WidgetConfig } from '../../store/useWorkspaceStore';
import { useWorkspaceStore } from '../../store/useWorkspaceStore';
import { cn } from '../../utils/cn';

// Import specific widget types
import { KPIWidget } from './widgets/KPIWidget';
import { ChartWidget } from './widgets/ChartWidget';
import { NoteWidget } from './widgets/NoteWidget';

interface SortableWidgetProps {
  widget: WidgetConfig;
}

export function SortableWidget({ widget }: SortableWidgetProps) {
  const { setSelectedEntity, selectedEntityId } = useWorkspaceStore();
  const isSelected = selectedEntityId === widget.id;

  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging,
  } = useSortable({ id: widget.id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  // Determine span based on layout config (simplified)
  const spanClass = widget.layout.w > 6 ? "md:col-span-2 xl:col-span-3" : 
                    widget.layout.w > 3 ? "md:col-span-2" : "col-span-1";
                    
  const renderWidgetContent = () => {
    switch (widget.widget_type) {
      case 'KPI': return <KPIWidget config={widget} />;
      case 'CHART': return <ChartWidget config={widget} />;
      case 'NOTE': return <NoteWidget config={widget} />;
      default: return <div className="p-4 text-sm text-gray-500">Unknown widget type: {widget.widget_type}</div>;
    }
  };

  return (
    <div
      ref={setNodeRef}
      style={style}
      className={cn(
        "group relative flex flex-col bg-white dark:bg-gray-900 border rounded-xl overflow-hidden shadow-sm transition-shadow",
        spanClass,
        isDragging ? "opacity-50 border-blue-500 shadow-xl z-50 scale-[1.02]" : "",
        isSelected ? "border-blue-500 ring-1 ring-blue-500" : "border-gray-200 dark:border-gray-800 hover:border-gray-300 dark:hover:border-gray-700"
      )}
      onClick={() => setSelectedEntity(widget.id)}
    >
      {/* Widget Header (Drag Handle) */}
      <div 
        className={cn(
          "h-10 flex items-center justify-between px-3 border-b transition-colors",
          isSelected ? "bg-blue-50/50 dark:bg-blue-900/20 border-blue-100 dark:border-blue-800/50" : "bg-gray-50 dark:bg-gray-900/50 border-gray-100 dark:border-gray-800"
        )}
      >
        <div className="flex items-center gap-2 flex-1">
          <button 
            className="p-1 text-gray-400 hover:text-gray-700 dark:hover:text-gray-300 cursor-grab active:cursor-grabbing"
            {...attributes} 
            {...listeners}
          >
            <GripHorizontal size={14} />
          </button>
          <span className="text-xs font-semibold uppercase tracking-wider text-gray-600 dark:text-gray-400 truncate">
            {widget.title}
          </span>
        </div>

        <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
          <button className="p-1 rounded text-gray-400 hover:text-gray-700 hover:bg-gray-200 dark:hover:text-gray-300 dark:hover:bg-gray-800">
            <Settings size={14} />
          </button>
          <button className="p-1 rounded text-gray-400 hover:text-red-600 hover:bg-red-50 dark:hover:text-red-400 dark:hover:bg-red-900/30">
            <X size={14} />
          </button>
        </div>
      </div>

      {/* Widget Body */}
      <div className="flex-1 p-4 relative min-h-[120px]">
        {renderWidgetContent()}
      </div>
    </div>
  );
}
