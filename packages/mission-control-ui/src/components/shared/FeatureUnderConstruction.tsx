import { Lock, Construction } from 'lucide-react';

interface Props {
  title: string;
  description?: string;
}

export function FeatureUnderConstruction({ title, description }: Props) {
  return (
    <div className="max-w-3xl mx-auto py-24 text-center space-y-6">
      <div className="w-20 h-20 bg-secondary/50 rounded-3xl flex items-center justify-center mx-auto shadow-inner border border-border/50">
        <Construction className="w-10 h-10 text-muted-foreground" />
      </div>
      
      <div>
        <h1 className="text-3xl font-bold tracking-tight">{title}</h1>
        <p className="text-muted-foreground mt-3 text-lg max-w-xl mx-auto leading-relaxed">
          {description || "This capability is currently disabled behind a feature flag while it undergoes development."}
        </p>
      </div>

      <div className="inline-flex items-center gap-2 px-4 py-2 bg-secondary/30 rounded-lg text-sm text-muted-foreground border border-border/50">
        <Lock className="w-4 h-4" />
        <span>Enable in Developer Workspace</span>
      </div>
    </div>
  );
}
