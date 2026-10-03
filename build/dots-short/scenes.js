// PARADOCS10X Short: "OpenAI Dots vs Grok Bot: One Agent or a Team?" (9:16). Uses build/standard/kinds.js.
const IMAGES=['orb','cloudpc','swarm','keys','standoff_v'];
BEATS=[
{cue:'OpenAI just gave you',...K.broll({img:'orb',tags:[{at:'one AI agent',text:'ONE AGENT',size:80}]})},
{cue:'Elon Musk\'s xAI gives you',...K.machine({mode:'shared',bots:4,title:'A WHOLE TEAM'})},
{cue:'OpenAI\'s Dots launched',...K.date({at:'September',month:'SEP',day:29,label:'OPENAI SHIPS',sub:'DOTS',src:'SOURCE: OPENAI'})},
{cue:'Each dot gets',...K.broll({img:'cloudpc',src:'SOURCE: OPENAI',tags:[{at:'cloud computer',text:'OWN COMPUTER'},{at:'four thousand',text:'4,000+ APPS',y:CY+150*U,bg:'#FFFFFF'},{at:'while you\'re away',text:'WORKS WHILE AWAY',y:CY+300*U,bg:GREEN}]})},
{cue:'xAI\'s Grok Bot came first.',...K.timeline({src:'SOURCE: XAI',a:{date:'AUG 11',label:'GROK BOT'},b:{date:'SEP 29',label:'DOTS'},span:{at:'came first',text:'7 WEEKS FIRST'}})},
{cue:'You run several bots',...K.machine({mode:'shared',bots:3,title:'ONE SHARED MACHINE',src:'SOURCE: XAI'})},
{cue:'and they message each other',...K.chat({title:'# crew',msgs:[{at:'message each other',who:'BOT A',text:'I\'ll do outreach.'},{at:'group chat',who:'BOT B',text:'I\'ve got invoices.'},{at:'split the work',who:'BOT C',text:'Taking the CRM.'}]})},
{cue:'The catch?',...K.slam({dark:true,lines:[{at:'catch',text:'THE CATCH',color:RED,size:140}]})},
{cue:'A dot needs ChatGPT Pro',...K.slam({dark:true,src:'REPORTED',lines:[{at:'ChatGPT Pro',text:'CHATGPT PRO',color:'#FFFFFF',size:90},{at:'a hundred dollars',text:'$100/MO',color:ACC,size:180,gap:220},{at:'can\'t get one',text:'NOT IN UK/EU YET',color:RED,size:80,gap:200}]})},
{cue:'Grok Bot starts at twenty',...K.bars({title:'CHEAPEST WAY IN',items:[{at:'Grok Bot starts',label:'DOTS',value:100,color:ACC,fmt:v=>'$'+Math.round(v)},{at:'twenty dollars',label:'GROK BOT',value:20,color:BLUE,fmt:v=>'$'+Math.round(v)}]})},
{cue:'but every bot shares',...K.broll({img:'keys',src:'REPORTED',stamp:{at:'same logins',text:'SHARED LOGINS',size:80}})},
{cue:'One careful agent',...K.cta({img:'standoff_v',left:'CAREFUL AGENT?',right:'CHEAP CREW?',atA:'careful agent',atB:'cheap crew',atC:'Comment'})},
];
(()=>{const l=['swarm','orb','cloudpc','keys'];let k=0;BEATS.forEach(b=>{if(!b.img&&!b.plate){b.plate=l[k++%l.length];b.pdir=k%2?1:-1}})})();
