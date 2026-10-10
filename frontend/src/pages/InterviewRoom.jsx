import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { interviewAPI } from '../services/api';

export default function InterviewRoom() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [interview, setInterview] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [answer, setAnswer] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [aiScore, setAiScore] = useState(null);
  const [aiFeedback, setAiFeedback] = useState('');
  const [ending, setEnding] = useState(false);
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  useEffect(() => {
    fetchInterview();
  }, [id]);

  const fetchInterview = async () => {
    try {
      const response = await interviewAPI.get(id);
      setInterview(response.data);
      const questions = response.data.interview_questions || [];
      if (questions.length > 0) {
        const unanswered = questions.find(q => !q.candidate_answer);
        setCurrentQuestion(unanswered || questions[questions.length - 1]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!answer.trim() || !currentQuestion) return;
    setSubmitting(true);
    try {
      const response = await interviewAPI.submitAnswer(
        id,
        currentQuestion.id,
        {
          candidate_answer: answer,
          time_taken_seconds: 60,
        }
      );
      const iq = response.data.interview_question;
      setAiScore(iq.ai_score);
      setAiFeedback(iq.ai_feedback);
      setSubmitted(true);
      fetchInterview();
    } catch (err) {
      alert(err.response?.data?.error || 'Failed to submit answer');
    } finally {
      setSubmitting(false);
    }
  };

  const handleEndInterview = async () => {
    setEnding(true);
    try {
      await interviewAPI.updateStatus(id, {
        status: 'completed',
        interviewer_notes: 'Interview completed via HireLinq',
      });
      navigate('/dashboard');
    } catch (err) {
      alert('Failed to end interview');
      setEnding(false);
    }
  };

  if (!interview) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-500">Loading interview room...</p>
        </div>
      </div>
    );
  }

  const isInterviewer = interview.interviewer?.id === user.id;
  const isCandidate = interview.candidate?.id === user.id;

  const getScoreColor = (score) => {
    if (score >= 8) return 'text-green-600';
    if (score >= 6) return 'text-blue-600';
    if (score >= 4) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreBg = (score) => {
    if (score >= 8) return 'bg-green-50 border-green-200';
    if (score >= 6) return 'bg-blue-50 border-blue-200';
    if (score >= 4) return 'bg-yellow-50 border-yellow-200';
    return 'bg-red-50 border-red-200';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white border-b border-gray-200 px-6 py-4">
        <div className="max-w-5xl mx-auto flex justify-between items-center">
          <div className="flex items-center gap-4">
            <h1 className="text-xl font-bold text-blue-600">HireLinq</h1>
            <span className="bg-gray-100 text-gray-700 px-3 py-1 rounded-full font-mono text-sm font-semibold">
              {interview.room_code}
            </span>
          </div>
          <div className="flex items-center gap-3">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
              interview.status === 'in_progress'
                ? 'bg-green-100 text-green-700'
                : 'bg-blue-100 text-blue-700'
            }`}>
              ● {interview.status_display}
            </span>
            {isInterviewer && (
              <button
                onClick={handleEndInterview}
                disabled={ending}
                className="bg-red-500 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-600 transition disabled:opacity-50"
              >
                {ending ? 'Ending...' : 'End Interview'}
              </button>
            )}
            <button
              onClick={() => navigate('/dashboard')}
              className="text-gray-500 hover:text-gray-700 text-sm"
            >
              ← Back
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-5xl mx-auto p-6">
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-white rounded-xl border border-gray-100 p-4 flex items-center gap-3">
            <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center text-purple-600 font-bold">
              {interview.candidate?.username?.[0]?.toUpperCase()}
            </div>
            <div>
              <p className="text-xs text-gray-500">Candidate</p>
              <p className="font-semibold text-gray-800">{interview.candidate?.username}</p>
            </div>
          </div>
          <div className="bg-white rounded-xl border border-gray-100 p-4 flex items-center gap-3">
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center text-blue-600 font-bold">
              {interview.interviewer?.username?.[0]?.toUpperCase()}
            </div>
            <div>
              <p className="text-xs text-gray-500">Interviewer</p>
              <p className="font-semibold text-gray-800">{interview.interviewer?.username}</p>
            </div>
          </div>
          <div className="bg-white rounded-xl border border-gray-100 p-4">
            <p className="text-xs text-gray-500 mb-1">Topics</p>
            <div className="flex flex-wrap gap-1">
              {interview.topics?.map((topic) => (
                <span key={topic} className="bg-blue-50 text-blue-600 text-xs px-2 py-0.5 rounded">
                  {topic}
                </span>
              ))}
            </div>
          </div>
        </div>

        {currentQuestion ? (
          <div className="bg-white rounded-xl border border-gray-100 shadow-sm p-6">
            <div className="flex justify-between items-start mb-6">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full font-medium">
                    {currentQuestion.question?.topic_display}
                  </span>
                  <span className="bg-orange-100 text-orange-700 text-xs px-2 py-1 rounded-full font-medium">
                    {currentQuestion.question?.difficulty_display}
                  </span>
                  <span className="bg-gray-100 text-gray-600 text-xs px-2 py-1 rounded-full">
                    Q{currentQuestion.order}
                  </span>
                </div>
                <h2 className="text-xl font-bold text-gray-800">
                  {currentQuestion.question?.title}
                </h2>
              </div>
            </div>

            <p className="text-gray-600 mb-6 bg-gray-50 rounded-lg p-4">
              {currentQuestion.question?.description}
            </p>

            {isCandidate && !submitted && !currentQuestion.candidate_answer && (
              <div>
                <label className="block text-gray-700 font-medium mb-2">
                  Your Answer
                </label>
                <textarea
                  className="w-full border border-gray-300 rounded-xl p-4 h-48 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none transition"
                  placeholder="Type your detailed answer here..."
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                />
                <div className="flex justify-between items-center mt-3">
                  <p className="text-sm text-gray-400">{answer.length} characters</p>
                  <button
                    onClick={handleSubmitAnswer}
                    disabled={submitting || answer.trim().length < 10}
                    className="bg-blue-600 text-white px-8 py-3 rounded-xl font-semibold hover:bg-blue-700 transition disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {submitting ? (
                      <span className="flex items-center gap-2">
                        <svg className="animate-spin h-4 w-4" viewBox="0 0 24 24" fill="none">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
                        </svg>
                        Evaluating...
                      </span>
                    ) : 'Submit Answer →'}
                  </button>
                </div>
              </div>
            )}

            {(submitted || currentQuestion.candidate_answer) && (
              <div className="space-y-4">
                {aiScore !== null && (
                  <div className={`border rounded-xl p-5 ${getScoreBg(aiScore)}`}>
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-semibold text-gray-800">🤖 AI Evaluation</h3>
                      <div className="flex items-center gap-2">
                        <span className={`text-3xl font-bold ${getScoreColor(aiScore)}`}>
                          {aiScore}
                        </span>
                        <span className="text-gray-400">/10</span>
                      </div>
                    </div>
                    {aiFeedback && (
                      <p className="text-gray-600 text-sm">{aiFeedback}</p>
                    )}
                  </div>
                )}

                {isInterviewer && currentQuestion.candidate_answer && (
                  <div className="bg-gray-50 rounded-xl p-5">
                    <h3 className="font-semibold text-gray-700 mb-3">
                      Candidate's Answer:
                    </h3>
                    <p className="text-gray-600">{currentQuestion.candidate_answer}</p>
                    {currentQuestion.ai_score !== null && (
                      <div className={`mt-4 border rounded-lg p-4 ${getScoreBg(currentQuestion.ai_score)}`}>
                        <div className="flex justify-between items-center">
                          <span className="font-medium text-gray-700">AI Score</span>
                          <span className={`text-2xl font-bold ${getScoreColor(currentQuestion.ai_score)}`}>
                            {currentQuestion.ai_score}/10
                          </span>
                        </div>
                        <p className="text-sm text-gray-600 mt-2">
                          {currentQuestion.ai_feedback}
                        </p>
                      </div>
                    )}
                  </div>
                )}
              </div>
            )}
          </div>
        ) : (
          <div className="bg-white rounded-xl border border-gray-100 p-12 text-center">
            <p className="text-5xl mb-4">📝</p>
            <p className="text-gray-500 text-lg">No questions added yet</p>
            {isInterviewer && (
              <p className="text-blue-600 mt-2 text-sm">
                Add questions from the API to begin the interview
              </p>
            )}
          </div>
        )}
      </div>
    </div>
  );
}