import React from 'react';
import type { Scenario } from '../types';

interface Props {
  scenarios: Scenario[];
  selectedId: string | null;
  onSelect: (scenario: Scenario) => void;
}

export const ScenarioSelector: React.FC<Props> = ({ scenarios, selectedId, onSelect }) => {
  return (
    <div className="card" style={{ marginBottom: '24px' }}>
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '14px' }}>
        <h3 style={{ fontSize: '0.95rem', fontWeight: 600, color: 'var(--text-main)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
          Select Pre-configured Demo Scenario
        </h3>
        <span style={{ fontSize: '0.8rem', color: 'var(--text-subtle)' }}>
          Click any scenario to populate inputs & route
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '12px' }}>
        {scenarios.map((sc) => {
          const isSelected = sc.id === selectedId;
          return (
            <button
              key={sc.id}
              onClick={() => onSelect(sc)}
              style={{
                textAlign: 'left',
                padding: '12px 14px',
                background: isSelected ? '#1e293b' : 'var(--bg-main)',
                border: isSelected ? '2px solid var(--accent-blue)' : '1px solid var(--border-color)',
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'all 0.15s ease',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                <span style={{ fontWeight: 600, fontSize: '0.85rem', color: isSelected ? '#60a5fa' : 'var(--text-main)' }}>
                  {sc.title}
                </span>
                <span
                  className={
                    sc.expected_route === 'MULTIMODAL'
                      ? 'badge badge-multimodal'
                      : 'badge badge-text'
                  }
                  style={{ fontSize: '0.65rem' }}
                >
                  {sc.expected_route}
                </span>
              </div>
              <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{sc.subtitle}</p>
            </button>
          );
        })}
      </div>
    </div>
  );
};
