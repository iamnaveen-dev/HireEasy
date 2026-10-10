import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { interviewAPI } from '../services/api';

export default function CreateInterview() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    candidate_email: '',
    interview_type: 'technical',
    topics: [],
    difficulty_level: 'medium',
    scheduled_at: '',
    duration_minutes: 60,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [roomCode, setRoomCode] = useState('');

  const topicOptions = [
    'python', 'django', 'javascript', 'react',
    'nodejs', 'sql', 'mysql', 'postgresql',
    'dsa', 'system_design', 'aws', 'docker',
  ];

  const handleTopicToggle = (topic) => {
    setFormData((prev) => ({
      ...prev,
      topics: prev.topics.includes(topic)
        ? prev.topics.filter((t) => t !== topic)
        : [...prev.topics, topic],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.topics.length === 0) {
      setError('Please select at least one topic');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const response = await interviewAPI.create(formData);
      setRoomCode(response.data.room_code);
    } catch (err) {
      const errors = err.response?.data;
      if (typeof errors === 'object') {
        const first = Object.values(errors)[0];
        setError(Array.isArray(first) ? first[0] : first);
      } else {
        setError('Failed to create interview');
      }
    } finally {
      setLoading(false);
    }
  };

  if (roomCode) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-lg p-8 max-w-md w-full text-center">
          <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <span className="text-3xl">✅</span>
          </div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">
            Interview Scheduled!
          </h2>
          <p className="text-gray-500 mb-6">
            Share this room code with the candidate
          </p>
          <div className="bg-blue-50 border-2 border-blue-200 rounded-xl p-6 mb-6">
            <p className="text-sm text-blue-500 mb-2">Room Code</p>
            <p className="text-4xl font-bold font-mono text-blue-600 tracking-widest">
              {roomCode}
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => {
                navigator.clipboard.writeText(roomCode);
                alert('Room code copied!');
              }}
              className="flex-1 border border-blue-600 text-blue-600 py-3 rounded-xl font-semibold hover:bg-blue-50 transition"
            >
              Copy Code
            </button>
            <button
              onClick={() => navigate('/dashboard')}
              className="flex-1 bg-blue-600 text-white py-3 rounded-xl font-semibold hover:bg-blue-700 transition"
            >
              Go to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-3xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-blue-600">HireLinq</h1>
          <button
            onClick={() => navigate('/dashboard')}
            className="text-gray-500 hover:text-gray-700 text-sm"
          >
            ← Back to Dashboard
          </button>
        </div>
      </nav>

      <div className="max-w-3xl mx-auto p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-800">
            Schedule Interview
          </h2>
          <p className="text-gray-500 mt-1">
            Fill in the details to create a new interview session
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl mb-6">
            ⚠️ {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-white rounded-xl border border-gray-100 p-6">
            <h3 className="font-semibold text-gray-700 mb-4">
              Candidate Details
            </h3>
            <div>
              <label className="block text-gray-600 text-sm font-medium mb-2">
                Candidate Email
              </label>
              <input
                type="email"
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
                placeholder="candidate@email.com"
                value={formData.candidate_email}
                onChange={(e) => setFormData({...formData, candidate_email: e.target.value})}
                required
              />
              <p className="text-xs text-gray-400 mt-1">
                Candidate must be registered on HireLinq
              </p>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-gray-100 p-6">
            <h3 className="font-semibold text-gray-700 mb-4">
              Interview Settings
            </h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-600 text-sm font-medium mb-2">
                  Interview Type
                </label>
                <select
                  className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={formData.interview_type}
                  onChange={(e) => setFormData({...formData, interview_type: e.target.value})}
                >
                  <option value="technical">Technical</option>
                  <option value="behavioural">Behavioural</option>
                  <option value="system_design">System Design</option>
                  <option value="coding">Coding Round</option>
                  <option value="hr">HR Round</option>
                  <option value="mixed">Mixed</option>
                </select>
              </div>
              <div>
                <label className="block text-gray-600 text-sm font-medium mb-2">
                  Difficulty Level
                </label>
                <select
                  className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={formData.difficulty_level}
                  onChange={(e) => setFormData({...formData, difficulty_level: e.target.value})}
                >
                  <option value="easy">Easy</option>
                  <option value="medium">Medium</option>
                  <option value="hard">Hard</option>
                </select>
              </div>
              <div>
                <label className="block text-gray-600 text-sm font-medium mb-2">
                  Date and Time
                </label>
                <input
                  type="datetime-local"
                  className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={formData.scheduled_at}
                  onChange={(e) => setFormData({...formData, scheduled_at: e.target.value})}
                  required
                />
              </div>
              <div>
                <label className="block text-gray-600 text-sm font-medium mb-2">
                  Duration (minutes)
                </label>
                <select
                  className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  value={formData.duration_minutes}
                  onChange={(e) => setFormData({...formData, duration_minutes: parseInt(e.target.value)})}
                >
                  <option value={30}>30 minutes</option>
                  <option value={45}>45 minutes</option>
                  <option value={60}>60 minutes</option>
                  <option value={90}>90 minutes</option>
                  <option value={120}>120 minutes</option>
                </select>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl border border-gray-100 p-6">
            <h3 className="font-semibold text-gray-700 mb-4">
              Topics to Cover
            </h3>
            <div className="flex flex-wrap gap-2">
              {topicOptions.map((topic) => (
                <button
                  key={topic}
                  type="button"
                  onClick={() => handleTopicToggle(topic)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
                    formData.topics.includes(topic)
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                  }`}
                >
                  {topic}
                </button>
              ))}
            </div>
            {formData.topics.length > 0 && (
              <p className="text-sm text-blue-600 mt-3">
                Selected: {formData.topics.join(', ')}
              </p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-blue-700 transition disabled:opacity-50"
          >
            {loading ? 'Scheduling...' : 'Schedule Interview →'}
          </button>
        </form>
      </div>
    </div>
  );
}