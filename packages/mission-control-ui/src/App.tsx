import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Shell } from './shared/components/layout/Shell';

import { MissionHome } from './features/home/MissionHome';
import { MissionCenter } from './features/missions/MissionCenter';
import { DecisionCenter } from './features/decisions/DecisionCenter';
import { Timeline } from './features/timeline/Timeline';
import { Copilot } from './features/copilot/Copilot';
import { GraphExp } from './features/graph/GraphExp';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Shell>
          <Routes>
            <Route path="/" element={<MissionHome />} />
            <Route path="/missions" element={<MissionCenter />} />
            <Route path="/decisions" element={<DecisionCenter />} />
            <Route path="/timeline" element={<Timeline />} />
            <Route path="/copilot" element={<Copilot />} />
            <Route path="/graph" element={<GraphExp />} />
          </Routes>
        </Shell>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
