#!/usr/bin/env python3
"""War of 56 2.0: deterministic, stylised civ strategy macro simulation.
NOT the Civilization V executable or a faithful implementation of custom mod Lua.
Every simulated turn is processed; map checkpoints every 25 turns and at the conclusion.
Python 3, numpy, scipy, matplotlib. Outputs reproducible campaign data and atlas.
"""
import ast, base64, csv, json, math, random, textwrap
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
from scipy.ndimage import gaussian_filter, label
from scipy.spatial import cKDTree
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, hsv_to_rgb
from matplotlib.lines import Line2D

SEED=20261102
OUT=Path(__file__).resolve().parents[1] / 'output'
OUT.mkdir(parents=True, exist_ok=True)
randomizer=random.Random(SEED)
rg=np.random.default_rng(SEED)
# Built-in roster is generated once from the verified War-of-54 baseline and
# two new civilization directories in the Nov 2 CoolWackyCivs2 v23 manifest.
ROSTER = [('The Boy Who Touched Paradise', 'Wacky I', 'Culture', 0.96, 1.02, 1.36, 1.03, 1.04, 0.97), ('The Relentless Seven', 'Wacky I', 'Domination', 1.23, 1.02, 1.17, 0.88, 1.07, 1.06), ('The Rou’ls Ascendancy', 'Wacky I', 'Domination', 1.33, 0.91, 0.86, 0.81, 0.92, 1.07), ('The Luna Network', 'Wacky I', 'Science', 1.14, 1.23, 0.91, 0.93, 1.18, 1.24), ('The Terra Framework', 'Wacky I', 'Science', 1.0, 1.32, 1.02, 0.96, 1.1, 1.02), ('The Capano Circuit', 'Wacky I', 'Science', 1.02, 1.18, 1.07, 0.93, 1.0, 1.01), ('The Filthy Realm', 'Wacky I', 'Culture', 1.13, 0.94, 1.23, 0.83, 0.92, 0.97), ('The Dual Order', 'Wacky I', 'Domination', 1.21, 0.91, 1.05, 1.07, 0.92, 0.96), ('The RomanGladius Network', 'Wacky I', 'Science', 1.06, 1.21, 1.07, 1.07, 1.23, 1.17), ('The Eternal Number Ten', 'Wacky I', 'Culture', 1.08, 1.08, 1.32, 1.12, 1.06, 0.97), ('The Boy Beyond the Sky', 'Wacky I', 'Culture', 1.11, 0.99, 1.27, 0.88, 1.02, 0.99), ('The First Night', 'Wacky I', 'Science', 1.04, 1.16, 1.1, 0.98, 1.02, 1.11), ('The Viltrum Empire', 'Wacky I', 'Domination', 1.51, 0.83, 0.73, 0.61, 0.91, 1.2), ('The Tokenized Intelligence', 'Wacky I', 'Science', 0.96, 1.37, 0.94, 0.9, 1.09, 0.93), ('The Sol Intellect', 'Wacky I', 'Science', 0.89, 1.46, 1.02, 0.93, 1.09, 0.93), ('The Kingdoms', 'Wacky I', 'Domination', 1.11, 0.92, 1.05, 1.02, 0.94, 1.19), ('The Shattered Empire', 'Wacky I', 'Domination', 1.22, 0.93, 0.89, 0.88, 1.0, 1.23), ('The Last City', 'Wacky I', 'Science', 1.19, 1.06, 0.88, 0.9, 0.87, 0.45), ('The Boundless City', 'Wacky II', 'Science', 1.16, 1.28, 1.17, 0.9, 1.12, 0.29), ('The Republic of Pigeons', 'Wacky II', 'Culture', 0.87, 1.27, 1.3, 1.17, 1.21, 1.08), ('The Indigo Champion', 'Wacky II', 'Domination', 1.27, 1.06, 0.91, 0.92, 0.99, 1.08), ('McPvP — The Endless Lobby', 'Wacky II', 'Domination', 1.37, 0.94, 0.88, 0.78, 0.92, 1.04), ('The Children of the Kingdom', 'Wacky II', 'Culture', 0.94, 0.96, 1.36, 1.04, 0.99, 0.95), ('The Twelfth Hour', 'Wacky II', 'Science', 1.04, 1.28, 1.04, 0.95, 1.06, 0.95), ('The Wandering Circus', 'Wacky II', 'Culture', 0.9, 1.0, 1.4, 1.1, 1.06, 1.12), ('The 11 Cats', 'Wacky II', 'Culture', 1.04, 1.02, 1.21, 1.0, 1.04, 1.02), ('The Kingdom of Saba', 'Wacky II', 'Diplomacy', 1.03, 1.1, 1.1, 1.31, 1.17, 1.12), ('The Substitute Classroom', 'Wacky II', 'Domination', 1.27, 0.91, 0.91, 0.89, 1.0, 1.06), ('The Conical Union', 'Wacky II', 'Science', 1.14, 1.15, 0.95, 0.9, 1.23, 1.17), ('The Kingdom of the Unrung Bell', 'Wacky II', 'Domination', 1.26, 0.97, 1.06, 0.86, 1.08, 1.01), ('The Urgal', 'Wacky II', 'Domination', 1.47, 0.84, 0.79, 0.71, 0.93, 1.11), ('The Jin Dynasty', 'Wacky II', 'Domination', 1.42, 1.02, 0.9, 1.08, 1.17, 1.22), ('The Threshold Court', 'Wacky II', 'Domination', 1.27, 0.98, 0.98, 0.98, 0.98, 1.04), ('The Honeycomb Commonwealth', 'Wacky II', 'Science', 0.93, 1.19, 1.19, 1.1, 1.33, 1.04), ('The Laureate Commonwealth', 'Wacky II', 'Culture', 1.14, 1.03, 1.46, 1.07, 1.05, 1.0), ('T1 — The ZOFGK Dynasty', 'Wacky II', 'Domination', 1.37, 0.99, 1.07, 0.87, 1.04, 1.05), ('The Republic of First Drafts', 'Wacky II', 'Science', 1.05, 1.27, 1.13, 1.03, 1.17, 1.02), ('The Lantern Fleet', 'Wacky II', 'Science', 1.04, 1.28, 1.18, 1.05, 1.1, 0.93), ('The Triumphal Imperium', 'Wacky II', 'Domination', 1.38, 0.96, 0.96, 0.86, 1.13, 1.14), ('The Freehold of Una Court', 'Una Court', 'Domination', 1.21, 1.0, 0.9, 0.9, 1.03, 0.98), ('The Dominion of Una Court', 'Una Court', 'Domination', 1.28, 0.96, 0.88, 0.84, 1.04, 0.98), ('The Ultimate Possessor', 'Una Court', 'Domination', 1.38, 0.97, 0.9, 0.82, 0.98, 1.03), ('The Soft Kitty Serenader', 'Una Court', 'Culture', 0.79, 1.02, 1.43, 1.18, 1.05, 0.94), ('The Library Exile', 'Una Court', 'Science', 1.02, 1.35, 1.12, 1.01, 1.04, 0.85), ('The Phone Stealer', 'Una Court', 'Diplomacy', 0.91, 1.1, 0.99, 1.32, 1.25, 0.92), ('The Princedom of Una Court', 'Una Court', 'Domination', 1.3, 0.99, 0.91, 0.85, 0.98, 1.05), ('The Wealthy of Una Court', 'Una Court', 'Diplomacy', 0.85, 1.09, 0.96, 1.49, 1.46, 0.96), ('The Possession Browsers', 'Standalone', 'Domination', 1.31, 0.94, 1.1, 0.83, 0.97, 1.02), ('The Boulder Circuit', 'Standalone', 'Science', 1.12, 1.23, 1.06, 0.95, 1.06, 1.02), ('Azul Baronis', 'Standalone', 'Domination', 1.47, 0.96, 0.84, 0.77, 0.99, 1.12), ('The Fleshborn Chorus', 'Standalone', 'Domination', 1.35, 1.14, 0.72, 0.65, 1.06, 1.24), ('Jetstar', 'Standalone', 'Diplomacy', 0.91, 1.0, 0.91, 1.36, 1.4, 1.13), ('The Commonwealth of Yesterday', 'Standalone', 'Culture', 1.03, 1.13, 1.39, 1.04, 1.02, 0.91), ('The Colony', 'Standalone', 'Science', 1.22, 1.31, 0.91, 1.15, 1.05, 0.95), ('Kadamba Dynasty of Goa', 'Standalone', 'Culture', 1.0, 1.13, 1.18, 1.22, 1.16, 1.04), ('The Fourth Generation White Room', 'Standalone', 'Science', 0.78, 1.15, 0.85, 0.71, 0.9, 0.36)]
assert len(ROSTER)==56
N=len(ROSTER); CS_COUNT=11
NAMES=[r[0] for r in ROSTER]
ID={n:i for i,n in enumerate(NAMES)}
ERA_NAMES=['Ancient','Classical','Medieval','Renaissance','Industrial','Modern','Atomic','Information']
W,H=186,96
Y,X=np.mgrid[0:H,0:W]
# Seven main continental shapes, broad enough for fifty-six starting capitals.
continents=[(27,24,27,20),(34,68,31,22),(77,36,34,26),(87,77,29,18),
            (138,26,34,22),(146,70,33,21),(104,10,22,11)]
