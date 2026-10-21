# -*- coding: utf-8 -*-
from prims import *

def street(lit, boarded=False, roof=True, figs=0):
    s=''.join(shop(150+i*280, 600, lit[i], roof=roof, boarded=boarded) for i in range(6))
    if figs:
        s+=''.join(fig(430+i*360, 800, .8, 'flat', 'down') for i in range(figs))
    return s+ground()

S=[]
A=S.append
A((1,"Nobody is calling it a depression. But look at your street. Half the shops are dark, and the lights still on are barely paying rent.",
   street([0,1,0,1,0,1])+card(140,980,'EDUCATIONAL ONLY.  NOT FINANCIAL ADVICE.',860,80,34)))
A((2,"Then look at the receipts stuffed in a kitchen drawer. Every one is higher than last year, for the same groceries.",
   box(460,380,1000,420,B)+''.join(box(520+(i%3)*300,440+(i//3)*150,250,120,Y,6) for i in range(6))
   +''.join(f'<ellipse cx="{645+(i%3)*300}" cy="{500+(i//3)*150}" rx="72" ry="30" fill="none" stroke="{R}" stroke-width="8"/>' for i in range(6))))
A((3,"A woman stares at her banking app. The balance hasn't moved in days, but the little red notification keeps blinking anyway.",
   fig(1340,420,1.3,'down','hold')+box(1180,440,130,230,B,7,12)+f'<circle cx="1300" cy="462" r="20" fill="{R}" stroke="{K}" stroke-width="6"/>'+box(560,760,260,30,N)+ground()))
A((4,"This is the quiet collapse nobody put on the news. Not a crash. A slow leak that drains everyone at the same time.",
   f'<path d="M820 360 L880 760 L1040 760 L1100 360 Z" fill="{B}" stroke="{K}" stroke-width="9"/>'
   +''.join(f'<circle cx="960" cy="{800+i*52}" r="13" fill="{R}"/>' for i in range(3))
   +f'<ellipse cx="960" cy="958" rx="120" ry="18" fill="{R}" stroke="{K}" stroke-width="7"/>'+t(960,250,'A SLOW LEAK',58)))
A((5,"On the wall, a calendar. Dates circled in red where bills fall due. Three circles in a single week.",
   box(420,250,1080,620)+box(420,250,1080,110,B)
   +''.join(box(470+c*150,400+r*120,130,100,W,6) for r in range(4) for c in range(7))
   +''.join(f'<ellipse cx="{535+c*150}" cy="{570}" rx="62" ry="48" fill="none" stroke="{R}" stroke-width="9"/>' for c in (2,3,4))))
A((6,"A man counts coins on his kitchen counter, sorting them into small stacks, as if each one still has somewhere important to go.",
   fig(1300,430,1.3,'flat','fwd')+box(560,760,820,32,N)
   +''.join(pile(640+i*180,700,3,Y,120,26) for i in range(4))+ground()))
A((7,"To understand why this feels different, you have to see the whole picture. Wages flat. Prices climbing. And nobody saying the word out loud.",
   axes()+f'<path d="M300 700 L1680 300" fill="none" stroke="{R}" stroke-width="15" stroke-linecap="round"/>'
   +f'<path d="M300 700 L1680 655" fill="none" stroke="{B}" stroke-width="15" stroke-linecap="round"/>'
   +f'<path d="M1680 300 L1680 655 L300 700 Z" fill="{R}" opacity=".12"/>'
   +t(1700,292,'PRICES',38,'start')+t(1700,668,'WAGES',38,'start')+t(960,170,'THE GAP IS THE STORY',54)))
A((8,"So follow one household through it. Zul and their partner. Two incomes, one mortgage, and a budget spreadsheet that used to balance just fine.",
   zul(560,430,1.0,'table')+fig(900,470,1.2,'neutral','fwd')+box(1120,640,640,330,W)+box(1120,640,640,70,B)
   +''.join(f'<line x1="1120" y1="{710+i*65}" x2="1760" y2="{710+i*65}" stroke="{K}" stroke-width="5"/>' for i in range(4))
   +''.join(f'<line x1="{1120+c*160}" y1="640" x2="{1120+c*160}" y2="970" stroke="{K}" stroke-width="5"/>' for c in range(1,4))+ground()))
A((9,"Normal used to look like this. A grocery cart, half full, and a total that matched the number in your head.",
   f'<path d="M620 420 L760 420 L860 760 L1420 760" fill="none" stroke="{K}" stroke-width="10" stroke-linecap="round"/>'
   +box(800,480,620,280,W)+''.join(box(830+(i%3)*200,510+(i//3)*120,170,100,[G,Y,N,G,Y,N][i],6) for i in range(3))
   +f'<circle cx="920" cy="840" r="46" fill="{W}" stroke="{K}" stroke-width="9"/><circle cx="1340" cy="840" r="46" fill="{W}" stroke="{K}" stroke-width="9"/>'))
A((10,"Watch her face as she scrolls past the total this time. Something small has shifted, and she already knows it.",
   fig(820,420,2.2,'down','hold')+box(1180,420,200,340,B,8,14)+box(1210,460,140,260,Y,6)
   +''.join(f'<line x1="1230" y1="{500+i*52}" x2="1330" y2="{500+i*52}" stroke="{K}" stroke-width="5"/>' for i in range(4))))
A((11,"Widen out to the whole neighbourhood. Same houses. Same cars in the driveways. But the porch lights go out earlier every month.",
   ''.join(shop(120+i*220,640,1 if i in (2,5) else 0,190,230) for i in range(8))+ground()))
A((12,"On the corner, a small business owner. He hasn't taken a paycheck in two months, and he still unlocks the door every morning.",
   box(900,440,560,510,W)+box(930,470,500,80,B)+box(1100,700,160,250,W)
   +f'<circle cx="1240" cy="830" r="12" fill="{Y}" stroke="{K}" stroke-width="5"/>'
   +fig(640,560,1.4,'flat','fwd')+ground()))
A((13,"A year ago his till was full and orderly. Today he counts it coin by coin.",
   box(220,420,620,400,B)+''.join(box(270+(i%3)*190,470+(i//3)*110,160,90,Y,6) for i in range(9))+t(530,900,'LAST YEAR',44)
   +box(1080,420,620,400,B)+''.join(box(1130+i*150,660,120,90,Y,6) for i in range(4))+t(1390,900,'TODAY',44)))
A((14,"He glances at the stack of unopened envelopes by the register. He knows exactly what's inside. He just isn't ready yet.",
   box(760,760,820,32,N)+''.join(box(960,700-i*34,420,40,Y,6) for i in range(6))
   +box(960,700-6*34,420,40,R,6)+fig(480,560,1.3,'flat','fwd')+ground()))
A((15,"Multiply that one shop by every main street in the country, and the picture stops looking small. It starts looking systemic.",
   ''.join(box(300+(i%5)*270,250+(i//5)*180,220,140, R if i in (1,4,7,9,12,15,18) else B,7) for i in range(20))+t(960,1020,'1 IN 3',62)))
A((16,"Inside a warehouse loading dock, supply orders have quietly shrunk for six months straight. Pallet by empty pallet.",
   ''.join(box(180+i*280,560,240,340,W) for i in range(6))
   +''.join(box(210+i*280,620,180,250,N,7) for i in range(2))+ground()))
A((17,"On the last box out the door, the shipping label carries an order number smaller than the one it replaced.",
   box(460,300,1000,620,N)+box(640,440,640,340,Y)
   +''.join(f'<line x1="690" y1="{520+i*70}" x2="1230" y2="{520+i*70}" stroke="{K}" stroke-width="7"/>' for i in range(4))
   +box(880,280,160,140,R,8)))
A((18,"Downtown, the office tower still blazes. Bonuses still announced. As if none of this touches them.",
   box(1180,160,520,790)+''.join(box(1220+(i%3)*160,210+(i//3)*120,120,90,Y,6) for i in range(18))+ground()))
A((19,"And on a desk up there, one empty coffee cup. The only object left after everyone else went home.",
   box(360,700,1200,36,N)+box(520,520,220,180,B)
   +f'<path d="M740 560 A 60 60 0 0 1 740 660" fill="none" stroke="{K}" stroke-width="9"/>'))
A((20,"Across town, a delivery driver checks his app for the next job. The queue that used to be full is mostly silence now.",
   fig(620,440,1.4,'down','hold')+box(1120,380,340,520,B,8,16)+box(1160,430,260,420,W,6)
   +''.join(f'<line x1="1190" y1="{490+i*90}" x2="1390" y2="{490+i*90}" stroke="{K}" stroke-width="5"/>' for i in range(4))))

A((21,"That night, Zul sits at the kitchen table, spreading bills into careful piles, choosing which ones can wait another week.",
   zul(520,470,1.1,'table')+box(760,742,840,30,N)
   +f'<line x1="820" y1="772" x2="820" y2="950" stroke="{K}" stroke-width="8"/><line x1="1540" y1="772" x2="1540" y2="950" stroke="{K}" stroke-width="8"/>'
   +pile(810,700,3,Y,140)+pile(990,700,3,R,140)+pile(1170,700,3,R,140)+pile(1350,700,3,Y,140)+ground()))
A((22,"Beside them, a single house key rests on a stack of moving boxes. It says more about this economy than any headline could.",
   ''.join(box(700,520+i*140,520,140,N) for i in range(3))
   +f'<circle cx="900" cy="470" r="46" fill="{B}" stroke="{K}" stroke-width="9"/><rect x="930" y="452" width="230" height="36" fill="{Y}" stroke="{K}" stroke-width="8"/>'
   +f'<rect x="1100" y="488" width="30" height="34" fill="{Y}" stroke="{K}" stroke-width="7"/>'+ground()))
A((23,"Two streets over, an eviction notice is taped to a door, the ink still fresh, the deadline printed in bold, unmovable type.",
   box(560,200,800,820,B)+box(680,420,560,400,Y)
   +''.join(box(660+i*540,400,80,34,R,6) for i in range(2))+''.join(box(660+i*540,790,80,34,R,6) for i in range(2))
   +t(960,620,'NOTICE TO VACATE',46)))
A((24,"By morning, the line at the food bank stretches around the building before the doors even open.",
   box(1180,460,560,490,B)+box(1400,760,160,190,W)
   +''.join(fig(240+i*150,660,.75,'flat','down') for i in range(7))+ground()))
A((25,"And for a moment, everything is still. Just hands, folded, waiting their turn, patient in a way that's almost unbearable.",
   box(620,620,680,300,B,9,24)
   +f'<path d="M760 600 Q860 470 980 560 Q1100 470 1180 600" fill="{W}" stroke="{K}" stroke-width="10" stroke-linecap="round"/>'
   +''.join(f'<line x1="{820+i*60}" y1="560" x2="{820+i*60}" y2="620" stroke="{K}" stroke-width="8" stroke-linecap="round"/>' for i in range(5))))
A((26,"In a rural town, the only bank branch for fifty miles posts a sign. It will close by autumn.",
   box(420,380,1080,570,N)+''.join(box(500+i*230,460,80,490,W) for i in range(5))
   +f'<path d="M380 380 L960 240 L1540 380 Z" fill="{W}" stroke="{K}" stroke-width="9" stroke-linejoin="round"/>'
   +box(760,600,400,220,Y)+t(960,730,'CLOSING',52)+ground()))
A((27,"The farmer who banked there for thirty years now drives an extra hour to deposit a single check.",
   f'<path d="M180 950 L820 520 L1100 520 L1740 950 Z" fill="{W}" stroke="{K}" stroke-width="9"/>'
   +box(140,560,560,170,G)+box(1220,560,560,170,G)+box(880,620,160,100,B)+box(900,580,80,50,B)+ground()))
A((28,"The same afternoon, a trader in the city watches numbers climb on a screen and calls this an opportunity.",
   fig(480,470,1.3,'flat','fwd')+box(800,300,960,460,W)
   +''.join(box(880+i*160,700-i*80,90,i*80+40,G,7) for i in range(5))
   +f'<line x1="840" y1="740" x2="1720" y2="740" stroke="{K}" stroke-width="8"/>'+t(828,772,'0',28)+box(1120,760,320,30,N)+ground()))
A((29,"Somewhere between them, a single seed sits in open soil. Patient. Waiting for conditions that haven't arrived yet.",
   f'<path d="M560 740 Q960 660 1360 740 L1360 880 L560 880 Z" fill="{N}" stroke="{K}" stroke-width="9"/>'
   +f'<ellipse cx="960" cy="700" rx="46" ry="62" fill="{Y}" stroke="{K}" stroke-width="9"/>'))
A((30,"On a factory floor, half the machines are covered in tarps. The other half still hum, running on the fumes of old orders.",
   ''.join(box(150+i*290,560,230,340, B if i<3 else W) for i in range(6))
   +''.join(f'<circle cx="{265+i*290}" cy="640" r="26" fill="{Y}" stroke="{K}" stroke-width="7"/>' for i in range(3,6))+ground()))
A((31,"Zul tightens a bolt on one of the working machines. Steady hands. Refusing to let this one stop running too.",
   box(980,460,620,490,B)+f'<circle cx="1290" cy="620" r="70" fill="{W}" stroke="{K}" stroke-width="10"/>'
   +f'<circle cx="1290" cy="620" r="26" fill="{Y}" stroke="{K}" stroke-width="8"/>'
   +zul(620,490,1.1,'table')+ground()))
A((32,"At home, a cracked piggy bank sits on a shelf, taped back together, still holding the coins nobody will spend.",
   box(420,790,1080,32,N)
   +f'<ellipse cx="900" cy="650" rx="240" ry="150" fill="{R}" stroke="{K}" stroke-width="10"/>'
   +f'<path d="M820 520 L860 650 L800 720" fill="none" stroke="{K}" stroke-width="8"/>'
   +box(790,560,120,44,Y,7)+box(770,664,120,44,Y,7)
   +''.join(box(1240+i*90,700,70,70,Y,7) for i in range(3))))
A((33,"Ignore this pattern long enough and whole towns hollow out. Storefronts empty. Streetlights buzzing over nobody at all.",
   street([0]*6,boarded=True)
   +''.join(f'<line x1="{320+i*680}" y1="950" x2="{320+i*680}" y2="420" stroke="{K}" stroke-width="9"/><circle cx="{320+i*680}" cy="400" r="34" fill="{Y}" stroke="{K}" stroke-width="8"/>' for i in range(2))))
A((34,"In a shared apartment, three strangers now split rent that one person used to cover alone.",
   fig(330,520,1.2)+fig(960,520,1.2)+fig(1590,520,1.2)
   +''.join(box(200+i*630,740,260,120,B) for i in range(3))+ground()))
A((35,"One detail says all of it. Three toothbrushes in a single cup, lined up like strangers learning to share a life.",
   box(780,620,360,330,B,10,18)
   +''.join(box(840+i*100,330,56,300,[R,G,Y][i],8,10) for i in range(3))))
A((36,"In a college town, graduates once queued for job fairs that now sit half empty in echoing gymnasiums.",
   ''.join(box(170+i*290,620,230,110,W) for i in range(6))
   +fig(285,520,.9)+fig(1735-290*2+45,520,.9)
   +f'<line x1="120" y1="760" x2="1800" y2="760" stroke="{K}" stroke-width="6"/>'+ground()))
A((37,"One of them holds a diploma rolled tight, still tied with ribbon. Not yet framed. Maybe never framed at all.",
   f'<g transform="rotate(-18 960 560)">'+box(520,480,880,170,Y)
   +f'<circle cx="520" cy="565" r="85" fill="{W}" stroke="{K}" stroke-width="10"/>'
   +f'<circle cx="1400" cy="565" r="85" fill="{W}" stroke="{K}" stroke-width="10"/>'
   +box(900,440,70,250,R,8)+'</g>'))
A((38,"An older worker, thirty years of experience, scrolls the same job board and finds the same silence.",
   fig(520,470,1.3,'down','fwd')+box(880,440,840,420,B)+box(920,480,760,340,W,6)
   +''.join(f'<line x1="960" y1="{540+i*80}" x2="1640" y2="{540+i*80}" stroke="{K}" stroke-width="5"/>' for i in range(4))+ground()))
A((39,"Outside, an open park at midday. The only crowd left is pigeons and empty benches.",
   ''.join(box(220+i*400,700,320,60,N)+f'<line x1="{260+i*400}" y1="760" x2="{260+i*400}" y2="860" stroke="{K}" stroke-width="8"/><line x1="{500+i*400}" y1="760" x2="{500+i*400}" y2="860" stroke="{K}" stroke-width="8"/>' for i in range(4))
   +''.join(f'<ellipse cx="{420+i*230}" cy="910" rx="26" ry="18" fill="{D}" stroke="{K}" stroke-width="6"/>' for i in range(5))
   +box(100,940,1720,30,G,0)+ground(940)))
A((40,"A freelancer works three gig apps at once, stacking small jobs just to equal one full paycheck.",
   fig(400,470,1.3,'flat','fwd')+''.join(box(760+i*300,420,220,380,B,8,14) for i in range(3))
   +box(700,800,1000,32,N)+ground()))

A((41,"Back at the house, Zul writes a single number on a sticky note and presses it to the fridge. A quiet promise to save that much this month.",
   box(1060,260,580,690,B)+f'<line x1="1060" y1="560" x2="1640" y2="560" stroke="{K}" stroke-width="8"/>'
   +box(1210,360,280,280,Y)+t(1350,530,'500',72)+zul(620,470,1.1,'up')+ground()))
A((42,"All of these braid into one picture. An entire economy balanced on paper-thin margins, dressed up as business as usual.",
   box(140,420,300,530,B)+box(1480,420,300,530,B)
   +box(440,610,1040,30,Y)+fig(960,440,1.0,'flat','hold',False)
   +f'<line x1="960" y1="560" x2="930" y2="610" stroke="{K}" stroke-width="7"/><line x1="960" y1="560" x2="990" y2="610" stroke="{K}" stroke-width="7"/>'))
A((43,"Then it happens. One envelope stamped final notice, held in trembling hands. The moment the quiet depression stops being invisible.",
   box(520,380,880,420,Y)+f'<path d="M520 380 L960 650 L1400 380" fill="none" stroke="{K}" stroke-width="9"/>'
   +box(760,450,400,120,W)+t(960,530,'FINAL NOTICE',44,fill=R)
   +f'<path d="M560 860 Q660 760 760 830" fill="none" stroke="{K}" stroke-width="10" stroke-linecap="round"/>'
   +f'<path d="M1160 830 Q1260 760 1360 860" fill="none" stroke="{K}" stroke-width="10" stroke-linecap="round"/>'))
A((44,"It falls open on the table. Pages scattered. Numbers circled in red that no amount of hoping will undo.",
   box(260,740,1400,34,N)
   +''.join(f'<g transform="rotate({-18+i*12} {460+i*250} 500)">'+box(460+i*250,380,230,300,Y)
            +f'<ellipse cx="{575+i*250}" cy="520" rx="68" ry="40" fill="none" stroke="{R}" stroke-width="9"/></g>' for i in range(5))))
A((45,"A face finally breaks. Not loudly. Just a long exhale, the kind that comes after holding something in for too many months.",
   box(1080,620,420,330,B)+fig(820,480,1.6,'down','down',False)
   +f'<line x1="820" y1="672" x2="760" y2="760" stroke="{K}" stroke-width="8" stroke-linecap="round"/>'+ground()))
A((46,"The room has changed too. Boxes half packed. Furniture tagged. A life folded down into something smaller.",
   ''.join(box(180+i*230,560,200,200,N) for i in range(3))+''.join(box(180+i*230,760,200,190,N) for i in range(2))
   +box(1000,700,560,250,B)+box(1120,620,60,80,Y,6)+box(1620,760,230,190,N)+ground()))
A((47,"Outside, the shop owner turns his key one last time, and the lock clicks shut on a door that won't open again.",
   box(1060,180,620,840,B)+f'<circle cx="1140" cy="620" r="60" fill="{W}" stroke="{K}" stroke-width="10"/>'
   +box(900,596,240,48,Y,8)+f'<rect x="860" y="632" width="34" height="40" fill="{Y}" stroke="{K}" stroke-width="7"/>'
   +f'<path d="M520 700 Q680 600 860 640" fill="none" stroke="{K}" stroke-width="11" stroke-linecap="round"/>'))
A((48,"The closed sign swings gently, the paint already peeling at its corners from years of use.",
   f'<line x1="760" y1="200" x2="820" y2="380" stroke="{K}" stroke-width="8"/><line x1="1160" y1="200" x2="1100" y2="380" stroke="{K}" stroke-width="8"/>'
   +box(640,380,640,320,R)+t(960,580,'CLOSED',88,fill=W)
   +f'<path d="M640 380 L720 380 L640 450 Z" fill="{W}" stroke="{K}" stroke-width="7"/>'
   +f'<path d="M1280 700 L1200 700 L1280 630 Z" fill="{W}" stroke="{K}" stroke-width="7"/>'))
A((49,"Neighbours gather on the sidewalk, not to shop, just to stand together, the way people do when something ends.",
   box(1240,300,620,560,B)+''.join(fig(300+i*170,560,1.0,'flat','down') for i in range(6))+ground()))
A((50,"And there's the whole street now. One more storefront gone dark. The pattern complete, impossible to unsee.",
   street([0,1,0,0,0,1])))
A((51,"But here, finally, a hand reaches for a pen instead of another bill, and starts writing a plan instead of an apology.",
   box(560,560,840,400,Y)+f'<line x1="980" y1="560" x2="980" y2="960" stroke="{K}" stroke-width="8"/>'
   +f'<g transform="rotate(32 1280 420)">'+box(1240,200,80,420,B)+f'<path d="M1240 620 L1280 700 L1320 620 Z" fill="{K}"/></g>'
   +f'<path d="M1480 820 Q1360 700 1240 700" fill="none" stroke="{K}" stroke-width="11" stroke-linecap="round"/>'))
A((52,"The first line reads simple and clear. Cut what we can. Save what we must. Ask for help.",
   box(360,260,1200,700,Y)+f'<line x1="960" y1="260" x2="960" y2="960" stroke="{K}" stroke-width="8"/>'
   +t(660,440,'CUT WHAT',40)+t(660,510,'WE CAN',40)+t(1260,440,'SAVE WHAT',40)+t(1260,510,'WE MUST',40)+t(960,780,'ASK FOR HELP',52)))
A((53,"Zul stands at the window, notebook in hand, watching the street below with something steadier than fear in their posture.",
   box(160,220,900,700,B)+box(200,260,820,620,W)
   +''.join(shop(240+i*260,640,1,220,230,False) for i in range(3))
   +f'<line x1="610" y1="220" x2="610" y2="920" stroke="{K}" stroke-width="8"/><line x1="160" y1="570" x2="1060" y2="570" stroke="{K}" stroke-width="8"/>'
   +zul(1460,470,1.1,'up')+box(1330,560,160,120,Y,7)+ground()))
A((54,"Slowly, a community garden fills an empty lot. Neighbours trade vegetables instead of cash, rebuilding value a different way.",
   ''.join(box(160+i*290,700,230,80,N)+''.join(f'<path d="M{200+i*290+j*60} 700 Q{215+i*290+j*60} 630 {230+i*290+j*60} 700" fill="{G}" stroke="{K}" stroke-width="7"/>' for j in range(3)) for i in range(6))
   +fig(430,480,.9)+fig(1180,480,.9)+ground()))
A((55,"A family sits down to a modest dinner. Simple food. But the tension at the table has finally eased into quiet.",
   box(480,720,980,34,Y)+''.join(f'<ellipse cx="{600+i*220}" cy="700" rx="78" ry="26" fill="{B}" stroke="{K}" stroke-width="8"/><ellipse cx="{600+i*220}" cy="694" rx="40" ry="14" fill="{G}" stroke="{K}" stroke-width="6"/>' for i in range(4))
   +fig(600,470,1.0,'flat','fwd',False)+fig(820,470,1.0,'flat','fwd',False)+fig(1040,470,1.0,'flat','fwd',False)+fig(1260,470,1.0,'flat','fwd',False)+ground()))
A((56,"That main street reopens one shop at a time, hand-painted signs replacing the glossy ones that came before.",
   street([1,0,1,0,1,0])+''.join(f'<path d="M{174+i*560} 578 L{374+i*560} 566 L{374+i*560} 614 L{174+i*560} 606 Z" fill="{Y}" stroke="{K}" stroke-width="7"/>' for i in range(3))))
A((57,"The shop owner stands in his doorway again. Not rich. Steady. His ledger balanced in his own hand.",
   box(1040,240,700,710,B)+box(1180,420,420,530,W)
   +fig(1390,540,1.4,'flat','fwd')+box(1240,660,300,140,Y)
   +f'<line x1="1390" y1="660" x2="1390" y2="800" stroke="{K}" stroke-width="7"/>'+ground()))
A((58,"Across the country, small signs repeat. Fuller carts. Shorter lines. Porch lights staying on a little later each week.",
   ''.join(box(170+i*580,420,220,200,W)+box(470+i*580,420,220,200,G)+t(400+i*580,700,['CARTS','LINES','LIGHTS'][i],40)
           +f'<path d="M400 520 L450 520" stroke="{K}" stroke-width="8"/>' for i in range(3))))
A((59,"None of this erases the hard years. But it proves something simple. People adapt, and quiet collapses can have quiet recoveries too.",
   f'<path d="M760 700 L820 920 L1100 920 L1160 700 Z" fill="{N}" stroke="{K}" stroke-width="10"/>'
   +f'<line x1="960" y1="700" x2="960" y2="480" stroke="{G}" stroke-width="12" stroke-linecap="round"/>'
   +f'<path d="M960 560 Q860 490 880 600 Z" fill="{G}" stroke="{K}" stroke-width="8"/>'
   +f'<path d="M960 520 Q1060 450 1040 560 Z" fill="{G}" stroke="{K}" stroke-width="8"/>'))
A((60,"The street settles into evening. Lights steady. People walking slow instead of hurried. The storm not gone, but finally survivable.",
   street([1,1,1,1,1,1],figs=3)))

# ---- COMPOSITION PASS: replace the 20 weak scenes ------------------------
OV = {}
def O(n, body): OV[n] = body

O(2, box(300,300,1320,520,B)+box(300,300,1320,70,B)
    + ''.join(f'<g transform="rotate({-12+i*9} {470+i*230} 560)">'+box(380+i*230,420,200,290,Y,7)
      + ''.join(f'<line x1="{400+i*230}" y1="{470+r*52}" x2="{560+i*230}" y2="{470+r*52}" stroke="{K}" stroke-width="5"/>' for r in range(3))
      + f'<ellipse cx="{480+i*230}" cy="{650}" rx="64" ry="34" fill="none" stroke="{R}" stroke-width="9"/></g>' for i in range(5))
    + f'<line x1="300" y1="820" x2="1620" y2="820" stroke="{K}" stroke-width="9"/>')

O(3, counter(520,720,900) + fig(760,430,1.9,'down','hold')
    + box(1120,400,190,330,B,8,16) + box(1150,440,130,250,W,6)
    + f'<circle cx="1296" cy="424" r="26" fill="{R}" stroke="{K}" stroke-width="7"/>'
    + ''.join(f'<line x1="1178" y1="{490+i*62}" x2="1252" y2="{490+i*62}" stroke="{K}" stroke-width="5"/>' for i in range(3))
    + ground())

O(4, f'<path d="M700 260 L800 740 L1120 740 L1220 260 Z" fill="{B}" stroke="{K}" stroke-width="11"/>'
    + f'<ellipse cx="960" cy="260" rx="260" ry="54" fill="{W}" stroke="{K}" stroke-width="11"/>'
    + f'<path d="M808 756 L838 756 L824 790 Z" fill="{R}" stroke="{K}" stroke-width="6"/>'
    + ''.join(f'<circle cx="824" cy="{826+i*54}" r="16" fill="{R}"/>' for i in range(3))
    + f'<ellipse cx="824" cy="986" rx="150" ry="22" fill="{R}" stroke="{K}" stroke-width="8"/>'
    + t(1480,560,'A SLOW',56)+t(1480,630,'LEAK',56))

O(6, counter(420,700,1120) + fig(700,430,1.7,'flat','fwd')
    + pile(880,660,4,Y,120,26)+pile(1060,660,3,Y,120,26)+pile(1240,660,3,Y,120,26)+pile(1420,660,2,Y,120,26)
    + ground())

O(9, f'<path d="M420 360 L560 360 L690 760 L1540 760" fill="none" stroke="{K}" stroke-width="12" stroke-linecap="round"/>'
    + f'<path d="M610 440 L1560 440 L1480 760 L700 760 Z" fill="{W}" stroke="{K}" stroke-width="11"/>'
    + ''.join(box(660+(i%3)*290,480+(i//3)*140,250,120,[G,Y,N,G,Y,N][i],8) for i in range(3))
    + f'<circle cx="790" cy="860" r="62" fill="{W}" stroke="{K}" stroke-width="11"/>'
    + f'<circle cx="1440" cy="860" r="62" fill="{W}" stroke="{K}" stroke-width="11"/>'
    + ''.join(f'<line x1="{700+i*290}" y1="440" x2="{700+i*290}" y2="760" stroke="{K}" stroke-width="7"/>' for i in range(1,4)))

O(10, f'<circle cx="700" cy="520" r="250" fill="{W}" stroke="{K}" stroke-width="12"/>'
    + f'<circle cx="610" cy="470" r="22" fill="{K}"/><circle cx="790" cy="470" r="22" fill="{K}"/>'
    + f'<path d="M620 650 Q700 596 780 650" fill="none" stroke="{K}" stroke-width="12" stroke-linecap="round"/>'
    + box(1180,280,420,620,B,10,26)+box(1230,350,320,470,Y,8)
    + ''.join(f'<line x1="1270" y1="{420+i*90}" x2="1510" y2="{420+i*90}" stroke="{K}" stroke-width="6"/>' for i in range(4))
    + f'<line x1="1270" y1="750" x2="1510" y2="750" stroke="{R}" stroke-width="12"/>')

O(12, box(980,360,640,590,W)+box(1010,390,580,90,B)+box(1180,640,240,310,W)
    + f'<circle cx="1390" cy="800" r="16" fill="{Y}" stroke="{K}" stroke-width="6"/>'
    + fig(820,520,1.6,'flat','fwd')
    + f'<line x1="900" y1="632" x2="1170" y2="760" stroke="{K}" stroke-width="9" stroke-linecap="round"/>'
    + ground())

O(14, counter(240,700,1440)
    + ''.join(box(1000,660-i*42,520,48,Y,7) for i in range(6))
    + box(1000,660-6*42,520,48,R,7)
    + hand(560,640,1.5)+hand(820,640,1.5,True)+ground())

O(16, ''.join(box(150+i*290,520,250,380,W) for i in range(6))
    + ''.join(box(180+i*290,580,190,290,N,8)+f'<line x1="{180+i*290}" y1="700" x2="{370+i*290}" y2="700" stroke="{K}" stroke-width="6"/>' for i in range(2))
    + ''.join(f'<line x1="{180+i*290}" y1="860" x2="{370+i*290}" y2="860" stroke="{K}" stroke-width="6" stroke-dasharray="18 14"/>' for i in range(2,6))
    + f'<line x1="100" y1="900" x2="1820" y2="900" stroke="{B}" stroke-width="10"/>'+ground())

O(17, box(300,220,1320,760,N)
    + f'<line x1="300" y1="600" x2="1620" y2="600" stroke="{K}" stroke-width="9"/>'
    + box(620,380,680,420,Y)
    + ''.join(f'<line x1="680" y1="{470+i*80}" x2="1240" y2="{470+i*80}" stroke="{K}" stroke-width="8"/>' for i in range(4))
    + box(840,180,240,120,R,9))

O(19, counter(260,700,1400)
    + f'<path d="M620 360 L680 700 L1180 700 L1240 360 Z" fill="{B}" stroke="{K}" stroke-width="12"/>'
    + f'<ellipse cx="930" cy="360" rx="310" ry="56" fill="{W}" stroke="{K}" stroke-width="12"/>'
    + f'<path d="M1240 420 A 110 110 0 0 1 1240 620" fill="none" stroke="{K}" stroke-width="14"/>'
    + ground())

O(22, ''.join(box(620,560+i*150,660,150,N) for i in range(3))
    + f'<line x1="950" y1="560" x2="950" y2="1010" stroke="{K}" stroke-width="7"/>'
    + f'<g transform="translate(950,470)"><circle cx="-180" cy="0" r="74" fill="{W}" stroke="{K}" stroke-width="11"/>'
    + f'<circle cx="-180" cy="0" r="28" fill="{W}" stroke="{K}" stroke-width="9"/>'
    + f'<rect x="-110" y="-26" width="300" height="52" fill="{Y}" stroke="{K}" stroke-width="11"/>'
    + f'<rect x="120" y="26" width="34" height="46" fill="{Y}" stroke="{K}" stroke-width="10"/>'
    + f'<rect x="176" y="26" width="34" height="46" fill="{Y}" stroke="{K}" stroke-width="10"/></g>'+ground())

O(25, box(560,700,800,300,B,10,30)
    + hand(810,640,1.9)+hand(1110,640,1.9,True)
    + f'<path d="M700 700 Q960 640 1220 700" fill="none" stroke="{K}" stroke-width="10"/>')

O(27, f'<path d="M820 420 L1100 420 L1700 950 L220 950 Z" fill="{W}" stroke="{K}" stroke-width="10"/>'
    + f'<line x1="960" y1="430" x2="960" y2="950" stroke="{K}" stroke-width="8" stroke-dasharray="40 46"/>'
    + box(120,480,700,200,G)+box(1100,480,700,200,G)
    + f'<line x1="120" y1="560" x2="820" y2="560" stroke="{K}" stroke-width="5"/><line x1="1100" y1="560" x2="1800" y2="560" stroke="{K}" stroke-width="5"/>'
    + box(880,560,180,110,B)+box(906,512,120,56,B)
    + f'<circle cx="918" cy="676" r="26" fill="{W}" stroke="{K}" stroke-width="8"/><circle cx="1022" cy="676" r="26" fill="{W}" stroke="{K}" stroke-width="8"/>')

O(28, counter(640,720,1120)
    + box(760,280,920,430,W)+box(790,310,860,370,W,6)
    + ''.join(box(850+i*150,640-i*72,100,i*72+34,G,7) for i in range(5))
    + f'<line x1="810" y1="676" x2="1630" y2="676" stroke="{K}" stroke-width="8"/>'+t(792,706,'0',28)
    + fig(430,500,1.6,'flat','fwd')
    + f'<line x1="504" y1="583" x2="640" y2="690" stroke="{K}" stroke-width="9" stroke-linecap="round"/>'+ground())

O(29, f'<path d="M360 700 Q960 560 1560 700 L1560 980 L360 980 Z" fill="{N}" stroke="{K}" stroke-width="11"/>'
    + ''.join(f'<line x1="{440+i*130}" y1="{770+(i%2)*40}" x2="{520+i*130}" y2="{770+(i%2)*40}" stroke="{K}" stroke-width="5"/>' for i in range(9))
    + f'<ellipse cx="960" cy="690" rx="92" ry="124" fill="{Y}" stroke="{K}" stroke-width="12"/>'
    + f'<path d="M960 600 Q1000 690 960 780" fill="none" stroke="{K}" stroke-width="7"/>')

O(31, box(900,420,700,530,B)
    + f'<circle cx="1250" cy="620" r="110" fill="{W}" stroke="{K}" stroke-width="12"/>'
    + f'<circle cx="1250" cy="620" r="40" fill="{Y}" stroke="{K}" stroke-width="10"/>'
    + ''.join(f'<line x1="1250" y1="620" x2="{1250+110*__import__("math").cos(i*1.047)}" y2="{620+110*__import__("math").sin(i*1.047)}" stroke="{K}" stroke-width="7"/>' for i in range(6))
    + zul(620,490,1.2,None)
    + f'<line x1="672" y1="614" x2="1140" y2="620" stroke="{K}" stroke-width="8" stroke-linecap="round"/>'
    + f'<line x1="568" y1="614" x2="520" y2="700" stroke="{K}" stroke-width="8" stroke-linecap="round"/>'+ground())

O(32, counter(300,820,1320,34,False)
    + f'<line x1="300" y1="854" x2="1620" y2="854" stroke="{K}" stroke-width="7"/>'
    + piggy(800,620,1.0)
    + ''.join(box(1340+i*90,740,70,70,Y,8) for i in range(3)))

O(45, box(980,620,420,340,B)+f'<line x1="980" y1="620" x2="980" y2="400" stroke="{K}" stroke-width="10"/>'
    + f'<line x1="980" y1="400" x2="1400" y2="400" stroke="{K}" stroke-width="10"/>'
    + f'<circle cx="840" cy="500" r="92" fill="{W}" stroke="{K}" stroke-width="11"/>'
    + f'<circle cx="812" cy="492" r="10" fill="{K}"/><circle cx="868" cy="492" r="10" fill="{K}"/>'
    + f'<path d="M808 548 Q840 526 872 548" fill="none" stroke="{K}" stroke-width="8" stroke-linecap="round"/>'
    + f'<line x1="840" y1="592" x2="880" y2="700" stroke="{K}" stroke-width="10"/>'
    + f'<line x1="856" y1="630" x2="760" y2="710" stroke="{K}" stroke-width="9" stroke-linecap="round"/>'
    + f'<line x1="880" y1="700" x2="1010" y2="712" stroke="{K}" stroke-width="10"/>'+ground())

O(47, box(1080,140,680,880,B)
    + f'<circle cx="1180" cy="600" r="86" fill="{W}" stroke="{K}" stroke-width="12"/>'
    + f'<circle cx="1180" cy="600" r="30" fill="{K}"/>'
    + f'<rect x="860" y="574" width="300" height="52" fill="{Y}" stroke="{K}" stroke-width="11"/>'
    + f'<circle cx="840" cy="600" r="66" fill="{W}" stroke="{K}" stroke-width="11"/>'
    + f'<circle cx="840" cy="600" r="24" fill="{W}" stroke="{K}" stroke-width="9"/>'
    + hand(600,700,1.7))

# apply overrides
S[:] = [(n, vo, OV.get(n, body)) for (n, vo, body) in S]

# ---- SECOND PASS: counters, hands, seed ----------------------------------
O2 = {}
def P(n, body): O2[n] = body

P(3, counter(480,700,980) + fig(820,400,1.9,'down','hold', legs=False)
   + box(1160,380,200,340,B,8,16) + box(1192,422,136,258,W,6)
   + f'<circle cx="1346" cy="402" r="26" fill="{R}" stroke="{K}" stroke-width="7"/>'
   + ''.join(f'<line x1="1220" y1="{474+i*62}" x2="1300" y2="{474+i*62}" stroke="{K}" stroke-width="5"/>' for i in range(3))
   + ground())

P(6, counter(380,700,1180) + fig(680,392,1.7,'flat','fwd', legs=False)
   + ''.join(pile(880+i*180,676,3+(i%2),Y,118,24) for i in range(4))
   + ground())

P(14, counter(220,720,1460)
   + ''.join(box(1020,680-i*42,520,48,Y,7) for i in range(6))
   + box(1020,680-6*42,520,48,R,7)
   + hand(600,648,1.7)+hand(840,648,1.7,True)+ground())

P(25, box(540,720,840,290,B,10,30)
   + hand(820,636,2.1)+hand(1100,636,2.1,True))

P(29, f'<path d="M300 660 Q960 530 1620 660 L1620 1000 L300 1000 Z" fill="{N}" stroke="{K}" stroke-width="11"/>'
   + ''.join(f'<line x1="{400+i*140}" y1="{780+(i%3)*46}" x2="{500+i*140}" y2="{780+(i%3)*46}" stroke="{K}" stroke-width="5"/>' for i in range(9))
   + f'<path d="M960 500 Q1080 600 1020 700 Q960 770 900 700 Q840 600 960 500 Z" fill="{Y}" stroke="{K}" stroke-width="12" stroke-linejoin="round"/>'
   + f'<path d="M960 560 Q1000 640 965 706" fill="none" stroke="{K}" stroke-width="7"/>')

S[:] = [(n, vo, O2.get(n, body)) for (n, vo, body) in S]

# ---- THIRD PASS: figures behind counters, simpler hands ------------------
O3 = {}
def Q(n, body): O3[n] = body

# figure drawn FIRST, counter painted over it -> figure sits behind the surface
Q(3, fig(760,360,2.0,'down','fwd', legs=False) + counter(460,700,1020)
   + box(1180,360,210,350,B,8,16) + box(1214,404,142,266,W,6)
   + f'<circle cx="1376" cy="382" r="27" fill="{R}" stroke="{K}" stroke-width="7"/>'
   + ''.join(f'<line x1="1244" y1="{460+i*64}" x2="1326" y2="{460+i*64}" stroke="{K}" stroke-width="5"/>' for i in range(3))
   + ground())

Q(6, fig(640,352,1.9,'flat','fwd', legs=False) + counter(360,700,1240)
   + ''.join(pile(900+i*180,676,3+(i%2),Y,118,24) for i in range(4)) + ground())

Q(14, fig(470,360,1.9,'flat','fwd', legs=False) + counter(240,700,1440)
   + ''.join(box(1040,680-i*42,500,48,Y,7) for i in range(6))
   + box(1040,680-6*42,500,48,R,7) + ground())

Q(25, box(520,740,880,270,B,10,34)
   + hand(830,660,2.0) + hand(1110,660,2.0, True)
   + f'<path d="M660 740 Q960 686 1260 740" fill="none" stroke="{K}" stroke-width="9"/>')

S[:] = [(n, vo, O3.get(n, body)) for (n, vo, body) in S]

# ---- FOURTH PASS: scene 25 only -----------------------------------------
O4 = {25: (box(460,760,1000,250,B,10,36)
   + f'<line x1="960" y1="760" x2="960" y2="1010" stroke="{K}" stroke-width="7"/>'
   + hand(810,680,2.2) + hand(1110,680,2.2, True))}
S[:] = [(n, vo, O4.get(n, body)) for (n, vo, body) in S]

# ---- FINAL: scene 25 reshot as waiting figures ---------------------------
# Hands failed four attempts at this line weight. The beat is stillness and
# waiting, so the shot now carries it with figures instead of anatomy.
O5 = {25: (''.join(fig(500+i*300,470,1.25,'flat','down', legs=False) for i in range(4))
   + counter(360,760,1240,34,False)
   + f'<line x1="360" y1="794" x2="360" y2="950" stroke="{K}" stroke-width="8"/>'
   + f'<line x1="1600" y1="794" x2="1600" y2="950" stroke="{K}" stroke-width="8"/>'
   + ''.join(f'<line x1="{500+i*300}" y1="794" x2="{500+i*300}" y2="950" stroke="{K}" stroke-width="7"/>' for i in range(4))
   + ground())}
S[:] = [(n, vo, O5.get(n, body)) for (n, vo, body) in S]
