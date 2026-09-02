import React from 'react';
import type { InferenceResult } from '../types';
import { ShieldAlert, ShieldCheck, FileText, Image as ImageIcon, Sparkles } from 'lucide-react';

interface Props {
  result: InferenceResult | null;
}

export const ResultPanel: React.FC<Props> = ({ result }) => {
  if (!result) {
    return (
      <div className="card" style={{ opacity: 0.6 }}>
        <h3 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-muted)' }}>
          Simulated Demonstration Outcome
        </h3>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-subtle)', marginTop: '8px' }}>
          Submit an email above to view simulated classification, signal breakdown, and explanation.
        </p>
      </div>
    );
  }

  const isSpam = result.simulated_label === 'SPAM';
  const pct = (result.simulated_spam_probability * 100).toFixed(0);

  return (
    <div className="card" style={{ border: `1px solid ${isSpam ? 'rgba(239, 68, 68, 0.4)' : 'rgba(16, 185, 129, 0.4)'}` }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-main)' }}>
          Demonstration Outcome & Signals
        </h3>
        <span className={isSpam ? 'badge badge-spam' : 'badge badge-legit'} style={{ fontSize: '0.9rem', padding: '6px 14px' }}>
          {isSpam ? 'SIMULATED SPAM' : 'SIMULATED LEGITIMATE'}
        </span>
      </div>

      {/* Main Score Box */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '20px',
          padding: '16px 20px',
          background: isSpam ? 'rgba(239, 68, 68, 0.08)' : 'rgba(16, 185, 129, 0.08)',
          borderRadius: '8px',
          border: `1px solid ${isSpam ? 'rgba(239, 68, 68, 0.2)' : 'rgba(16, 185, 129, 0.2)'}`,
          marginBottom: '20px',
        }}
      >
        {isSpam ? (
          <ShieldAlert size={40} color="#f87171" style={{ flexShrink: 0 }} />
        ) : (
          <ShieldCheck size={40} color="#34d399" style={{ flexShrink: 0 }} />
        )}

        <div style={{ flexGrow: 1 }}>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: '8px' }}>
            <span style={{ fontSize: '1.8rem', fontWeight: 700, color: isSpam ? '#f87171' : '#34d399' }}>
              {pct}%
            </span>
            <span style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Simulated Spam Probability
            </span>
          </div>

          <div style={{ background: '#334155', height: '6px', borderRadius: '3px', marginTop: '6px', overflow: 'hidden' }}>
            <div
              style={{
                width: `${pct}%`,
                height: '100%',
                background: isSpam ? '#ef4444' : '#10b981',
                transition: 'width 0.4s ease',
              }}
            />
          </div>
        </div>
      </div>

      {/* Detected Signals Grid */}
      <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '10px', textTransform: 'uppercase' }}>
        Detected Content Signals
      </h4>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '10px', marginBottom: '16px' }}>
        <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-color)', borderRadius: '6px', padding: '10px 12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px', color: '#60a5fa', fontSize: '0.75rem', fontWeight: 600 }}>
            <FileText size={14} />
            <span>TEXT SIGNALS</span>
          </div>
          <ul style={{ fontSize: '0.8rem', color: 'var(--text-main)', paddingLeft: '16px' }}>
            {result.detected_signals.text.map((sig, i) => (
              <li key={i}>{sig}</li>
            ))}
          </ul>
        </div>

        <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-color)', borderRadius: '6px', padding: '10px 12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px', color: '#34d399', fontSize: '0.75rem', fontWeight: 600 }}>
            <ImageIcon size={14} />
            <span>IMAGE SIGNALS</span>
          </div>
          <ul style={{ fontSize: '0.8rem', color: 'var(--text-main)', paddingLeft: '16px' }}>
            {result.detected_signals.image.map((sig, i) => (
              <li key={i}>{sig}</li>
            ))}
          </ul>
        </div>

        <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-color)', borderRadius: '6px', padding: '10px 12px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px', color: '#c084fc', fontSize: '0.75rem', fontWeight: 600 }}>
            <Sparkles size={14} />
            <span>CROSS-MODAL SIGNALS</span>
          </div>
          <ul style={{ fontSize: '0.8rem', color: 'var(--text-main)', paddingLeft: '16px' }}>
            {result.detected_signals.crossmodal.map((sig, i) => (
              <li key={i}>{sig}</li>
            ))}
          </ul>
        </div>
      </div>

      {/* Explanation text */}
      <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-color)', borderRadius: '6px', padding: '12px', fontSize: '0.85rem', color: 'var(--text-muted)' }}>
        <strong style={{ color: 'var(--text-main)' }}>Pipeline Decision Explanation: </strong>
        {result.explanation}
      </div>
    </div>
  );
};
