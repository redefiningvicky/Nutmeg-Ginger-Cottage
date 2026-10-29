import json, os, time, secrets, random, threading
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
ROOT=Path(__file__).parent
SOUND_ASSETS={'/assets/sfx/'+f.name for f in (ROOT/'assets'/'sfx').glob('*.wav')}
ROOMS={}; LOCK=threading.RLock()
MAKER_PASSWORD={'salt':'91e7ad4a51c0fa6a42392e6b05ae78d2','hash':'87eb2ff29e89fb1f3bc23f2a708a15fea29ee428d52794b82b4dff5023ecba14'}
MAKER_TOKENS={};MAKER_ATTEMPTS={}
def maker_auth(action,password,client):
 import hashlib,hmac
 if action=='maker_setup':raise ValueError('The maker password is already configured. Please sign in.')
 if not isinstance(password,str) or len(password)>128:raise ValueError('Incorrect password.')
 now=time.time();attempts=[x for x in MAKER_ATTEMPTS.get(client,[]) if now-x<60]
 if len(attempts)>=5:raise ValueError('Too many attempts. Please try again in a minute.')
 MAKER_ATTEMPTS[client]=attempts+[now]
 digest=hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(MAKER_PASSWORD['salt']),300000).hex()
 if not hmac.compare_digest(digest,MAKER_PASSWORD['hash']):raise ValueError('Incorrect password.')
 token=secrets.token_urlsafe(32);MAKER_TOKENS[token]=now+3600;MAKER_ATTEMPTS.pop(client,None);return {'token':token}
def maker_preview(token,outcome):
 if not isinstance(token,str) or MAKER_TOKENS.get(token,0)<time.time():raise ValueError('Please sign in to Maker Results.')
 if outcome not in ['win','lose']:raise ValueError('Choose a win or loss preview.')
 win=outcome=='win';return {'recap':{'correct':16 if win else 8,'guesses':20,'perfect_rounds':6 if win else 2,'rounds':10,'rescues':0 if win else 2},'preview':True,'code':'PREVIEW','me':'maker','host':'maker','phase':'finished','round':10,'progress':100 if win else 0,'buttons':2 if win else 0,'used_gumdrops':[] if win else [1,2],'deadline':0,'next_at':0,'answered':2,'players':[{'id':'maker','name':'Vicky'},{'id':'guest','name':'Preview Player'}],'answers':{'maker':{'value':True,'auto':False},'guest':{'value':win,'auto':False}},'mine':{'value':True},'puzzle':{'question':'Have you saved the cottage?','answer':'The last biscuit is in place.' if win else 'We will need another batch of biscuits.'},'result':{'win':win,'correct':win,'explanation':'An example ending for the game maker.','count':2 if win else 0,'delta':20 if win else -10,'rescued':False}}

