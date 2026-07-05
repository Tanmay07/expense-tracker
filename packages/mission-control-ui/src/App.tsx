import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Shell } from './layout/Shell';
import { Home } from './pages/Home';
import { Expenses } from './pages/Expenses';
import { Missions } from './pages/Missions';
import { PlaceholderPage } from './pages/PlaceholderPage';
import { DeveloperWorkspace } from './pages/DeveloperWorkspace';
import { useContextInit } from './hooks/useContextInit';

function App() {
  useContextInit();

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Shell />}>
          <Route index element={<Home />} />
          <Route path="expenses" element={<Expenses />} />
          <Route path="missions" element={<Missions />} />
          <Route path="settings" element={<DeveloperWorkspace />} />
          
          {/* Feature Flagged routes */}
          <Route path="investments" element={<PlaceholderPage flag="investments" title="Investment Portfolio" />} />
          <Route path="analytics" element={<PlaceholderPage flag="analytics" title="Analytics Platform" />} />
          <Route path="budgets" element={<PlaceholderPage flag="budgets" title="Budget Planner" />} />
          <Route path="governance" element={<PlaceholderPage flag="governance" title="Governance Platform" />} />
          <Route path="knowledge-graph" element={<PlaceholderPage flag="knowledgeGraph" title="Knowledge Graph Explorer" />} />
          
          {/* Catch all */}
          <Route path="*" element={<PlaceholderPage flag="analytics" title="Module Not Found" />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
