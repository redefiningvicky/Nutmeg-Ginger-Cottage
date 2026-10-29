from pathlib import Path
import numpy as np
from scipy.io.wavfile import write
sr=22050;beat=.68;bar=beat*6;bars=16;duration=bars*bar+3.4
out=np.zeros((int(duration*sr),2),dtype=np.float64);rng=np.random.default_rng(81)
def place(y,start,pan=0):
 i=int(start*sr);n=min(len(y),len(out)-i)
 if n>0:out[i:i+n,0]+=y[:n]*np.sqrt((1-pan)/2);out[i:i+n,1]+=y[:n]*np.sqrt((1+pan)/2)
def string(midi,start,dur,level,pan,bright=.8):
 t=np.arange(int(dur*sr))/sr;freq=440*2**((midi-69)/12);env=(1-np.exp(-t/.36))*np.minimum(1,np.maximum(0,(dur-t)/.75))**1.5
 y=np.zeros_like(t)
 for detune in [-.0014,.0012]:
  phase=2*np.pi*freq*(1+detune)*t+.17*np.sin(2*np.pi*4.2*t+rng.uniform(0,6))
  for h in range(1,9):y+=np.sin(h*phase+rng.uniform(0,.25))*(np.exp(-h*(.23 if bright else .4))/h**1.5)
 place(y*env*level,start,pan)
def piano(midi,start,level,pan):
 t=np.arange(int(2.7*sr))/sr;f=440*2**((midi-69)/12);y=np.zeros_like(t)
 for h in range(1,8):
  fh=f*h*np.sqrt(1+.00007*h*h);decay=np.exp(-t*(1.4+h*.32));y+=np.cos(2*np.pi*fh*t)*decay/h**1.8
 y*=(1-np.exp(-t/.012))*np.minimum(1,(2.7-t)/.25)
 place(y*level,start,pan)
# Original lilting score in F major, with soft minor colors and a resolving homecoming.
chords=[(41,48,53,57),(38,45,50,53),(46,53,58,62),(48,55,60,64),(41,48,53,57),(43,50,55,58),(46,53,58,62),(48,55,60,64),(38,45,50,53),(45,52,57,60),(46,53,58,62),(41,48,53,57),(43,50,55,58),(48,55,60,64),(48,55,60,64),(41,48,53,57)]
melodies=[(65,72),(69,74),(70,77),(76,72),(69,77),(74,70),(72,69),(67,72),(69,74),(72,76),(77,74),(72,69),(70,74),(76,79),(77,72),(69,65)]
for i,c in enumerate(chords):
 start=i*bar
 string(c[0]-12,start,bar+.65,.027,-.25,False)
 string(c[1],start+.025,bar+.6,.018,.15,False)
 string(c[3],start+.045,bar+.55,.014,-.12)
 for j,note in enumerate(melodies[i]):string(note,start+j*bar/2,bar/2+.7,.014,-.35)
 for j,idx in enumerate([0,2,1,3,2,1]):piano(c[idx]+12,start+j*beat,.028,.3)
# Diffuse room reflections; no buzzy waveforms or conspicuous rhythmic echo.
dry=out.copy()
for k in range(1,25):
 delay=int((.047+k*.053+rng.uniform(-.009,.009))*sr);gain=.09*np.exp(-k/8)
 out[delay:]+=dry[:-delay,::-1 if k%2 else 1]*gain
peak=np.max(np.abs(out));out*=.55/max(peak,.55)
fade=int(1.5*sr);out[-fade:]*=np.linspace(1,0,fade)[:,None];out[:int(.15*sr)]*=np.linspace(0,1,int(.15*sr))[:,None]
write(str(Path(__file__).resolve().parents[1]/'assets/fairytale-orchestra.wav'),sr,(out*32767).astype(np.int16))
print('Rendered original soft chamber score:',round(duration,1),'seconds')
