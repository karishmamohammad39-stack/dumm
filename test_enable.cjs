const { execSync } = require('child_process');
try {
  const filter = `[0:v]negate=enable='between(t,0.5,1.0)',rgbashift=rh=20:bv=20:enable='between(t,1.2,1.7)'[v_out]`;
  
  execSync(`ffmpeg -f lavfi -i testsrc=duration=2:size=1280x720:rate=30 -filter_complex "${filter}" -map "[v_out]" -y test_enable.mp4`, {stdio:'pipe'});
  console.log('success');
} catch(e) {
  console.error(e.stderr.toString());
}
