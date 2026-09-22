/* Build-time only: CSS-tree parses selectors; no runtime dependency is shipped. */
const fs=require('node:fs'),path=require('node:path');
const css=require(process.env.SUNFLEX_CSS_TREE||'css-tree');
const root=path.resolve(__dirname,'..'),draft=path.resolve(process.argv[2]);
const used=new Set(JSON.parse(fs.readFileSync(path.join(root,'data/product-infographic-classes.json'))));
const scope=':where(.product-editorial) :is(#product-benefits,#blind-corner) .sunflex-infographic';
const ast=css.parse(['style.css','technical-layout.css'].map(f=>fs.readFileSync(path.join(draft,f),'utf8')).join('\n'));
css.walk(ast,{visit:'Atrule',enter(node,item,list){
 if(['font-face','keyframes'].includes(node.name)){list.remove(item);return css.walk.skip}
 if(node.name==='media'&&node.prelude){const q=css.generate(node.prelude);if(q.includes('prefers-reduced-motion')){list.remove(item);return css.walk.skip}
  node.name='container';node.prelude=css.parse('sunflex-infographic '+q,{context:'atrulePrelude',atrule:'container'});
 }
}});
css.walk(ast,{visit:'Rule',enter(node,item,list){
 if(!node.prelude||node.prelude.type!=='SelectorList')return;
 const kept=[];
 node.prelude.children.forEach(selector=>{
  const raw=css.generate(selector),classes=[];
  css.walk(selector,{visit:'ClassSelector',enter(n){classes.push(n.name)}});
  if(classes.includes('comparison'))return;
  if(raw===':root'){kept.push(scope);return}
  if(!classes.some(c=>used.has(c)))return;
  kept.push(scope+' '+raw);
 });
 if(!kept.length){list.remove(item);return css.walk.skip}
 node.prelude=css.parse(kept.join(','),{context:'selectorList'});
}});
const out=path.join(root,'assets/sunflex-v2/product-infographics.css');
fs.writeFileSync(out,'/* Scoped product infographic compositions. */\n'+css.generate(ast)+'\n');
console.log('Scoped visual CSS: '+fs.statSync(out).size+' bytes');
