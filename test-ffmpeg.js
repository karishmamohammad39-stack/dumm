const { execSync } = require('child_process');

// Mock beat expression
const beatTimes = [0, 2.5];
const beatExprs = beatTimes.map(t => `between(t,${t.toFixed(2)},${(t+0.3).toFixed(2)})`).join('+');
const isBeatExpr = beatExprs || '0';

const filterStr = `[0:v]crop=ih*(9/16):ih,eq=contrast=1.2:saturation=1.4:brightness=0.4*(${isBeatExpr}),crop=in_w-20:in_h-20:10+15*sin(t*40)*(${isBeatExpr}):10+15*cos(t*45)*(${isBeatExpr})[v_out]`;

console.log("Testing filter string:\n", filterStr);

try {
  // Use a dummy input (color source) to test if the filter parses
  execSync(`ffmpeg -f lavfi -i color=c=black:s=1280x720 -filter_complex "${filterStr}" -map "[v_out]" -frames:v 1 -y NUL`, { stdio: 'pipe' });
  console.log("FFmpeg filter syntax is valid!");
} catch (e) {
  console.error("FFmpeg error:", e.stderr ? e.stderr.toString() : e.message);
}
