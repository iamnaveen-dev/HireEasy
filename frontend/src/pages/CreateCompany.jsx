import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function CreateCompany() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    industry: 'technology',
    size: '1-10',
    website: '',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const token = localStorage.getItem('access_token');
      await axios.post(
        'http://127.0.0.1:8000/api/companies/create/',
        formData,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      navigate('/dashboard');
    } catch (err) {
      const errors = err.response?.data;
      if (typeof errors === 'object') {
        const first = Object.values(errors)[0];
        setError(Array.isArray(first) ? first[0] : first);
      } else {
        setError('Failed to create company');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-2xl mx-auto flex justify-between items-center">
          <h1 className="text-xl font-bold text-blue-600">HireLinq</h1>
          <button
            onClick={() => navigate('/dashboard')}
            className="text-gray-500 hover:text-gray-700 text-sm"
          >
            ← Back
          </button>
        </div>
      </nav>

      <div className="max-w-2xl mx-auto p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-800">
            Register Your Company
          </h2>
          <p className="text-gray-500 mt-1">
            Set up your company to start scheduling interviews
          </p>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl mb-6">
            ⚠️ {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="bg-white rounded-xl border border-gray-100 p-6 space-y-5">
          <div>
            <label className="block text-gray-600 text-sm font-medium mb-2">
              Company Name
            </label>
            <input
              type="text"
              className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="e.g. TechCorp India"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              required
            />
          </div>

          <div>
            <label className="block text-gray-600 text-sm font-medium mb-2">
              Description
            </label>
            <textarea
              className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 h-24 resize-none"
              placeholder="What does your company do?"
              value={formData.description}
              onChange={(e) => setFormData({...formData, description: e.target.value})}
            />
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-gray-600 text-sm font-medium mb-2">
                Industry
              </label>
              <select
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={formData.industry}
                onChange={(e) => setFormData({...formData, industry: e.target.value})}
              >
                <option value="technology">Technology</option>
                <option value="finance">Finance</option>
                <option value="healthcare">Healthcare</option>
                <option value="education">Education</option>
                <option value="ecommerce">E-Commerce</option>
                <option value="startup">Startup</option>
                <option value="consulting">Consulting</option>
                <option value="other">Other</option>
              </select>
            </div>
            <div>
              <label className="block text-gray-600 text-sm font-medium mb-2">
                Company Size
              </label>
              <select
                className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={formData.size}
                onChange={(e) => setFormData({...formData, size: e.target.value})}
              >
                <option value="1-10">1-10 employees</option>
                <option value="11-50">11-50 employees</option>
                <option value="51-200">51-200 employees</option>
                <option value="201-500">201-500 employees</option>
                <option value="1000+">1000+ employees</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-gray-600 text-sm font-medium mb-2">
              Website (optional)
            </label>
            <input
              type="url"
              className="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="https://yourcompany.com"
              value={formData.website}
              onChange={(e) => setFormData({...formData, website: e.target.value})}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-4 rounded-xl font-bold text-lg hover:bg-blue-700 transition disabled:opacity-50"
          >
            {loading ? 'Creating...' : 'Register Company →'}
          </button>
        </form>
      </div>
    </div>
  );
}