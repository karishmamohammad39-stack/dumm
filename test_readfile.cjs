const { FFmpeg } = require('@ffmpeg/ffmpeg');

async function run() {
  const ff = new FFmpeg();
  await ff.load();
  try {
    const data = await ff.readFile('nonexistent.mp4');
    console.log('ReadFile succeeded???', data.length);
  } catch (e) {
    console.log('ReadFile threw an error:', e.message);
  }
}
run();