field=np.zeros((H,W))
for a,b,rx,ry in continents:
    field=np.maximum(field,1.13-((X-a)/rx)**2-((Y-b)/ry)**2)
noise=gaussian_filter(rg.normal(size=(H,W)),sigma=3.9)
noise/=max(noise.std(),1e-5)
land=(field+0.125*noise)>.13
land[:3,:]=False; land[-3:,:]=False;land[:,:3]=False;land[:,-3:]=False
components,ncomponents=label(land)
spots=np.column_stack(np.where(land))[:,::-1]
# Place capitals and city states separated from each other, with component checks.
points=[tuple(spots[randomizer.randrange(len(spots))])]
while len(points)<N+CS_COUNT:
    chosen=np.asarray(points)
    d2=np.min(((spots[:,None,:]-chosen[None,:,:])**2).sum(axis=2),axis=1)
    d2=np.where(d2>=28,d2,-1e9)
    if np.max(d2)<0:raise RuntimeError('Not enough valid land for capitals')
    score=d2+rg.uniform(0,12,len(spots))
    points.append(tuple(map(int,spots[int(np.argmax(score))])))
randomizer.shuffle(points)
start_pos=points[:N]; citystates=points[N:]
start_comp=[int(components[y,x]) for x,y in start_pos]
# Variant starting wealth and biome quality (small enough not to dominate strategy).
homeland=[randomizer.uniform(.89,1.12) for _ in range(N)]

civs=[]
for i,(name,group,style,mil,sci,tour,dip,econ,expansion) in enumerate(ROSTER):
    civs.append(dict(id=i,name=name,group=group,style=style,mil_trait=mil,sci_trait=sci,
        culture_trait=tour,dip_trait=dip,econ_trait=econ,expand_trait=expansion,
        tech=0.,culture=0.,tourism=0.,gold=170.,army=75*mil*homeland[i],
        score=0,alive=True,alliances=0,delegates=0,inf_count=0,cultural_progress=0.,
        science_progress=0.,momentum=0,veteran=0,crisis=False,last_win=-100,
        war_fatigue=0.,science_parts=0.,sci_hold=0,culture_hold=0,dom_hold=0,
        last_found=-200,threat=0.,victory_aim=style,city_count=1,capital_count=1,
        money_stolen=0,damage_taken=0,military=0))

cities=[]
for i,(x,y) in enumerate(start_pos):
    cities.append(dict(id=i,name=f'{NAMES[i][:26]} · Capital',x=x,y=y,comp=start_comp[i],owner=i,
      founder=i,capital=True,founded=0,fort=100.,siege={},pop=1.0,age=0))
next_city_id=N
wars={}    # directional pair (attacker,defender): declarer / target
war_cooldown=defaultdict(lambda:-9999)
alliances=np.zeros((N,CS_COUNT),float)
cs_owners=[-1]*CS_COUNT
citystate_comp=[int(components[y,x]) for x,y in citystates]
events=[]; snapshots=[]
victory=None

# Color palette deliberately fixed for consistent replay, independent of map changes.
hues=np.linspace(0,1,N,endpoint=False)
rg.shuffle(hues)
colors=[tuple(hsv_to_rgb([h,0.67,0.84 if (i%4) else 0.72])) for i,h in enumerate(hues)]
colorhex=['#%02x%02x%02x'%tuple(int(x*255) for x in col) for col in colors]

