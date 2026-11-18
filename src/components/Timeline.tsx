import { useRef, useState, useEffect, useCallback } from 'react';
import { Scissors, Copy, Trash2, SplitSquareHorizontal, ZoomIn, ZoomOut } from 'lucide-react';
import './Timeline.css';
import type { HighlightClip } from '../types';

interface TimelineProps {
  currentTime: number;
  duration: number;
  onSeek: (time: number) => void;
  videoSrc: string | null;
  bgmSrc?: string | null;
  cinematicMode?: boolean;
  generatedClips?: HighlightClip[];
  onDeleteClip?: (id: string) => void;
  onUpdateClip?: (id: string, updates: Partial<Pick<HighlightClip, 'start' | 'end' | 'label'>>) => void;
  onSplitClip?: (id: string, splitTime: number) => void;
  onAddClip?: (clip: Omit<HighlightClip, 'id'>) => void;
}

const formatRulerTime = (seconds: number): string => {
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  if (m > 0) return `${m}:${s.toString().padStart(2, '0')}`;
  return `0:${s.toString().padStart(2, '0')}`;
};

const Timeline = ({
  currentTime,
  duration,
  onSeek,
  videoSrc,
  bgmSrc,
  cinematicMode = false,
  generatedClips = [],
  onDeleteClip,
  onUpdateClip,
  onSplitClip,
  onAddClip,
}: TimelineProps) => {
  const scrollRef = useRef<HTMLDivElement>(null);
  const rulerScrollRef = useRef<HTMLDivElement>(null);
  const trackInnerRef = useRef<HTMLDivElement>(null);
  const [zoom, setZoom] = useState(50);
  const [selectedClipId, setSelectedClipId] = useState<string | null>(null);

  // Playhead / Ruler scrub state
  const isScrubbingRef = useRef(false);

  // Drag-to-create state
  const drawDrag = useRef<{ startX: number; startTime: number } | null>(null);
  const [drawingClip, setDrawingClip] = useState<{ start: number; end: number } | null>(null);

  // Trim-handle drag state
  const trimDrag = useRef<{
    clipId: string;
    edge: 'start' | 'end';
    origValue: number;
    startMouseX: number;
    trackWidth: number;
  } | null>(null);

  // Scale: zoom 50 = 1x, zoom 100 = 3x, zoom 1 = 0.3x
  const zoomScale = 0.3 + (zoom / 100) * 2.7;

  const playheadPercent = duration > 0 ? (currentTime / duration) * 100 : 0;

  // Sync ruler scroll with tracks scroll
  useEffect(() => {
    const tracksEl = scrollRef.current;
    const rulerEl = rulerScrollRef.current;
    if (!tracksEl || !rulerEl) return;
    const onScroll = () => { rulerEl.scrollLeft = tracksEl.scrollLeft; };
    tracksEl.addEventListener('scroll', onScroll, { passive: true });
    return () => tracksEl.removeEventListener('scroll', onScroll);
  }, []);

  // Mouse wheel horizontal scroll on tracks and ruler
  useEffect(() => {
    const tracksEl = scrollRef.current;
    const rulerEl = rulerScrollRef.current;
    if (!tracksEl) return;

    const onWheel = (e: WheelEvent) => {
      if (e.deltaY !== 0 && !e.shiftKey) {
        e.preventDefault();
        tracksEl.scrollLeft += e.deltaY;
      }
    };

    tracksEl.addEventListener('wheel', onWheel, { passive: false });
    rulerEl?.addEventListener('wheel', onWheel, { passive: false });

    return () => {
      tracksEl.removeEventListener('wheel', onWheel);
      rulerEl?.removeEventListener('wheel', onWheel);
    };
  }, []);

  // ── Helper: pixel X → video time ──
  const xToTime = useCallback((clientX: number): number => {
    const inner = trackInnerRef.current;
    if (!inner || duration === 0) return 0;
    const rect = inner.getBoundingClientRect();
    const pct = (clientX - rect.left) / rect.width;
    return Math.max(0, Math.min(pct * duration, duration));
  }, [duration]);

  // ── Ruler scrub handlers ──
  const handleRulerMouseDown = (e: React.MouseEvent) => {
    if (!duration) return;
    e.preventDefault();
    isScrubbingRef.current = true;
    onSeek(xToTime(e.clientX));
  };

  const handlePlayheadMouseDown = (e: React.MouseEvent) => {
    if (!duration) return;
    e.preventDefault();
    e.stopPropagation();
    isScrubbingRef.current = true;
  };

  // ── Track area click → seek (only when not on a clip) ──
  const handleTrackAreaClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!duration || !trackInnerRef.current) return;
    // Don't seek if we just finished drawing a new clip
    if (drawDrag.current) return;
    onSeek(xToTime(e.clientX));
  };

  const handleClipClick = (e: React.MouseEvent, clipId: string, startTime: number) => {
    e.stopPropagation();
    setSelectedClipId(clipId);
    onSeek(startTime);
  };

  const handleDeleteClip = (e: React.MouseEvent, id: string) => {
    e.stopPropagation();
    if (selectedClipId === id) setSelectedClipId(null);
    onDeleteClip?.(id);
  };

  const handleDeleteSelected = () => {
    if (selectedClipId) {
      onDeleteClip?.(selectedClipId);
      setSelectedClipId(null);
    }
  };

  // ── Split at playhead ──
  const handleSplit = () => {
    if (!videoSrc || duration === 0 || !onSplitClip) return;
    // Find clip containing currentTime
    const target = generatedClips.find(c => currentTime > c.start && currentTime < c.end);
    if (target) {
      onSplitClip(target.id, currentTime);
    } else if (onAddClip && generatedClips.length === 0) {
      // No clips yet — split the full video at playhead
      if (currentTime > 0.1 && currentTime < duration - 0.1) {
        onAddClip({ start: 0, end: currentTime, label: 'Part 1' });
        onAddClip({ start: currentTime, end: duration, label: 'Part 2' });
      }
    }
  };

  // ── Trim handle mouse events ──
  const handleTrimMouseDown = (
    e: React.MouseEvent,
    clipId: string,
    edge: 'start' | 'end',
    currentValue: number
  ) => {
    e.stopPropagation();
    e.preventDefault();
    const inner = trackInnerRef.current;
    if (!inner) return;
    trimDrag.current = {
      clipId,
      edge,
      origValue: currentValue,
      startMouseX: e.clientX,
      trackWidth: inner.getBoundingClientRect().width,
    };
  };

  // ── Draw-to-create mouse events ──
  const handleTrackBodyMouseDown = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!videoSrc || duration === 0 || !onAddClip) return;
    // Only left-click on empty area (not on a clip)
    if ((e.target as HTMLElement).closest('.clip')) return;
    e.preventDefault();
    const t = xToTime(e.clientX);
    drawDrag.current = { startX: e.clientX, startTime: t };
    setDrawingClip({ start: t, end: t });
  };

  // Global mouse move + up for trim, draw, and playhead scrubbing
  useEffect(() => {
    const onMouseMove = (e: MouseEvent) => {
      // Ruler / Playhead scrub
      if (isScrubbingRef.current && duration > 0) {
        onSeek(xToTime(e.clientX));
        return;
      }
      // Trim drag
      if (trimDrag.current) {
        const { clipId, edge, trackWidth } = trimDrag.current;
        const inner = trackInnerRef.current;
        if (!inner || duration === 0) return;
        const rect = inner.getBoundingClientRect();
        const pct = (e.clientX - rect.left) / trackWidth;
        const newTime = Math.max(0, Math.min(pct * duration, duration));
        const clip = generatedClips.find(c => c.id === clipId);
        if (!clip || !onUpdateClip) return;
        if (edge === 'start') {
          const newStart = Math.min(newTime, clip.end - 0.1);
          onUpdateClip(clipId, { start: parseFloat(newStart.toFixed(3)) });
        } else {
          const newEnd = Math.max(newTime, clip.start + 0.1);
          onUpdateClip(clipId, { end: parseFloat(newEnd.toFixed(3)) });
        }
        return;
      }
      // Draw drag
      if (drawDrag.current && duration > 0) {
        const t = xToTime(e.clientX);
        const { startTime } = drawDrag.current;
        setDrawingClip({
          start: Math.min(startTime, t),
          end: Math.max(startTime, t),
        });
      }
    };

    const onMouseUp = (e: MouseEvent) => {
      if (isScrubbingRef.current) {
        isScrubbingRef.current = false;
      }
      if (trimDrag.current) {
        trimDrag.current = null;
        return;
      }
      if (drawDrag.current && drawingClip && onAddClip) {
        const minDur = 0.3;
        if (drawingClip.end - drawingClip.start > minDur) {
          onAddClip({
            start: parseFloat(drawingClip.start.toFixed(3)),
            end: parseFloat(drawingClip.end.toFixed(3)),
            label: 'Manual Clip',
          });
        }
        drawDrag.current = null;
        setDrawingClip(null);
      }
    };

    window.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    return () => {
      window.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
    };
  }, [generatedClips, duration, drawingClip, onUpdateClip, onAddClip, onSeek, xToTime]);

  // Build ruler marks based on duration
  const buildRulerMarks = () => {
    if (duration === 0) {
      return Array.from({ length: 21 }).map((_, i) => ({
        label: `0:${String(i).padStart(2, '00')}`,
        pct: i / 20,
      }));
    }
    const totalSeconds = duration;
    let step = 1;
    if (totalSeconds > 600) step = 60;
    else if (totalSeconds > 120) step = 30;
    else if (totalSeconds > 60) step = 10;
    else if (totalSeconds > 30) step = 5;
    else step = 1;

    const marks = [];
    for (let t = 0; t <= totalSeconds; t += step) {
      marks.push({ label: formatRulerTime(t), pct: t / totalSeconds });
    }
    return marks;
  };

  const marks = buildRulerMarks();
  const innerWidth = `${100 * zoomScale}%`;

  const selectedClip = generatedClips.find(c => c.id === selectedClipId);

  return (
    <div className="timeline-container glass-panel">
      {/* ── Toolbar ── */}
      <div className="timeline-header">
        <div className="timeline-tools">
          <button
            className="tool-icon-btn"
            title="Split clip at playhead (S)"
            disabled={!videoSrc || duration === 0}
            onClick={handleSplit}
          >
            <SplitSquareHorizontal size={16} />
          </button>
          <button className="tool-icon-btn" title="Cut (Ctrl+X)" disabled={!videoSrc}>
            <Scissors size={16} />
          </button>
          <button className="tool-icon-btn" title="Duplicate selected clip" disabled={!selectedClip || !onAddClip}
            onClick={() => {
              if (selectedClip && onAddClip) {
                onAddClip({ start: selectedClip.start, end: selectedClip.end, label: selectedClip.label + ' (copy)' });
              }
            }}
          >
            <Copy size={16} />
          </button>
          <button
            className="tool-icon-btn danger"
            title="Delete selected clip (Del)"
            disabled={!selectedClipId}
            onClick={handleDeleteSelected}
          >
            <Trash2 size={16} />
          </button>
          {generatedClips.length > 0 && (
            <span className="clip-count-badge">
              {generatedClips.length} clip{generatedClips.length > 1 ? 's' : ''}
            </span>
          )}
          {selectedClip && (
            <span className="selected-clip-info">
              ✂ {selectedClip.label} &nbsp;
              <span className="clip-time-range">
                {formatRulerTime(selectedClip.start)} – {formatRulerTime(selectedClip.end)}
                &nbsp;({(selectedClip.end - selectedClip.start).toFixed(1)}s)
              </span>
            </span>
          )}
        </div>

        <div className="timeline-zoom">
          <button
            className="tool-icon-btn"
            onClick={() => setZoom(z => Math.max(1, z - 10))}
            title="Zoom Out"
          >
            <ZoomOut size={15} />
          </button>
          <input
            type="range"
            min="1"
            max="100"
            value={zoom}
            className="styled-slider zoom-slider"
            onChange={e => setZoom(Number(e.target.value))}
          />
          <button
            className="tool-icon-btn"
            onClick={() => setZoom(z => Math.min(100, z + 10))}
            title="Zoom In"
          >
            <ZoomIn size={15} />
          </button>
          <span className="zoom-label">{zoomScale.toFixed(1)}x</span>
        </div>
      </div>

      {/* ── Ruler (synced scroll, always visible, click/drag to scrub) ── */}
      <div className="timeline-ruler-scroll" ref={rulerScrollRef}>
        <div
          className="timeline-ruler"
          style={{ width: innerWidth, cursor: duration > 0 ? 'ew-resize' : 'default' }}
          onMouseDown={handleRulerMouseDown}
          title="Click or drag to scrub playhead"
        >
          {marks.map((mark, i) => (
            <div key={i} className="ruler-mark" style={{ left: `${mark.pct * 100}%` }}>
              <span>{mark.label}</span>
            </div>
          ))}
        </div>
      </div>

      {/* ── Tracks (scrollable) ── */}
      <div
        className="timeline-tracks"
        ref={scrollRef}
        onClick={handleTrackAreaClick}
        style={{ cursor: videoSrc ? 'crosshair' : 'default' }}
      >
        <div className="timeline-track-inner" style={{ width: innerWidth }} ref={trackInnerRef}>

          {/* AI Cuts Track */}
          <div className="track-container magic-cuts-track">
            <div className="track-header ai-track-header">
              <span>AI</span>
            </div>
            <div
              className="track-body"
              onMouseDown={handleTrackBodyMouseDown}
            >
              {generatedClips.map(clip => {
                const widthPercent = duration > 0 ? ((clip.end - clip.start) / duration) * 100 : 0;
                const leftPercent = duration > 0 ? (clip.start / duration) * 100 : 0;
                const isSelected = clip.id === selectedClipId;
                return (
                  <div
                    key={clip.id}
                    className={`clip ai-clip${isSelected ? ' selected' : ''}`}
                    style={{ width: `${widthPercent}%`, left: `${leftPercent}%` }}
                    onClick={e => handleClipClick(e, clip.id, clip.start)}
                    title={`${clip.label}: ${formatRulerTime(clip.start)} – ${formatRulerTime(clip.end)}`}
                  >
                    {/* Left trim handle */}
                    <div
                      className="trim-handle trim-handle-left"
                      onMouseDown={e => handleTrimMouseDown(e, clip.id, 'start', clip.start)}
                      title="Drag to trim start"
                    />
                    <span className="clip-label">{clip.label}</span>
                    {/* Right trim handle */}
                    <div
                      className="trim-handle trim-handle-right"
                      onMouseDown={e => handleTrimMouseDown(e, clip.id, 'end', clip.end)}
                      title="Drag to trim end"
                    />
                    {onDeleteClip && (
                      <button
                        className="clip-delete-btn"
                        onClick={e => handleDeleteClip(e, clip.id)}
                        title="Remove clip"
                      >
                        ×
                      </button>
                    )}
                  </div>
                );
              })}

              {/* Drawing preview */}
              {drawingClip && duration > 0 && (
                <div
                  className="clip drawing-clip"
                  style={{
                    left: `${(drawingClip.start / duration) * 100}%`,
                    width: `${((drawingClip.end - drawingClip.start) / duration) * 100}%`,
                    pointerEvents: 'none',
                  }}
                >
                  <span className="clip-label">
                    {(drawingClip.end - drawingClip.start).toFixed(1)}s
                  </span>
                </div>
              )}

              {generatedClips.length === 0 && !drawingClip && (
                <div className="timeline-empty-hint">
                  <span>Drag on track to add manual clip · AI clips appear here after generation</span>
                </div>
              )}
            </div>
          </div>

          {/* Video Track */}
          <div className="track-container">
            <div className="track-header"><span>V1</span></div>
            <div className="track-body">
              {videoSrc ? (
                <div className="clip video-clip" style={{ width: '100%', left: '0%' }}>
                  <span className="clip-label">Imported Video</span>
                </div>
              ) : (
                <div className="timeline-empty-hint">
                  <span>Drag &amp; drop video to start editing</span>
                </div>
              )}
            </div>
          </div>

          {/* Audio Track */}
          <div className="track-container">
            <div className="track-header"><span>A1</span></div>
            <div className="track-body">
              {bgmSrc ? (
                <div className="clip audio-clip" style={{ width: '100%', left: '0%' }}>
                  <div className="waveform-mock" />
                  <span className="clip-label">Background Audio</span>
                </div>
              ) : (
                <div className="timeline-empty-hint">
                  <span>No background audio</span>
                </div>
              )}
            </div>
          </div>

          {/* Text / Caption Track */}
          <div className="track-container">
            <div className="track-header"><span>T1</span></div>
            <div className="track-body">
              {cinematicMode ? (
                <div className="clip text-clip" style={{ width: '30%', left: '10%' }}>
                  <span className="clip-label">"Cinematic Style"</span>
                </div>
              ) : (
                <div className="timeline-empty-hint">
                  <span>No text overlays</span>
                </div>
              )}
            </div>
          </div>

          {/* Playhead */}
          <div className="playhead" style={{ left: `${playheadPercent}%` }}>
            <div
              className="playhead-top"
              onMouseDown={handlePlayheadMouseDown}
              title="Drag to scrub"
            />
            <div className="playhead-line" />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Timeline;
