import { Route, Routes } from "react-router-dom";
import { AppShell } from "./layouts/AppShell";
import { AssistantPage } from "./pages/AssistantPage";
import { PaymentsPage } from "./pages/PaymentsPage";
import { DashboardPage } from "./pages/DashboardPage";

export default function App() {
  return (
    <AppShell>
      <Routes>
        <Route path="/" element={<AssistantPage />} />
        <Route path="/payments" element={<PaymentsPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </AppShell>
  );
}
