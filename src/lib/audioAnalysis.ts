/**
 * audioAnalysis.ts
 * Robust Web Audio API based beat and transient detection engine with adaptive thresholding.
 */

export async function detectBeats(audioUrl: string): Promise<number[]> {
  try {
    // Fetch the audio file
    const response = await fetch(audioUrl);
    const arrayBuffer = await response.arrayBuffer();

    // Decode using AudioContext to dynamically support arbitrary track lengths without 40s limits
    const tempAudioCtx = new (window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext)();
    const audioBuffer = await tempAudioCtx.decodeAudioData(arrayBuffer.slice(0));
    await tempAudioCtx.close();

    // Create an offline context matching the exact duration and sample rate of the audio track
    const sampleRate = audioBuffer.sampleRate;
    const totalSamples = audioBuffer.length;
    const filterContext = new OfflineAudioContext(1, totalSamples, sampleRate);

    const source = filterContext.createBufferSource();
    source.buffer = audioBuffer;

    // Apply lowpass biquad filter (150Hz) to isolate bass kicks and sub-bass transients
    const filter = filterContext.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = 150;
    filter.Q.value = 1.0;

    source.connect(filter);
    filter.connect(filterContext.destination);
    source.start(0);

    // Render the lowpass-filtered buffer
    const filteredBuffer = await filterContext.startRendering();
    const channelData = filteredBuffer.getChannelData(0);

    return getAdaptivePeaks(channelData, sampleRate);
  } catch (error) {
    console.error("Error in beat detection:", error);
    return [];
  }
}

/**
 * Finds amplitude peaks in the audio data using dynamic adaptive thresholding.
 */
function getAdaptivePeaks(data: Float32Array, sampleRate: number): number[] {
  if (data.length === 0) return [];

  // 1. Calculate overall mean energy and standard deviation for adaptive thresholding
  let sum = 0;
  let maxAbs = 0;
  const step = 50; // Sub-sample for performance
  for (let i = 0; i < data.length; i += step) {
    const val = Math.abs(data[i]);
    sum += val;
    if (val > maxAbs) maxAbs = val;
  }
  const mean = sum / (data.length / step);

  // If audio is practically silent, return early
  if (maxAbs < 0.02) return [];

  // Adaptive threshold: slightly above mean, scaled to peak dynamics
  const adaptiveThreshold = Math.max(0.08, Math.min(mean * 2.2, maxAbs * 0.45));

  // Chunk size: 0.28 seconds between beats (~214 BPM max) to prevent duplicate triggers
  const chunkSize = Math.floor(sampleRate * 0.28);
  const peaks: number[] = [];

  for (let i = 0; i < data.length; i += chunkSize) {
    let maxVolume = 0;
    let peakIndex = i;
    const chunkEnd = Math.min(i + chunkSize, data.length);

    for (let j = i; j < chunkEnd; j++) {
      const volume = Math.abs(data[j]);
      if (volume > maxVolume) {
        maxVolume = volume;
        peakIndex = j;
      }
    }

    if (maxVolume >= adaptiveThreshold) {
      const timestamp = parseFloat((peakIndex / sampleRate).toFixed(3));
      peaks.push(timestamp);
    }
  }

  return peaks;
}
