import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import { PatientRegistrationPage, CaregiverRegistrationPage, PatientLoginPage, CaregiverLoginPage } from './pages/AuthPages';
import DashboardPage from './pages/DashboardPage';
import BaselineAssessmentPage from './pages/BaselineAssessmentPage';
import './index.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/register/patient" element={<PatientRegistrationPage />} />
        <Route path="/register/caregiver" element={<CaregiverRegistrationPage />} />
        <Route path="/login/patient" element={<PatientLoginPage />} />
        <Route path="/login/caregiver" element={<CaregiverLoginPage />} />
        <Route path="/assessment" element={<BaselineAssessmentPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
