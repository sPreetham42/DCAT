import type { InferenceResult } from '../types';

interface Props {
  result: InferenceResult | null;
}

export const ArchitectureDiagram: React.FC<Props> = ({ result }) => {
  const currentModality = result ? result.modality : null;

  const isTextActive = currentModality === 'text';
  const isImageActive = currentModality === 'image';
  const isMultimodalActive = currentModality === 'multimodal';

  return (
    <div className="card" style={{ marginBottom: '24px' }}>
      <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-main)', marginBottom: '4px' }}>
        DCAT Conditional Routing Architecture Diagram
      </h3>
      <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '20px' }}>
        Dynamic execution flow highlighting active vs bypassed neural modules based on detected email content.
      </p>

      <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '24px', position: 'relative' }}>
        {/* Flow Architecture Diagram Layout */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>

          {/* Top Stage */}
          <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
            <div style={{ padding: '8px 16px', background: '#334155', border: '1px solid #475569', borderRadius: '6px', fontSize: '0.8rem', fontWeight: 600 }}>
              RAW EMAIL
            </div>
            <span style={{ color: 'var(--text-subtle)' }}>→</span>
            <div style={{ padding: '8px 16px', background: '#334155', border: '1px solid #475569', borderRadius: '6px', fontSize: '0.8rem', fontWeight: 600 }}>
              MIME PARSER & PREPROCESSOR
            </div>
            <span style={{ color: 'var(--text-subtle)' }}>→</span>
            <div style={{ padding: '8px 16px', background: '#2563eb', border: '1px solid #3b82f6', color: 'white', borderRadius: '6px', fontSize: '0.8rem', fontWeight: 700 }}>
              MODALITY ROUTER
            </div>
          </div>

          <div style={{ height: '16px', width: '2px', background: 'var(--border-color)' }}></div>

          {/* Three Branch Routes */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '16px', width: '100%' }}>

            {/* TEXT ONLY BRANCH */}
            <div
              style={{
                border: `2px solid ${isTextActive ? '#3b82f6' : 'var(--border-color)'}`,
                borderRadius: '8px',
                padding: '14px',
                background: isTextActive ? 'rgba(59, 130, 246, 0.1)' : 'rgba(15, 23, 42, 0.3)',
                opacity: currentModality && !isTextActive ? 0.35 : 1,
                transition: 'all 0.3s ease',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <span style={{ fontWeight: 700, fontSize: '0.8rem', color: isTextActive ? '#60a5fa' : 'var(--text-muted)' }}>
                  TEXT ONLY ROUTE
                </span>
                {isTextActive && <span className="badge badge-text">ACTIVE</span>}
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.75rem' }}>
                <div style={{ padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px', border: '1px solid var(--border-color)' }}>
                  DistilBERT Text Encoder
                </div>
                <div style={{ padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px', border: '1px solid var(--border-color)' }}>
                  Text Projection (256-d)
                </div>
                <div style={{ padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px', border: '1px solid var(--border-color)' }}>
                  Mean Pooling
                </div>
                <div style={{ padding: '6px 10px', background: 'rgba(239, 68, 68, 0.1)', color: '#f87171', borderRadius: '4px', border: '1px border-dashed' }}>
                  ❌ MobileViT & Cross-Attention SKIPPED
                </div>
              </div>
            </div>

            {/* IMAGE ONLY BRANCH */}
            <div
              style={{
                border: `2px solid ${isImageActive ? '#10b981' : 'var(--border-color)'}`,
                borderRadius: '8px',
                padding: '14px',
                background: isImageActive ? 'rgba(16, 185, 129, 0.1)' : 'rgba(15, 23, 42, 0.3)',
                opacity: currentModality && !isImageActive ? 0.35 : 1,
                transition: 'all 0.3s ease',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <span style={{ fontWeight: 700, fontSize: '0.8rem', color: isImageActive ? '#34d399' : 'var(--text-muted)' }}>
                  IMAGE ONLY ROUTE
                </span>
                {isImageActive && <span className="badge badge-image">ACTIVE</span>}
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.75rem' }}>
                <div style={{ padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px', border: '1px solid var(--border-color)' }}>
                  MobileViT Vision Encoder
                </div>
                <div style={{ padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px', border: '1px solid var(--border-color)' }}>
                  Vision Projection (256-d)
                </div>
                <div style={{ padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px', border: '1px solid var(--border-color)' }}>
                  Mean Pooling
                </div>
                <div style={{ padding: '6px 10px', background: 'rgba(239, 68, 68, 0.1)', color: '#f87171', borderRadius: '4px' }}>
                  ❌ DistilBERT & Cross-Attention SKIPPED
                </div>
              </div>
            </div>

            {/* MULTIMODAL BRANCH */}
            <div
              style={{
                border: `2px solid ${isMultimodalActive ? '#a855f7' : 'var(--border-color)'}`,
                borderRadius: '8px',
                padding: '14px',
                background: isMultimodalActive ? 'rgba(168, 85, 247, 0.1)' : 'rgba(15, 23, 42, 0.3)',
                opacity: currentModality && !isMultimodalActive ? 0.35 : 1,
                transition: 'all 0.3s ease',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                <span style={{ fontWeight: 700, fontSize: '0.8rem', color: isMultimodalActive ? '#c084fc' : 'var(--text-muted)' }}>
                  MULTIMODAL ROUTE
                </span>
                {isMultimodalActive && <span className="badge badge-multimodal">ACTIVE</span>}
              </div>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '0.75rem' }}>
                <div style={{ padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px', border: '1px solid var(--border-color)' }}>
                  DistilBERT + MobileViT (Both)
                </div>
                <div style={{ padding: '6px 10px', background: 'rgba(168, 85, 247, 0.2)', color: '#e9d5ff', fontWeight: 600, borderRadius: '4px', border: '1px solid rgba(168, 85, 247, 0.4)' }}>
                  2x Bidirectional Cross-Attention
                </div>
                <div style={{ padding: '6px 10px', background: 'var(--bg-card)', borderRadius: '4px', border: '1px solid var(--border-color)' }}>
                  Concatenation & Mean Pooling
                </div>
                <div style={{ padding: '6px 10px', background: 'rgba(16, 185, 129, 0.1)', color: '#34d399', borderRadius: '4px' }}>
                  ✓ Both Encoders & Cross-Attention RUN
                </div>
              </div>
            </div>

          </div>

          <div style={{ height: '16px', width: '2px', background: 'var(--border-color)' }}></div>

          {/* Shared Classifier Base */}
          <div style={{ width: '100%', padding: '12px', background: 'rgba(30, 41, 59, 0.9)', border: '1px solid var(--border-color)', borderRadius: '8px', textAlign: 'center' }}>
            <span style={{ fontWeight: 700, fontSize: '0.85rem', color: 'var(--text-main)' }}>
              SHARED CLASSIFICATION HEAD
            </span>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '2px' }}>
              LayerNorm → Linear(256, 128) → GELU → Dropout(0.3) → Linear(128, 1) → BCEWithLogitsLoss
            </p>
          </div>

        </div>
      </div>
    </div>
  );
};
