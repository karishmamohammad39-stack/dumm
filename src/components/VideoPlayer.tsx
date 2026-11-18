import { useState, useRef, useEffect, useCallback } from 'react';
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Volume2,
  VolumeX,
  Maximize2,
  MonitorSmartphone,
  Square,
  Smartphone,
  Gauge,
  ChevronLeft,
  ChevronRight,
  UploadCloud,
} from 'lucide-react';
import './VideoPlayer.css';
import type { CaptionSegment, VideoFilters, AspectRatio } from '../types';

interface VideoPlayerProps {
  videoSrc: string | null;
  isPlaying: boolean;
  setIsPlaying: (playing: boolean) => void;
  currentTime: number;
  setCurrentTime: (time: number) => void;
  duration: number;
  setDuration: (duration: number) => void;
  seekTime: number | null;
  setSeekTime: (time: number | null) => void;
  captions?: CaptionSegment[];
  filters?: VideoFilters;
  isMuted?: boolean;
  setIsMuted?: (muted: boolean) => void;
  cinematicMode?: boolean;
  aspectRatio?: AspectRatio;
  onAspectRatioChange?: (ar: AspectRatio) => void;
  onDropVideo?: (file: File) => void;
}

const formatTime = (timeInSeconds: number) => {
  if (isNaN(timeInSeconds) || timeInSeconds < 0) return '00:00:00';
  const hrs = Math.floor(timeInSeconds / 3600);
  const mins = Math.floor((timeInSeconds % 3600) / 60);
  const secs = Math.floor(timeInSeconds % 60);
  return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
};

