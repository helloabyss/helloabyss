const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs');
const FF='/opt/pw-browsers/ffmpeg-1011/ffmpeg-linux', FPS=+(process.argv[2]||12);
const W=1920,H=1080;
const D=JSON.parse(fs.readFileSync('aip-durations.json')).durations;
(async()=>{
  const b=await chromium.launch({args:['--no-sandbox']});
  const p=await b.newPage({viewport:{width:W,height:H},deviceScaleFactor:1});
  await p.goto('file://'+require('path').resolve('aip-player.html'),{waitUntil:'load'});
  const ff=spawn(FF,['-y','-f','image2pipe','-c:v','mjpeg','-framerate',String(FPS),
    '-i','pipe:0','-c:v','libvpx','-b:v','2600k','-crf','14','-pix_fmt','yuv420p',
    '-deadline','realtime','-cpu-used','5','aip-silent.webm'],{stdio:['pipe','ignore','ignore']});
  let total=0;
  for(let s=0;s<D.length;s++){
    const n=Math.max(1,Math.round(D[s]*FPS));
    for(let f=0;f<n;f++){
      await p.evaluate(([a,b])=>window.setFrame(a,b),[s,n>1?f/(n-1):0]);
      const buf=await p.screenshot({type:'jpeg',quality:88,clip:{x:0,y:0,width:W,height:H}});
      if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));
      total++;
    }
    if(s%10===0) console.log('  scene '+(s+1)+'/'+D.length);
  }
  ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await b.close();
  console.log('aip-silent.webm — '+total+' frames @ '+FPS+'fps = '+(total/FPS).toFixed(2)+'s');
})();
