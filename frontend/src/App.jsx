import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import PatientDashboard from './pages/PatientDashboard';
import RudasPage from './pages/RudasPage';
import GamesPage from './pages/GamesPage';
import MemoryPage from './pages/MemoryPage';
import RemindersPage from './pages/RemindersPage';
import ApprovalsPage from './pages/ApprovalsPage';
import CaregiverDashboard from './pages/CaregiverDashboard';
import HealthcareWorkerDashboard from './pages/HealthcareWorkerDashboard';
import HealthCheckPage from './pages/HealthCheckPage';
import ProtectedRoute from './components/ProtectedRoute';
import OfflineBanner from './components/OfflineBanner';
import { AuthProvider } from './context/AuthContext';
import { LocaleProvider } from './context/LocaleContext';
import { OfflineProvider } from './offline/OfflineProvider';
import './styles/global.css';

export default function App() {
  return (
    <LocaleProvider><AuthProvider><OfflineProvider><BrowserRouter><OfflineBanner /><Routes>
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/health" element={<HealthCheckPage />} />
      <Route element={<ProtectedRoute roles={['patient']} />}>
        <Route path="/assessment/rudas" element={<RudasPage />} />
        <Route path="/patient" element={<PatientDashboard />} />
        <Route path="/games" element={<GamesPage />} />
        <Route path="/memory" element={<MemoryPage />} />
        <Route path="/reminders" element={<RemindersPage />} />
        <Route path="/approvals" element={<ApprovalsPage />} />
      </Route>
      <Route element={<ProtectedRoute roles={['caregiver']} />}><Route path="/caregiver" element={<CaregiverDashboard />} /></Route>
      <Route element={<ProtectedRoute roles={['hcw']} />}><Route path="/healthcare-worker" element={<HealthcareWorkerDashboard />} /></Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes></BrowserRouter></OfflineProvider></AuthProvider></LocaleProvider>
  );
}
