const fs=require('fs'),vm=require('vm'),assert=require('assert');
for(const [file,kind,count] of [['prince-cupcake','petal',19],['prince-victory','wand',25],['rebuild-team','cherry',25],['happily-ever-after','heart',21]]){
 const source=fs.readFileSync(`assets/${file}.svg`,'utf8');
 assert(source.includes('[data-magic]:hover'));assert(source.includes('[data-magic]:focus-visible'));
 assert.equal((source.match(/data-magic=/g)||[]).length,count);
 const code=source.match(/<script>([\s\S]*?)<\/script>/)[1].replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&');
 for(const kind of new Set([...source.matchAll(/data-magic="([^"]+)"/g)].map(m=>m[1])))for(const reduced of [false,true]){
  const particles=['petal','wand','heart','cherry'].includes(kind),n=particles?22:1;
  const handlers={},animations=[],layers=[],timers=[];
  const element=()=>({children:[],setAttribute(){},appendChild(e){this.children.push(e)},animate(f,o){animations.push({f,o})},remove(){this.removed=true}});
  const svg=element();svg.addEventListener=(n,f)=>handlers[n]=f;svg.createSVGPoint=()=>({matrixTransform:()=>({x:40,y:50})});svg.appendChild=e=>layers.push(e);
  vm.runInNewContext(code,{document:{documentElement:svg,createElementNS:element},matchMedia:()=>({matches:reduced}),setTimeout:f=>timers.push(f),Math});
  const target={animate(f,o){animations.push({f,o})},getBBox:()=>({x:0,y:0,width:20,height:20}),getCTM:()=>({}),getAttribute:()=>kind};
  const event={target:{closest:()=>target},type:'click'};handlers.click(event);
  assert.equal(animations.length,n);assert.equal(layers[0].children.length,particles?22:0);
  if(particles)timers.shift()();assert(layers[0].removed);
  handlers.keydown({...event,type:'keydown',key:'Escape'});assert.equal(animations.length,n);
  handlers.keydown({...event,type:'keydown',key:'Enter',preventDefault(){}});assert.equal(animations.length,n*2);
  if(reduced)assert(animations.every(a=>a.o.duration===(particles?400:350)));
 }
}
console.log('Ending artwork: all 90 interactive details respond to click and keyboard; particle cleanup and reduced motion pass.');
