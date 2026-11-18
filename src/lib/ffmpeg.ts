import { FFmpeg } from '@ffmpeg/ffmpeg';
import { fetchFile } from '@ffmpeg/util';
import type { HighlightClip, CaptionSegment, VideoFilters, AspectRatio } from '../types';

import coreURL from '@ffmpeg/core?url';
import wasmURL from '@ffmpeg/core/wasm?url';

let ffmpegInstance: FFmpeg | null = null;
const BACKEND_URL = 'http://localhost:8000';

export const loadFFmpeg = async (onProgress?: (progress: number) => void): Promise<FFmpeg> => {
  if (ffmpegInstance) return ffmpegInstance;

  const ff = new FFmpeg();

  ff.on('log', ({ message }) => console.log('[FFmpeg]', message));

  if (onProgress) {
    ff.on('progress', ({ progress }) => onProgress(Math.min(progress * 100, 99)));
  }

  await ff.load({ coreURL, wasmURL });
  ffmpegInstance = ff;
  return ff;
};

export interface ExportOptions {
  onProgress?: (progress: number) => void;
  cinematicMode?: boolean;
  bgmFile?: File;
  filters?: VideoFilters;
  aspectRatio?: AspectRatio;
}

/** Map AspectRatio to FFmpeg crop filter */
const aspectRatioCrop = (ar: AspectRatio): string | null => {
  switch (ar) {
    case '9:16': return 'crop=ih*(9/16):ih';
    case '1:1':  return 'crop=ih:ih';
    case '4:5':  return 'crop=ih*(4/5):ih';
    default:     return null;
  }
};

/** Build eq filter from VideoFilters */
const buildEqFilter = (filters?: VideoFilters): string | null => {
  if (!filters) return null;
  const brightness = filters.exposure / 100;
  const contrast   = 1 + filters.contrast / 100;
  const saturation = 1 + filters.saturation / 100;
  if (brightness === 0 && contrast === 1 && saturation === 1) return null;
  return `eq=brightness=${brightness.toFixed(3)}:contrast=${contrast.toFixed(3)}:saturation=${saturation.toFixed(3)}`;
};

/** Safely exec an FFmpeg command — always re-encode to avoid codec/container mismatch */
const execClip = async (
  ff: FFmpeg,
  inputFile: string,
  outputFile: string,
  start: number,
  dur: number,
  vfFilter: string | null,
  crf = 26,
): Promise<void> => {
  const args: string[] = [
    // Input seeking BEFORE -i is fast-seek (keyframe accurate for start)
    '-ss', start.toFixed(3),
    '-i', inputFile,
    '-t', Math.max(0.1, dur).toFixed(3),
  ];

  if (vfFilter) {
    args.push('-vf', vfFilter);
  }

  // Always re-encode — avoids codec/container mismatch that causes Exit code 1
  args.push(
    '-c:v', 'libx264', '-preset', 'ultrafast', '-crf', crf.toString(),
    '-c:a', 'aac', '-b:a', '128k',
    '-movflags', '+faststart',
    '-y',
    outputFile,
  );

  const exit = await ff.exec(args);
  if (exit !== 0) {
    throw new Error(`Encoding clip failed (start=${start.toFixed(1)}s, dur=${dur.toFixed(1)}s, exit=${exit}). Your video may be in an unsupported codec.`);
  }
};

