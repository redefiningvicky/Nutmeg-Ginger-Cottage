const {readFileSync}=require('node:fs');const vm=require('node:vm');const assert=require('node:assert/strict');
const app={innerHTML:''},error={};const sandbox={document:{querySelector:s=>s==='#app'?app:s==='#error'?error:null},sessionStorage:{getItem:()=>null},setInterval:()=>0,console};vm.createContext(sandbox);vm.runInContext(readFileSync(__dirname+'/index.html','utf8').split('<script>')[1].split('</script>')[0],sandbox);
vm.runInContext(`
if(cottageRooms.length!==6)throw Error('Six rooms required');
for(const room of cottageRooms){
 cottageRoom=room.id;cottageMode='room';
 if(!cottageInterior(0).includes('0 of 6 features built'))throw Error('Empty room incorrectly built');
 if(!cottageInterior(100).includes('6 of 6 features built'))throw Error('Completed room missing features');
 const threshold=room.items[2][2];
 cottageItem=2;
 if(!cottageInterior(threshold).includes(room.items[2][0]+' · Built'))throw Error('New furniture not built');
 if(!cottageInterior(threshold-1).includes(room.items[2][0]+' · Not Built Yet'))throw Error('Damaged furniture not removed');
}
cottageFloor=0;if(!cottagePlan(50).includes('Enter Kitchen'))throw Error('Kitchen missing');
cottageFloor=1;if(!cottagePlan(50).includes('Enter Bathroom'))throw Error('Bathroom missing');
cottageRoom='bathroom';cottageMode='room';cottageItem=2;
state={phase:'lobby',code:'TEST',me:'host',host:'host',players:[{id:'host',name:'Nutmeg fan'},{id:'guest',name:'Friend'}],progress:65,buttons:2};render();
if(!document.querySelector('#app').innerHTML.includes('Teacup Bath · Built'))throw Error('Live progress did not build feature');
state.progress=55;render();
if(!document.querySelector('#app').innerHTML.includes('Teacup Bath · Not Built Yet'))throw Error('Live damage did not remove feature');
if(cottageRoom!=='bathroom'||cottageMode!=='room')throw Error('Room navigation lost on score update');

cottageRoom='kitchen';if(!cottageInterior(100).includes('Peppermint Fridge'))throw Error('Peppermint Fridge missing');
cottageRoom='pantry';if(!cottageInterior(100).includes('Gummy Bear Shelf')||!cottageInterior(100).includes('Fudge Workbench'))throw Error('Pantry features missing');
state={...state,phase:'finished',round:3,progress:100,deadline:0,next_at:0,answered:2,mine:{value:true},puzzle:{question:'Did you save the cottage?',answer:'It is fully built.'},result:{win:true,correct:true,count:2,delta:20,explanation:'The cottage is complete.'},answers:{host:{value:true,auto:false},guest:{value:true,auto:false}}};render();
if(!document.querySelector('#app').innerHTML.includes('/assets/prince-cupcake.svg'))throw Error('Victory illustration missing');
if(!document.querySelector('#app').innerHTML.includes('Your Fairytale Scrapbook'))throw Error('Ending scrapbook missing');
if(!document.querySelector('#app').innerHTML.includes('/assets/happily-ever-after.svg'))throw Error('Couple illustration missing');
if(!document.querySelector('#app').innerHTML.includes('Play Again With Your Team'))throw Error('Replay label missing');
if(!document.querySelector('#app').innerHTML.includes('>Team Nutmeg & Ginger</span>'))throw Error('Team badge missing');
if(document.querySelector('#app').innerHTML.includes('You wouldn’t understand'))throw Error('Old victory line remains');

state.result.win=false;render();
if(!document.querySelector('#app').innerHTML.includes('/assets/prince-victory.svg')||!document.querySelector('#app').innerHTML.includes('/assets/rebuild-team.svg'))throw Error('Defeat illustrations missing');
if(document.querySelector('#app').innerHTML.includes('👑'))throw Error('Crown emoji remains');
for(const r of cottageRooms){if(r.items.length!==6)throw Error('Room must have six items')}
if(cottageRooms.find(r=>r.id==='kitchen').items[5][0]!=='Espresso-Bean Maker')throw Error('Coffee maker missing');
if(!scene({progress:50,buttons:1,used_gumdrops:[1]}).includes('rescue-gumdrop used'))throw Error('Used rescue must fade');

state.phase='rescue';state.buttons=2;state.used_gumdrops=[];state.progress=0;render();
if(!document.querySelector('#app').innerHTML.includes('One more chance?')||!document.querySelector('#app').innerHTML.includes('Rescue 2: available'))throw Error('Rescue choice missing');
state.used_gumdrops=[2];state.buttons=1;render();
if(document.querySelector('#app').innerHTML.includes('Use Gumdrop'))throw Error('Used rescue offered again');

for(const room of cottageRooms){for(const art of [roomFurniture(room.id),cottageDecoration(room.id),roomExtra(room.id)]){if(contrastRoomArt(art,room.id).includes('fill="'+room.color+'"'))throw Error('Furniture matches its room wall')}}
if(!roomExtra('living').includes('Jawbreakers in three jars'))throw Error('Bonbon jars missing');
if(!cottageDecoration('pantry').includes('Fudge gift boxes'))throw Error('Fudge gifts missing');
if(!roomExtra('pantry').includes('cy="194"'))throw Error('Third truffle missing');

if(!scrapbookBook().includes('Sapphire gemstone: release magical fairy dust'))throw Error('Interactive sapphire missing');
if(scrapbookBook().includes('stroke="#eed395" stroke-width="8"'))throw Error('Yellow-gold ring remains');
const created=[];let removed=false;let cleanup;
document.createElementNS=()=>({setAttribute(){},appendChild(x){created.push(x)},animate(frames,options){if(options.duration<=0)throw Error('Invalid sparkle animation')},remove(){removed=true}});
window={matchMedia:()=>({matches:false})};setTimeout=fn=>{cleanup=fn};
sparkleSapphire({currentTarget:{closest:()=>({appendChild(){}})}});
if(created.length!==30)throw Error('Fairy dust particles missing');cleanup();if(!removed)throw Error('Fairy dust not cleaned up');

`,sandbox);
assert(!app.innerHTML.includes('Icing by icing. Brick by biscuit.'));
console.log('Cottage checks passed: six rooms, both floors, construction and destruction, captions.');

vm.runInContext(`
makerSavedState=null;if(scrapbookBuilders({preview:true,players:[{name:'Vicky'}]})!=='')throw Error('Preview names must not appear as real builders');
makerSavedState={players:[{name:'Actual Builder'}]};const previewBuilders=scrapbookBuilders({preview:true,players:[{name:'Vicky'}]});if(!previewBuilders.includes('Actual Builder')||previewBuilders.includes('Vicky'))throw Error('Only room players belong in builder credits');
if(!scrapbookBuilders({players:[{name:'Vicky'}]}).includes('Vicky'))throw Error('A player actually named Vicky must remain');
`,sandbox);console.log('Builder credits use real room players only, including in Maker Results previews.');
