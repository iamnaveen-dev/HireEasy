import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { interviewAPI, reportAPI } from '../services/api';

export default function Dashboard() {
  const navigate = useNavigate();
  const [interviews, setInterviews] = useState([]);
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [roomCode, setRoomCode] = useState('');
  const [activeTab, setActiveTab] = useState('interviews');
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [interviewsRes, reportsRes] = await Promise.all([
        interviewAPI.list(),
        reportAPI.list(),
      ]);
      setInterviews(interviewsRes.data.interviews || []);
      setReports(reportsRes.data.reports || []);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleJoin = async () => {
    if (!roomCode) return;
    try {
      const response = await interviewAPI.join(roomCode);
      navigate(`/interview/${response.data.interview.id}`);
    } catch (err) {
      alert(err.response?.data?.error || 'Invalid room code');
    }
  };

  const handleLogout = () => {
    localStorage.clear();
    navigate('/login');
  };

  const getStatusConfig = (status) => {
    const configs = {
      scheduled: { bg: 'bg-blue-100', text: 'text-blue-700', dot: 'bg-blue-500' },
      waiting: { bg: 'bg-yellow-100', text: 'text-yellow-700', dot: 'bg-yellow-500' },
      in_progress: { bg: 'bg-green-100', text: 'text-green-700', dot: 'bg-green-500' },
      completed: { bg: 'bg-gray-100', text: 'text-gray-700', dot: 'bg-gray-500' },
      cancelled: { bg: 'bg-red-100', text: 'text-red-700', dot: 'bg-red-500' },
    };
    return configs[status] || configs.completed;
  };

  const getRecommendationConfig = (rec) => {
    const configs = {
      strong_hire: { color: 'text-green-600', bg: 'bg-green-50', border: 'border-green-200' },
      hire: { color: 'text-green-500', bg: 'bg-green-50', border: 'border-green-200' },
      maybe: { color: 'text-yellow-600', bg: 'bg-yellow-50', border: 'border-yellow-200' },
      no_hire: { color: 'text-red-500', bg: 'bg-red-50', border: 'border-red-200' },
      strong_no_hire: { color: 'text-red-700', bg: 'bg-red-50', border: 'border-red-200' },
    };
    return configs[rec] || configs.maybe;
  };

  const getRoleColor = (role) => {
    const colors = {
      candidate: 'bg-purple-100 text-purple-700',
      interviewer: 'bg-blue-100 text-blue-700',
      company_admin: 'bg-orange-100 text-orange-700',
      super_admin: 'bg-red-100 text-red-700',
    };
    return colors[role] || 'bg-gray-100 text-gray-700';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-500">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold text-blue-600">
            Hire<span className="text-gray-800">Linq</span>
          </h1>
          <div className="flex items-center gap-4">
            {(user.role === 'company_admin' || user.role === 'interviewer') && (
              <button
                onClick={() => navigate('/interview/create')}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700 transition"
              >
                + Schedule Interview
              </button>
            )}
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center text-white text-sm font-bold">
                {user.username?.[0]?.toUpperCase()}
              </div>
              <div>
                <p className="text-sm font-medium text-gray-800">{user.username}</p>
                <span className={`text-xs px-2 py-0.5 rounded-full ${getRoleColor(user.role)}`}>
                  {user.role?.replace('_', ' ')}
                </span>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="text-gray-500 hover:text-red-500 transition text-sm font-medium"
            >
              Logout →
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto p-6">
        {user.role === 'company_admin' && interviews.length === 0 && (
          <div className="bg-blue-50 border border-blue-200 rounded-xl p-6 mb-6 flex justify-between items-center">
            <div>
              <p className="font-semibold text-blue-800">
                Welcome to HireLinq!
              </p>
              <p className="text-blue-600 text-sm mt-1">
                Register your company first to start scheduling interviews
              </p>
            </div>
            <button
              onClick={() => navigate('/company/create')}
              className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition whitespace-nowrap"
            >
              Register Company →
            </button>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <p className="text-gray-500 text-sm mb-1">Total Interviews</p>
            <p className="text-3xl font-bold text-blue-600">{interviews.length}</p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <p className="text-gray-500 text-sm mb-1">Completed</p>
            <p className="text-3xl font-bold text-green-600">
              {interviews.filter(i => i.status === 'completed').length}
            </p>
          </div>
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-5">
            <p className="text-gray-500 text-sm mb-1">Reports Ready</p>
            <p className="text-3xl font-bold text-purple-600">{reports.length}</p>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 mb-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            🚪 Join Interview Room
          </h2>
          <div className="flex gap-3">
            <input
              type="text"
              placeholder="Enter room code (e.g. HX72KP9M)"
              className="flex-1 border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 uppercase font-mono text-lg tracking-widest"
              value={roomCode}
              onChange={(e) => setRoomCode(e.target.value.toUpperCase())}
              maxLength={8}
            />
            <button
              onClick={handleJoin}
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
            >
              Join →
            </button>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-sm border border-gray-100">
          <div className="flex border-b border-gray-100">
            <button
              onClick={() => setActiveTab('interviews')}
              className={`px-6 py-4 font-medium text-sm transition ${
                activeTab === 'interviews'
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Interviews ({interviews.length})
            </button>
            <button
              onClick={() => setActiveTab('reports')}
              className={`px-6 py-4 font-medium text-sm transition ${
                activeTab === 'reports'
                  ? 'text-blue-600 border-b-2 border-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Reports ({reports.length})
            </button>
          </div>

          <div className="p-6">
            {activeTab === 'interviews' && (
              <>
                {interviews.length === 0 ? (
                  <div className="text-center py-12">
                    <p className="text-4xl mb-3">📋</p>
                    <p className="text-gray-500">No interviews yet</p>
                    {(user.role === 'company_admin' || user.role === 'interviewer') && (
                      <button
                        onClick={() => navigate('/interview/create')}
                        className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-blue-700 transition"
                      >
                        Schedule your first interview →
                      </button>
                    )}
                  </div>
                ) : (
                  <div className="space-y-3">
                    {interviews.map((interview) => {
                      const statusConfig = getStatusConfig(interview.status);
                      return (
                        <div
                          key={interview.id}
                          onClick={() => navigate(`/interview/${interview.id}`)}
                          className="border border-gray-100 rounded-xl p-4 hover:bg-blue-50 hover:border-blue-200 cursor-pointer transition"
                        >
                          <div className="flex justify-between items-start">
                            <div className="flex-1">
                              <div className="flex items-center gap-2 mb-2">
                                <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium ${statusConfig.bg} ${statusConfig.text}`}>
                                  <span className={`w-1.5 h-1.5 rounded-full ${statusConfig.dot}`}></span>
                                  {interview.status_display}
                                </span>
                                <span className="text-xs text-gray-400 font-mono">
                                  {interview.room_code}
                                </span>
                              </div>
                              <p className="font-medium text-gray-800">
                                {interview.candidate?.username}
                                <span className="text-gray-400 font-normal"> interviewed by </span>
                                {interview.interviewer?.username}
                              </p>
                              <p className="text-sm text-gray-500 mt-1">
                                Topics: {interview.topics?.join(', ')}
                              </p>
                            </div>
                            <div className="text-right ml-4">
                              {interview.overall_score > 0 && (
                                <div className="bg-blue-50 rounded-lg px-3 py-2 text-center">
                                  <p className="text-2xl font-bold text-blue-600">
                                    {interview.overall_score}
                                  </p>
                                  <p className="text-xs text-blue-400">/ 10</p>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </>
            )}

            {activeTab === 'reports' && (
              <>
                {reports.length === 0 ? (
                  <div className="text-center py-12">
                    <p className="text-4xl mb-3">📊</p>
                    <p className="text-gray-500">No reports yet</p>
                  </div>
                ) : (
                  <div className="space-y-3">
                    {reports.map((report) => {
                      const recConfig = getRecommendationConfig(report.recommendation);
                      return (
                        <div
                          key={report.id}
                          className={`border rounded-xl p-4 ${recConfig.bg} ${recConfig.border}`}
                        >
                          <div className="flex justify-between items-center">
                            <div>
                              <p className="font-semibold text-gray-800">
                                {report.candidate_name}
                              </p>
                              <p className="text-sm text-gray-500">
                                Interviewed by {report.interviewer_name}
                              </p>
                            </div>
                            <div className="text-right">
                              <p className="text-2xl font-bold text-gray-800">
                                {report.overall_score}
                                <span className="text-sm font-normal text-gray-500">/10</span>
                              </p>
                              <p className={`text-sm font-semibold ${recConfig.color}`}>
                                {report.recommendation_display}
                              </p>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}