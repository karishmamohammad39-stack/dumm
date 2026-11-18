const { execSync } = require('child_process');
try {
  const isBeatExpr = "between(t,0.5,1.0)";
  const zoomAmount = 0.15;
  const zoomCrop = `crop='in_w - (in_w*${zoomAmount}*(${isBeatExpr}))':'in_h - (in_h*${zoomAmount}*(${isBeatExpr}))':'(in_w-out_w)/2 + 20*sin(t*50)*(${isBeatExpr})':'(in_h-out_h)/2 + 20*cos(t*55)*(${isBeatExpr})'`;
  
  const filter = `[0:v]crop=ih*(9/16):ih,eq=contrast=1.3:saturation=1.5:brightness='0.3*(${isBeatExpr})',hue='h=t*10*(${isBeatExpr})',vignette=PI/4,${zoomCrop}[v_out]`;
  
  execSync(`ffmpeg -f lavfi -i testsrc=duration=2:size=1280x720:rate=30 -filter_complex "${filter}" -map "[v_out]" -y test_vfx.mp4`, {stdio:'pipe'});
  console.log('success');
} catch(e) {
  console.error(e.stderr.toString());
}
