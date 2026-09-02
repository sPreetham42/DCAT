import React from 'react';
import { BookOpen, Layers, Cpu, ShieldCheck } from 'lucide-react';

export const HowItWorksSection: React.FC = () => {
  return (
    <div className="card" style={{ marginBottom: '32px', background: 'var(--bg-card)' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px' }}>
        <BookOpen size={20} color="var(--accent-blue)" />
        <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-main)' }}>
          Research Concept Summary (For Reviewers & Faculty)
        </h3>
      </div>

      <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginBottom: '16px', lineHeight: 1.6 }}>
        The <strong>Dynamic Cross-Attention Transformer (DCAT)</strong> architecture addresses two key methodological flaws in prior multimodal email spam research:
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '16px' }}>
        <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', color: '#60a5fa', fontWeight: 600, fontSize: '0.85rem' }}>
            <Layers size={16} />
            <span>1. Dynamic Modality Routing</span>
          </div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
            Traditional multimodal frameworks run heavy vision models on <em>every</em> email—even plain text—or inject fake <code className="mono">0.5</code> dummy probability vectors. DCAT inspects content first: if an email contains only text, it executes only DistilBERT, skipping vision models entirely.
          </p>
        </div>

        <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', color: '#c084fc', fontWeight: 600, fontSize: '0.85rem' }}>
            <Cpu size={16} />
            <span>2. Cross-Modal Feature Interaction</span>
          </div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
            When an email contains both text and images (multimodal), features interact through <strong>bidirectional cross-attention layers</strong> before mean pooling. This allows textual phrasing (e.g. <em>"verify your account"</em>) to attend directly to visual banner signals (e.g. <em>"CLAIM $5,000"</em>).
          </p>
        </div>

        <div style={{ background: 'var(--bg-main)', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '14px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px', color: '#34d399', fontWeight: 600, fontSize: '0.85rem' }}>
            <ShieldCheck size={16} />
            <span>3. Single Shared Classification Head</span>
          </div>
          <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
            Rather than training three independent classifiers or late-fusing outputs, all three computational paths (<code className="mono">TEXT</code>, <code className="mono">IMAGE</code>, <code className="mono">MULTIMODAL</code>) map into a single 256-dimensional shared latent space and a <strong>single shared classification head</strong>.
          </p>
        </div>
      </div>
    </div>
  );
};
