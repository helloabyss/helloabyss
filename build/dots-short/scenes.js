// PARADOCS10X Short: "OpenAI Dots vs Grok Bot: One Agent or a Team?" (9:16). Uses build/standard/kinds.js.
const IMAGES=['orb','cloudpc','swarm','keys','glass','standoff_v'];
BEATS=[
{cue:'This summer, more than',...K.broll({img:'swarm',src:'SOURCE: OPENAI',stat:{at:'twelve hundred',value:1200,label:'OPENAI AGENTS',color:'#FFFFFF',size:200},stamp:{at:'escaped',text:'ESCAPED',y:CY+300*U,size:90}})},
{cue:'and hundreds of them hacked',...K.broll({img:'glass',src:'REPORTED',stamp:{at:'hacked',text:'HACKED',size:110}})},
{cue:'Now OpenAI wants to give you one.',...K.broll({img:'orb',tags:[{at:'give you one',text:'ONE FOR YOU',size:80}]})},
{cue:'Elon Musk\'s xAI wants',...K.machine({mode:'shared',bots:4,title:'A WHOLE TEAM'})},
{cue:'OpenAI\'s Dots launched',...K.date({at:'September',month:'SEP',day:29,label:'OPENAI SHIPS',sub:'DOTS',src:'SOURCE: OPENAI'})},
{cue:'Each dot gets',...K.broll({img:'cloudpc',src:'SOURCE: OPENAI',tags:[{at:'cloud computer',text:'OWN COMPUTER'},{at:'four thousand',text:'4,000+ APPS',y:CY+150*U,bg:'#FFFFFF'},{at:'while you\'re away',text:'WORKS WHILE AWAY',y:CY+300*U,bg:GREEN}]})},
{cue:'xAI\'s Grok Bot came first.',...K.timeline({src:'SOURCE: XAI',a:{date:'AUG 11',label:'GROK BOT'},b:{date:'SEP 29',label:'DOTS'},span:{at:'came first',text:'7 WEEKS FIRST'}})},
{cue:'You run several bots',...K.machine({mode:'shared',bots:3,title:'ONE SHARED MACHINE',src:'SOURCE: XAI'})},
{cue:'and they message each other',...K.chat({title:'# crew',msgs:[{at:'message each other',who:'BOT A',text:'I\'ll do outreach.'},{at:'each other',who:'BOT B',text:'I\'ve got invoices.'},{at:'group chat',who:'BOT C',text:'Taking the CRM.'}]})},
{cue:'The catch?',...K.slam({dark:true,lines:[{at:'catch',text:'THE CATCH',color:RED,size:140}]})},
{cue:'A dot needs ChatGPT Pro',...K.slam({dark:true,src:'REPORTED',lines:[{at:'ChatGPT Pro',text:'CHATGPT PRO',color:'#FFFFFF',size:90},{at:'a hundred dollars',text:'$100/MO',color:ACC,size:180,gap:220}]})},
{cue:'Grok Bot starts at twenty',...K.bars({title:'CHEAPEST WAY IN',items:[{at:'Grok Bot starts',label:'DOTS',value:100,color:ACC,fmt:v=>'$'+Math.round(v)},{at:'twenty,',label:'GROK BOT',value:20,color:BLUE,fmt:v=>'$'+Math.round(v)}]})},
{cue:'but every bot shares',...K.broll({img:'keys',src:'REPORTED',stamp:{at:'same logins',text:'SHARED LOGINS',size:80}})},
{cue:'And those escaped agents?',...K.slam({dark:true,src:'REPORTED',lines:[{at:'escaped agents',text:'WHAT BROKE',color:'#FFFFFF',size:84},{at:'broke them out',text:'THEM OUT?',color:'#FFFFFF',size:84,gap:130},{at:'one thing they shared',text:'WHAT THEY',color:RED,size:100,gap:130},{at:'they shared',text:'SHARED.',color:RED,size:100,gap:130}]})},
{cue:'One careful agent',...K.cta({img:'standoff_v',left:'CAREFUL AGENT?',right:'CHEAP CREW?',atA:'careful agent',atB:'cheap crew',atC:'Comment'})},
];
(()=>{const l=['swarm','orb','cloudpc','keys'];let k=0;BEATS.forEach(b=>{if(!b.img&&!b.plate){b.plate=l[k++%l.length];b.pdir=k%2?1:-1}})})();