export const exportMagicCuts = async (
  videoFile: File,
  clips: HighlightClip[],
  options?: ExportOptions,
): Promise<string> => {
  if (clips.length === 0) throw new Error('No clips to export.');

  const backendReady = await isBackendAvailable();
  const isLargeFile = videoFile.size > 300 * 1024 * 1024; // > 300 MB (e.g. 1GB, 3GB, 10GB)

  // Use high-performance 64-bit native FFmpeg backend whenever available or for large files
  if (backendReady || isLargeFile) {
    if (!backendReady) {
      const sizeMB = (videoFile.size / 1024 / 1024).toFixed(0);
      throw new Error(
        `Video size is ${sizeMB} MB. For large files (1GB - 10GB+), start the backend server via 'run.bat' for high-speed native encoding.`
      );
    }
    return exportWithBackend(videoFile, clips, options);
  }

  const ff = await loadFFmpeg(options?.onProgress);
  const wasmFiles: string[] = [];

  // Write source files into the WASM virtual filesystem
  const ext = videoFile.name.match(/\.\w+$/)?.[0] ?? '.mp4';
  const inputFile = `input${ext}`;
  await ff.writeFile(inputFile, await fetchFile(videoFile));
  wasmFiles.push(inputFile);

  let bgmFile: string | null = null;
  if (options?.bgmFile) {
    const bext = options.bgmFile.name.match(/\.\w+$/)?.[0] ?? '.mp3';
    bgmFile = `bgm${bext}`;
    await ff.writeFile(bgmFile, await fetchFile(options.bgmFile));
    wasmFiles.push(bgmFile);
  }

  try {
    // ── PASS 1: Cut + encode each clip ─────────────────────────────────────
    const clipFiles: string[] = [];

    for (let i = 0; i < clips.length; i++) {
      const clip = clips[i];
      const dur = clip.end - clip.start;
      if (dur < 0.05) continue; // skip tiny/broken clips

      const outFile = `clip_${i}.mp4`;
      wasmFiles.push(outFile);
      clipFiles.push(outFile);

      let vfParts: string[] = [];

      if (options?.cinematicMode) {
        // 9:16 portrait crop + subtle Ken Burns zoom
        vfParts = [`crop=ih*(9/16):ih`, `zoompan=z='min(zoom+0.0015,1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280:fps=30`];
      } else {
        const crop = aspectRatioCrop(options?.aspectRatio ?? '16:9');
        const eq   = buildEqFilter(options?.filters);
        if (crop) vfParts.push(crop);
        if (eq)   vfParts.push(eq);
      }

      const vfFilter = vfParts.length > 0 ? vfParts.join(',') : null;
      const crf = options?.cinematicMode ? 24 : 26;
      await execClip(ff, inputFile, outFile, clip.start, dur, vfFilter, crf);

      // Update progress (clips take 80% of total)
      options?.onProgress?.(Math.round(((i + 1) / clips.length) * 80));
    }

    if (clipFiles.length === 0) throw new Error('All clips were too short to export.');

    // ── PASS 2: Concatenate ─────────────────────────────────────────────────
    let joinedFile: string;

    if (clipFiles.length === 1) {
      joinedFile = clipFiles[0];
    } else {
      const concatList = clipFiles.map(f => `file '${f}'`).join('\n');
      await ff.writeFile('concat.txt', concatList);
      wasmFiles.push('concat.txt', 'joined.mp4');

      const concatExit = await ff.exec([
        '-f', 'concat', '-safe', '0',
        '-i', 'concat.txt',
        '-c', 'copy',         // safe: all clips are already same codec/params
        '-y', 'joined.mp4',
      ]);
      if (concatExit !== 0) throw new Error('Failed to join clips. Try fewer clips.');
      joinedFile = 'joined.mp4';
    }

    options?.onProgress?.(88);

    // ── PASS 3: BGM mix (optional) ──────────────────────────────────────────
    let finalFile = joinedFile;

    if (bgmFile) {
      wasmFiles.push('final.mp4');
      const mixExit = await ff.exec([
        '-i', joinedFile,
        '-i', bgmFile,
        '-filter_complex',
        // Normalize video audio and mix with BGM at 0.4 volume
        '[0:a]volume=1.0[va];[1:a]volume=0.4[ba];[va][ba]amix=inputs=2:duration=first[a_out]',
        '-map', '0:v',
        '-map', '[a_out]',
        '-c:v', 'copy',
        '-c:a', 'aac', '-b:a', '192k',
        '-shortest',
        '-y', 'final.mp4',
      ]);

      if (mixExit === 0) {
        finalFile = 'final.mp4';
      } else {
        console.warn('BGM mix failed — exporting without background music.');
      }
    }

    options?.onProgress?.(98);

    const data = await ff.readFile(finalFile);
    options?.onProgress?.(100);
    return URL.createObjectURL(new Blob([data as Uint8Array], { type: 'video/mp4' }));

  } finally {
    for (const f of wasmFiles) {
      try { await ff.deleteFile(f); } catch { /* ok */ }
    }
  }
};

