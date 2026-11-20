const {chromium}=require('playwright');
const S='/tmp/claude-0/-home-user-Padr-o-/f4cfd31c-08a1-5478-97d3-f6c9c56ebd61/scratchpad/';
(async()=>{
  const b=await chromium.launch();
  const p=await b.newPage();
  await p.goto('file://'+S+'lavagem-segura.html',{waitUntil:'networkidle'});
  await p.evaluate(()=>document.fonts.ready);
  await p.waitForTimeout(1000);
  const fonts=await p.evaluate(()=>[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family+' '+f.weight));
  console.log('fontes',fonts.join(' | '));
  // páginas que estouram a altura
  const over=await p.evaluate(()=>[...document.querySelectorAll('.page')].map((el,i)=>{
    const r=el.getBoundingClientRect();
    let max=0;el.querySelectorAll('*').forEach(c=>{if(c.closest('.ft'))return;const b=c.getBoundingClientRect();max=Math.max(max,b.bottom-r.top)});
    return [i+1,Math.round(max*0.2646),Math.round(el.scrollHeight*0.2646)];
  }));
  console.log('conteudo(mm) por pagina [pag, base do conteudo, scrollHeight]:',JSON.stringify(over));
  await p.pdf({path:S+'Lavagem-Segura-Tidioli-Studio.pdf',width:'210mm',height:'297mm',printBackground:true,preferCSSPageSize:true});
  await b.close();
})();
