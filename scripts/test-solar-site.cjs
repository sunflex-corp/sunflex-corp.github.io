const assert=require('node:assert/strict'),vm=require('node:vm'),fs=require('node:fs'),path=require('node:path');
const source=fs.readFileSync(path.join(__dirname,'../assets/sunflex-v2/solar-site.js'),'utf8');
function el(extra={}){return Object.assign({dataset:{},value:'',textContent:'',hidden:false,attrs:{},style:{},events:{},children:{},lists:{},selectedIndex:0,classList:{add(){},toggle(){}},addEventListener(k,f){this.events[k]=f},setAttribute(k,v){this.attrs[k]=v},removeAttribute(k){delete this.attrs[k]},focus(){this.focused=true},querySelector(s){return this.children[s]||null},querySelectorAll(s){return this.lists[s]||[]}},extra);}
function setup(search=''){
 const q=el(),selects=['problem','installation','connectivity','process'].map(name=>el({name})),tabs=['','detect','alert','respond','record'].map(category=>el({dataset:{category}}));
 const tools=el({children:{'input[name=q]':q},lists:{select:selects,'[data-category]':tabs}});
 const products=[['카메라 영상','detect','monitoring','mobile'],['AI 위험성평가','record','inspection-record','software'],['비상 방송','alert','emergency-alert','fixed']].map(([search,category,problem,installation])=>el({dataset:{search,category,problem,installation,connectivity:'lte',process:''}}));
 const count=el(),empty=el(),filter=el(),reset=el(),menu=el({open:true,contains:()=>false,children:{summary:el()}});
 const galleryImage=el(),thumbs=[el({dataset:{gallerySrc:'/one.webp',galleryAlt:'정면'}}),el({dataset:{gallerySrc:'/two.webp',galleryAlt:'측면'}})];
 const gallery=el({children:{'.gallery-stage img':galleryImage,'.gallery-thumbs':el()},lists:{'[data-gallery-src]':thumbs}});
 const need=el(),faqInput=el(),questions=[el({textContent:'제품 자료 요청'}),el({textContent:'설치 문의'})],faqStatus=el();
 const doc=el({children:{'.catalog-tools':tools,'#result-count':count,'.catalog-empty':empty,'.catalog-filters':filter,'.solar-menu':menu,'.product-gallery':gallery,'#product-names':el({textContent:'{"camera":"이동식 CCTV"}'}),'#need':need,'#support-search':faqInput,'.faq-search':el(),'#support-search-status':faqStatus,'#main-content':el()},lists:{'[data-catalog-card]':products,'[data-reset]':[reset],'.faq details':questions},documentElement:{scrollHeight:3000},body:{append(){}},createElement:()=>el()});
 const loc={href:'https://example.test/products/'+search,search};const history={replaceState(a,b,url){this.url=url}};const win=el({matchMedia:()=>({matches:true}),scrollTo(){}});
 vm.runInNewContext(source,{document:doc,window:win,location:loc,history,URL,URLSearchParams,innerHeight:900,scrollY:0,requestAnimationFrame:f=>f()});
 return {q,selects,tabs,products,count,empty,reset,menu,galleryImage,thumbs,need,faqInput,questions,faqStatus,history,win,loc,doc};
}
const t=setup();assert.equal(t.count.textContent,'3');
t.tabs[4].events.click();assert.equal(t.count.textContent,'1');assert.equal(t.products[1].hidden,false);assert.match(t.history.url,/category=record/);
t.q.value='없는제품';t.q.events.input();assert.equal(t.count.textContent,'0');assert.equal(t.empty.hidden,false);
t.reset.events.click();assert.equal(t.count.textContent,'3');assert.equal(t.q.focused,true);assert.equal(t.empty.hidden,true);
t.selects[1].value='mobile';t.selects[1].events.change();assert.equal(t.count.textContent,'1');assert.equal(t.products[0].hidden,false);
t.thumbs[1].events.click();assert.equal(t.galleryImage.src,'/two.webp');assert.equal(t.galleryImage.alt,'측면');assert.equal(t.thumbs[0].attrs['aria-pressed'],'false');
t.doc.events.keydown({key:'Escape'});assert.equal(t.menu.open,false);assert.equal(t.menu.children.summary.focused,true);
t.faqInput.value='설치';t.faqInput.events.input();assert.equal(t.questions[0].hidden,true);assert.equal(t.questions[1].hidden,false);
const deep=setup('?category=eyes&q=카메라&installation=mobile&product=camera');assert.equal(deep.count.textContent,'1');assert.equal(deep.need.value,'이동식 CCTV 도입 문의');
deep.loc.search='?category=record';deep.win.events.popstate();assert.equal(deep.products[1].hidden,false);assert.equal(deep.products[0].hidden,true);
console.log('PASS: combined filters, empty/reset, URL restore and aliases, popstate, gallery state, Escape focus, FAQ search, product inquiry prefill.');
