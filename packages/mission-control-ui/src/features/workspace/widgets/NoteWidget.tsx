import type { WidgetConfig } from '../../../store/useWorkspaceStore';

interface NoteWidgetProps {
  config: WidgetConfig;
}

export function NoteWidget({ config }: NoteWidgetProps) {
  return (
    <div className="h-full">
      <textarea 
        className="w-full h-full min-h-[150px] resize-none bg-transparent outline-none text-sm text-gray-700 dark:text-gray-300 placeholder-gray-400"
        placeholder="Type markdown notes here..."
        defaultValue={config.settings.content || ""}
      />
    </div>
  );
}
