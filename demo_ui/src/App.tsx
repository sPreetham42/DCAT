import React, { useState, useEffect } from 'react';
import { Header } from './components/Header';
import { ScenarioSelector } from './components/ScenarioSelector';
import { EmailInputForm } from './components/EmailInputForm';
import { RouterPanel } from './components/RouterPanel';
import { ArchitectureDiagram } from './components/ArchitectureDiagram';
import { CrossAttentionVisualization } from './components/CrossAttentionVisualization';
import { ResultPanel } from './components/ResultPanel';
import { ComputationComparison } from './components/ComputationComparison';
import { HowItWorksSection } from './components/HowItWorksSection';
import type { Scenario, InferenceResult } from './types';

export const App: React.FC = () => {
  const [scenarios, setScenarios] = useState<Scenario[]>([]);
  const [selectedScenarioId, setSelectedScenarioId] = useState<string | null>(null);

  const [sender, setSender] = useState('colleague@company.com');
  const [subject, setSubject] = useState('Meeting confirmation');
  const [body, setBody] = useState('Your meeting is confirmed for tomorrow at 10:00 AM.');
  const [imageB64, setImageB64] = useState<string | null>(null);

  const [result, setResult] = useState<InferenceResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  // Load scenarios on mount
  useEffect(() => {
    fetch('/api/scenarios')
      .then((res) => res.json())
      .then((data) => {
        if (data.scenarios && Array.isArray(data.scenarios)) {
          setScenarios(data.scenarios);
          // Select scenario 1 on initial load
          if (data.scenarios.length > 0) {
            handleScenarioSelect(data.scenarios[0]);
          }
        }
      })
      .catch((err) => {
        console.warn('Backend API not responding, using fallback state:', err);
      });
  }, []);

  const handleScenarioSelect = (scenario: Scenario) => {
    setSelectedScenarioId(scenario.id);
    setSender(scenario.sender);
    setSubject(scenario.subject);
    setBody(scenario.body);
    setImageB64(scenario.image_b64);
    analyzePayload(scenario.sender, scenario.subject, scenario.body, scenario.image_b64);
  };

  const analyzePayload = async (
    snd: string,
    sbj: string,
    bdy: string,
    img: string | null
  ) => {
    setIsLoading(true);
    try {
      const res = await fetch('/api/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sender: snd,
          subject: sbj,
          body: bdy,
          image_b64: img,
        }),
      });

      if (!res.ok) {
        throw new Error(`API error: ${res.status}`);
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error('Failed to analyze email:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleManualAnalyze = () => {
    setSelectedScenarioId(null);
    analyzePayload(sender, subject, body, imageB64);
  };

  return (
    <div style={{ minHeight: '100vh', background: 'var(--bg-main)', color: 'var(--text-main)', paddingBottom: '40px' }}>
      <Header />

      <main style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 20px' }}>
        <ScenarioSelector
          scenarios={scenarios}
          selectedId={selectedScenarioId}
          onSelect={handleScenarioSelect}
        />

        {/* Input & Router Side-by-Side Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(420px, 1fr))', gap: '24px', marginBottom: '24px' }}>
          <EmailInputForm
            sender={sender}
            setSender={setSender}
            subject={subject}
            setSubject={setSubject}
            body={body}
            setBody={setBody}
            imageB64={imageB64}
            setImageB64={setImageB64}
            onAnalyze={handleManualAnalyze}
            isLoading={isLoading}
          />

          <RouterPanel result={result} />
        </div>

        {/* Dynamic Architecture Flow Diagram */}
        <ArchitectureDiagram result={result} />

        {/* Cross Attention Token Interactions (only rendered when MULTIMODAL) */}
        <CrossAttentionVisualization result={result} />

        {/* Demonstration Outcome & Signals */}
        <ResultPanel result={result} />

        {/* Computation Comparison Panel */}
        <ComputationComparison result={result} />

        {/* How It Works for Faculty & Reviewers */}
        <HowItWorksSection />
      </main>
    </div>
  );
};

export default App;
