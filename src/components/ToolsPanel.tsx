import { useState, useRef, useEffect } from 'react';
import { Sparkles, Send, Bot, SlidersHorizontal } from 'lucide-react';
import './ToolsPanel.css';
import type { PipelineStep, VideoFilters, AspectRatio } from '../types';

interface ToolsPanelProps {
  onGenerate: () => void;
  isGenerating: boolean;
  pipelineStep?: PipelineStep;
  exportProgress?: number;
  cinematicMode?: boolean;
  onCinematicModeChange?: (active: boolean) => void;
  onAiPrompt?: (prompt: string) => void;
  onAgenticEdit?: (prompt: string, sector: string) => void;
  videoFilters?: VideoFilters;
  onFiltersChange?: (filters: VideoFilters) => void;
  aspectRatio?: AspectRatio;
  onAspectRatioChange?: (ar: AspectRatio) => void;
}

const ASPECT_RATIOS: AspectRatio[] = ['16:9', '9:16', '1:1', '4:5'];

const ToolsPanel = ({
  onGenerate,
  isGenerating,
  pipelineStep = 'idle',
  exportProgress = 0,
  cinematicMode = false,
  onCinematicModeChange,
  onAiPrompt,
  onAgenticEdit,
  videoFilters = { exposure: 0, contrast: 0, saturation: 0 },
  onFiltersChange,
  aspectRatio = '16:9',
  onAspectRatioChange,
}: ToolsPanelProps) => {
  const [prompt, setPrompt] = useState('');
  const [chatHistory, setChatHistory] = useState<{ role: 'user' | 'ai'; text: string }[]>([
    { role: 'ai', text: 'Hi! I am your AI Video Editor. What vibe are we going for today? Try saying "Make a fast cinematic trailer" or "Sync to the beat".' }
  ]);
  const [showFilters, setShowFilters] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }, [chatHistory]);

  const handleSend = () => {
    if (!prompt.trim()) return;
    setChatHistory(prev => [...prev, { role: 'user', text: prompt }]);

    // Trigger mock AI logic in App.tsx
    onAiPrompt?.(prompt);

    // Mock AI response
    setTimeout(() => {
      setChatHistory(prev => [
        ...prev,
        { role: 'ai', text: `Got it! I've updated the timeline and applied effects for "${prompt}". Generating now...` }
      ]);
      onGenerate();
    }, 1500);

    setPrompt('');
  };

  const updateFilter = (key: keyof VideoFilters, value: number) => {
    onFiltersChange?.({ ...videoFilters, [key]: value });
  };

  return (
    <aside className="tools-panel glass-panel ai-command-center">
      <div className="tools-header">
        <Bot size={20} className="ai-icon-glow" style={{ color: 'var(--accent-primary)' }} />
        <h2 style={{ fontSize: '0.9rem', fontWeight: 600, letterSpacing: '1px', textTransform: 'uppercase' }}>AI Command Center</h2>
      </div>

      <div className="chat-container">
        <div className="chat-history">
          {chatHistory.map((msg, idx) => (
            <div key={idx} className={`chat-bubble ${msg.role}`}>
              {msg.role === 'ai' && <Sparkles size={14} className="bubble-icon" />}
              <span>{msg.text}</span>
            </div>
          ))}
          <div ref={chatEndRef} />
        </div>

        {pipelineStep !== 'idle' && (
          <div className="pipeline-status-card">
            <div className="pipeline-header">
              <span className="pipeline-title">
                {pipelineStep === 'analyzing' && 'AI Analysis...'}
                {pipelineStep === 'loading_ffmpeg' && 'Loading Engine...'}
                {pipelineStep === 'exporting' && 'Rendering Reel...'}
                {pipelineStep === 'done' && 'Complete!'}
              </span>
              <span className="pipeline-pct">{Math.round(exportProgress)}%</span>
            </div>
            <div className="mini-progress-track">
              <div
                className="mini-progress-fill"
                style={{ width: `${exportProgress}%` }}
              />
            </div>
          </div>
        )}
      </div>

      <div className="chat-input-wrapper">
        <input
          type="text"
          placeholder="E.g. Make a fast cinematic trailer..."
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          disabled={isGenerating}
        />
        <button
          className="send-btn"
          onClick={handleSend}
          disabled={isGenerating || !prompt.trim()}
          title="Send to Local Pipeline"
        >
          <Send size={16} />
        </button>
      </div>

      <div style={{ padding: '0 15px', marginTop: '10px' }}>
        <button
          className="generate-btn"
          style={{ width: '100%', background: 'linear-gradient(90deg, #ff0055, #ffaa00)', color: 'white', fontWeight: 'bold' }}
          onClick={() => {
            if (!prompt.trim()) {
              alert("Please enter a prompt first (e.g. 'Make a hyper-fast reel with zooms')");
              return;
            }
            onAgenticEdit?.(prompt, 'reels');
          }}
          disabled={isGenerating}
        >
          <Bot size={16} style={{ marginRight: '8px' }} />
          Run Backend Agentic Edit
        </button>
      </div>

      {/* ── Adjustments Panel (scrollable when expanded) ── */}
      <div style={{ overflowY: 'auto', flexShrink: 0, maxHeight: showFilters ? '260px' : 'auto', padding: '10px 15px 0' }}>
        <button
          className="generate-btn"
          style={{ width: '100%', background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.12)', color: 'var(--text-secondary)', fontWeight: 500, fontSize: '0.8rem' }}
          onClick={() => setShowFilters(v => !v)}
        >
          <SlidersHorizontal size={14} style={{ marginRight: '6px' }} />
          {showFilters ? 'Hide' : 'Show'} Adjustments
        </button>

        {showFilters && (
          <div className="filters-panel" style={{ marginTop: '10px' }}>
            {/* Aspect Ratio */}
            <div className="filter-row" style={{ marginBottom: '10px' }}>
              <label className="filter-label">Aspect Ratio</label>
              <div style={{ display: 'flex', gap: '4px', flexWrap: 'wrap', marginTop: '4px' }}>
                {ASPECT_RATIOS.map(ar => (
                  <button
                    key={ar}
                    onClick={() => onAspectRatioChange?.(ar)}
                    style={{
                      padding: '3px 8px',
                      borderRadius: '4px',
                      fontSize: '0.72rem',
                      fontWeight: 600,
                      border: '1px solid rgba(255,255,255,0.15)',
                      background: aspectRatio === ar ? 'var(--accent-primary)' : 'rgba(255,255,255,0.06)',
                      color: aspectRatio === ar ? '#000' : 'var(--text-secondary)',
                      cursor: 'pointer',
                    }}
                  >
                    {ar}
                  </button>
                ))}
              </div>
            </div>

            {/* Exposure */}
            <div className="filter-row">
              <label className="filter-label">
                Exposure <span style={{ color: 'var(--accent-primary)' }}>{videoFilters.exposure > 0 ? '+' : ''}{videoFilters.exposure}</span>
              </label>
              <input
                type="range" min="-100" max="100" step="1"
                value={videoFilters.exposure}
                className="styled-slider"
                onChange={e => updateFilter('exposure', Number(e.target.value))}
              />
            </div>

            {/* Contrast */}
            <div className="filter-row">
              <label className="filter-label">
                Contrast <span style={{ color: 'var(--accent-primary)' }}>{videoFilters.contrast > 0 ? '+' : ''}{videoFilters.contrast}</span>
              </label>
              <input
                type="range" min="-100" max="100" step="1"
                value={videoFilters.contrast}
                className="styled-slider"
                onChange={e => updateFilter('contrast', Number(e.target.value))}
              />
            </div>

            {/* Saturation */}
            <div className="filter-row">
              <label className="filter-label">
                Saturation <span style={{ color: 'var(--accent-primary)' }}>{videoFilters.saturation > 0 ? '+' : ''}{videoFilters.saturation}</span>
              </label>
              <input
                type="range" min="-100" max="100" step="1"
                value={videoFilters.saturation}
                className="styled-slider"
                onChange={e => updateFilter('saturation', Number(e.target.value))}
              />
            </div>

            {/* Reset button */}
            {(videoFilters.exposure !== 0 || videoFilters.contrast !== 0 || videoFilters.saturation !== 0) && (
              <button
                onClick={() => onFiltersChange?.({ exposure: 0, contrast: 0, saturation: 0 })}
                style={{ marginTop: '6px', fontSize: '0.72rem', background: 'none', border: 'none', color: 'rgba(255,80,80,0.85)', cursor: 'pointer' }}
              >
                Reset adjustments
              </button>
            )}
          </div>
        )}
      </div>

      <div className="tools-footer">
        <div className="cinematic-toggle-wrap">
          <label className="cinematic-toggle-label">
            <input
              type="checkbox"
              checked={cinematicMode}
              onChange={(e) => onCinematicModeChange?.(e.target.checked)}
            />
            <span className="toggle-box"></span>
            <div className="cinematic-toggle-text">
              <span className="cinematic-title">Force Telugu Cinematic Style</span>
              <span className="cinematic-sub">High energy, beats shake &amp; filters</span>
            </div>
          </label>
        </div>
      </div>
    </aside>
  );
};

export default ToolsPanel;