# Each line is a reviewed puzzle: question, truthful dodge, answer, explanation.
PUZZLES=[
('Did you hide the gumdrops in the cupboard?', 'Anyone opening that cupboard for gumdrops would find exactly what they wanted.',True,'He says the gumdrops can be found in the cupboard.'),
('Did you eat the last cookie?', 'There were two cookies. I ate one. The other is still on the plate.',False,'A cookie remains, so he did not eat the last one.'),
('Is Nutmeg inside the cottage?', 'Every person inside is wearing a hat. Nutmeg is not wearing a hat.',False,'If Nutmeg were inside, he would have a hat.'),
('Have you got my golden key?', 'Your golden key is the only thing in my left pocket.',True,'The key is in his pocket, so he has it.'),
('Did you open the window?', 'It has stayed shut since breakfast, and I arrived after lunch.',False,'The window has not opened during his visit.'),
('Are all three candy jars empty?', 'One jar still has a peppermint rattling around in it.',False,'One nonempty jar means they are not all empty.'),
('Is the dragon asleep?', 'That snoring is coming from the dragon, who only snores while sleeping.',True,'The dragon is snoring, which here means it is sleeping.'),
('Did you take more than one cupcake?', 'I took one for each hand, and both my hands are holding one.',True,'Two hands holding one cupcake each means two cupcakes.'),
('Is the bridge safe to cross?', 'The only unsafe bridge is the red one. This bridge is blue.',True,'The blue bridge is not the only unsafe bridge, which is red.'),
('Are you hiding behind the door?', 'You can see all of me standing beside Nutmeg in the middle of the room.',False,'He is visible in the middle of the room, not behind the door.'),
('Did you give Nutmeg a present?', 'The parcel I handed him had a tag saying “A gift for Nutmeg.”',True,'He handed Nutmeg a gift.'),
('Is there any icing left?', 'You could scrape every bowl clean and still not collect a single drop.',False,'There is no icing to collect.'),
('Did the wolf arrive before you?', 'When I arrived, the wolf had already finished his tea here.',True,'The wolf was already there, so arrived first.'),
('Are exactly two candles lit?', 'Of the three candles, only the middle one is unlit.',True,'Three candles minus one unlit candle leaves exactly two lit.'),
('Is your ribbon longer than mine?', 'Mine reaches ten inches. Yours reaches twelve.',False,'Ten inches is shorter than twelve.'),
('Have you ever visited this cottage before today?', 'Yesterday Nutmeg served me tea right here in this cottage.',True,'Yesterday’s visit was before today.'),
('Is the treasure in the red box?', 'It is in one of these two boxes. The blue box is empty.',True,'With only red and blue to choose from, it must be in red.'),
('Did you leave any sweets for Nutmeg?', 'I ate every sweet on the plate, and those were the only sweets we had.',False,'He ate all the available sweets.'),
('Can everyone at the table see the cake?', 'Nutmeg is at the table, and a tall vase blocks his view of the cake.',False,'At least Nutmeg cannot see it, so not everyone can.'),
('Is it still raining outside?', 'The rain stopped an hour ago and has not started again.',False,'The rain has stopped.'),
('Did you finish your chores?', 'My list had three chores. I have completed all three.',True,'Every chore on his list is complete.'),
('Is Prince Fondant the tallest person here?', 'Nutmeg is shorter than Prince Fondant, but I am taller than Prince Fondant.',False,'Timber is taller, so Prince Fondant is not the tallest.'),
('Did you put sugar in the tea?', 'I stirred in two spoonfuls from the jar labeled sugar, which contains only sugar.',True,'The spoonfuls he added were sugar.'),
('Is the gate locked?', 'You can push it open without a key; its lock is not engaged.',False,'An unengaged lock means the gate is unlocked.')]
from question_packs import PACK_QUESTIONS, PACK_INFO
PACK_INDICES={}
for pack_id, questions in PACK_QUESTIONS.items():
 PACK_INDICES[pack_id]=list(range(len(PUZZLES),len(PUZZLES)+len(questions)));PUZZLES.extend(questions)
PACK_INDICES['mixed']=list(range(len(PUZZLES)))
def deal_pack(r):
 pool=PACK_INDICES[r.get('pack','mixed')];previous=set(r.get('deck',[]));deck=[]
 for truth in [True,False]:
  eligible=[i for i in pool if PUZZLES[i][2] is truth];fresh=[i for i in eligible if i not in previous]
  deck.extend(random.sample(fresh if len(fresh)>=5 else eligible,5))
 random.shuffle(deck);r['deck']=deck

def set_pack(r,pid,pack):
 if pid!=r['host']:raise ValueError('Only the host can choose a question pack.')
 if r['phase']!='lobby':raise ValueError('Choose the pack before the game starts.')
 if pack not in PACK_INDICES:raise ValueError('Choose an available question pack.')
 r['pack']=pack

TAUNTS=["He didn't say no. That sounds like a yes to me.", "All those extra words? I'd choose no. Very confidently.", "He's hiding a yes behind that wooden smile. Surely.", 'A royal tip: no. My hair and I are almost certain.', 'Listen to what he avoided saying. Perhaps your first guess needs a makeover.', 'Such careful wording usually means no. Or does it?', "I hear a yes. Don't let a little logic spoil a perfectly royal guess.", 'That sounded convincing. Suspiciously convincing. Shall we choose the opposite?', 'No would look rather splendid beside my crown.', 'Yes has such a lovely ring to it. Why trouble yourself with the details?']
def advance(r):
 r['round']+=1;r['phase']='question';r['deadline']=time.time()+20;r['answers']={};r['result']=None;r['reactions']={};r['intro_until']=time.time()+3 if r['round']==10 else 0;r['deadline']=max(time.time(),r['intro_until'])+20

def add_reaction(r,pid,kind,round_number):
 if r['phase'] not in ['reveal','rescue','finished']:raise ValueError('Reactions open when the truth comes out.')
 if round_number!=r['round']:raise ValueError('That reaction belongs to an earlier round.')
 if kind not in ['heart','laugh','surprised']:raise ValueError('Choose one of the three reactions.')
 r.setdefault('reactions',{})[pid]=kind