# Logging records what is actually resolved by the model.
def log(turn,kind,description,who=None,where=None,importance=1):
    events.append(dict(turn=turn,kind=kind,text=description,ids=who or [],xy=where,importance=importance))

def era(turn):return min(7,turn//165)
def same_land(a,b):return components[a[1],a[0]]==components[b[1],b[0]]
def d(a,b):return math.dist(a,b)
def cities_of(owner):return [c for c in cities if c['owner']==owner]
def war_pair(a,b):return tuple(sorted([a,b]))
def at_war(a,b):return war_pair(a,b) in wars

def trait_factor(i,kind,t):
    c=civs[i];n=c['name']; e=era(t); f=1.
    if n=='The Triumphal Imperium' and kind=='mil':f*=1+.02*c['momentum']
    if n=='The Triumphal Imperium' and kind=='econ':f*=1+.04*c['momentum']
    if n=='T1 — The ZOFGK Dynasty' and kind=='mil':f*=1+.020*c['veteran']
    if n=='The Lantern Fleet' and kind in ('science','culture'):
        coastal=sum(1 for z in cities_of(i) if z.get('coastal',False))
        f*=1+min(.15,coastal*.035)
    if n=='The Republic of First Drafts' and kind=='science':f*=1+min(.16,len(cities_of(i))*.028)
    if n=='The Viltrum Empire' and kind=='mil':f*=.65 if 635<=t<=725 else (1.15 if t>725 else 1.09)
    if n=='The Shattered Empire' and kind=='mil':f*=.79 if 430<=t<=510 else 1.
    if n=='The Kingdoms' and kind=='mil':f*=.84 if 555<=t<=630 else 1.
    if n=='The Jin Dynasty' and kind=='mil':f*=1.20 if 180<t<660 else 1.
    if n=='The Urgal' and kind=='mil':f*=1.28 if t%160<32 else 1.
    if n=='The Sol Intellect' and kind=='science':f*=1.10+max(0,e-2)*.027
    if n=='The Boundless City' and kind=='science':f*=1+.035*e
    if n=='The Last City' and kind=='mil':f*=1.26
    if n=='The Fourth Generation White Room':
        if kind=='mil':f*=.58+.11*e+min(.48,foreign_cap_losses*.014)
        if kind=='science':f*=.78+.065*e
    if n=='The Soft Kitty Serenader' and kind=='culture':f*=1.10
    if n=='The Laureate Commonwealth' and kind=='culture':f*=1+.029*e
    if n=='The Fleshborn Chorus' and kind=='econ':f*=1.07
    if n=='The Twelfth Hour' and kind=='science':f*=1.12 if t%36<6 else 1.
    if n=='Azul Baronis' and kind=='mil':f*=1.11 if e>=4 else 1.0
    if n=='The Wealthy of Una Court' and kind=='dip':f*=1+.044*e
    return f

foreign_cap_losses=0
# State of researched research, culture, military and other victory thresholds.
def get_victory_state(t):
    living=[z for z in civs if z['alive']]
    for d in civs:
        if not d['alive']:
            d['city_count']=0
            d['capital_count']=0
            d['alliances']=0
            d['delegates']=0
    for c in living:
        i=c['id']; own=cities_of(i)
        c['city_count']=len(own)
        c['capital_count']=sum(1 for city in own if city['capital'])
        c['military']=int(c['army']*trait_factor(i,'mil',t))
        c['science_progress']=min(1., c['tech']/110*.84 + min(1.,c['science_parts']/32)*.16)
        others=[x for x in living if x['id']!=i]
        ratios=[c['tourism']/(x['culture']*.80+75+x['tech']*.15) for x in others]
        c['inf_count']=sum(x>=1 for x in ratios)
        c['cultural_progress']=(sum(min(1.,x) for x in ratios)/len(ratios)) if ratios else 0
        c['threat']=max(c['science_progress'],c['cultural_progress'],
                        min(1.,c['delegates']/27) if c['alliances']>=4 else 0,
                        c['capital_count']/math.ceil(.70*N))
        c['score']=round(35 + .67*c['tech'] + .15*c['culture'] + c['city_count']*17 +
            c['capital_count']*32 +c['army']*.30+max(0,c['gold'])*.012)

def calc_map(t):
    owned=[z for z in cities if civs[z['owner']]['alive']]
    if not owned:return np.full((H//2,W//2),255,np.uint8)
    # Coarser 2x2 land grid used by replay. Claimed city radius grows with age.
    yy,xx=np.mgrid[0:H:2,0:W:2]
    plotcomp=components[::2,::2]
    samples=np.column_stack((xx.ravel(),yy.ravel()))
    places=np.array([(q['x'],q['y']) for q in owned])
    cc=np.array([q['comp'] for q in owned])
    radii=np.array([4.4+min(9.6,math.sqrt(max(0,t-q['founded']))*.36) for q in owned])
    # No claims across disconnected landmasses; Voronoi among city centers.
    sq=np.sum((samples[:,None,:]-places[None,:,:])**2,axis=2)
    sq=np.where(plotcomp.ravel()[:,None]!=cc[None,:],1e10,sq)
    idx=np.argmin(sq,axis=1)
    dist2=sq[np.arange(len(samples)),idx]
    owned_by=np.array([q['owner'] for q in owned],dtype=np.uint8)
    res=np.where((dist2<=radii[idx]**2)&(plotcomp.ravel()>0),owned_by[idx],255)
    return res.reshape(H//2,W//2).astype(np.uint8)

def snapshot(t,force=False):
    get_victory_state(t)
    territory=calc_map(t)
    snapshot_wars=[]
    for w in wars.values():
        snapshot_wars.append(dict(a=w['a'],b=w['b'],since=w['since'],attacker=w['lead'],reason=w['reason']))
    snapshots.append(dict(turn=t,era=ERA_NAMES[era(t)],
      territory=base64.b64encode(territory.tobytes()).decode('ascii'),
      city_owners=[q['owner'] for q in cities],city_ids=[q['id'] for q in cities],
      statistics=[{k:(round(c[k],2) if isinstance(c[k],float) else c[k]) for k in
          ('score','army','tech','tourism','culture','gold','alliances','delegates','inf_count','cultural_progress','science_progress','threat','alive','city_count','capital_count','momentum','veteran')} for c in civs],
      wars=snapshot_wars,cs_owners=cs_owners.copy(),eventcount=len(events)))

for q in cities:
    x,y=q['x'],q['y']
    # Adjacent water on the same 96x186 grid is a coarse coast proxy.
    q['coastal']=any(0<=x+dx<W and 0<=y+dy<H and not land[y+dy,x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))

maxturn=1450
vote_turns=set(range(875,maxturn+1,125))
for t in range(maxturn+1):
    e=era(t)
    if t and t%165==0:log(t,'era',f'The world enters the {ERA_NAMES[e]} era.',importance=3)
    if t in (635,725,430,510,555,630):
        if t==635:log(t,'crisis','The Viltrumite Scourge disrupts Viltrumite military readiness.',[ID['The Viltrum Empire']],importance=3)
        if t==725:log(t,'crisis','The Viltrum Empire emerges from the Scourge and rebuilds.',[ID['The Viltrum Empire']],importance=2)
        if t==430:log(t,'crisis','Provincial unrest weakens The Shattered Empire.',[ID['The Shattered Empire']],importance=2)
        if t==555:log(t,'crisis','House rivalries interfere with The Kingdoms’ campaigns.',[ID['The Kingdoms']],importance=2)
    # Actual city ownership determines economic capacity each turn.
    city_counts=Counter(z['owner'] for z in cities)
    # Slow, controlled population development of living cities.
    for q in cities:
        q['age']=t-q['founded']
        q['pop']=min(25.,1.0+q['age']*.011)
        # Recover city defense outside active siege.
        if not q['siege']:
            q['fort']=min(100.,q['fort']+.35)
    for c in civs:
        if not c['alive']:continue
        i=c['id']; nc=city_counts[i]
        city_quality=sum(z['pop']**.48 for z in cities if z['owner']==i)
        size=min(3.,.78+.21*city_quality)
        specialist=1.0+.08*e
        econ_rate=(1.2+3.65*c['econ_trait']*size)*(1+e*.17)*trait_factor(i,'econ',t)
        upkeep=(.008*c['army']+1.7*nc+1.2*sum(i in (w['a'],w['b']) for w in wars.values()))
        c['gold']+=econ_rate-upkeep
        if c['gold']<0:c['gold']=0.
        tech_rate=.041 * c['sci_trait']*specialist*size*homeland[i]*trait_factor(i,'science',t)
        if nc==1 and c['name'] not in ('The Boundless City','The Last City','The Fourth Generation White Room'):
            tech_rate*=.8
        c['tech']+=tech_rate
        c['culture']+=.20 * c['culture_trait']*specialist*size*trait_factor(i,'culture',t)
        # Tourism begins later and accelerates with modern mass communication.
        tour_unlock=max(0,min(2.5,(t-260)/330))
        c['tourism']+=.24*c['culture_trait']*tour_unlock*size*trait_factor(i,'culture',t)
        # Mobilization does not create unbounded armies; economic base matters.
        recruitment=.18*c['mil_trait']*size*(1+.19*e)*trait_factor(i,'econ',t)
        recruitment*=.77 if c['gold']<75 else 1.
        c['army']=min(950,c['army']+recruitment-.0045*c['army'])
        c['war_fatigue']=max(0,c['war_fatigue']-.01)
        # Production abstraction for spaceship parts (once tech threshold is reached).
        if c['tech']>=110 and c['science_parts']<32:
            c['science_parts']+=.22*size*c['econ_trait']
        # Snapshot a defended harbor only, not an unconditional naval boost.
        if c['name']=='The Triumphal Imperium' and t-c['last_win']>0:
            c['momentum']=max(0,c['momentum']-1)
    # Wealthy Trent taxes rich foreign powers (paired treasury debits and credits).
    if t>=100 and t%110==0 and civs[ID['The Wealthy of Una Court']]['alive']:
        wt=civs[ID['The Wealthy of Una Court']]
        donors=sorted((z for z in civs if z['alive'] and z['id']!=wt['id']),key=lambda z:z['gold'],reverse=True)
        for z in donors[:2]:
            if z['gold']<200:continue
            stolen=round(z['gold']*.05,2)
            z['gold']-=stolen;wt['gold']+=stolen;wt['money_stolen']+=stolen
            log(t,'economy',f'Wealthy Trent transfers {stolen:,.0f} Gold from {z["name"]} through an audit.',[wt['id'],z['id']],importance=1)
    # Found new CITY NODES, not just increase abstract city counts.
    if t>=60 and t%10==0:
        eligible=[c for c in civs if c['alive']]
        randomizer.shuffle(eligible)
        founded_this_turn=0
        for c in eligible:
            if founded_this_turn>=4:break
            i=c['id']; mine=cities_of(i)
            if c['name'] in ('The Boundless City','The Last City','The Fourth Generation White Room'):continue
            if len(mine)>=7:continue
            ideal_interval=(165./max(.58,c['expand_trait']))*(1+.26*max(0,len(mine)-2))
            if t-c['last_found']<ideal_interval and len(mine)>1:continue
            if t<75 and len(mine)>=1:continue
            if t<175 and len(mine)>=2:continue
            if c['gold']<60:continue
            possibles=[]
            for q in mine:
                ax,ay=q['x'],q['y']
                for _ in range(34):
                    angle=randomizer.random()*2*math.pi;radius=randomizer.uniform(5,15)
                    x=int(ax+math.cos(angle)*radius);y=int(ay+math.sin(angle)*radius)
                    if not (3<=x<W-3 and 3<=y<H-3 and land[y,x]):continue
                    if components[y,x]!=q['comp']:continue
                    separation=min((math.dist((x,y),(z['x'],z['y'])) for z in cities),default=100)
                    if separation<4.1:continue
                    if min((math.dist((x,y),z) for z in citystates),default=100)<3.5:continue
                    if separation<5.3 and len(mine)>3:continue
                    possibles.append((separation+randomizer.random()*3.4,x,y))
            if not possibles:continue
            _,x,y=max(possibles)
            coastal=any(0<=x+dx<W and 0<=y+dy<H and not land[y+dy,x+dx] for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)))
            new=dict(id=next_city_id,name=f'{c["name"][:20]} · City {len(mine)+1}',x=x,y=y,
               comp=int(components[y,x]),owner=i,founder=i,capital=False,founded=t,
               fort=100.,siege={},pop=1.,age=0,coastal=coastal)
            next_city_id+=1;cities.append(new)
            c['gold']-=42; c['last_found']=t;founded_this_turn+=1
            if t<280 or len(mine)>=4:
                log(t,'settlement',f'{c["name"]} founds its {len(mine)+1}th city.',[i],[x,y],importance=1)
    # World Congress proxy: investments allocate influence to existing CS.
    if t>0 and t%5==0:
        alliances*=.982
        for c in civs:
            if not c['alive']:continue
            i=c['id'];dip=c['dip_trait']*trait_factor(i,'dip',t)
            if c['style']!='Diplomacy' and randomizer.random()>.35:continue
            wanted=min(5,1+(3 if c['style']=='Diplomacy' else 0)+int(dip>1.25))
            best=list(range(CS_COUNT))
            best.sort(key=lambda j: (alliances[i,j]+(j*17+i*23)%53),reverse=True)
            # Diplomats concentrate existing relationships; military powers have sparse opportunistic allies.
            targets=best[:wanted]
            for j in targets:
                if c['gold']<=40:break
                bid=(3.1 if c['style']=='Diplomacy' else 1.25)*dip
                alliances[i,j]+=bid;c['gold']-=bid*.6
        old=cs_owners.copy()
        for j in range(CS_COUNT):
            scores=np.where(np.array([c['alive'] for c in civs]),alliances[:,j],-1)
            ii=int(np.argmax(scores))
            cs_owners[j]=ii if scores[ii]>=19 else -1
        for j,(prev,new) in enumerate(zip(old,cs_owners)):
            if prev!=new and t>=250 and new>=0:
                log(t,'diplomacy',f'{NAMES[new]} gains the allegiance of City-State {j+1}.',[new],[*citystates[j]],importance=1)
    allied=Counter(z for z in cs_owners if z>=0)
    for c in civs:
        if not c['alive']:continue
        c['alliances']=allied[c['id']]
        c['delegates']=int(6+2.0*era(t)+c['dip_trait']*.6 + 3.2*c['alliances'])
    # Target selection considers victory risk, defensibility, geography and relation.
    if t>=75 and t%9==0:
        live=[c for c in civs if c['alive']]
        get_victory_state(t)
        active=sum(1 for w in wars.values())
        for a in sorted(live,key=lambda z:z['mil_trait']*(1+z['threat']*.08),reverse=True):
            if active>=min(23,7+era(t)*2):break
            ai=a['id']; own=cities_of(ai)
            if not own:continue
            if sum(ai in (w['a'],w['b']) for w in wars.values())>=2:continue
            # Don't allow hyperaggressive civs to declare every nine turns.
            intent=.13 +.24*max(0,a['mil_trait']-1.0)
            if a['style']=='Domination':intent+=.14
            if a['name'] in ('The Last City','The Boundless City'):intent*=.14
            if a['war_fatigue']>7:intent*=.4
            candidates=[]
            for b in live:
                bi=b['id']
                if ai==bi or at_war(ai,bi):continue
                if t-war_cooldown[war_pair(ai,bi)]<65:continue
                their=cities_of(bi)
                if not their:continue
                dd=min((d((s['x'],s['y']),(q['x'],q['y'])) for s in own for q in their if s['comp']==q['comp']),default=999)
                ocean=e>=4 and dd==999
                if dd==999:
                    if not ocean:continue
                    dd=min(d((s['x'],s['y']),(q['x'],q['y'])) for s in own for q in their)+20
                limit=(19 if e<=2 else 27 if e<=4 else 47)
                if dd>limit:continue
                winthreat=b['threat']
                power=(a['army']*trait_factor(ai,'mil',t))/(b['army']*trait_factor(bi,'mil',t)+1)
                if power<.56 and winthreat<.79:continue
                candidates.append((1.3*winthreat + .22*power-.023*dd+.04*randomizer.random(),bi,winthreat,dd,power))
            if not candidates:continue
            candidates.sort(reverse=True)
            _,bi,winthreat,dd,power=candidates[0]
            if winthreat>.78:intent+=.18
            if winthreat>.92:intent+=.19
            if randomizer.random()>intent:continue
            w=dict(a=ai,b=bi,lead=ai,since=t,last=t,score=0,reason='victory denial' if winthreat>.75 else 'territorial expansion')
            wars[war_pair(ai,bi)]=w;active+=1
            log(t,'war',f'{a["name"]} declares war on {NAMES[bi]} ({w["reason"]}); nearby armies mobilise.',[ai,bi],importance=3)
            if winthreat>.80:
                log(t,'coalition',f'Victory-threat response: {a["name"]} intervenes against {NAMES[bi]} ({winthreat*100:.0f}% modeled threat).',[ai,bi],importance=2)
    # Each ongoing war has a local front, casualties, and gradual city-defense losses.
    for key,w in list(wars.items()):
        ai=w['a'];bi=w['b']
        if not civs[ai]['alive'] or not civs[bi]['alive']:
            wars.pop(key,None);continue
        elapsed=t-w['since']
        if elapsed>95 or (elapsed>33 and randomizer.random()<.009 and abs(w['score'])<2):
            war_cooldown[key]=t;wars.pop(key,None)
            for q in cities:
                q['siege'].pop(ai,None);q['siege'].pop(bi,None)
            log(t,'peace',f'{NAMES[ai]} and {NAMES[bi]} sign a peace settlement after {elapsed} turns.',[ai,bi],importance=2)
            continue
        if t%2:continue
        # Front pressure: defender may counterattack based on comparative power.
        a=civs[ai];b=civs[bi]
        ra=a['army']*trait_factor(ai,'mil',t);rb=b['army']*trait_factor(bi,'mil',t)
        if ra<10 or rb<10:continue
        attack_side=ai if (randomizer.random()<max(.12,min(.88,.56+.20*(ra-rb)/(ra+rb)))) else bi
        defend_side=bi if attack_side==ai else ai
        atk=civs[attack_side];defd=civs[defend_side]
        their=cities_of(defend_side);ours=cities_of(attack_side)
        if not their or not ours:continue
        scored=[]
        for city in their:
            close=min((d((city['x'],city['y']),(o['x'],o['y'])) for o in ours if o['comp']==city['comp']),default=999)
            if close==999 and e>=4:close=min(d((city['x'],city['y']),(o['x'],o['y'])) for o in ours)+20
            if close> (19 if e<=2 else 28 if e<=4 else 47):continue
            scored.append((close+(.0 if city['capital'] else -1.5)+randomizer.random()*2,city))
        if not scored:continue
        _,target=min(scored,key=lambda z:z[0])
        applied=(atk['army']*trait_factor(attack_side,'mil',t))/(defd['army']*trait_factor(defend_side,'mil',t)+1)
        home=1.27 if target['capital'] else 1.04
        ratio=max(.15,min(3.0,applied/home))
        # Small front-line clashes cause genuine mutual losses.
        if randomizer.random()<.51:
            aloss=randomizer.uniform(.002,.013)*atk['army']*(1.1 if ratio<.85 else 1)
            dloss=randomizer.uniform(.002,.013)*defd['army']*(1.1 if ratio>1.18 else 1)
            atk['army']=max(1.,atk['army']-aloss)
            defd['army']=max(1.,defd['army']-dloss)
            atk['damage_taken']+=aloss;defd['damage_taken']+=dloss
            atk['war_fatigue']+=.022;defd['war_fatigue']+=.022
            if randomizer.random()<.44*max(.25,min(1.4,ratio)):
                atk['last_win']=t
                if atk['name']=='The Triumphal Imperium':atk['momentum']=min(6,atk['momentum']+1)
                if atk['name']=='T1 — The ZOFGK Dynasty':atk['veteran']=min(7,atk['veteran']+1) if t%35==0 else atk['veteran']
                if t%15==0:log(t,'battle',f'{atk["name"]} wins a field engagement against {defd["name"]}; both armies suffer losses.',[attack_side,defend_side],[target['x'],target['y']])
        if ratio>.58:
            gain= (1.0+2.8*max(0,ratio-.6)) * randomizer.uniform(.55,1.45)
            if ratio<.85:gain*=.38
            if target['capital']:gain*=.74
            target['siege'][attack_side]=target['siege'].get(attack_side,0.)+gain
            # Siege requires multiple rounds; city capture changes an actual node.
            if target['siege'][attack_side]>= (35 if target['capital'] else 22):
                prev=target['owner'];target['owner']=attack_side
                target['siege'].clear();target['fort']=40.
                atk['army']*=.96;defd['army']*=.97
                atk['gold']+=25;w['score']+=1 if attack_side==ai else -1
                if target['capital']:
                    foreign_cap_losses+=1
                    log(t,'capital',f'{atk["name"]} captures the founding capital of {NAMES[target["founder"]]} from {defd["name"]}.',[attack_side,prev,target['founder']],[target['x'],target['y']],importance=5)
                else:log(t,'conquest',f'{atk["name"]} captures a city from {defd["name"]}.',[attack_side,prev],[target['x'],target['y']],importance=3)
                if atk['name']=='The Triumphal Imperium':atk['momentum']=min(6,atk['momentum']+2);atk['last_win']=t
                if not cities_of(prev):
                    civs[prev]['alive']=False
                    log(t,'elimination',f'{NAMES[prev]} is eliminated by {atk["name"]}.',[prev,attack_side],importance=5)
        if t%10==0 and t-w['since']>10 and randomizer.random()<.22:
            target['siege'][attack_side]=max(0,target['siege'].get(attack_side,0)-2.0)
    # New threats are estimated from actual accumulated state.
    get_victory_state(t)
    # Additional defensive expenditure if any major rival approaches victory.
    threatening=sorted([c for c in civs if c['alive']],key=lambda c:c['threat'],reverse=True)[:3]
    if t>=500 and t%25==0:
        for c in threatening[:2]:
            if c['threat']>=.76:
                log(t,'warning',f'Global strategic alarm: {c["name"]} is {c["threat"]*100:.0f}% toward its most advanced modeled victory pathway.',[c['id']],importance=2)
    if t>=550 and t%15==0:
        leader=threatening[0]
        if leader['threat']>.77:
            opponents=[c for c in civs if c['alive'] and c['id']!=leader['id']]
            # Resistance is strongest where foreign tourism has influence.
            for x in opponents:
                x['culture']+=.13*max(0,leader['cultural_progress']-.66)*x['culture_trait']*(e+1)
            # City-state coalitions spend Gold against the diplomatic leader.
            if leader['alliances']>=4:
                for op in sorted(opponents,key=lambda c:c['dip_trait']*c['econ_trait'],reverse=True)[:4]:
                    if op['gold']>180:
                        j=int(np.argmin(alliances[op['id'],:]))
                        alliances[op['id'],j]+=7;op['gold']-=18
    # Victory eligibility checks; all victory paths are tailored, but thresholds shared.
    live=[c for c in civs if c['alive']]
    contenders=[]
    for c in live:
        i=c['id'];other=[z for z in live if z['id']!=i]
        r=[c['tourism']/(z['culture']*.80+75+z['tech']*.15) for z in other]
        influential=sum(z>=1 for z in r)
        popular=sum(z>=.60 for z in r)
        if t>=550 and influential>=math.ceil(.90*len(other)) and popular==len(other):c['culture_hold']+=1
        else:c['culture_hold']=0
        if c['culture_hold']==1:log(t,'victory',f'{c["name"]} begins a fifteen-turn cultural victory hold ({influential}/{len(other)} influential).',[i],importance=4)
        if c['culture_hold']>=15:contenders.append((t,i,'Culture'))
        if c['tech']>=110 and c['science_parts']>=32:contenders.append((t,i,'Science'))
        if c['capital_count']>=math.ceil(.70*N) and any(z['founder']==i and z['owner']==i for z in cities) and c['army']>max((z['army'] for z in other),default=0):
            c['dom_hold']+=1
        else:c['dom_hold']=0
        if c['dom_hold']>=45:contenders.append((t,i,'Domination'))
    if t in vote_turns:
        ranking=sorted(live,key=lambda c:c['delegates'],reverse=True)
        for z in ranking[:3]:
            log(t,'vote',f'World Leader vote: {z["name"]} fields {z["delegates"]}/27 required delegates with {z["alliances"]} City-State allies.',[z['id']],importance=2)
        for c in live:
            if c['alliances']>=4 and c['delegates']>=27:
                contenders.append((t,c['id'],'Diplomacy'))
    if t%25==0:snapshot(t)
    if contenders:
        contenders.sort(key=lambda r:(-civs[r[1]]['threat'],-civs[r[1]]['score'],r[1]))
        _,cid,kind=contenders[0]
        victory=dict(turn=t,id=cid,name=NAMES[cid],method=kind,qualified=[{'id':x[1],'method':x[2]} for x in contenders])
        log(t,'victory',f'{NAMES[cid]} wins a modeled {kind} Victory.',[cid],importance=5)
        if t%25!=0:snapshot(t,True)
        break

end=t
assert len(snapshots)==len({s['turn'] for s in snapshots})
assert snapshots[-1]['turn']==end
# Event references can always be matched to a city at the time of an event.
for z in civs:
    assert math.isfinite(z['score']) and z['army']>=0

# Saving the complete replay as compact RLE-free base64 map bytes and city ownership lists.
result=dict(title='The War of 56: Balanced Mega-Simulation 2.0',seed=SEED,
    disclaimer='An original turn-by-turn strategic approximation, NOT a Civilization V game run or mod Lua execution.',
    settings=dict(civilizations=N,city_states=CS_COUNT,max_turn=maxturn,game_speed='Marathon (abstract calendar)',
      snapshots_every=25,turn_step=1,marathon_speed_note='Only a turn-counter interpretation; not exact Civ V game-speed yields.'),
    roster=[dict(id=i,name=q[0],collection=q[1],preferred=q[2],traits=list(q[3:])) for i,q in enumerate(ROSTER)],
    colors=colorhex,world=dict(width=W//2,height=H//2,land=base64.b64encode(land[::2,::2].astype(np.uint8).tobytes()).decode('ascii'),
       city_states=[list(x) for x in citystates], start_capitals=[list(x) for x in start_pos],map_scale=2),
    cities=[{k:v for k,v in q.items() if k not in ('siege','fort','age','pop')} for q in cities],
    events=events,snapshots=snapshots,winner=victory,endturn=end,
    final_ranking=sorted(range(N),key=lambda i:(-civs[i]['score'],i)),
    model_rules=dict(science='Research >=110 and spaceship production >=32',
      culture='Influential >=90% of surviving civs; Popular to all others for 15 turns',
      domination='Own >=70% of founding capitals and own home capital; lead armies for 45 turns',
      diplomacy='At a periodic vote, >=27 delegate proxies and >=4 city-state allies',
      no_time='No turn-limit score victory; simulation stops at 1450 if none qualifies',
      war='Territorial wars have active fronts, per-turn casualties, multi-turn sieges and peace treaties',
      counterplay='Visible victory threat raises war incentives; targeted diplomatic and cultural responses',
      citystate='11 city-states with persistently competitive influence bidding',
      geography='Procedurally generated land and schematic city-radius political borders',
      restrictions='Human-only civilizations treated as expert AI to allow a hypothetical 56-civ contest'))
OUT.joinpath('war56_results.json').write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'),default=lambda v:v.item() if hasattr(v,'item') else str(v)))
with OUT.joinpath('war56_final_roster.csv').open('w',newline='',encoding='utf-8') as f:
    writer=csv.writer(f)
    writer.writerow(['Rank','Civ','Collection','Preferred victory','Score','Cities','Capitals held','Army','Science','Culture','Tourism','Influential','Allies','Delegates','Survived'])
    for rank,i in enumerate(result['final_ranking'],1):
        c=civs[i]
        writer.writerow([rank,c['name'],c['group'],c['style'],c['score'],c['city_count'],c['capital_count'],round(c['army'],1),round(c['tech'],1),round(c['culture'],1),round(c['tourism'],1),c['inf_count'],c['alliances'],c['delegates'],c['alive']])

# Renderer uses the true snapshot territory map; no decorative AI-imagined geography.
from matplotlib import patheffects
terrain=np.frombuffer(base64.b64decode(result['world']['land']),dtype=np.uint8).reshape(H//2,W//2)
sea=np.array([[0.065,.17,.255,1.]])
from matplotlib.colors import to_rgba
palette=np.array([to_rgba(h) for h in colorhex]+[to_rgba('#ccd8bd')])

def plot(ax,s,labels=False):
    img=np.frombuffer(base64.b64decode(s['territory']),dtype=np.uint8).reshape(H//2,W//2)
    bg=np.zeros((H//2,W//2,4),dtype=float);bg[:]=to_rgba('#123247')
    lm=terrain>0; bg[lm]=palette[np.where(img[lm]==255,56,img[lm])]
    ax.imshow(bg,origin='upper',extent=(0,W, H,0),interpolation='nearest',aspect='equal')
    # Nation-colored city circles, gold border for capitals, small dot for secondary cities.
    ids=s['city_ids'];owners=s['city_owners'];cityid_to_idx={c['id']:j for j,c in enumerate(result['cities'])}
    for k,cid in enumerate(ids):
        ci=result['cities'][cityid_to_idx[cid]]
        ax.scatter(ci['x'],ci['y'],s=23 if ci['capital'] else 4.8,marker='o',
           facecolor=colorhex[owners[k]],edgecolor='#ffe9a0' if ci['capital'] else '#071b2a',
           linewidth=.8 if ci['capital'] else .15,zorder=7)
        if labels and ci['capital']:
            ax.text(ci['x']+.7,ci['y']-1.2,str(ci['founder']+1),color='white',fontsize=5.5,weight='bold',
              path_effects=[patheffects.withStroke(linewidth=1.5,foreground='#0b2030')],zorder=9)
    for j,(x,y) in enumerate(citystates):
        ax.scatter(x,y,marker='*',s=28,facecolor='#ffdfa1',edgecolor='#1b272c',linewidth=.45,zorder=10)
    for w in s['wars']:
        a=w['a'];b=w['b'];al=[q for k,q in enumerate(ids) if owners[k]==a];bl=[q for k,q in enumerate(ids) if owners[k]==b]
        if not al or not bl:continue
        aa=min((cityid_to_idx[cid] for cid in al),key=lambda idx: min(d((result['cities'][idx]['x'],result['cities'][idx]['y']),(result['cities'][cityid_to_idx[cb]]['x'],result['cities'][cityid_to_idx[cb]]['y'])) for cb in bl))
        u=result['cities'][aa];v=min((result['cities'][cityid_to_idx[cb]] for cb in bl),key=lambda q:d((u['x'],u['y']),(q['x'],q['y'])))
        ax.annotate('',xy=(v['x'],v['y']),xytext=(u['x'],u['y']),arrowprops=dict(arrowstyle='-|>',lw=.9,color='#ff4434',alpha=.75),zorder=9)
    ax.set(xlim=(0,W),ylim=(H,0));ax.set_axis_off();ax.set_title(f'Turn {s["turn"]:4}  ·  {s["era"]}',size=12,color='#182a35',weight='bold',loc='left')

maps=[s for s in snapshots if s['turn']%150==0]
if snapshots[-1] not in maps:maps.append(snapshots[-1])
# 12 panel atlas, avoid excess overlapping legend.
mapshots=maps[:12]
fig,axes=plt.subplots(math.ceil(len(mapshots)/2),2,figsize=(17.5,math.ceil(len(mapshots)/2)*4.25),dpi=105)
for ax,s in zip(axes.ravel(),mapshots):plot(ax,s,labels=False)
for ax in axes.ravel()[len(mapshots):]:ax.axis('off')
fig.suptitle(f'THE WAR OF 56 · POLITICAL WORLD REPLAY · SEED {SEED}',fontsize=19,weight='bold',y=.998)
fig.text(.5,.008,'Colored city territories = estimated political control  ·  golden circles = founding capitals  ·  gold stars = City-States  ·  red arrows = active wars',ha='center',fontsize=10)
fig.subplots_adjust(top=.957,bottom=.027,hspace=.32,wspace=.07,left=.025,right=.975)
fig.savefig(OUT/'war56_world_atlas.png',dpi=105,facecolor='#f6f7f8',bbox_inches='tight');plt.close(fig)
fig,ax=plt.subplots(figsize=(18,9.6),dpi=120)
plot(ax,snapshots[-1],labels=True)
fig.suptitle(f'THE WAR OF 56 · TURN {end} · {"VICTORY: "+victory["name"] if victory else "TURN LIMIT"}',fontsize=17,weight='bold')
fig.savefig(OUT/'war56_final_map.png',dpi=140,facecolor='#f6f7f8',bbox_inches='tight');plt.close(fig)

# Narrative highlights grouped by 25-turn window, with no made-up events.
byera=defaultdict(list)
for v in events:byera[v['turn']//165].append(v)
report=[f'# THE WAR OF 56 — Balanced Mega-Simulation 2.0',
    '',f'**Seed:** {SEED} · **Turns processed:** {end+1} · **Civs:** {N} · **City-States:** 11 · **Map checkpoints:** {len(snapshots)}',
    '', '> This is a deterministic, illustrative strategy model—not a game of Civilization V, AI trained on actual mods, or exact Lua implementation. The geography, borders, armies, science, battles and diplomacy are simulated abstractions.',
    '',f'## Outcome', '',
    f'**{victory["name"]} — {victory["method"]} victory, turn {end}.**' if victory else f'**No victory by turn {end}.**',
    '', '## Campaign statistics', '',
    f'- Cities founded: {len(cities)-N}; total city nodes: {len(cities)}.',
    f'- Wars declared: {sum(z["kind"]=="war" for z in events)}.',
    f'- Founding capitals conquered: {sum(z["kind"]=="capital" for z in events)}.',
    f'- Secondary city captures: {sum(z["kind"]=="conquest" for z in events)}.',
    f'- Eliminations: {sum(z["kind"]=="elimination" for z in events)}.',
    '', '## Complete final standings', '',
    '| Rank | Civilization | Score | Cities | Capitals | Army | Science | Tourism | Influence | Allies |',
    '|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for rank,i in enumerate(result['final_ranking'],1):
    c=civs[i]
    report.append(f'| {rank} | {c["name"]}{" 🏆" if victory and victory["id"]==i else ""} | {c["score"]} | {c["city_count"]} | {c["capital_count"]} | {int(c["army"])} | {c["tech"]:.1f} | {c["tourism"]:.1f} | {c["inf_count"]} | {c["alliances"]} |')
report+=['','## Era-by-era campaign log','']
for k in range(0,era(end)+1):
    stuff=byera[k];report.append(f'### {ERA_NAMES[k]} Era — Turns {k*165}–{min(end,(k+1)*165-1)}')
    major=sorted(stuff,key=lambda v:(-v['importance'],v['turn']))
    selected=major[:42]
    selected.sort(key=lambda v:v['turn'])
    for v in selected:report.append(f'- **T{v["turn"]:04d}** [{v["kind"]}] {v["text"]}')
    if len(stuff)>len(selected):report.append(f'- *Plus {len(stuff)-len(selected)} additional logged events in the complete replay.*')
    report.append('')
report+=['## 25-turn checkpoint standing (top three)','', '| Turn | Leader | Second | Third | Open wars |', '|---:|---|---|---|---:|']
for s in snapshots:
    order=sorted(range(N),key=lambda i:(-s['statistics'][i]['score'],i))
    names=[f'{NAMES[i]} ({s["statistics"][i]["score"]})' for i in order[:3]]
    report.append(f'| {s["turn"]} | {names[0]} | {names[1]} | {names[2]} | {len(s["wars"])} |')
report+=['','## Rules & limitations','']
for k,v in result['model_rules'].items():report.append(f'- **{k}:** {v}.')
report+=['','**Reproducibility:** `python sim56_v2.py` writes the same seeded results and visualizations. The accompanying interactive replay uses the saved `war56_results.json` data.',
        '**Source verification:** Repository rosters were checked against SolusGo/CoolWackyCivs v28, CoolWackyCivs2 v23 and Freehold-of-Una-Court v3, with nine earlier standalone names carried over as provisional.']
(OUT/'war56_campaign_report.md').write_text('\n'.join(report),encoding='utf-8')
print('SEED',SEED,'TURN',end,'WINNER',victory,'SNAPSHOTS',len(snapshots),'CITIES',len(cities),
      'WARS',sum(z['kind']=='war' for z in events),'CAPITALS',sum(z['kind']=='capital' for z in events),
      'EVENTS',len(events))
print('TOP TEN',[(NAMES[i],civs[i]['score']) for i in result['final_ranking'][:10]])
print('MAJOR EVENTS',[(v['turn'],v['kind'],v['text'][:80]) for v in events if v['importance']>=4][:15])