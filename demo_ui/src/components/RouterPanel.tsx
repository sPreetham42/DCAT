import React from 'react';
import type { InferenceResult } from '../types';
import { CheckCircle2, XCircle } from 'lucide-react';

interface Props {
  result: InferenceResult | null;
}

export const RouterPanel: React.FC<Props> = ({ result }) => {
  if (!result) {
    return (
      <div className="card" style={{ opacity: 0.6 }}>
        <h3 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-muted)' }}>
          Modality Router & Execution Status
        </h3>
        <p style={{ fontSize: '0.85rem', color: 'var(--text-subtle)', marginTop: '8px' }}>
          Submit an email above to view real-time content detection & conditional route selection.
        </p>
      </div>
    );
  }

  const getRouteBadgeClass = (mod: string) => {
    switch (mod) {
      case 'text':
        return 'badge badge-text';
      case 'image':
        return 'badge badge-image';
      case 'multimodal':
        return 'badge badge-multimodal';
      default:
        return 'badge badge-empty';
    }
  };

  return (
    <div className="card">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-main)' }}>
          Modality Router & Execution Status
        </h3>
        <span className={getRouteBadgeClass(result.modality)} style={{ fontSize: '0.85rem', padding: '6px 12px' }}>
          SELECTED ROUTE: {result.modality.toUpperCase()}
        </span>
      </div>

      {/* Content Detection Flags */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', marginBottom: '20px', background: 'var(--bg-main)', padding: '14px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
        <div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Text Modality Flag</span>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '4px' }}>
            {result.has_text ? (
              <>
                <CheckCircle2 size={18} color="#34d399" />
                <span style={{ fontWeight: 600, fontSize: '0.9rem', color: '#34d399' }}>Meaningful Text Present</span>
              </>
            ) : (
              <>
                <XCircle size={18} color="#94a3b8" />
                <span style={{ fontSize: '0.9rem', color: '#94a3b8' }}>Text Absent / Below Threshold</span>
              </>
            )}
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-subtle)' }}>{result.text_length} characters</span>
        </div>

        <div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', textTransform: 'uppercase' }}>Vision Modality Flag</span>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginTop: '4px' }}>
            {result.has_meaningful_image ? (
              <>
                <CheckCircle2 size={18} color="#34d399" />
                <span style={{ fontWeight: 600, fontSize: '0.9rem', color: '#34d399' }}>Meaningful Image Present</span>
              </>
            ) : (
              <>
                <XCircle size={18} color="#94a3b8" />
                <span style={{ fontSize: '0.9rem', color: '#94a3b8' }}>Image Absent / Filtered</span>
              </>
            )}
          </div>
          <span style={{ fontSize: '0.75rem', color: 'var(--text-subtle)' }}>
            {result.image_count} extracted ({result.filtered_image_count} filtered tracking pixels)
          </span>
        </div>
      </div>

      {/* Pipeline Checklist */}
      <h4 style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '10px', textTransform: 'uppercase' }}>
        Conditional Execution Checklist
      </h4>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {result.pipeline_steps.map((step, idx) => {
          const isExecuted = step.status === 'executed';
          return (
            <div
              key={idx}
              style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                padding: '10px 14px',
                background: isExecuted ? 'rgba(30, 41, 59, 0.8)' : 'rgba(15, 23, 42, 0.4)',
                border: `1px solid ${isExecuted ? 'rgba(59, 130, 246, 0.3)' : 'rgba(51, 65, 85, 0.4)'}`,
                borderRadius: '6px',
                opacity: isExecuted ? 1 : 0.45,
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                {isExecuted ? (
                  <CheckCircle2 size={16} color="#38bdf8" />
                ) : (
                  <XCircle size={16} color="#64748b" />
                )}
                <div>
                  <span style={{ fontWeight: 600, fontSize: '0.85rem', color: isExecuted ? 'var(--text-main)' : 'var(--text-subtle)' }}>
                    {step.name}
                  </span>
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{step.description}</p>
                </div>
              </div>

              <span
                style={{
                  fontSize: '0.7rem',
                  fontWeight: 700,
                  textTransform: 'uppercase',
                  padding: '2px 8px',
                  borderRadius: '4px',
                  background: isExecuted ? 'rgba(56, 189, 248, 0.15)' : 'rgba(100, 116, 139, 0.15)',
                  color: isExecuted ? '#38bdf8' : '#64748b',
                }}
              >
                {step.status.toUpperCase()}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
