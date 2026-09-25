import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Brain, ArrowLeft } from 'lucide-react';
import { apiFetch } from '../lib/api';

const assessmentQuestions = [
  {
    domain: 'orientation',
    question_number: 1,
    label: 'What is today’s date and day?',
    max_score: 5,
    options: [
      { label: 'Completely correct', value: 5 },
      { label: 'Partially correct', value: 3 },
      { label: 'Needs support', value: 1 },
      { label: 'Incorrect', value: 0 },
    ],
  },
  {
    domain: 'praxis',
    question_number: 1,
    label: 'Please imitate the hand movement shown.',
    max_score: 2,
    options: [
      { label: 'Excellent imitation', value: 2 },
      { label: 'Partial imitation', value: 1 },
      { label: 'Not able', value: 0 },
    ],
  },
  {
    domain: 'drawing',
    question_number: 1,
    label: 'Please draw a clock face and set the hands to 10:10.',
    max_score: 3,
    options: [
      { label: 'Correct', value: 3 },
      { label: 'Mostly correct', value: 2 },
      { label: 'Needs prompts', value: 1 },
      { label: 'Incorrect', value: 0 },
    ],
  },
  {
    domain: 'judgement',
    question_number: 1,
    label: 'If you smelled smoke in the kitchen, what would you do first?',
    max_score: 4,
    options: [
      { label: 'Correct response', value: 4 },
      { label: 'Reasonable action', value: 2 },
      { label: 'Needs guidance', value: 1 },
      { label: 'Not safe', value: 0 },
    ],
  },
  {
    domain: 'memory',
    question_number: 1,
    label: 'Recall the five words from the earlier prompt.',
    max_score: 8,
    options: [
      { label: '5 words recalled', value: 8 },
      { label: '4 words', value: 6 },
      { label: '3 words', value: 4 },
      { label: '2 or fewer', value: 2 },
      { label: 'No recall', value: 0 },
    ],
  },
  {
    domain: 'language',
    question_number: 1,
    label: 'Name the object shown and explain its use.',
    max_score: 8,
    options: [
      { label: 'Clear and accurate', value: 8 },
      { label: 'Mostly accurate', value: 6 },
      { label: 'Partial answer', value: 4 },
      { label: 'Needs support', value: 2 },
      { label: 'Unable to answer', value: 0 },
    ],
  },
];

function BaselineAssessmentPage() {
  const navigate = useNavigate();
  const [scores, setScores] = useState(() => Object.fromEntries(assessmentQuestions.map((q) => [q.domain, String(q.max_score)])));
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const totalScore = useMemo(
    () => Object.values(scores).reduce((sum, value) => sum + Number(value), 0),
    [scores]
  );

  const handleChange = (domain, value) => {
    setScores((current) => ({ ...current, [domain]: value }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      const payload = {
        responses: assessmentQuestions.map((question) => ({
          domain: question.domain,
          question_number: question.question_number,
          response_value: String(scores[question.domain]),
          score: Number(scores[question.domain]),
          max_score: question.max_score,
          notes: `Baseline score for ${question.domain}`,
        })),
      };

      const result = await apiFetch('/api/assessments/baseline', {
        method: 'POST',
        body: payload,
      });

      const userMatch = JSON.parse(localStorage.getItem('smritisaathi_user') || '{}');
      const nextUser = { ...userMatch, baseline_completed: true };
      localStorage.setItem('smritisaathi_user', JSON.stringify(nextUser));
      navigate('/dashboard');

      if (result?.id) {
        return;
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container" style={{ maxWidth: '900px', paddingTop: '2rem', paddingBottom: '3rem' }}>
      <div className="card flex-col gap-lg">
        <div className="flex items-center gap-md" style={{ justifyContent: 'space-between' }}>
          <button className="btn btn-secondary" type="button" onClick={() => navigate('/dashboard')} style={{ minWidth: 'auto', padding: '0.7rem 1rem' }}>
            <ArrowLeft size={18} /> Back
          </button>
          <div className="flex items-center gap-sm" style={{ color: 'var(--color-primary)' }}>
            <Brain size={24} />
            <strong>RUDAS baseline</strong>
          </div>
        </div>

        <div className="text-center">
          <h1 className="title">Patient baseline assessment</h1>
          <p className="text-muted">This is a one-time baseline check to understand current cognitive function. It helps tailor future activities and updates.</p>
        </div>

        <div className="card" style={{ background: '#F8FAFC', border: '1px solid #E2E8F0' }}>
          <strong>Total score so far:</strong> {totalScore} / 30
        </div>

        <form className="flex-col gap-lg" onSubmit={handleSubmit}>
          {assessmentQuestions.map((question) => (
            <div key={`${question.domain}-${question.question_number}`} className="card" style={{ background: '#fff', border: '1px solid #E2E8F0' }}>
              <h2 className="subtitle" style={{ marginBottom: '0.75rem' }}>{question.label}</h2>
              <div className="flex-col gap-sm">
                {question.options.map((option) => (
                  <label key={`${question.domain}-${option.value}`} className="flex gap-sm items-center" style={{ padding: '0.3rem 0' }}>
                    <input
                      type="radio"
                      name={question.domain}
                      value={String(option.value)}
                      checked={String(scores[question.domain]) === String(option.value)}
                      onChange={() => handleChange(question.domain, String(option.value))}
                    />
                    <span>{option.label}</span>
                  </label>
                ))}
              </div>
            </div>
          ))}

          {error ? <div className="card" style={{ border: '1px solid var(--color-error)', color: 'var(--color-error)', background: '#FEE2E2' }}>{error}</div> : null}

          <button className="btn btn-primary" type="submit" disabled={loading}>
            {loading ? 'Saving baseline...' : 'Submit baseline'}
          </button>
        </form>
      </div>
    </div>
  );
}

export default BaselineAssessmentPage;