// ── Backend utilities ───────────────────────────────────────────────────────

export const isBackendAvailable = async (): Promise<boolean> => {
  try {
    const res = await fetch(`${BACKEND_URL}/health`, { signal: AbortSignal.timeout(2000) });
    return res.ok;
  } catch {
    return false;
  }
};

export const exportWithBackend = async (
  videoFile: File,
  clips: HighlightClip[],
  options?: ExportOptions,
): Promise<string> => {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open('POST', `${BACKEND_URL}/export-reel`);
    xhr.responseType = 'blob';

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        // Upload accounts for 0 - 75%
        const percent = Math.round((event.loaded / event.total) * 75);
        options?.onProgress?.(percent);
      }
    };

    xhr.onload = () => {
      if (xhr.status >= 200 && xhr.status < 300) {
        options?.onProgress?.(100);
        const blob = xhr.response;
        resolve(URL.createObjectURL(blob));
      } else {
        reject(new Error(`Backend export failed (status ${xhr.status}). Check server console.`));
      }
    };

    xhr.onerror = () => {
      reject(new Error('Network error connecting to backend. Ensure backend is running.'));
    };

    const fd = new FormData();
    fd.append('video', videoFile);
    fd.append('clips', JSON.stringify(clips));
    fd.append('cinematic_mode', options?.cinematicMode ? 'true' : 'false');
    fd.append('aspect_ratio', options?.aspectRatio ?? '16:9');
    fd.append('exposure', (options?.filters?.exposure ?? 0).toString());
    fd.append('contrast', (options?.filters?.contrast ?? 0).toString());
    fd.append('saturation', (options?.filters?.saturation ?? 0).toString());
    if (options?.bgmFile) {
      fd.append('bgm', options.bgmFile);
    }

    xhr.send(fd);
  });
};

export const transcribeWithBackend = async (
  videoUrl: string,
  start: number,
  end: number,
  onStatus?: (msg: string) => void,
): Promise<CaptionSegment[]> => {
  if (!await isBackendAvailable()) {
    throw new Error('Backend not available. Start it with: cd backend && python main.py');
  }

  onStatus?.('Fetching video...');
  const response = await fetch(videoUrl);
  const blob = await response.blob();
  const file = new File([blob], 'video.mp4', { type: 'video/mp4' });

  const makeFormData = () => {
    const fd = new FormData();
    fd.append('video', file);
    fd.append('trim_start', start.toString());
    fd.append('trim_end', end.toString());
    return fd;
  };

  onStatus?.('Transcribing with Whisper...');
  const res = await fetch(`${BACKEND_URL}/upload`, { method: 'POST', body: makeFormData() });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ error: 'Unknown error' }));
    throw new Error(err.error || `Backend error ${res.status}`);
  }

  const transcribeRes = await fetch(`${BACKEND_URL}/transcribe`, {
    method: 'POST',
    body: makeFormData(),
  }).catch(() => null);

  if (transcribeRes?.ok) {
    const data = await transcribeRes.json();
    return (data.segments as Array<{ id: number; start: number; end: number; text: string }>)
      .map((s, i) => ({ id: i, start: s.start, end: s.end, text: s.text }));
  }

  return [];
};

export const exportAgenticCuts = async (
  videoFile: File,
  prompt: string,
  sector: string,
  onStatus?: (msg: string) => void,
): Promise<string> => {
  if (!await isBackendAvailable()) {
    throw new Error('Backend not available. Start it: cd backend && python main.py');
  }

  onStatus?.('Sending to 4-Pillar AI Engine...');
  const fd = new FormData();
  fd.append('video', videoFile);
  fd.append('prompt', prompt);
  fd.append('sector', sector);

  const res = await fetch(`${BACKEND_URL}/agentic-edit`, { method: 'POST', body: fd });

  if (!res.ok) {
    let msg = `HTTP ${res.status}`;
    try { msg = (await res.json()).error || msg; } catch { /* ok */ }
    throw new Error(`AI Engine failed: ${msg}`);
  }

  onStatus?.('Downloading your masterpiece...');
  const blob = await res.blob();
  return URL.createObjectURL(blob);
};
