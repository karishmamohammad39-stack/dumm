const { execSync } = require('child_process');
try {
  // Test portrait crop followed by a smooth CapCut zoom pump
  const vfStr = `crop=ih*(9/16):ih,zoompan=z='max(1.0, 1.25 - (in/15)*0.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280,fps=30`;
  
  execSync(`ffmpeg -f lavfi -i testsrc=duration=2:size=1920x1080:rate=30 -vf "${vfStr}" -y test_zoompan2.mp4`, {stdio:'pipe'});
  console.log('success');
} catch(e) {
  console.error(e.stderr.toString());
}
