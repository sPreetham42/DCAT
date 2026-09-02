import React from 'react';
import type { InferenceResult } from '../types';
import { Cpu, Zap } from 'lucide-react';

interface Props {
  result: InferenceResult | null;
}

export const ComputationComparison: React.FC<Props> = ({ result }) => {
  const isTextOnly = result?.modality === 'text';
  const isImageOnly = result?.modality === 'image';
  const isMultimodal = result?.modality === 'multimodal';

  return (
    <div className="card" style={{ marginBottom: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
        <Zap size={20} color="var(--accent-amber)" />
        <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-main)' }}>
          Conditional Computation Savings Model
        </h3>
      </div>

      <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '16px' }}>
        Comparison showing how DCAT avoids invoking unnecessary neural network encoders when email modalities are absent.
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
        {/* Conventional Pipeline Box */}
        <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '10px' }}>
            <Cpu size={16} color="#94a3b8" />
            <span style={{ fontWeight: 600, fontSize: '0.85rem', color: '#94a3b8' }}>
              Conventional Multimodal Pipeline
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '0.8rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px' }}>
              <span>Text Encoder (DistilBERT)</span>
              <span style={{ color: '#38bdf8', fontWeight: 600 }}>ALWAYS RUN</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px' }}>
              <span>Vision Encoder (MobileViT)</span>
              <span style={{ color: '#38bdf8', fontWeight: 600 }}>ALWAYS RUN (or fake 0.5 input)</span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px' }}>
              <span>Fusion Network</span>
              <span style={{ color: '#38bdf8', fontWeight: 600 }}>ALWAYS RUN</span>
            </div>
          </div>
          <p style={{ fontSize: '0.75rem', color: '#ef4444', marginTop: '10px' }}>
            ⚠️ Wastes GPU memory & latency executing vision models on text-only emails.
          </p>
        </div>

        {/* Proposed DCAT Pipeline Box */}
        <div style={{ background: 'rgba(59, 130, 246, 0.08)', border: '1px solid rgba(59, 130, 246, 0.3)', borderRadius: '8px', padding: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '10px' }}>
            <Zap size={16} color="#60a5fa" />
            <span style={{ fontWeight: 600, fontSize: '0.85rem', color: '#60a5fa' }}>
              Proposed DCAT Conditional Pipeline
            </span>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', fontSize: '0.8rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px' }}>
              <span>Text Encoder</span>
              <span style={{ color: isImageOnly ? '#f43f5e' : '#34d399', fontWeight: 600 }}>
                {isImageOnly ? 'SKIPPED' : 'RUN'}
              </span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px' }}>
              <span>Vision Encoder</span>
              <span style={{ color: isTextOnly ? '#f43f5e' : '#34d399', fontWeight: 600 }}>
                {isTextOnly ? 'SKIPPED' : 'RUN'}
              </span>
            </div>
            <div style={{ display: 'flex', justifyContent: 'space-between', padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px' }}>
              <span>Cross-Attention</span>
              <span style={{ color: isMultimodal ? '#34d399' : '#f43f5e', fontWeight: 600 }}>
                {isMultimodal ? 'RUN' : 'SKIPPED'}
              </span>
            </div>
          </div>

          <p style={{ fontSize: '0.75rem', color: '#34d399', marginTop: '10px', fontWeight: 600 }}>
            ✓ {result ? result.computation_saved_description : 'Dynamic content routing bypasses unused encoders.'}
          </p>
        </div>
      </div>
    </div>
  );
};
