"""Original finalized sound palette made ONLY from additive sine tones and envelopes.
No noise, filters, recordings, downloaded samples, or external sound library.
"""
from pathlib import Path
import json
import numpy as np
from scipy.io.wavfile import write
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'assets'/'sfx';DEST.mkdir(exist_ok=True)
SR=22050
rows=json.loads((ROOT/'scripts'/'room_sound_catalog.json').read_text())
specs=[]
for j,row in enumerate(rows):
 base=50+(j*7)%36;style=j%3
 notes=[base,base+7] if style==0 else [base+7,base,base+12] if style==1 else [base,base+4,base+7]
 specs.append(dict(id=row['tone'],label=row['label'],group=row['group'],notes=notes,step=[.15,.12,.14][style],style=style,description=['Rounded two-note bell','Gentle three-note pluck','Soft rising three-note chime'][style]))
extras=[
 ('gumdrop','Gumdrop Rescues','Magic & Details',[84,88,91,96],.065,1,'A tiny rising candy melody'),
 ('sapphire','Sapphire Gemstone','Magic & Details',[84,91,96,103],.105,2,'Bright, slowly rising magical notes'),
 ('heart','Hearts','Magic & Details',[64,67,72],.15,0,'A warm, tender three-note phrase'),
 ('chocolate-button','Clothing Gumdrop Buttons','Magic & Details',[60,72],.08,1,'Two rounded button notes'),
 ('icing','Prince Fondant’s Icing','Magic & Details',[65,69,72,77],.12,0,'A light rising swirl of tones'),
 ('cherry','Cherry','Magic & Details',[79,76,84],.09,1,'A playful up-and-down melody'),
 ('petal','Rose Petals','Magic & Details',[88,84,79,76],.14,2,'Quiet descending petal notes'),
 ('bow','Ginger’s Hair Bow','Magic & Details',[74,77,81],.11,0,'A gentle bow-shaped musical phrase'),
 ('cake','Cake on the Oven','Magic & Details',[62,69,74],.13,0,'A soft, fluffy three-note bell'),
 ('freezer','Upper Freezer Door','Magic & Details',[86,81,74],.13,2,'A cool descending chime'),
 ('magical-light','All Four Character Profiles','Magic & Details',[79,86,91,98],.11,2,'A shimmering magical-light arpeggio'),
 ('ui','General Interface Click','Magic & Details',[67,74],.06,1,'A short, quiet confirmation tone')]
extras += [
 ('wand','Magic Wands','Ending Illustrations',[76,83,88],.16,2,'Gentle golden-light notes'),
 ('crown','Prince Fondant’s Crown','Ending Illustrations',[67,74,79],.18,0,'A soft royal bell phrase'),
 ('trophy','Trophies','Ending Illustrations',[69,76,81],.17,0,'Warm celebration notes'),
 ('certificate','Certificates','Ending Illustrations',[72,76,79],.19,1,'A delicate flutter of tones'),
 ('medal','Medals','Ending Illustrations',[74,69,81],.18,2,'A gentle swaying chime'),
 ('jar','Icing Jars','Ending Illustrations',[65,72,77],.19,0,'Soft rounded jar notes'),
 ('toolbox','Toolboxes','Ending Illustrations',[57,64,69],.18,1,'A warm low musical knock'),
 ('chocolate','Chocolate Pieces','Ending Illustrations',[60,67,72],.17,0,'Mellow chocolate-like notes'),
 ('candy','Wrapped Candies','Ending Illustrations',[77,81,84],.15,1,'A gentle candy twirl'),
 ('feather','Timber’s Feather','Ending Illustrations',[81,77,74],.20,2,'A slow, light feather phrase'),
 ('icing-tube','Icing Tubes','Ending Illustrations',[62,69,74],.19,2,'A soft curling melody'),
 ('cupcake','Background Cupcakes','Ending Illustrations',[70,74,77],.17,0,'A tender cupcake celebration'),
 ('storybook-page','Storybook Pages','Storybook',[60,64,67],.21,1,'Quiet notes for turning a page'),
 ('storybook-rings','Wedding Rings','Storybook',[72,79,84],.21,2,'A gentle wedding-ring shimmer'),
 ('storybook-heart','Storybook Hearts','Storybook',[65,69,74],.22,0,'A soft phrase of joy and love')]
