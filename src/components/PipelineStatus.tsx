import { useEffect, useState } from 'react';
import { CheckCircle2, AlertCircle, Loader2, Wand2, Film, Download, X, RefreshCw } from 'lucide-react';
import type { PipelineStep } from '../types';
import './PipelineStatus.css';

interface PipelineStatusProps {
  step: PipelineStep;
  message: string;
  error: string;
  progress: number;
  onDismiss: () => void;
  onRetry: () => void;
}

const STEP_CONFIG: Record<PipelineStep, {
  icon: React.ReactNode;
  title: string;
  color: string;
  spin?: boolean;
}> = {
  idle: { icon: null, title: '', color: '' },
  analyzing: {
    icon: <Wand2 size={18} />,
    title: 'AI Analyzing',
    color: 'var(--accent-primary)',
    spin: false,
  },
  loading_ffmpeg: {
    icon: <Film size={18} />,
    title: 'Loading Encoder',
    color: '#a78bfa',
    spin: true,
  },
  exporting: {
    icon: <Download size={18} />,
    title: 'Creating Video',
    color: '#34d399',
    spin: true,
  },
  done: {
    icon: <CheckCircle2 size={18} />,
    title: 'Video Ready!',
    color: '#34d399',
  },
  error: {
    icon: <AlertCircle size={18} />,
    title: 'Pipeline Error',
    color: '#f87171',
  },
};

const STEPS_ORDER: PipelineStep[] = ['analyzing', 'loading_ffmpeg', 'exporting', 'done'];

const PipelineStatus = ({
  step,
  message,
  error,
  progress,
  onDismiss,
  onRetry,
}: PipelineStatusProps) => {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    if (step !== 'idle') {
      setVisible(true);
    }
    if (step === 'done') {
      // Auto-dismiss after 5 seconds
      const timer = setTimeout(() => {
        setVisible(false);
        setTimeout(onDismiss, 400); // wait for fade out
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [step, onDismiss]);

  if (step === 'idle' || !visible) return null;

  const config = STEP_CONFIG[step];
  const activeStepIndex = STEPS_ORDER.indexOf(step);

  return (
    <div className={`pipeline-toast ${visible ? 'visible' : 'hidden'}`}>
      {/* Header */}
      <div className="pipeline-toast-header">
        <div className="pipeline-toast-title" style={{ color: config.color }}>
          <span className={config.spin ? 'spin-icon' : ''}>
            {config.icon}
          </span>
          <span>{config.title}</span>
        </div>
        {(step === 'done' || step === 'error') && (
          <button className="pipeline-dismiss" onClick={() => { setVisible(false); setTimeout(onDismiss, 400); }}>
            <X size={14} />
          </button>
        )}
      </div>

      {/* Message */}
      <p className="pipeline-toast-msg">{error || message}</p>

      {/* Progress bar for exporting */}
      {step === 'exporting' && (
        <div className="pipeline-progress-track">
          <div
            className="pipeline-progress-fill"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}

      {/* Step dots */}
      {step !== 'error' && (
        <div className="pipeline-steps">
          {STEPS_ORDER.map((s, i) => {
            const isDone = i < activeStepIndex || step === 'done';
            const isActive = i === activeStepIndex && step !== 'done';
            return (
              <div key={s} className="pipeline-step-item">
                <div
                  className={`pipeline-step-dot ${isDone ? 'done' : ''} ${isActive ? 'active' : ''}`}
                />
                {i < STEPS_ORDER.length - 1 && (
                  <div className={`pipeline-step-line ${isDone ? 'done' : ''}`} />
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Error retry */}
      {step === 'error' && (
        <button className="pipeline-retry-btn" onClick={onRetry}>
          <RefreshCw size={13} />
          Try Again
        </button>
      )}

      {/* Spinner for active steps */}
      {(step === 'analyzing' || step === 'loading_ffmpeg') && (
        <div className="pipeline-spinner-row">
          <Loader2 size={14} className="spin-icon" style={{ color: config.color }} />
          <span>Please wait...</span>
        </div>
      )}
    </div>
  );
};

export default PipelineStatus;
