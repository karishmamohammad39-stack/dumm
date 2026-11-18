import React, { useState, useEffect } from 'react';
import { Sparkles, Download, Settings, X, Keyboard } from 'lucide-react';
import './Header.css';

interface HeaderProps {
  onExport: () => void;
  isExporting: boolean;
  exportProgress: number;
}

const SHORTCUTS = [
  { key: 'Space', action: 'Play / Pause' },
  { key: 'J', action: 'Skip Back 5s' },
  { key: 'L', action: 'Skip Forward 5s' },
  { key: 'K', action: 'Pause' },
  { key: 'M', action: 'Mute / Unmute' },
  { key: '← →', action: 'Step 1 frame' },
];

const Header: React.FC<HeaderProps> = ({ onExport, isExporting, exportProgress }) => {
  const [projectName, setProjectName] = useState('Untitled Project');
  const [isEditing, setIsEditing] = useState(false);
  const [showShortcuts, setShowShortcuts] = useState(false);
  const [showSettings, setShowSettings] = useState(false);

  // Close modals on Escape
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        setShowShortcuts(false);
        setShowSettings(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleNameBlur = (e: React.FocusEvent<HTMLInputElement>) => {
    const val = e.target.value.trim();
    setProjectName(val || 'Untitled Project');
    setIsEditing(false);
  };

  return (
    <>
      <header className="header-container glass-panel">
        <div className="logo-section">
          <Sparkles className="logo-icon" size={26} />
          <h1 className="logo-text">Vibe-Cuts</h1>
          <div className="header-divider" />
          {isEditing ? (
            <input
              className="project-name-input"
              defaultValue={projectName}
              autoFocus
              onBlur={handleNameBlur}
              onKeyDown={e => { if (e.key === 'Enter') (e.target as HTMLInputElement).blur(); }}
            />
          ) : (
            <span
              className="project-name"
              onClick={() => setIsEditing(true)}
              title="Click to rename"
            >
              {projectName}
            </span>
          )}
        </div>

        <div className="header-actions">
          <button
            className="icon-btn"
            onClick={() => setShowShortcuts(v => !v)}
            title="Keyboard Shortcuts"
          >
            <Keyboard size={18} />
          </button>
          <button
            className="icon-btn"
            title="Settings"
            onClick={() => setShowSettings(v => !v)}
          >
            <Settings size={18} />
          </button>
          <button
            className="primary-btn export-btn"
            onClick={onExport}
            disabled={isExporting}
          >
            <Download size={16} />
            <span>{isExporting ? `Exporting ${exportProgress.toFixed(0)}%` : 'Export Video'}</span>
            {isExporting && (
              <div className="export-progress-bar" style={{ width: `${exportProgress}%` }} />
            )}
          </button>
        </div>
      </header>

      {/* Keyboard Shortcuts Modal */}
      {showShortcuts && (
        <div className="modal-backdrop" onClick={() => setShowShortcuts(false)}>
          <div className="modal-panel" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Keyboard Shortcuts</h3>
              <button className="icon-btn" onClick={() => setShowShortcuts(false)}>
                <X size={18} />
              </button>
            </div>
            <div className="shortcuts-list">
              {SHORTCUTS.map(s => (
                <div key={s.key} className="shortcut-row">
                  <kbd className="kbd">{s.key}</kbd>
                  <span>{s.action}</span>
                </div>
              ))}
            </div>
            <p style={{ marginTop: '16px', fontSize: '0.72rem', color: 'var(--text-muted)', textAlign: 'center' }}>
              Press Esc to close
            </p>
          </div>
        </div>
      )}

      {/* Settings Modal */}
      {showSettings && (
        <div className="modal-backdrop" onClick={() => setShowSettings(false)}>
          <div className="modal-panel" onClick={e => e.stopPropagation()}>
            <div className="modal-header">
              <h3>Settings</h3>
              <button className="icon-btn" onClick={() => setShowSettings(false)}>
                <X size={18} />
              </button>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div className="shortcut-row" style={{ justifyContent: 'space-between' }}>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Backend URL</span>
                <code style={{ fontSize: '0.78rem', color: 'var(--accent-primary)', background: 'rgba(0,240,255,0.08)', padding: '3px 8px', borderRadius: '4px' }}>
                  localhost:8000
                </code>
              </div>
              <div className="shortcut-row" style={{ justifyContent: 'space-between' }}>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>FFmpeg Engine</span>
                <code style={{ fontSize: '0.78rem', color: '#34d399', background: 'rgba(52,211,153,0.08)', padding: '3px 8px', borderRadius: '4px' }}>
                  WASM (in-browser)
                </code>
              </div>
              <div className="shortcut-row" style={{ justifyContent: 'space-between' }}>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>Whisper Model</span>
                <code style={{ fontSize: '0.78rem', color: '#a78bfa', background: 'rgba(167,139,250,0.08)', padding: '3px 8px', borderRadius: '4px' }}>
                  base (backend)
                </code>
              </div>
            </div>
            <p style={{ marginTop: '16px', fontSize: '0.72rem', color: 'var(--text-muted)', textAlign: 'center' }}>
              Press Esc to close
            </p>
          </div>
        </div>
      )}
    </>
  );
};

export default Header;
