const { execSync } = require('child_process');
try {
  let filterStr = `[0:v]crop=ih*(9/16):ih`;
  filterStr += `,eq=contrast=1.3:saturation=1.5`;

  const negateExprs = [`between(t,0.5,0.6)`];
  const rgbaExprs = [`between(t,1.0,1.2)`];
  const flashExprs = [`between(t,1.5,1.7)`];
  
  if (negateExprs.length > 0) filterStr += `,negate=enable='${negateExprs.join('+')}'`;
  if (rgbaExprs.length > 0) filterStr += `,rgbashift=rh=20:bh=-20:enable='${rgbaExprs.join('+')}'`;
  if (flashExprs.length > 0) filterStr += `,eq=brightness=0.4:enable='${flashExprs.join('+')}'`;
  
  const beatExprs = [`((1-(t-0.5)/0.3)*between(t,0.5,0.8))`, `((1-(t-1.0)/0.3)*between(t,1.0,1.3))`].join('+');
  const decayExpr = beatExprs || '0';
  const shakeX = `in_w*0.04*sin(t*80)*(${decayExpr})`;
  const shakeY = `in_h*0.04*cos(t*90)*(${decayExpr})`;
  filterStr += `,vignette=PI/4,crop='in_w*0.85':'in_h*0.85':'(in_w-out_w)/2 + ${shakeX}':'(in_h-out_h)/2 + ${shakeY}'[v_out]`;
  
  execSync(`ffmpeg -f lavfi -i testsrc=duration=2:size=1280x720:rate=30 -filter_complex "${filterStr}" -map "[v_out]" -y test_full.mp4`, {stdio:'pipe'});
  console.log('success');
} catch(e) {
  console.error(e.stderr.toString());
}
