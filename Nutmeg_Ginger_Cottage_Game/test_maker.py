import unittest,hashlib
from unittest.mock import patch
import server
class MakerTests(unittest.TestCase):
 def setUp(self):
  salt='1234567890abcdef1234567890abcdef';self.password='test-only-maker-password';digest=hashlib.pbkdf2_hmac('sha256',self.password.encode(),bytes.fromhex(salt),300000).hex();self.setting=patch.object(server,'MAKER_PASSWORD',{'salt':salt,'hash':digest});self.setting.start();server.MAKER_ATTEMPTS.clear()
 def tearDown(self):self.setting.stop()
 def test_password_required(self):
  with self.assertRaises(ValueError):server.maker_preview(None,'win')
  with self.assertRaises(ValueError):server.maker_auth('maker_auth','incorrect-password','test')
  auth=server.maker_auth('maker_auth',self.password,'test');self.assertTrue(server.maker_preview(auth['token'],'win')['result']['win']);self.assertFalse(server.maker_preview(auth['token'],'lose')['result']['win'])
 def test_preview_never_changes_live_rooms(self):
  before=repr(server.ROOMS);auth=server.maker_auth('maker_auth',self.password,'test')
  for outcome in ['win','lose']:
   state=server.maker_preview(auth['token'],outcome);self.assertTrue(state['preview']);self.assertEqual(state['phase'],'finished')
  self.assertEqual(repr(server.ROOMS),before)
 def test_password_cannot_be_overwritten(self):
  with self.assertRaises(ValueError):server.maker_auth('maker_setup','replacement-password','test')
if __name__=='__main__':unittest.main()
