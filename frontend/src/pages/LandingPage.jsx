import React from 'react';
import { Link } from 'react-router-dom';
import { Heart, Brain, Bell, Users, Volume2 } from 'lucide-react';

const LandingPage = () => {
  return (
    <div className="container flex-col gap-lg" style={{ minHeight: '100vh', paddingBottom: '3rem' }}>
      
      {/* Header / Logo */}
      <header className="flex flex-col items-center text-center" style={{ marginTop: '2rem' }}>
        <Heart size={64} color="var(--color-primary)" />
        <h1 className="title" style={{ fontSize: '3rem', margin: '1rem 0' }}>SmritiSaathi</h1>
        <p className="subtitle text-muted" style={{ maxWidth: '800px', margin: '0 auto' }}>
          SmritiSaathi helps older adults stay engaged through simple cognitive games, memory aids, reminders, and caregiver-supported progress tracking.
        </p>
      </header>

      {/* Accessibility / Voice Option Placeholder */}
      <div className="flex justify-center" style={{ marginTop: '1rem' }}>
        <button className="btn btn-secondary" aria-label="Turn on voice assistance">
          <Volume2 size={24} /> Enable Voice Assistance
        </button>
      </div>

      <hr style={{ border: '1px solid #E2E8F0', margin: '2rem 0' }} />

      {/* Main Actions */}
      <div className="grid grid-cols-2 gap-lg" style={{ maxWidth: '900px', margin: '0 auto' }}>
        
        {/* Patient Section */}
        <div className="card flex-col items-center text-center gap-md">
          <Brain size={48} color="var(--color-secondary)" />
          <h2 className="title" style={{ fontSize: '1.75rem', marginBottom: 0 }}>For Patients</h2>
          <p className="text-muted" style={{ minHeight: '80px' }}>
            Play games, view family memories, and check your daily reminders.
          </p>
          <div className="flex-col gap-sm" style={{ width: '100%' }}>
            <Link to="/login/patient" className="btn btn-primary btn-block">Patient Login</Link>
            <Link to="/register/patient" className="btn btn-secondary btn-block">Register as Patient</Link>
          </div>
        </div>

        {/* Caregiver Section */}
        <div className="card flex-col items-center text-center gap-md">
          <Users size={48} color="var(--color-primary-light)" />
          <h2 className="title" style={{ fontSize: '1.75rem', marginBottom: 0 }}>For Caregivers</h2>
          <p className="text-muted" style={{ minHeight: '80px' }}>
            Support your loved ones, manage reminders, and view progress securely.
          </p>
          <div className="flex-col gap-sm" style={{ width: '100%' }}>
            <Link to="/login/caregiver" className="btn btn-primary btn-block" style={{ backgroundColor: 'var(--color-primary-light)' }}>Caregiver Login</Link>
            <Link to="/register/caregiver" className="btn btn-secondary btn-block">Register as Caregiver</Link>
          </div>
        </div>

      </div>

      <hr style={{ border: '1px solid #E2E8F0', margin: '2rem 0' }} />

      {/* Features & Disclaimers */}
      <div className="flex-col gap-md" style={{ maxWidth: '800px', margin: '0 auto' }}>
        <h3 className="subtitle text-center">What we provide:</h3>
        <div className="grid grid-cols-2 gap-md">
          <div className="card">
            <strong>Cognitive Engagement:</strong> Simple, culturally familiar games adapted to your comfort level.
          </div>
          <div className="card">
            <strong>Memory Aids:</strong> Keep photos and names of loved ones close to you.
          </div>
          <div className="card">
            <strong>Daily Reminders:</strong> Never miss your medicine, hydration, or appointments.
          </div>
          <div className="card">
            <strong>Caregiver Support:</strong> Authorized family members can help manage routines.
          </div>
        </div>
        
        <div className="card text-center" style={{ backgroundColor: '#FEF3C7', border: '1px solid #F59E0B', marginTop: '1rem' }}>
          <p style={{ color: '#92400E', fontWeight: 600 }}>
            Important: The platform is designed for accessibility and low-complexity use. It supports cognitive engagement and monitoring but does not provide a medical diagnosis.
          </p>
        </div>
      </div>
      
    </div>
  );
};

export default LandingPage;
