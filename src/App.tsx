import { useState, useEffect, useCallback, useRef } from 'react';
import './App.css';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import VideoPlayer from './components/VideoPlayer';
import Timeline from './components/Timeline';
import ToolsPanel from './components/ToolsPanel';
import PipelineStatus from './components/PipelineStatus';
import type { HighlightClip, PipelineStep, VideoFilters, AspectRatio } from './types';
import { exportMagicCuts, exportAgenticCuts } from './lib/ffmpeg';
import { detectBeats } from './lib/audioAnalysis';
import { type MediaFile } from './types';

function App() {
  const [videoMedia, setVideoMedia] = useState<MediaFile | null>(null);
  const [bgmMedia, setBgmMedia] = useState<MediaFile | null>(null);
  const [referenceMedia, setReferenceMedia] = useState<MediaFile | null>(null);

  const videoSrc = videoMedia?.url || null;
  const bgmSrc = bgmMedia?.url || null;
  const [cinematicMode, setCinematicMode] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [seekTime, setSeekTime] = useState<number | null>(null);
  const [isMuted, setIsMuted] = useState(false);

  // ── Color / Format adjustments ──
  const [videoFilters, setVideoFilters] = useState<VideoFilters>({ exposure: 0, contrast: 0, saturation: 0 });
  const [aspectRatio, setAspectRatio] = useState<AspectRatio>('16:9');

  const currentTimeRef = useRef(0);
  const durationRef = useRef(0);
  // Keep cinematicMode accessible inside effects without stale closures
  const cinematicModeRef = useRef(cinematicMode);
  const bgmSrcRef = useRef(bgmSrc);

  useEffect(() => { cinematicModeRef.current = cinematicMode; }, [cinematicMode]);
  useEffect(() => { bgmSrcRef.current = bgmSrc; }, [bgmSrc]);

  // AI Generator State
  const [isGenerating, setIsGenerating] = useState(false);
  const [generatedClips, setGeneratedClips] = useState<HighlightClip[]>([]);

  // Export State
  const [isExporting, setIsExporting] = useState(false);
  const [exportProgress, setExportProgress] = useState(0);

  // ── AUTO PIPELINE ──
  const [pipelineStep, setPipelineStep] = useState<PipelineStep>('idle');
  const [pipelineMessage, setPipelineMessage] = useState('');
  const [pipelineError, setPipelineError] = useState('');
  const autoPipelineRef = useRef(false);  // tracks if auto-mode is armed
  const clipsReadyRef = useRef<HighlightClip[]>([]);

  // Keep refs in sync
  const handleSetCurrentTime = useCallback((t: number) => {
    currentTimeRef.current = t;
    setCurrentTime(t);
  }, []);

  const handleSetDuration = useCallback((d: number) => {
    durationRef.current = d;
    setDuration(d);
  }, []);

  const handleVideoUpload = (file: MediaFile) => {
    setVideoMedia(file);
    setIsPlaying(false);
    setCurrentTime(0);
    setDuration(0);
    currentTimeRef.current = 0;
    durationRef.current = 0;
    setGeneratedClips([]);
    clipsReadyRef.current = [];
    setPipelineStep('idle');
    setPipelineError('');
    setPipelineMessage('');
    autoPipelineRef.current = true;
  };

  // ── STEP 1: When duration becomes known, generate highlights ──
  // Uses refs for cinematicMode and bgmSrc to avoid stale closure values.
  useEffect(() => {
    if (!autoPipelineRef.current) return;
    if (duration <= 0 || !videoSrc) return;

    autoPipelineRef.current = false;

    const analyzeVideo = async () => {
      try {
        setPipelineStep('analyzing');
        setPipelineMessage('AI is analyzing video rhythm and highlights...');
        setIsGenerating(true);

        // Read current values from refs to avoid stale closure
        const isCinematic = cinematicModeRef.current;
        const currentBgmSrc = bgmSrcRef.current;
        let beats: number[] = [];

        if (isCinematic && currentBgmSrc) {
          setPipelineMessage('Analyzing background music for kick beats...');
          beats = await detectBeats(currentBgmSrc);
        }

        const clips: HighlightClip[] = [];

        if (beats.length > 2) {
          // Beat-Aligned Montage: Rhythmic cut points
          const numClips = Math.min(beats.length - 1, 12);
          for (let i = 0; i < numClips; i++) {
            const beatDur = Math.max(0.4, beats[i+1] - beats[i]);
            const progressRatio = (i + 0.5) / numClips;
            const centerTime = duration * progressRatio;
            const start = Math.max(0, centerTime - (beatDur / 2));
            const end = Math.min(duration, start + beatDur);

            clips.push({
              id: `ai-beat-${Date.now()}-${i}`,
              start: parseFloat(start.toFixed(3)),
              end: parseFloat(end.toFixed(3)),
              label: `Beat Drop ${i + 1}`,
            });
          }
        } else {
          // Multi-Segment Highlight Cuts
          const numClips = isCinematic ? 6 : 4;
          const segmentSpan = duration / numClips;

          for (let i = 0; i < numClips; i++) {
            const clipDur = isCinematic ? Math.min(segmentSpan * 0.4, 2.5) : Math.min(segmentSpan * 0.5, 6.0);
            const start = (i * segmentSpan) + (segmentSpan * 0.1);
            const end = Math.min(duration, start + clipDur);

            clips.push({
              id: `ai-clip-${Date.now()}-${i}`,
              start: parseFloat(start.toFixed(3)),
              end: parseFloat(end.toFixed(3)),
              label: isCinematic ? `Fast Cut ${i + 1}` : `Highlight ${i + 1}`,
            });
          }
        }

        clipsReadyRef.current = clips;
        setGeneratedClips(clips);
        setPipelineStep('idle');
        setPipelineMessage(`✨ Found ${clips.length} highlight clips. Click "Export Video" to render your reel.`);
      } catch (err) {
        console.error("Analysis failed", err);
        setPipelineError("Failed to analyze beats.");
        setPipelineStep('error');
      } finally {
        setIsGenerating(false);
      }
    };

    analyzeVideo();
  }, [duration, videoSrc]); // intentionally omits cinematicMode/bgmSrc — read from refs above

  // ── Keyboard shortcuts ──
  const handleKeyDown = useCallback((e: KeyboardEvent) => {
    const tag = (e.target as HTMLElement).tagName.toLowerCase();
    if (tag === 'input' || tag === 'textarea') return;

    switch (e.code) {
      case 'Space':
        e.preventDefault();
        if (videoSrc) setIsPlaying(p => !p);
        break;
      case 'KeyK':
        if (videoSrc) setIsPlaying(false);
        break;
      case 'KeyJ':
        if (videoSrc) setSeekTime(Math.max(0, currentTimeRef.current - 10));
        break;
      case 'KeyL':
        if (videoSrc) setSeekTime(Math.min(durationRef.current, currentTimeRef.current + 10));
        break;
      case 'KeyM':
        if (videoSrc) setIsMuted(m => !m);
        break;
      default:
        break;
    }
  }, [videoSrc]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  // ── Manual Generate (button in ToolsPanel) ──
  const handleGenerateMagicCuts = async () => {
    if (!videoSrc || duration === 0) return;

    try {
      setPipelineStep('analyzing');
      setPipelineMessage('Re-analyzing video and audio for highlights...');
      setIsGenerating(true);
      clipsReadyRef.current = [];

      const isCinematic = cinematicMode;
      let beats: number[] = [];

      if (isCinematic && bgmSrc) {
        setPipelineMessage('Analyzing background music for beats...');
        beats = await detectBeats(bgmSrc);
      }

      const clips: HighlightClip[] = [];

      if (beats.length > 2) {
        // Masterpiece Montage: Up to 15 rapid cuts
        const numClips = Math.min(beats.length - 1, 15);
        for (let i = 0; i < numClips; i++) {
          const beatDur = beats[i+1] - beats[i];
          let start = (duration * 0.05) + Math.random() * (duration * 0.85);
          const end = Math.min(start + beatDur, duration);

          clips.push({
            id: `ai-beat-${Date.now()}-${i}`,
            start: parseFloat(start.toFixed(3)),
            end: parseFloat(end.toFixed(3)),
            label: `Beat Cut ${i + 1}`,
          });
        }
      } else {
        const numClips = isCinematic ? Math.floor(Math.random() * 5) + 6 : Math.floor(Math.random() * 2) + 2;
        let start = duration * 0.05;

        for (let i = 0; i < numClips; i++) {
          const clipDur = isCinematic ? Math.min(duration * 0.08, 1.5) : Math.min(duration * 0.15, 15);
          if (isCinematic) {
            start = (duration * 0.05) + Math.random() * (duration * 0.85);
          }
          const end = Math.min(start + clipDur, duration);
          clips.push({
            id: `ai-clip-${Date.now()}-${i}`,
            start: parseFloat(start.toFixed(3)),
            end: parseFloat(end.toFixed(3)),
            label: isCinematic ? `Fast Cut ${i + 1}` : `Highlight ${i + 1}`,
          });
          if (!isCinematic) {
            start = end + (duration * 0.2);
          }
        }
      }

      clipsReadyRef.current = clips;
      setGeneratedClips(clips);
      setPipelineStep('idle');
      setPipelineMessage('');
    } catch (err) {
      console.error(err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleDeleteClip = (id: string) => {
    setGeneratedClips(prev => prev.filter(c => c.id !== id));
    clipsReadyRef.current = clipsReadyRef.current.filter(c => c.id !== id);
  };

  const handleUpdateClip = (id: string, updates: Partial<Pick<HighlightClip, 'start' | 'end' | 'label'>>) => {
    setGeneratedClips(prev =>
      prev.map(c => c.id === id ? { ...c, ...updates } : c)
    );
    clipsReadyRef.current = clipsReadyRef.current.map(c =>
      c.id === id ? { ...c, ...updates } : c
    );
  };

  const handleSplitClip = (id: string, splitTime: number) => {
    const clip = generatedClips.find(c => c.id === id);
    if (!clip) return;
    const uid = () => `manual-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`;
    const left: HighlightClip = { id: uid(), start: clip.start, end: parseFloat(splitTime.toFixed(3)), label: clip.label + ' A' };
    const right: HighlightClip = { id: uid(), start: parseFloat(splitTime.toFixed(3)), end: clip.end, label: clip.label + ' B' };
    const updated = generatedClips.map(c => (c.id === id ? null : c)).filter((c): c is HighlightClip => c !== null);
    const idx = generatedClips.findIndex(c => c.id === id);
    updated.splice(idx, 0, left, right);
    setGeneratedClips(updated);
    clipsReadyRef.current = updated;
  };

  const handleAddClip = (clip: Omit<HighlightClip, 'id'>) => {
    const newClip: HighlightClip = {
      id: `manual-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
      ...clip,
    };
    setGeneratedClips(prev => [...prev, newClip]);
    clipsReadyRef.current = [...clipsReadyRef.current, newClip];
  };

  // ── Manual Export ──
  const handleExport = async () => {
    if (!videoMedia) {
      setPipelineStep('error');
      setPipelineError('Please upload a video first (drag & drop or use the Media panel on the left).');
      return;
    }
    const clipsToExport = generatedClips.length > 0 ? generatedClips : [{
      id: 'full_video',
      start: 0,
      end: duration > 0 ? duration : 10,
      label: 'Full Video',
    }];

    try {
      setIsExporting(true);
      setExportProgress(0);
      setPipelineStep('exporting');
      setPipelineMessage(generatedClips.length > 0 ? 'Encoding your highlight reel...' : 'Encoding your video...');

      const outputUrl = await exportMagicCuts(
        videoMedia.file,
        clipsToExport,
        {
          onProgress: (p) => setExportProgress(p),
          cinematicMode,
          bgmFile: bgmMedia?.file,
          filters: videoFilters,
          aspectRatio,
        }
      );

      setExportProgress(100);

      const a = document.createElement('a');
      a.href = outputUrl;
      a.download = `VIBE_CUTS_EXPORT_${Date.now()}.mp4`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(outputUrl), 10000);

      setPipelineStep('done');
      setPipelineMessage('Download complete!');
    } catch (error: any) {
      console.error('Export failed', error);
      setPipelineStep('error');
      setPipelineError(error?.message || 'Export failed. See browser console for details.');
    } finally {
      setIsExporting(false);
      setExportProgress(0);
    }
  };

  const handleDismissPipeline = () => {
    setPipelineStep('idle');
    setPipelineMessage('');
    setPipelineError('');
  };

  const handleAiPrompt = (prompt: string) => {
    const p = prompt.toLowerCase();
    if (p.includes('cinematic') || p.includes('telugu') || p.includes('shake') || p.includes('fast') || p.includes('beat') || p.includes('masterpiece') || p.includes('capcut') || p.includes('effect') || p.includes('vfx') || p.includes('epic')) {
      setCinematicMode(true);
    } else if (p.includes('basic') || p.includes('simple') || p.includes('normal') || p.includes('remove')) {
      setCinematicMode(false);
    }
  };

  // ── Agentic (Backend) Pipeline ──
  const handleAgenticEdit = async (prompt: string, sector: string = 'reels') => {
    if (!videoMedia) {
      alert('Please upload a video first.');
      return;
    }

    try {
      setIsExporting(true);
      setExportProgress(10); // Indeterminate start
      setPipelineStep('analyzing');
      setPipelineMessage('The AI Engine is crafting a 4-Pillar JSON Editing Plan...');

      const outputUrl = await exportAgenticCuts(
        videoMedia.file,
        prompt,
        sector,
        (msg) => setPipelineMessage(msg)
      );

      setExportProgress(100);

      const a = document.createElement('a');
      a.href = outputUrl;
      a.download = `AGENTIC_VFX_MASTERPIECE_${Date.now()}.mp4`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(() => URL.revokeObjectURL(outputUrl), 10000);

      setPipelineStep('done');
      setPipelineMessage('Agentic Edit successfully downloaded!');
    } catch (error) {
      console.error('Agentic Edit failed', error);
      setPipelineStep('error');
      setPipelineError(error instanceof Error ? error.message : 'Server error');
    } finally {
      setIsExporting(false);
      setExportProgress(0);
    }
  };

  return (
    <div className="app-container">
      <Header
        onExport={handleExport}
        isExporting={isExporting}
        exportProgress={exportProgress}
      />
      <Sidebar
        onVideoUpload={handleVideoUpload}
        onAudioUpload={(file) => setBgmMedia(file)}
        onReferenceUpload={(file) => setReferenceMedia(file)}
      />
      <VideoPlayer
        videoSrc={videoSrc}
        isPlaying={isPlaying}
        setIsPlaying={setIsPlaying}
        currentTime={currentTime}
        setCurrentTime={handleSetCurrentTime}
        duration={duration}
        setDuration={handleSetDuration}
        seekTime={seekTime}
        setSeekTime={setSeekTime}
        isMuted={isMuted}
        setIsMuted={setIsMuted}
        cinematicMode={cinematicMode}
        filters={videoFilters}
        aspectRatio={aspectRatio}
        onAspectRatioChange={setAspectRatio}
        onDropVideo={(file) => {
          const media: import('./types').MediaFile = {
            url: URL.createObjectURL(file),
            name: file.name,
            size: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
            type: 'video',
            file,
          };
          handleVideoUpload(media);
        }}
      />
      <ToolsPanel
        isGenerating={isGenerating}
        onGenerate={handleGenerateMagicCuts}
        pipelineStep={pipelineStep}
        exportProgress={exportProgress}
        cinematicMode={cinematicMode}
        onCinematicModeChange={setCinematicMode}
        onAiPrompt={handleAiPrompt}
        onAgenticEdit={handleAgenticEdit}
        videoFilters={videoFilters}
        onFiltersChange={setVideoFilters}
        aspectRatio={aspectRatio}
        onAspectRatioChange={setAspectRatio}
      />
      <Timeline
        currentTime={currentTime}
        duration={duration}
        onSeek={time => setSeekTime(time)}
        videoSrc={videoSrc}
        bgmSrc={bgmSrc}
        cinematicMode={cinematicMode}
        generatedClips={generatedClips}
        onDeleteClip={handleDeleteClip}
        onUpdateClip={handleUpdateClip}
        onSplitClip={handleSplitClip}
        onAddClip={handleAddClip}
      />

      {/* Auto-pipeline floating status toast */}
      <PipelineStatus
        step={pipelineStep}
        message={pipelineMessage}
        error={pipelineError}
        progress={exportProgress}
        onDismiss={handleDismissPipeline}
        onRetry={handleExport}
      />

      {/* Reference video — stored in state, available for future style-matching features */}
      {referenceMedia && (
        <div style={{ display: 'none' }} aria-hidden="true" data-reference-file={referenceMedia.name} />
      )}
    </div>
  );
}

export default App;