const formatHoverTime = (timeInSeconds: number) => {
  if (isNaN(timeInSeconds) || timeInSeconds < 0) return '00:00';
  const mins = Math.floor(timeInSeconds / 60);
  const secs = Math.floor(timeInSeconds % 60);
  const ms = Math.floor((timeInSeconds % 1) * 10);
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}.${ms}`;
};

const PLAYBACK_SPEEDS = [0.5, 1, 1.25, 1.5, 2];

const VideoPlayer = ({
  videoSrc,
  isPlaying,
  setIsPlaying,
  currentTime,
  setCurrentTime,
  duration,
  setDuration,
  seekTime,
  setSeekTime,
  captions = [],
  filters,
  isMuted: isMutedProp = false,
  setIsMuted: setIsMutedProp,
  cinematicMode,
  aspectRatio = '16:9',
  onAspectRatioChange,
  onDropVideo,
}: VideoPlayerProps) => {
  const [volume, setVolume] = useState(1);
  const [isMuted, setIsMutedLocal] = useState(false);
  const [showVolume, setShowVolume] = useState(false);
  const [showSpeedMenu, setShowSpeedMenu] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const [isScrubbing, setIsScrubbing] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const [hoverTime, setHoverTime] = useState<number | null>(null);
  const [hoverLeft, setHoverLeft] = useState(0);

  const videoRef = useRef<HTMLVideoElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const progressRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Sync aspect ratio when cinematic mode toggles
  useEffect(() => {
    if (cinematicMode && aspectRatio !== '9:16') {
      onAspectRatioChange?.('9:16');
    }
  }, [cinematicMode, aspectRatio, onAspectRatioChange]);

  // Sync isMuted from parent (keyboard shortcut M)
  useEffect(() => {
    setIsMutedLocal(isMutedProp);
  }, [isMutedProp]);

  // Propagate local mute changes up to parent
  const setIsMuted = (val: boolean) => {
    setIsMutedLocal(val);
    setIsMutedProp?.(val);
  };

  // Apply video filters as CSS filter
  useEffect(() => {
    if (videoRef.current && filters) {
      const brightness = 1 + filters.exposure / 100;
      const contrast = 1 + filters.contrast / 100;
      const saturate = 1 + filters.saturation / 100;
      videoRef.current.style.filter = `brightness(${brightness}) contrast(${contrast}) saturate(${saturate})`;
    }
  }, [filters]);

  // Handle external playback control
  useEffect(() => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.play().catch(e => console.error('Playback failed', e));
      } else {
        videoRef.current.pause();
      }
    }
  }, [isPlaying, videoSrc]);

  // Handle seeking from Timeline
  useEffect(() => {
    if (seekTime !== null && videoRef.current) {
      videoRef.current.currentTime = seekTime;
      setSeekTime(null);
    }
  }, [seekTime, setSeekTime]);

  // Ensure duration is set even if onLoadedMetadata fires early
  useEffect(() => {
    if (videoRef.current && videoRef.current.readyState >= 1) {
      const dur = videoRef.current.duration;
      if (dur > 0 && dur !== duration) {
        setDuration(dur);
      }
    }
  }, [videoSrc, duration, setDuration]);

  // Volume & Speed sync
  useEffect(() => {
    if (videoRef.current) {
      videoRef.current.volume = volume;
      videoRef.current.muted = isMuted;
      videoRef.current.playbackRate = playbackSpeed;
    }
  }, [volume, isMuted, playbackSpeed]);

  const handleTimeUpdate = () => {
    if (videoRef.current && !isScrubbing) {
      setCurrentTime(videoRef.current.currentTime);
    }
  };

  const handleLoadedMetadata = () => {
    if (videoRef.current) {
      setDuration(videoRef.current.duration);
    }
  };

  const handleEnded = () => {
    setIsPlaying(false);
  };

  const skip = useCallback((seconds: number) => {
    if (videoRef.current && duration > 0) {
      const targetTime = Math.max(0, Math.min(videoRef.current.currentTime + seconds, duration));
      videoRef.current.currentTime = targetTime;
      setCurrentTime(targetTime);
    }
  }, [duration, setCurrentTime]);

  const stepFrame = (frames: number) => {
    // 25fps default frame step = 0.04s
    skip(frames * 0.04);
  };

  const handleProgressClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!progressRef.current || !duration) return;
    const rect = progressRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const pct = Math.max(0, Math.min(x / rect.width, 1));
    const newTime = pct * duration;
    if (videoRef.current) videoRef.current.currentTime = newTime;
    setCurrentTime(newTime);
  };

  const handleProgressMouseDown = (e: React.MouseEvent<HTMLDivElement>) => {
    setIsScrubbing(true);
    handleProgressClick(e);
  };

  useEffect(() => {
    if (!isScrubbing) return;

    const handleWindowMouseMove = (e: MouseEvent) => {
      if (!progressRef.current || !duration) return;
      const rect = progressRef.current.getBoundingClientRect();
      const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
      const pct = x / rect.width;
      const newTime = pct * duration;
      if (videoRef.current) videoRef.current.currentTime = newTime;
      setCurrentTime(newTime);
    };

    const handleWindowMouseUp = () => {
      setIsScrubbing(false);
    };

    window.addEventListener('mousemove', handleWindowMouseMove);
    window.addEventListener('mouseup', handleWindowMouseUp);
    return () => {
      window.removeEventListener('mousemove', handleWindowMouseMove);
      window.removeEventListener('mouseup', handleWindowMouseUp);
    };
  }, [isScrubbing, duration, setCurrentTime]);

  const handleProgressMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!progressRef.current || !duration) return;
    const rect = progressRef.current.getBoundingClientRect();
    const x = Math.max(0, Math.min(e.clientX - rect.left, rect.width));
    const pct = x / rect.width;
    setHoverTime(pct * duration);
    setHoverLeft(x);
  };

  const handleProgressMouseLeave = () => {
    setHoverTime(null);
  };

  const toggleFullscreen = () => {
    if (!containerRef.current) return;
    if (!document.fullscreenElement) {
      containerRef.current.requestFullscreen().catch(console.error);
    } else {
      document.exitFullscreen();
    }
  };

  // Canvas Drag & Drop handlers
  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file && (file.type.startsWith('video/') || file.name.match(/\.(mp4|mov|webm|mkv|avi)$/i))) {
      onDropVideo?.(file);
    }
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      onDropVideo?.(file);
    }
  };

  const progressPercent = duration > 0 ? (currentTime / duration) * 100 : 0;

  // Active caption
  const activeCaptions = captions.filter(
    c => currentTime >= c.start && currentTime <= c.end
  );

  const getAspectRatioClass = (ar: AspectRatio) => {
    switch (ar) {
      case '9:16': return 'ar-9-16';
      case '1:1':  return 'ar-1-1';
      case '4:5':  return 'ar-4-5';
      case '16:9':
      default:     return 'ar-16-9';
    }
  };

  return (
    <main className="player-container" ref={containerRef}>
      {/* ── Toolbar ── */}
      <div className="player-toolbar">
        <div className="format-toggle">
          <button
            className={`format-btn ${aspectRatio === '16:9' ? 'active' : ''}`}
            onClick={() => onAspectRatioChange?.('16:9')}
            title="Widescreen (16:9 YouTube / Desktop)"
          >
            16:9
          </button>
          <button
            className={`format-btn ${aspectRatio === '9:16' ? 'active' : ''}`}
            onClick={() => onAspectRatioChange?.('9:16')}
            title="Vertical (9:16 Reels / Shorts / TikTok)"
          >
            <Smartphone size={14} /> 9:16
          </button>
          <button
            className={`format-btn ${aspectRatio === '1:1' ? 'active' : ''}`}
            onClick={() => onAspectRatioChange?.('1:1')}
            title="Square (1:1 Instagram Post)"
          >
            <Square size={13} /> 1:1
          </button>
          <button
            className={`format-btn ${aspectRatio === '4:5' ? 'active' : ''}`}
            onClick={() => onAspectRatioChange?.('4:5')}
            title="Portrait (4:5 Social Feed)"
          >
            <MonitorSmartphone size={14} /> 4:5
          </button>
        </div>

        <div className="toolbar-right-badges">
          <span className="aspect-ratio-indicator">{aspectRatio}</span>
          <div className="resolution-badge">4K ULTRA HD</div>
        </div>
      </div>

      {/* ── Canvas Area ── */}
      <div
        className="canvas-area"
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <input
          type="file"
          ref={fileInputRef}
          style={{ display: 'none' }}
          accept="video/*,.mkv,.mp4,.mov,.webm,.avi"
          onChange={handleFileInputChange}
        />

        <div className={`video-canvas glass-panel ${getAspectRatioClass(aspectRatio)} ${isDragOver ? 'drag-over' : ''}`}>
          {videoSrc ? (
            <>
              <video
                ref={videoRef}
                src={videoSrc}
                className="actual-video"
                onTimeUpdate={handleTimeUpdate}
                onLoadedMetadata={handleLoadedMetadata}
                onEnded={handleEnded}
                onClick={() => setIsPlaying(!isPlaying)}
              />
              {activeCaptions.length > 0 && (
                <div className="caption-overlay">
                  {activeCaptions.map(c => (
                    <span key={c.id} className="caption-text">{c.text}</span>
                  ))}
                </div>
              )}
            </>
          ) : (
            <div
              className="video-placeholder clickable"
              onClick={() => fileInputRef.current?.click()}
              title="Click or drag video here to open"
            >
              <div className="placeholder-inner">
                <div className="placeholder-icon-ring">
                  <UploadCloud size={38} className="upload-icon-pulse" />
                </div>
                <span className="placeholder-text">Drop a video here to begin</span>
                <span className="placeholder-sub">or click to browse files · MP4, MKV, MOV, WebM</span>
              </div>
              <div className="ai-overlay-mockup">
                <span className="caption-mock">✨ Studio Mode Ready</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* ── Precision Progress Scrubber ── */}
      <div
        className="progress-bar-container"
        ref={progressRef}
        onMouseDown={handleProgressMouseDown}
        onMouseMove={handleProgressMouseMove}
        onMouseUp={() => setIsScrubbing(false)}
        onMouseLeave={handleProgressMouseLeave}
      >
        {hoverTime !== null && (
          <div className="scrubber-tooltip" style={{ left: `${hoverLeft}px` }}>
            {formatHoverTime(hoverTime)}
          </div>
        )}
        <div className="progress-track">
          <div className="progress-fill" style={{ width: `${progressPercent}%` }} />
          <div className="progress-thumb" style={{ left: `${progressPercent}%` }} />
        </div>
      </div>

      {/* ── Player Controls Bar ── */}
      <div className="player-controls glass-panel">
        <div className="time-display">
          <span className="time-current">{formatTime(currentTime)}</span>
          <span className="time-divider">/</span>
          <span className="time-total">{formatTime(duration)}</span>
        </div>

        {/* Primary Playback controls */}
        <div className="playback-actions">
          <button
            className="control-btn frame-step-btn"
            onClick={() => stepFrame(-1)}
            disabled={!videoSrc}
            title="Step Back 1 Frame (Arrow Left)"
          >
            <ChevronLeft size={16} />
            <span className="step-label">-1f</span>
          </button>

          <button className="control-btn" onClick={() => skip(-5)} disabled={!videoSrc} title="Skip Back 5s (J)">
            <SkipBack size={18} />
          </button>

          <button
            className="control-btn play-btn"
            onClick={() => setIsPlaying(!isPlaying)}
            disabled={!videoSrc}
            style={{ opacity: videoSrc ? 1 : 0.4 }}
            title={isPlaying ? "Pause (Space)" : "Play (Space)"}
          >
            {isPlaying ? <Pause size={22} /> : <Play size={22} className="play-icon-offset" />}
          </button>

          <button className="control-btn" onClick={() => skip(5)} disabled={!videoSrc} title="Skip Forward 5s (L)">
            <SkipForward size={18} />
          </button>

          <button
            className="control-btn frame-step-btn"
            onClick={() => stepFrame(1)}
            disabled={!videoSrc}
            title="Step Forward 1 Frame (Arrow Right)"
          >
            <span className="step-label">+1f</span>
            <ChevronRight size={16} />
          </button>
        </div>

        {/* Secondary controls (speed, volume, fullscreen) */}
        <div className="secondary-actions">
          {/* Speed Selector */}
          <div
            className="speed-wrapper"
            onMouseEnter={() => setShowSpeedMenu(true)}
            onMouseLeave={() => setShowSpeedMenu(false)}
          >
            <button className="control-btn speed-toggle-btn" title="Playback Speed">
              <Gauge size={16} />
              <span className="speed-val">{playbackSpeed}x</span>
            </button>
            {showSpeedMenu && (
              <div className="speed-menu-popup">
                {PLAYBACK_SPEEDS.map(s => (
                  <button
                    key={s}
                    className={`speed-option ${playbackSpeed === s ? 'active' : ''}`}
                    onClick={() => {
                      setPlaybackSpeed(s);
                      setShowSpeedMenu(false);
                    }}
                  >
                    {s}x
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Volume */}
          <div
            className="volume-wrapper"
            onMouseEnter={() => setShowVolume(true)}
            onMouseLeave={() => setShowVolume(false)}
          >
            <button
              className="control-btn"
              onClick={() => setIsMuted(!isMuted)}
              title={isMuted ? 'Unmute (M)' : 'Mute (M)'}
            >
              {isMuted || volume === 0 ? <VolumeX size={18} /> : <Volume2 size={18} />}
            </button>
            <div className={`volume-slider-popup ${showVolume ? 'visible' : ''}`}>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={isMuted ? 0 : volume}
                className="volume-slider"
                onChange={e => {
                  const v = parseFloat(e.target.value);
                  setVolume(v);
                  if (v > 0) setIsMuted(false);
                }}
                style={{
                  background: `linear-gradient(to right, var(--accent-primary) ${(isMuted ? 0 : volume) * 100}%, rgba(255,255,255,0.15) ${(isMuted ? 0 : volume) * 100}%)`
                }}
              />
            </div>
          </div>

          <button className="control-btn" onClick={toggleFullscreen} title="Toggle Fullscreen">
            <Maximize2 size={18} />
          </button>
        </div>
      </div>
    </main>
  );
};

export default VideoPlayer;
