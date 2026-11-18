export interface MediaFile {
  url: string;
  name: string;
  size: string;
  type: 'video' | 'audio' | 'reference' | 'text';
  file: File;
}

export interface HighlightClip {
  id: string;
  start: number;
  end: number;
  label: string;
}

export type PipelineStep = 'idle' | 'analyzing' | 'loading_ffmpeg' | 'exporting' | 'done' | 'error';

export interface CaptionSegment {
  id: number;
  start: number;
  end: number;
  text: string;
}

export type AspectRatio = '16:9' | '9:16' | '1:1' | '4:5';

export interface VideoFilters {
  exposure: number;   // -100 to 100, default 0
  contrast: number;   // -100 to 100, default 0
  saturation: number; // -100 to 100, default 0
}
