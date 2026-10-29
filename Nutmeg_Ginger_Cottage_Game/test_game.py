import unittest,time
from server import PUZZLES,advance,resolve,tick,view,use_gumdrop,add_reaction
class GameTests(unittest.TestCase):
 def room(self,n=2):
  return dict(code='TEST',players={str(i):str(i) for i in range(n)},host='0',phase='lobby',round=0,progress=50,buttons=2,answers={},result=None,deadline=0,next_at=0,deck=list(range(10)))
 def answer(self,r,count):
  truth=PUZZLES[r['deck'][r['round']-1]][2]
  r['answers']={p:dict(value=truth if i<count else not truth,auto=False) for i,p in enumerate(r['players'])}
 def test_scoring_for_all_room_sizes(self):
  for n in range(2,9):
   for correct in range(n+1):
    r=self.room(n);advance(r);self.answer(r,correct);resolve(r)
    self.assertAlmostEqual(r['progress'],50+30*correct/n-10)
 def test_two_rescues_then_loss(self):
  r=self.room()
  for remaining in [1,0]:
   advance(r);r['progress']=5;self.answer(r,0);resolve(r)
   self.assertEqual(r['phase'],'rescue');self.assertEqual(r['buttons'],remaining+1);self.assertEqual(r['progress'],0)
   use_gumdrop(r,2-remaining)
   self.assertEqual(r['buttons'],remaining);self.assertEqual(r['progress'],25);self.assertTrue(r['result']['rescued'])
  advance(r);r['progress']=5;self.answer(r,0);resolve(r)
  self.assertEqual(r['phase'],'finished');self.assertFalse(r['result']['win'])
 def test_win_and_tenth_round_loss(self):
  r=self.room();advance(r);r['progress']=90;self.answer(r,2);resolve(r)
  self.assertEqual(r['progress'],100);self.assertTrue(r['result']['win'])
  r=self.room();r['round']=9;advance(r);self.answer(r,0);resolve(r)
  self.assertEqual(r['phase'],'rescue');self.assertFalse(r['result']['win'])
 def test_timeout_fills_only_missing_answers(self):
  r=self.room();advance(r);r['answers']['0']=dict(value=True,auto=False);r['deadline']=time.time()-1;tick(r)
  self.assertFalse(r['answers']['0']['auto']);self.assertTrue(r['answers']['1']['auto']);self.assertEqual(r['phase'],'reveal')
 def test_private_choices_and_answer_key(self):
  r=self.room();advance(r);self.answer(r,1);s=view(r,'0')
  self.assertNotIn('answers',s);self.assertNotIn('deck',s);self.assertNotIn('correct',s['puzzle']);self.assertIsNone(s['result'])
  self.assertEqual(s['mine'],r['answers']['0'])
 def test_automatic_next_round(self):
  r=self.room();advance(r);self.answer(r,2);resolve(r);r['next_at']=time.time()-1;tick(r)
  self.assertEqual(r['round'],2);self.assertEqual(r['phase'],'question');self.assertEqual(r['answers'],{})
 def test_rescue_selection_and_duplicate_prevention(self):
  r=self.room();advance(r);r['progress']=5;self.answer(r,0);resolve(r)
  use_gumdrop(r,2);self.assertEqual(r['used_gumdrops'],[2]);self.assertEqual(r['buttons'],1)
  with self.assertRaises(ValueError):use_gumdrop(r,1)
  advance(r);r['progress']=5;self.answer(r,0);resolve(r)
  with self.assertRaises(ValueError):use_gumdrop(r,2)
  self.assertEqual(r['buttons'],1);use_gumdrop(r,1);self.assertEqual(r['buttons'],0)
 def test_final_round_rescue_keeps_round_limit(self):
  r=self.room();r['round']=9;advance(r);r['progress']=55;self.answer(r,2);resolve(r)
  self.assertEqual(r['phase'],'rescue');use_gumdrop(r,1)
  self.assertTrue(r['result']['win']);self.assertEqual(r['round'],10);self.assertEqual(r['progress'],100)
 def test_rescue_waits_without_timeout(self):
  r=self.room();advance(r);r['progress']=5;self.answer(r,0);resolve(r);r['next_at']=time.time()-100
  tick(r);self.assertEqual(r['phase'],'rescue');self.assertEqual(r['buttons'],2)
 def test_finished_scrapbook_uses_all_rounds(self):
  r=self.room();r['progress']=90;advance(r);self.answer(r,1);resolve(r)
  advance(r);self.answer(r,2);resolve(r);recap=view(r,'0')['recap']
  self.assertEqual(recap,{'correct':3,'guesses':4,'perfect_rounds':1,'rounds':2,'rescues':0})