def resolve(r):
 q=PUZZLES[r['deck'][r['round']-1]]
 for pid in r['players']:
  if pid not in r['answers']:r['answers'][pid]={'value':bool(secrets.randbits(1)),'auto':True}
 correct=sum(a['value']==q[2] for a in r['answers'].values());delta=30*correct/len(r['players'])-10
 r['progress']=max(0,min(100,r['progress']+delta));rescued=False
 r.setdefault('history',[]).append({'correct':correct,'total':len(r['players']),'automatic':sum(a['auto'] for a in r['answers'].values())})
 win=r['progress']>=100;over=win or r['progress']==0 or r['round']>=10
 r['phase']='rescue' if over and not win and r['buttons']>0 else 'finished' if over else 'reveal';r['next_at']=time.time()+8;r['result']={'correct':q[2],'explanation':q[3],'count':correct,'delta':delta,'rescued':rescued,'win':win}

def use_gumdrop(r,number):
 if r['phase']!='rescue':raise ValueError('Gumdrops can be used when the team is prompted for a rescue.')
 if type(number) is not int or number not in [1,2]:raise ValueError('Choose gumdrop 1 or 2.')
 used=r.setdefault('used_gumdrops',[])
 if number in used or r['buttons']<=0:raise ValueError('That gumdrop has already been used.')
 used.append(number);r['buttons']-=1;r['progress']=min(100,r['progress']+25);r['result']['rescued']=True
 r['result']['win']=r['progress']>=100
 if r['result']['win']:r['phase']='finished'
 elif r['round']>=10:r['phase']='rescue' if r['buttons']>0 else 'finished'
 else:r['phase']='reveal'
 r['next_at']=time.time()+8

def tick(r):
 if r['phase']=='question' and time.time()>=r['deadline']:resolve(r)
 elif r['phase']=='reveal' and time.time()>=r['next_at']:advance(r)

def view(r,pid):
 tick(r);out={k:r[k] for k in ['code','phase','round','progress','buttons','deadline','next_at','result','host']}
 out['players']=[{'id':p,'name':n} for p,n in r['players'].items()];out['server_time']=time.time();out['me']=pid
 out['pack']=r.get('pack','mixed');out['packs']=PACK_INFO
 out['intro_until']=r.get('intro_until',0);out['reactions']=r.get('reactions',{})
 out['used_gumdrops']=r.get('used_gumdrops',[])
 out['mine']=r['answers'].get(pid);out['answered']=len(r['answers'])
 if r['phase']!='lobby':
  q=PUZZLES[r['deck'][r['round']-1]];out['puzzle']={'question':q[0],'answer':q[1]};out['taunt']=TAUNTS[(r['round']-1)%len(TAUNTS)]
 if r['phase'] in ['reveal','finished','rescue']:out['answers']=r['answers']
 if r['phase']=='finished':out['recap']={'correct':sum(h['correct'] for h in r.get('history',[])),'guesses':sum(h['total'] for h in r.get('history',[])),'perfect_rounds':sum(h['correct']==h['total'] for h in r.get('history',[])),'rounds':len(r.get('history',[])),'rescues':2-r['buttons']}
 return out
