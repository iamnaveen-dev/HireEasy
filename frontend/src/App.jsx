import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import InterviewRoom from './pages/InterviewRoom';
import CreateInterview from './pages/CreateInterview';
import CreateCompany from './pages/CreateCompany';

function PrivateRoute({ children }) {
  const token = localStorage.getItem('access_token');
  return token ? children : <Navigate to="/login" />;
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/dashboard" element={
          <PrivateRoute>
            <Dashboard />
          </PrivateRoute>
        } />
        <Route path="/interview/create" element={
          <PrivateRoute>
            <CreateInterview />
          </PrivateRoute>
        } />
        <Route path="/interview/:id" element={
          <PrivateRoute>
            <InterviewRoom />
          </PrivateRoute>
        } />
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/company/create" element={
         <PrivateRoute>
           <CreateCompany />
         </PrivateRoute>
        } />
      </Routes>
    </BrowserRouter>
  );
}