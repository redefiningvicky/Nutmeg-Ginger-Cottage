import io,threading,unittest,wave,hashlib
from urllib.request import urlopen
from urllib.error import HTTPError
from server import SOUND_ASSETS,Handler,ThreadingHTTPServer
class SoundAssetTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.http=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=cls.http.serve_forever,daemon=True).start();cls.base=f'http://127.0.0.1:{cls.http.server_port}'
 @classmethod
 def tearDownClass(cls):cls.http.shutdown();cls.http.server_close()
 def test_all_effects_are_served_and_decodable(self):
  self.assertEqual(len(SOUND_ASSETS),78);hashes=set()
  for asset in SOUND_ASSETS:
   with self.subTest(asset=asset):
    with urlopen(self.base+asset+'?v=foley1') as response:
     self.assertEqual(response.headers['Content-Type'],'audio/wav');data=response.read()
    hashes.add(hashlib.sha256(data).digest())
    with wave.open(io.BytesIO(data)) as audio:
     self.assertEqual(audio.getnchannels(),1);self.assertEqual(audio.getsampwidth(),2);self.assertEqual(audio.getframerate(),22050)
     duration=audio.getnframes()/audio.getframerate();self.assertGreaterEqual(duration,.25);self.assertLessEqual(duration,1.65)
  self.assertEqual(len(hashes),78)
 def test_unknown_audio_path_is_not_served(self):
  with self.assertRaises(HTTPError) as error:urlopen(self.base+'/assets/sfx/not-a-sound.wav')
  self.assertEqual(error.exception.code,404)

 def test_sound_review_page_contains_the_complete_draft_catalog(self):
  import json,re
  with urlopen(self.base+'/sound-library') as response:
   self.assertEqual(response.status,200);page=response.read().decode()
  catalog=json.loads(re.search(r'<script id="sound-data" type="application/json">(.*?)</script>',page).group(1))
  self.assertEqual(len(catalog),78);self.assertEqual(len({entry['id'] for entry in catalog}),78)
  self.assertTrue(all('tones only' in entry['source'] for entry in catalog))
  self.assertNotIn('/api/',page)
 def test_generator_has_no_noise_or_filters(self):
  from pathlib import Path
  source=(Path(__file__).parent/'scripts'/'render_sfx.py').read_text()
  for forbidden in ['np.random','scipy.signal','sosfilt','butter(', 'def noise(']:self.assertNotIn(forbidden,source)

 def test_finalized_palette_has_soft_peaks(self):
  import json,array
  from pathlib import Path
  root=Path(__file__).parent
  manifest=json.loads((root/'assets'/'sfx'/'manifest.json').read_text())
  for kind,spec in manifest.items():
   self.assertEqual(spec['status'],'Finalized — soft and gentle')
   self.assertLessEqual(spec['peak'],.241)
   with wave.open(str(root/'assets'/'sfx'/(kind+'.wav'))) as audio:
    samples=array.array('h',audio.readframes(audio.getnframes()))
    self.assertEqual(samples[0],0);self.assertEqual(samples[-1],0)
