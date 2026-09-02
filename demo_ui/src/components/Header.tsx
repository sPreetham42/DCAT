import React from 'react';
import { ShieldCheck, Info } from 'lucide-react';

export const Header: React.FC = () => {
  return (
    <header style={{ borderBottom: '1px solid var(--border-color)', padding: '20px 0', marginBottom: '24px' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '16px' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <ShieldCheck size={28} color="var(--accent-blue)" />
            <h1 style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-main)', letterSpacing: '-0.02em' }}>
              Multimodal Email Spam Detection
            </h1>
          </div>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem', marginTop: '4px' }}>
            Conditional Cross-Attention Transformer (DCAT) — Research Demonstration Prototype
          </p>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.3)', padding: '8px 14px', borderRadius: '8px', fontSize: '0.8rem', color: '#93c5fd' }}>
          <Info size={16} style={{ flexShrink: 0 }} />
          <span>
            <strong>Prototype Demonstration Only</strong> — Classification results & attention weights are simulated.
          </span>
        </div>
      </div>
    </header>
  );
};
