import { Navigate, Outlet } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function ProtectedRoute({ roles }) {
  const { user, loading } = useAuth();
  if (loading) return <main className="page-shell"><p>Loading your account...</p></main>;
  if (!user) return <Navigate to="/login" replace />;
  if (roles?.length && !roles.includes(user.role)) return <main className="page-shell"><h1>Access denied</h1></main>;
  return <Outlet />;
}