import React from 'react';
import type { InferenceResult } from '../types';
import { ArrowLeftRight, AlertCircle } from 'lucide-react';

interface Props {
  result: InferenceResult | null;
}

export const CrossAttentionVisualization: React.FC<Props> = ({ result }) => {
  if (!result || result.modality !== 'multimodal') {
    return null;
  }

  return (
    <div className="card" style={{ marginBottom: '24px', border: '1px solid rgba(168, 85, 247, 0.4)' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <ArrowLeftRight size={20} color="#c084fc" />
          <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-main)' }}>
            Cross-Modal Feature Interaction (Multimodal Route Active)
          </h3>
        </div>
        <span className="badge badge-multimodal">2x Cross-Attention Layers</span>
      </div>

      <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
        In the DCAT architecture, textual tokens and visual feature patches interact bidirectionally across attention layers prior to mean pooling.
      </p>

      {/* Token Linkage Visualization Grid */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '12px', marginBottom: '16px' }}>
        {result.cross_attention_pairs.map((pair, idx) => (
          <div
            key={idx}
            style={{
              padding: '12px 14px',
              background: 'var(--bg-main)',
              border: '1px solid var(--border-color)',
              borderRadius: '8px',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
            }}
          >
            <div style={{ display: 'flex', flexDirection: 'column' }}>
              <span style={{ fontSize: '0.7rem', color: '#60a5fa', textTransform: 'uppercase' }}>Text Token</span>
              <span className="mono" style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-main)' }}>
                "{pair.text_token}"
              </span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '0 8px' }}>
              <ArrowLeftRight size={16} color="#c084fc" />
              <span style={{ fontSize: '0.65rem', color: '#c084fc', fontWeight: 700 }}>{(pair.strength * 100).toFixed(0)}%</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', textAlign: 'right' }}>
              <span style={{ fontSize: '0.7rem', color: '#34d399', textTransform: 'uppercase' }}>Image Patch / OCR</span>
              <span className="mono" style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--text-main)' }}>
                "{pair.image_token}"
              </span>
            </div>
          </div>
        ))}
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.75rem', color: 'var(--text-subtle)', background: 'rgba(15, 23, 42, 0.6)', padding: '8px 12px', borderRadius: '6px' }}>
        <AlertCircle size={14} color="#f59e0b" />
        <span>
          <strong>Research Note:</strong> Illustrative interaction map for concept demonstration — not actual model attention weights.
        </span>
      </div>
    </div>
  );
};
