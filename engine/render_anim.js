const { chromium } = require('playwright');
const { spawn } = require('child_process');
const fs = require('fs'), path = require('path');
const FF='/opt/pw-browsers/ffmpeg-1011/ffmpeg-linux';
const W=1920,H=1080;
const D=JSON.parse(fs.readFileSync('aip-durations.json')).durations;
const STILLS = process.argv[2]==='stills';
const FPS = STILLS?12:+(process.argv[2]||20);
(async()=>{
  const b=await chromium.launch({args:['--no-sandbox']});
  const p=await b.newPage({viewport:{width:W,height:H},deviceScaleFactor:1});
  await p.goto('file://'+path.resolve('aip-anim.html'),{waitUntil:'load'});
  const n=await p.evaluate(()=>window.NSC);
  if(n!==D.length) throw new Error('scene count '+n+' != durations '+D.length);
  if(STILLS){
    fs.mkdirSync('animstills',{recursive:true});
    // three samples through each of a representative set of beats
    for(const s of [0,2,3,4,7,8,14,15,16,19,22,23,26,29,33,34,38,41]){
      for(const t of [0.35,0.85]){
        await p.evaluate(([a,b])=>window.setFrame(a,b),[s,t]);
        await p.screenshot({path:`animstills/${String(s).padStart(2,'0')}-t${t*100|0}.png`});
      }
    }
    await b.close(); console.log('animstills/ written'); return;
  }
  const ff=spawn(FF,['-y','-f','image2pipe','-c:v','mjpeg','-framerate',String(FPS),
    '-i','pipe:0','-c:v','libvpx','-b:v','3000k','-crf','12','-pix_fmt','yuv420p',
    '-deadline','realtime','-cpu-used','5','aip-silent.webm'],{stdio:['pipe','ignore','ignore']});
  let total=0;
  for(let s=0;s<D.length;s++){
    const fr=Math.max(1,Math.round(D[s]*FPS));
    for(let f=0;f<fr;f++){
      await p.evaluate(([a,b])=>window.setFrame(a,b),[s,fr>1?f/(fr-1):0]);
      const buf=await p.screenshot({type:'jpeg',quality:86,clip:{x:0,y:0,width:W,height:H}});
      if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));
      total++;
    }
    if(s%6===0) console.log('  beat '+(s+1)+'/'+D.length+'  '+total+' frames');
  }
  ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await b.close();
  console.log('aip-silent.webm — '+total+' frames @ '+FPS+'fps = '+(total/FPS).toFixed(2)+'s');
})();
