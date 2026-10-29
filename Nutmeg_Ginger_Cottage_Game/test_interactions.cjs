const fs=require('fs'),vm=require('vm'),assert=require('assert');
let toast,timer;const c={document:{querySelector:s=>s==='#character-reaction'?toast:s==='#app'?{innerHTML:''}:null,body:{appendChild:e=>toast=e},createElement:()=>({setAttribute(){},remove(){toast=null}})},sessionStorage:{getItem:()=>null},setInterval:()=>0,setTimeout:f=>(timer=f,1),clearTimeout:()=>{},console};vm.createContext(c);vm.runInContext(fs.readFileSync(__dirname+'/index.html','utf8').split('<script>')[1].split('</script>')[0],c);
vm.runInContext(`
for(const who of Object.keys(characterLines)){characterReaction(who);if(!document.querySelector('#character-reaction').innerHTML.includes('character-quote'))throw Error('Reaction card missing');}
state={progress:100};
for(const [id,i,marker] of [['living',3,'cozy-flame'],['living',5,'lamp-light'],['office',2,'lamp-light'],['kitchen',2,'sweet-steam'],['bedroom',3,'cabinet-open'],['office',5,'candy-twinkle'],['bedroom',2,'cotton-bounce'],['bathroom',3,'taffy-water'],['bathroom',5,'cabinet-open'],['pantry',2,'gummy-dance'],['pantry',3,'fudge-wiggle'],['kitchen',5,'espresso-pour'],['living',2,'mallow-squish'],['office',3,'book-sway'],['bedroom',4,'rug-ripple'],['bathroom',2,'tea-bubbles'],['pantry',4,'trolley-roll'],['living',4,'jawbreaker-jars'],['office',4,'pretzel-rock']]){
 cottageRoom=id;inspectCottageItem(i);if(!cottageActions[id+':'+i])throw Error('Toggle did not turn on');
 const markup=interactiveFurniture(id,i,i===3?cottageDecoration(id):i===5?familyPainting(id):i===4?roomExtra(id):roomFurniture(id));if(!markup.includes(marker))throw Error('Visual effect missing');
 inspectCottageItem(i);if(cottageActions[id+':'+i])throw Error('Toggle did not turn off');
 state.progress=0;inspectCottageItem(i);if(cottageActions[id+':'+i])throw Error('Missing furniture became active');state.progress=100;
}
state={progress:100};toggleFurnitureDetail('freezer-door','kitchen',3);let fridgeArt=peppermintFridge(cottageDecoration('kitchen'));if(!fridgeArt.includes('Freezer door: close')||!fridgeArt.includes('Fridge door: open'))throw Error('Freezer should open independently');toggleFurnitureDetail('fridge-door','kitchen',3);fridgeArt=peppermintFridge(cottageDecoration('kitchen'));if(!fridgeArt.includes('Freezer door: close')||!fridgeArt.includes('Fridge door: close'))throw Error('Both doors should open');toggleFurnitureDetail('freezer-door','kitchen',3);fridgeArt=peppermintFridge(cottageDecoration('kitchen'));if(!fridgeArt.includes('Freezer door: open')||!fridgeArt.includes('Fridge door: close'))throw Error('Freezer should close independently');state.progress=0;fridgeArt=peppermintFridge(cottageDecoration('kitchen'));if(fridgeArt.includes('door: close'))throw Error('Unbuilt doors should remain closed');state.progress=100;
if((gummyBearShelf().match(/class="gummy-bear"/g)||[]).length!==9)throw Error('Nine gummy bears required');
state={progress:100};toggleFurnitureDetail('oven-cake','kitchen',2);if(!interactiveFurniture('kitchen',2,roomFurniture('kitchen')).includes('class="cake-wiggle"'))throw Error('Cake animation missing');toggleFurnitureDetail('desk-books','office',2);if(!interactiveFurniture('office',2,roomFurniture('office')).includes('class="desk-book-sway"'))throw Error('Desk books animation missing');if(cottageActions['office:2'])throw Error('Books unexpectedly switched on lamp');
if(!face('gingy').includes('role="button"'))throw Error('Character not accessible');
`,c);timer();assert.equal(toast,null);console.log('Character reactions, toast dismissal, furniture toggles and construction gates pass.');
(async()=>{
 const status={textContent:'',classList:{toggle(){}}};const originalQuery=c.document.querySelector;
 c.document.querySelector=s=>s==='#copy-status'?status:originalQuery(s);
 vm.runInContext("state={code:'ABCDE'}",c);let copied='';c.navigator={clipboard:{writeText:async value=>copied=value}};
 await vm.runInContext('copyRoomCode()',c);assert.equal(copied,'ABCDE');assert.equal(status.textContent,'Room code copied!');timer();assert.equal(status.textContent,'');
 await vm.runInContext('copyWebsite()',c);assert.equal(copied,'https://nutmeg-ginger-cottage.airyant14.chatgpt.site/');assert.equal(status.textContent,'Website link copied!');timer();assert.equal(status.textContent,'');
 c.navigator.clipboard.writeText=async()=>{throw Error('Blocked')};let selected=false,removed=false;
 c.document.createElement=()=>({style:{},setAttribute(){},select(){selected=true},remove(){removed=true}});c.document.execCommand=()=>true;
 await vm.runInContext('copyRoomCode()',c);assert(selected&&removed);assert.equal(status.textContent,'Room code copied!');
 c.document.execCommand=()=>false;await vm.runInContext('copyRoomCode()',c);assert.equal(status.textContent,'Copy this room code: ABCDE');
 await vm.runInContext('copyWebsite()',c);assert.equal(status.textContent,'Copy this website link: https://nutmeg-ginger-cottage.airyant14.chatgpt.site/');
 console.log('Room-code and website copying, brief confirmation, legacy fallback and manual fallback pass.');
})().catch(e=>{console.error(e);process.exitCode=1});