class RoomNameTests(unittest.TestCase):
 def test_duplicate_names_are_rejected(self):
  import json,threading,urllib.request,urllib.error
  from http.server import ThreadingHTTPServer
  from server import Handler
  srv=ThreadingHTTPServer(('127.0.0.1',0),Handler)
  threading.Thread(target=srv.serve_forever,daemon=True).start()
  def post(action,data):
   req=urllib.request.Request('http://127.0.0.1:'+str(srv.server_port)+'/api/'+action,data=json.dumps(data).encode(),headers={'Content-Type':'application/json'})
   return json.load(urllib.request.urlopen(req))
  try:
   room=post('create',{'name':'Cookie Baker'})
   for name in ['Cookie Baker','cookie baker','  COOKIE   BAKER  ']:
    with self.assertRaises(urllib.error.HTTPError) as caught:
     post('join',{'code':room['code'],'name':name})
    self.assertEqual(caught.exception.code,400)
    self.assertIn('choose a different name',json.load(caught.exception)['error'])
   guest=post('join',{'code':room['code'],'name':'Another Baker'})
   self.assertIn('pid',guest)
  finally:
   srv.shutdown();srv.server_close()
if __name__=='__main__':unittest.main()

class SocialFeatureTests(unittest.TestCase):
 room=GameTests.room
 answer=GameTests.answer
 def test_reactions_shared_and_reset(self):
  r=self.room();advance(r);self.answer(r,2);resolve(r)
  add_reaction(r,'0','heart',r['round'])
  self.assertEqual(view(r,'1')['reactions'],{'0':'heart'})
  add_reaction(r,'0','laugh',r['round'])
  self.assertEqual(r['reactions'],{'0':'laugh'})
  for kind,round_number in [('unexpected',r['round']),('heart',r['round']-1)]:
   with self.assertRaises(ValueError):add_reaction(r,'1',kind,round_number)
  advance(r);self.assertEqual(r['reactions'],{})
  with self.assertRaises(ValueError):add_reaction(r,'0','heart',r['round'])
 def test_final_intro_preserves_answer_time(self):
  r=self.room();r['round']=9;advance(r)
  self.assertAlmostEqual(r['intro_until']-time.time(),3,delta=.1)
  self.assertAlmostEqual(r['deadline']-r['intro_until'],20,delta=.1)
  self.assertEqual(view(r,'0')['intro_until'],r['intro_until'])

class QuestionPackTests(unittest.TestCase):
 def test_authored_pack_balance(self):
  from server import PACK_INDICES
  for pack in ['royal','sweet','mischief']:
   pool=PACK_INDICES[pack]
   self.assertEqual(len(pool),20)
   self.assertEqual(sum(PUZZLES[i][2] for i in pool),10)
   self.assertEqual(len({PUZZLES[i][0] for i in pool}),20)
 def test_replays_are_fresh_and_balanced(self):
  from server import deal_pack
  for pack in ['mixed','royal','sweet','mischief']:
   r={'pack':pack,'deck':[]};deal_pack(r);first=set(r['deck']);deal_pack(r)
   self.assertEqual(len(r['deck']),10);self.assertEqual(len(set(r['deck'])),10)
   self.assertEqual(sum(PUZZLES[i][2] for i in r['deck']),5)
   self.assertFalse(first.intersection(r['deck']))
 def test_host_lobby_selection_only(self):
  from server import set_pack
  r={'phase':'lobby','host':'host'};set_pack(r,'host','sweet');self.assertEqual(r['pack'],'sweet')
  for pid,pack in [('guest','royal'),('host','unknown')]:
   with self.assertRaises(ValueError):set_pack(r,pid,pack)
  r['phase']='question'
  with self.assertRaises(ValueError):set_pack(r,'host','royal')
 def test_pack_selection_visible_without_answers(self):
  r=GameTests.room(self);r['pack']='royal';s=view(r,'1')
  self.assertEqual(s['pack'],'royal');self.assertEqual(len(s['packs']),4)
  self.assertNotIn('deck',s);self.assertNotIn('questions',s['packs'][1])
