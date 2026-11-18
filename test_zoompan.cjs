const { execSync } = require('child_process');
try {
  // CapCut style bounce pump: starts at 1.3x zoom and quickly zooms out to 1.0x over 15 frames (0.5s)
  // zoompan evaluates for each output frame. `in` is the input frame count.
  // We want z to decay from 1.3 to 1.0
  const zoompan = `zoompan=z='max(1.0, 1.3 - (in/15)*0.3)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1280x720`;
  
  execSync(`ffmpeg -f lavfi -i testsrc=duration=2:size=1280x720:rate=30 -vf "${zoompan}" -y test_zoompan.mp4`, {stdio:'pipe'});
  console.log('success');
} catch(e) {
  console.error(e.stderr.toString());
}
