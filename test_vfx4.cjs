const { execSync } = require('child_process');
try {
  const t = 0.5;
  const decayExpr = `((1-(t-${t.toFixed(2)})/0.3)*between(t,${t.toFixed(2)},${(t+0.3).toFixed(2)}))`;
  
  const shakeX = `in_w*0.05*sin(t*80)*(${decayExpr})`;
  const shakeY = `in_h*0.05*cos(t*90)*(${decayExpr})`;
  
  const zoomCrop = `crop='in_w*0.85':'in_h*0.85':'(in_w-out_w)/2 + ${shakeX}':'(in_h-out_h)/2 + ${shakeY}'`;
  
  const filter = `[0:v]crop=ih*(9/16):ih,eq=contrast=1.5:saturation=2.0:brightness='0.6*(${decayExpr})',vignette=PI/3,${zoomCrop}[v_out]`;
  
  execSync(`ffmpeg -f lavfi -i testsrc=duration=2:size=1280x720:rate=30 -filter_complex "${filter}" -map "[v_out]" -y test_vfx4.mp4`, {stdio:'pipe'});
  console.log('success');
} catch(e) {
  console.error(e.stderr.toString());
}