extras += [('outside', 'Outside', 'Cottage Navigation', [55, 62, 67], 0.16, 0, 'A soft, gentle three-note phrase'), ('inside', 'Inside', 'Cottage Navigation', [56, 63, 68], 0.163, 1, 'A soft, gentle three-note phrase'), ('enter-cottage', 'Enter Cottage', 'Cottage Navigation', [57, 64, 69], 0.166, 2, 'A soft, gentle three-note phrase'), ('first-floor', 'First Floor', 'Cottage Navigation', [58, 65, 70], 0.169, 0, 'A soft, gentle three-note phrase'), ('second-floor', 'Second Floor', 'Cottage Navigation', [59, 66, 71], 0.17200000000000001, 1, 'A soft, gentle three-note phrase'), ('enter-kitchen', 'Enter Kitchen', 'Cottage Navigation', [60, 67, 72], 0.175, 2, 'A soft, gentle three-note phrase'), ('enter-living', 'Enter Living Room', 'Cottage Navigation', [61, 68, 73], 0.178, 0, 'A soft, gentle three-note phrase'), ('enter-office', 'Enter Office', 'Cottage Navigation', [62, 69, 74], 0.181, 1, 'A soft, gentle three-note phrase'), ('enter-bedroom', 'Enter Bedroom', 'Cottage Navigation', [63, 70, 75], 0.184, 2, 'A soft, gentle three-note phrase'), ('enter-bathroom', 'Enter Bathroom', 'Cottage Navigation', [64, 71, 76], 0.187, 0, 'A soft, gentle three-note phrase'), ('enter-pantry', 'Enter Sweet Pantry', 'Cottage Navigation', [65, 72, 77], 0.19, 1, 'A soft, gentle three-note phrase'), ('room-enlarge', 'Enlarge Room', 'Cottage Navigation', [66, 73, 78], 0.193, 2, 'A soft, gentle three-note phrase'), ('desk-books', 'Books on the Pretzel Desk', 'Office', [67, 74, 79], 0.196, 0, 'A soft, gentle three-note phrase')]
extras += [('desk-lamp','Mini Table Lamp on Pretzel Desk','Office',[64,71,80],.185,0,'A warm, gentle lamp-light chime')]
extras += [('keepsake-box','Ginger’s Keepsake Box','Storybook',[62,69,78],.205,0,'A gentle keepsake-box shimmer')]
for key,label,group,notes,step,style,description in extras:specs.append(dict(id=key,label=label,group=group,notes=notes,step=step,style=style,description=description))
manifest={}
for spec in specs:
 duration=(len(spec['notes'])-1)*spec['step']+.85
 t=np.arange(int(SR*duration))/SR;y=np.zeros_like(t)
 for i,midi in enumerate(spec['notes']):
  start=i*spec['step'];z=np.maximum(t-start,0);f=440*2**((midi-76)/12)
  attack=[.045,.032,.055][spec['style']];decay=[.23,.19,.28][spec['style']]
  env=(1-np.exp(-z/attack))*np.exp(-z/decay)*(t>=start)
  tone=np.sin(2*np.pi*f*z)+[.05,.035,.025][spec['style']]*np.sin(2*np.pi*2*f*z)+.008*np.sin(2*np.pi*3*f*z)
  y+=tone*env*(.86**i)
 peak=np.max(np.abs(y));y*=.24/max(peak,1e-9)
 fade=int(.08*SR);y[-fade:]*=np.linspace(1,0,fade)
 write(DEST/(spec['id']+'.wav'),SR,(y*32767).astype(np.int16))
 manifest[spec['id']]={**spec,'duration':round(len(y)/SR,3),'peak':round(float(np.max(np.abs(y))),4),'rms':round(float(np.sqrt(np.mean(y*y))),4),'source':'Original code-generated sine tones only','status':'Finalized — soft and gentle'}
(DEST/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(f'Rendered {len(manifest)} finalized soft tone-only sounds, including 36 unique room-item tones.')
