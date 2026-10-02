'use strict';
// Executable-reference analysis using a real JS parser (acorn): comments and string/template text can never count as references.
const path=require('path');
const tryReq=ps=>{for(const p of ps){try{if(p)return require(p)}catch(e){}}throw new Error('acorn not found (npm i acorn@8 in pass0/)')};
const acorn=tryReq([process.env.ACORN_PATH,path.join(__dirname,'node_modules/acorn'),'/tmp/p0/node_modules/acorn','acorn']);
function analyze(src,names){const ast=acorn.parse(src,{ecmaVersion:'latest',locations:true}),res={};names.forEach(n=>res[n]={declared:[],refs:[]});
 const visit=(n,p,key)=>{if(!n||typeof n.type!=='string')return;
  if(n.type==='Identifier'&&res[n.name]){let skip=false;
   if(p&&p.type==='MemberExpression'&&key==='property'&&!p.computed)skip=true;
   else if(p&&p.type==='Property'&&key==='key'&&!p.computed&&!p.shorthand)skip=true;
   else if(p&&(p.type==='MethodDefinition'||p.type==='PropertyDefinition')&&key==='key'&&!p.computed)skip=true;
   else if(p&&(p.type==='LabeledStatement'||p.type==='BreakStatement'||p.type==='ContinueStatement')&&key==='label')skip=true;
   if(!skip){const L=n.loc.start.line;if(p&&((p.type==='FunctionDeclaration'&&key==='id')||(p.type==='VariableDeclarator'&&key==='id')))res[n.name].declared.push(L);else res[n.name].refs.push(L)}}
  for(const k of Object.keys(n)){if(k==='loc'||k==='start'||k==='end')continue;const v=n[k];if(Array.isArray(v))v.forEach(c=>visit(c,n,k));else if(v&&typeof v.type==='string')visit(v,n,k)}};
 visit(ast,null,null);return res}
module.exports={analyze};
if(require.main===module){const fs=require('fs');let t=fs.readFileSync(process.argv[2],'utf8');if(process.argv[2].endsWith('.html'))t=[...t.matchAll(/<script>([\s\S]*?)<\/script>/g)].pop()[1];console.log(JSON.stringify(analyze(t,process.argv.slice(3))))}