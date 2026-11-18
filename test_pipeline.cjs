const { execSync } = require('child_process');
const fs = require('fs');

try {
  // Pass 1: generate 2 clips
  const clip1Args = `-ss 0 -i testsrc=duration=2:size=1920x1080:rate=30 -t 1.5 -vf "crop=ih*(9/16):ih,zoompan=z='max(1.0, 1.25 - (in/15)*0.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280,fps=30" -c:v libx264 -preset ultrafast -y output_0.mp4`;
  execSync(`ffmpeg -f lavfi ${clip1Args}`, {stdio:'pipe'});
  
  const clip2Args = `-ss 0 -i testsrc=duration=2:size=1920x1080:rate=30 -t 1.5 -vf "crop=ih*(9/16):ih,zoompan=z='max(1.0, 1.25 - (in/15)*0.25)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=720x1280,fps=30" -c:v libx264 -preset ultrafast -y output_1.mp4`;
  execSync(`ffmpeg -f lavfi ${clip2Args}`, {stdio:'pipe'});
  
  // Concat
  fs.writeFileSync('concat_list.txt', "file 'output_0.mp4'\nfile 'output_1.mp4'");
  execSync(`ffmpeg -f concat -safe 0 -i concat_list.txt -c copy -y final_output.mp4`, {stdio:'pipe'});
  
  // Pass 2
  const filterStr = `[0:v]eq=contrast=1.3:saturation=1.5,negate=enable='between(t,1.50,1.60)',rgbashift=rh=20:bh=-20:enable='between(t,1.50,1.75)',vignette=PI/4[v_out]`;
  execSync(`ffmpeg -i final_output.mp4 -filter_complex "${filterStr}" -map "[v_out]" -c:v libx264 -preset ultrafast -y reel_cinematic.mp4`, {stdio:'pipe'});
  
  console.log('pipeline success');
} catch(e) {
  console.error(e.stderr ? e.stderr.toString() : e.toString());
}
