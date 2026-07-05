import { useFeatureFlags } from '../core/flags/useFeatureFlags';
import type { FeatureFlag } from '../core/flags/useFeatureFlags';
import { FeatureUnderConstruction } from '../components/shared/FeatureUnderConstruction';

interface Props {
  flag: FeatureFlag;
  title: string;
}

export function PlaceholderPage({ flag, title }: Props) {
  const { flags } = useFeatureFlags();
  const isEnabled = flags[flag];

  if (!isEnabled) {
    return <FeatureUnderConstruction title={title} />;
  }

  // If enabled but not implemented yet, just show a blank scaffold ready for dev
  return (
    <div className="max-w-4xl mx-auto space-y-4">
      <h1 className="text-3xl font-bold tracking-tight">{title}</h1>
      <div className="p-12 text-center border border-dashed border-border rounded-xl text-muted-foreground">
        Flag '{flag}' enabled! Ready for Implementation.
      </div>
    </div>
  );
}
