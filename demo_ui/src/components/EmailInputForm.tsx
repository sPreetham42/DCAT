import React, { useState } from 'react';
import { X, Send, Image as ImageIcon } from 'lucide-react';

interface Props {
  sender: string;
  setSender: (val: string) => void;
  subject: string;
  setSubject: (val: string) => void;
  body: string;
  setBody: (val: string) => void;
  imageB64: string | null;
  setImageB64: (val: string | null) => void;
  onAnalyze: () => void;
  isLoading: boolean;
}

export const EmailInputForm: React.FC<Props> = ({
  sender,
  setSender,
  subject,
  setSubject,
  body,
  setBody,
  imageB64,
  setImageB64,
  onAnalyze,
  isLoading,
}) => {
  const [dragActive, setDragActive] = useState(false);

  const handleImageFile = (file: File) => {
    if (!file.type.startsWith('image/')) {
      alert('Please upload an image file (PNG, JPEG, etc.)');
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      const result = e.target?.result as string;
      if (result) {
        // Strip data:image/...;base64, prefix
        const base64Data = result.split(',')[1] || result;
        setImageB64(base64Data);
      }
    };
    reader.readAsDataURL(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleImageFile(e.dataTransfer.files[0]);
    }
  };

  return (
    <div className="card">
      <h3 style={{ fontSize: '1rem', fontWeight: 600, color: 'var(--text-main)', marginBottom: '16px' }}>
        Email Message Input
      </h3>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
        <div>
          <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
            Sender Address
          </label>
          <input
            type="text"
            value={sender}
            onChange={(e) => setSender(e.target.value)}
            placeholder="security@example.com"
            style={{
              width: '100%',
              padding: '8px 12px',
              background: 'var(--bg-main)',
              border: '1px solid var(--border-color)',
              borderRadius: '6px',
              color: 'var(--text-main)',
              fontSize: '0.875rem',
            }}
          />
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
            Subject Header
          </label>
          <input
            type="text"
            value={subject}
            onChange={(e) => setSubject(e.target.value)}
            placeholder="Your account status update"
            style={{
              width: '100%',
              padding: '8px 12px',
              background: 'var(--bg-main)',
              border: '1px solid var(--border-color)',
              borderRadius: '6px',
              color: 'var(--text-main)',
              fontSize: '0.875rem',
            }}
          />
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
            Email Body Content
          </label>
          <textarea
            rows={5}
            value={body}
            onChange={(e) => setBody(e.target.value)}
            placeholder="Enter the body text of the email message..."
            style={{
              width: '100%',
              padding: '10px 12px',
              background: 'var(--bg-main)',
              border: '1px solid var(--border-color)',
              borderRadius: '6px',
              color: 'var(--text-main)',
              fontSize: '0.875rem',
              resize: 'vertical',
            }}
          />
        </div>

        <div>
          <label style={{ display: 'block', fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '4px' }}>
            Attached / Inline Image (Optional)
          </label>

          {imageB64 ? (
            <div style={{ position: 'relative', display: 'inline-block', border: '1px solid var(--border-color)', borderRadius: '8px', padding: '8px', background: 'var(--bg-main)' }}>
              <img
                src={`data:image/png;base64,${imageB64}`}
                alt="Attached Preview"
                style={{ maxHeight: '120px', borderRadius: '4px', display: 'block' }}
              />
              <button
                onClick={() => setImageB64(null)}
                title="Remove image"
                style={{
                  position: 'absolute',
                  top: '-8px',
                  right: '-8px',
                  background: '#ef4444',
                  color: 'white',
                  border: 'none',
                  borderRadius: '50%',
                  width: '24px',
                  height: '24px',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                }}
              >
                <X size={14} />
              </button>
            </div>
          ) : (
            <div
              onDragOver={(e) => { e.preventDefault(); setDragActive(true); }}
              onDragLeave={() => setDragActive(false)}
              onDrop={handleDrop}
              style={{
                border: `2px dashed ${dragActive ? 'var(--accent-blue)' : 'var(--border-color)'}`,
                borderRadius: '8px',
                padding: '16px',
                textAlign: 'center',
                background: dragActive ? 'rgba(59, 130, 246, 0.05)' : 'var(--bg-main)',
                cursor: 'pointer',
              }}
              onClick={() => {
                const el = document.getElementById('file-upload-input');
                if (el) el.click();
              }}
            >
              <ImageIcon size={24} style={{ color: 'var(--text-muted)', margin: '0 auto 6px' }} />
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                Drag & drop an image here, or <span style={{ color: '#60a5fa' }}>click to browse</span>
              </p>
              <input
                id="file-upload-input"
                type="file"
                accept="image/*"
                style={{ display: 'none' }}
                onChange={(e) => {
                  if (e.target.files && e.target.files[0]) {
                    handleImageFile(e.target.files[0]);
                  }
                }}
              />
            </div>
          )}
        </div>

        <button
          onClick={onAnalyze}
          disabled={isLoading}
          className="btn btn-primary"
          style={{ marginTop: '8px', padding: '12px', fontSize: '0.95rem' }}
        >
          {isLoading ? 'Processing Phase 1 Preprocessing & Routing...' : (
            <>
              <Send size={18} />
              <span>Analyze Email & Route Modality</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
};