class Handler(BaseHTTPRequestHandler):
 def log_message(self,*args):pass
 def send(self,status,obj):
  data=json.dumps(obj).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
 def do_GET(self):
  from urllib.parse import urlparse,parse_qs
  url=urlparse(self.path)
  if url.path=='/api/maker_status':return self.send(200,{'configured':True})
  if url.path=='/api/state':
   q=parse_qs(url.query)
   with LOCK:
    r=ROOMS.get(q.get('code',[''])[0]);pid=q.get('pid',[''])[0]
    if not r or pid not in r['players']:return self.send(404,{'error':'Room not found. Create or join a room again.'})
    return self.send(200,view(r,pid))
  if url.path in SOUND_ASSETS or url.path in ['/assets/cottage.svg','/assets/faces.svg','/assets/outside.svg','/assets/wife.svg','/assets/prince-cupcake.svg','/assets/happily-ever-after.svg','/assets/fairytale-orchestra.wav','/assets/prince-victory.svg','/assets/rebuild-team.svg']:
   asset=ROOT/url.path.lstrip('/')
   if not asset.exists():return self.send(404,{'error':'Asset not found'})
   data=asset.read_bytes();self.send_response(200);self.send_header('Content-Length',str(len(data)));self.send_header('Content-Type','audio/wav' if asset.suffix=='.wav' else 'image/svg+xml' if asset.suffix=='.svg' else 'image/png');self.send_header('Cache-Control','public, max-age=3600');self.end_headers();self.wfile.write(data);return
  if url.path in ['/sound-library','/sound-library.html']:
   data=(ROOT/'sound-library.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data);return
  if url.path not in ['/','/index.html']:return self.send(404,{'error':'Not found'})
  data=(ROOT/'index.html').read_bytes();self.send_response(200);self.send_header('Content-Type','text/html; charset=utf-8');self.end_headers();self.wfile.write(data)
 def do_POST(self):
  try:
   size=int(self.headers.get('Content-Length',0))
   if size>4096:raise ValueError('Request too large.')
   body=json.loads(self.rfile.read(size));action=self.path.rsplit('/',1)[-1]
   with LOCK:
    if action in ['maker_setup','maker_auth']:return self.send(200,maker_auth(action,body.get('password'),self.client_address[0]))
    if action=='maker_preview':return self.send(200,maker_preview(body.get('token'),body.get('outcome')))
    if action in ['create','join']:
     name=' '.join(str(body.get('name','')).split())[:20]
     if not name:raise ValueError('Enter a player name.')
     pid=secrets.token_hex(16)
     if action=='create':
      code=''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(5))
      while code in ROOMS:code=''.join(secrets.choice('ABCDEFGHJKLMNPQRSTUVWXYZ23456789') for _ in range(5))
      r={'code':code,'players':{},'host':pid,'phase':'lobby','round':0,'progress':50,'buttons':2,'deadline':0,'next_at':0,'result':None,'answers':{},'pack':'mixed','deck':[]};ROOMS[code]=r
     else:
      code=str(body.get('code','')).strip().upper();r=ROOMS.get(code)
      if not r:raise ValueError('That room does not exist.')
      if r['phase']!='lobby':raise ValueError('This game has started. Join the next game.')
      if len(r['players'])>=8:raise ValueError('This room already has eight players.')
     if any(existing.casefold()==name.casefold() for existing in r['players'].values()):
      raise ValueError('That name is already taken in this room. Please choose a different name.')
     r['players'][pid]=name
     return self.send(200,{'code':code,'pid':pid})
    r=ROOMS.get(body.get('code'));pid=body.get('pid')
    if not r or pid not in r['players']:raise ValueError('Your room session has expired.')
    tick(r)
    if action=='start':
     if pid!=r['host']:raise ValueError('Only the host can start.')
     if r['phase']!='lobby' or len(r['players'])<2:raise ValueError('You need at least two players in the lobby.')
     deal_pack(r);advance(r)
    elif action=='set_pack':
     set_pack(r,pid,body.get('pack'))
    elif action=='react':
     add_reaction(r,pid,body.get('reaction'),body.get('round'))
    elif action=='answer':
     if r['phase']!='question':raise ValueError('This question has ended.')
     if time.time()<r.get('intro_until',0):raise ValueError('The final round starts in a moment.')
     if body.get('round')!=r['round']:raise ValueError('That answer belongs to an earlier round.')
     if not isinstance(body.get('value'),bool):raise ValueError('Choose yes or no.')
     r['answers'][pid]={'value':body['value'],'auto':False}
    elif action=='rescue':
     use_gumdrop(r,body.get('gumdrop'))
    elif action=='decline_rescue':
     if pid!=r['host'] or r['phase']!='rescue':raise ValueError('Only the host can continue without a rescue when prompted.')
     r['phase']='finished';r['result']['win']=False
    elif action=='restart':
     if r['phase']!='finished' or (pid!=r['host'] and not r['result'].get('win')):raise ValueError('Only the host can reset after a loss. Any player can play again after a win.')
     r.update(phase='lobby',round=0,progress=50,buttons=2,used_gumdrops=[],history=[],reactions={},intro_until=0,answers={},result=None)
    else:raise ValueError('Unknown action.')
    self.send(200,view(r,pid))
  except (ValueError,KeyError,TypeError) as e:self.send(400,{'error':str(e)})
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=int(os.environ.get('PORT','3000')));parser.add_argument('--host',default='0.0.0.0');parser.add_argument('--strictPort',action='store_true');args=parser.parse_args()
 port=args.port;print(f'Nutmeg game running on http://0.0.0.0:{port}',flush=True);ThreadingHTTPServer((args.host,port),Handler).serve_forever()
