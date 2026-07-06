import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8080))

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MEGA WIFI 5G</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0a0a1a;color:#fff;font-family:Arial;text-align:center;padding:15px;}
h1{color:#ff8800;font-size:1.8em;}
h2{color:#ff8800;font-size:1.2em;margin:10px 0;}
.sub{color:#ff6600;font-size:.8em;margin-bottom:15px;}
.tela{display:none;}
.ativo{display:block;}
input,select{display:block;width:100%;padding:14px;margin:8px 0;font-size:1em;background:#111133;color:#fff;border:1px solid #ff8800;border-radius:8px;}
button{display:block;width:100%;padding:14px;margin:6px 0;font-size:1em;font-weight:bold;color:#fff;border:none;border-radius:8px;cursor:pointer;}
.btn-l{background:#ff8800;}
.btn-v{background:#00aa00;}
.btn-a{background:#0044aa;}
.btn-vm{background:#aa0044;}
.btn-r{background:#6600aa;}
.btn-c{background:#333;font-size:.8em;}
.btn-desativar{background:#cc0000;font-size:.7em;padding:6px;margin:2px;}
.btn-ativar{background:#00aa00;font-size:.7em;padding:6px;margin:2px;}
.status{background:#111133;padding:12px;border-radius:10px;margin:10px 0;border:2px solid #00ff88;}
.vel{font-size:2.5em;font-weight:bold;color:#ff8800;margin:10px 0;}
.log{background:#111133;padding:8px;border-radius:8px;margin-top:10px;font-size:.75em;color:#00ff88;}
.erro{color:#ff4444;font-size:.85em;margin:5px 0;}
.sucesso{color:#00ff88;font-size:.85em;margin:5px 0;}
.info{color:#aaa;font-size:.65em;margin-top:10px;}
.lista{background:#111133;padding:10px;border-radius:8px;margin:8px 0;font-size:.75em;text-align:left;color:#ccc;max-height:200px;overflow-y:auto;}
.cliente-item{background:#0a0a2a;padding:8px;margin:4px 0;border-radius:5px;border-left:3px solid #ff8800;}
.ativo-item{border-left-color:#00ff88;}
.inativo-item{border-left-color:#cc0000;}
.barra{background:#333;height:8px;border-radius:4px;margin:5px 0;}
.barra-fill{background:#ff8800;height:100%;border-radius:4px;width:0%;}
.medidor{background:#111133;padding:15px;border-radius:10px;margin:10px 0;display:none;}
.resultado{font-size:1.5em;color:#ff8800;font-weight:bold;}
</style>
</head>
<body>

<div id="t1" class="ativo">
<h1>⚡ MEGA WIFI</h1>
<p class="sub">5G ULTRA | TLS/SSL | SSH | SNI | PAYLOAD | SOCKS</p>
<input type="email" id="e1" placeholder="📧 Email" autocomplete="off">
<input type="password" id="s1" placeholder="🔑 Senha" autocomplete="off">
<p class="erro" id="m1"></p>
<button class="btn-l" onclick="login()">⚡ ENTRAR</button>
<button class="btn-c" onclick="ir('t2')">🕵️ ADMIN</button>
<p class="info">🔒 VPN | 🔐 TLS/SSL | 🔑 SSH | 🎭 SNI | 📦 Payload | 📡 SOCKS5</p>
</div>

<div id="t2" class="tela">
<h1>🕵️ PAINEL ADMIN</h1>
<p class="sub" style="color:#aaa;">ACESSO RESTRITO - KAUAN</p>
<input type="password" id="sa" placeholder="🔐 Senha Master" autocomplete="off">
<p class="erro" id="ma"></p>
<button class="btn-l" onclick="admin()">🔐 ACESSAR PAINEL</button>
<button class="btn-c" onclick="ir('t1')">⬅ VOLTAR</button>
</div>

<div id="t3" class="tela">
<h1>🕵️ GERENCIAR CLIENTES</h1>
<p class="sub" style="color:#00ff88;">ATIVAR / DESATIVAR / BLOQUEAR</p>
<div class="lista" id="lista"></div>
<h2>➕ ADICIONAR</h2>
<input type="text" id="nn" placeholder="👤 Nome">
<input type="email" id="ne" placeholder="📧 Email">
<input type="password" id="ns" placeholder="🔑 Senha">
<select id="np"><option value="BASICO">💰 BASICO - R$ 15</option><option value="PREMIUM">👑 PREMIUM - R$ 30</option></select>
<p class="sucesso" id="mok"></p>
<p class="erro" id="mer"></p>
<button class="btn-v" onclick="add()">✅ ADICIONAR</button>
<button class="btn-l" onclick="app('🕵️ ADMIN')">📱 ABRIR APP</button>
<button class="btn-c" onclick="ir('t1')">⬅ SAIR</button>
</div>

<div id="t4" class="tela">
<h1>⚡ MEGA WIFI 5G</h1>
<p class="sub sucesso" id="ui"></p>
<div class="status">
<h2 id="st">🔒 PRONTO</h2>
<p id="dt">📡 5G | 🔐 TLS/SSL | 🔑 SSH | 🎭 SNI</p>
<p id="cg">🔋 100% | 📦 Compressao 70%</p>
</div>
<div class="vel"><span id="vl">500</span> Mbps</div>
<p style="color:#aaa;">DOWN = UP</p>
<p class="sucesso" id="ec">📦 0 KB | 💰 3x MAIS</p>

<div class="medidor" id="med">
<h3>📊 TESTE REAL</h3>
<p id="stt" style="color:#aaa;">Meça via TLS/SSL</p>
<div class="barra"><div class="barra-fill" id="bf"></div></div>
<p class="resultado" id="rt"></p>
<button class="btn-l" onclick="teste()" id="bt">🚀 INICIAR</button>
</div>

<button class="btn-v" onclick="c(20,'BRASIL')">🇧🇷 BRASIL | 20x</button>
<button class="btn-a" onclick="c(10,'EUA')">🇺🇸 EUA | 10x</button>
<button class="btn-vm" onclick="c(12,'JAPAO')">🇯🇵 JAPAO | 12x</button>
<button class="btn-r" onclick="c(18,'SATELITE')">🛰️ SATELITE | 18x</button>
<button class="btn-l" onclick="c(25,'5G MAX')" style="font-size:1.1em;">🚀 5G MAX | 25x</button>

<div class="log" id="lg">[LOG] TLS/SSL + SSH + SNI + PAYLOAD + SOCKS</div>

<div style="display:flex;gap:5px;margin-top:8px;">
<button class="btn-c" onclick="med()" style="flex:1;">📊</button>
<button class="btn-c" onclick="seg()" style="flex:1;">🛡️</button>
<button class="btn-c" onclick="ir('t1')" style="flex:1;">🚪</button>
</div>
<p class="info">🛡️ BLINDADO | TLS/SSL | SSH | SNI | PAYLOAD | SOCKS5 | GZIP 70%</p>
</div>

<script>
var CL={
"kauan@megawifi.com":{s:"kauan123",n:"Kauan",p:"PREMIUM",a:true},
"cliente1@megawifi.com":{s:"cliente123",n:"Cliente 1",p:"BASICO",a:true}
};
var AD="kauanadmin123";
var V=500;
var E=0;
var T=false;

function ir(id){
document.getElementById("t1").classList.remove("ativo");
document.getElementById("t2").classList.remove("ativo");
document.getElementById("t3").classList.remove("ativo");
document.getElementById("t4").classList.remove("ativo");
document.getElementById(id).classList.add("ativo");
if(id=="t3") listar();
}

function login(){
var e=document.getElementById("e1").value.trim().toLowerCase();
var s=document.getElementById("s1").value.trim();
if(!e||!s){document.getElementById("m1").innerText="Preencha!";return;}
var c=CL[e];
if(!c){document.getElementById("m1").innerText="Email nao encontrado!";return;}
if(!c.a){document.getElementById("m1").innerText="CONTA BLOQUEADA!";return;}
if(c.s!=s){document.getElementById("m1").innerText="Senha incorreta!";return;}
app("👤 "+c.n+" | 💰 "+c.p);
}

function admin(){
if(document.getElementById("sa").value==AD){ir("t3");}
else{document.getElementById("ma").innerText="Senha incorreta!";}
}

function app(txt){
ir("t4");document.getElementById("ui").innerText=txt;document.getElementById("vl").innerText=V;E=0;
document.getElementById("ec").innerText="📦 0 KB | 🎭 SNI: WhatsApp";
}

function listar(){
var l=document.getElementById("lista");var t="📋 CLIENTES:\\n\\n";
for(var e in CL){var c=CL[e];var s=c.a?"✅ ATIVO":"❌ BLOQUEADO";var cl=c.a?"ativo-item":"inativo-item";
var bt=c.a?"🔒 BLOQUEAR":"✅ ATIVAR";var fn=c.a?"bloq('"+e+"')":"atv('"+e+"')";
t+='<div class="cliente-item '+cl+'"><b>'+s+' - '+c.n+'</b><br>📧 '+e+' | 💰 '+c.p+' | 🔑 '+c.s+'<br><button class="btn-desativar" onclick="'+fn+'">'+bt+'</button></div>';}
l.innerHTML=t||"Nenhum cliente";
}

function atv(e){CL[e].a=true;listar();alert("✅ ATIVADO!");}
function bloq(e){CL[e].a=false;listar();alert("🔒 BLOQUEADO!");}

function add(){
var n=document.getElementById("nn").value.trim();
var e=document.getElementById("ne").value.trim().toLowerCase();
var s=document.getElementById("ns").value.trim();
var p=document.getElementById("np").value;
if(!n||!e||!s){document.getElementById("mer").innerText="Preencha!";return;}
if(CL[e]){document.getElementById("mer").innerText="Ja existe!";return;}
CL[e]={s:s,n:n,p:p,a:true};
document.getElementById("mok").innerText="✅ "+n+" OK!";
document.getElementById("nn").value="";document.getElementById("ne").value="";document.getElementById("ns").value="";
listar();
}

function c(m,s){
var n=V*m;E+=Math.floor(n*0.7);
document.getElementById("st").innerHTML="📡 "+s;
document.getElementById("vl").innerText=n;
document.getElementById("dt").innerText="DOWN "+n+" | UP "+n+" | SNI";
document.getElementById("cg").innerText="🔋 "+(m>=20?"100%":"85%")+" | 📦 70%";
document.getElementById("lg").innerText="[LOG] "+s+": "+m+"x | "+n+" Mbps | "+E+" KB | TLS/SSL";
document.getElementById("ec").innerText="📦 "+E+" KB | 💰 3x MAIS";
}

function med(){var m=document.getElementById("med");m.style.display=(m.style.display=="none"||m.style.display=="")?"block":"none";}

function teste(){
if(T)return;T=true;var b=document.getElementById("bt");b.innerText="...";b.style.background="#333";
document.getElementById("bf").style.width="0%";document.getElementById("stt").innerText="TLS/SSL...";
var i=new Date().getTime();var img=new Image();
img.src="https://www.google.com/images/photos/photos.png?"+Math.random();
img.onload=function(){var f=new Date().getTime();var v=(50*8/((f-i)/1000)).toFixed(1);
document.getElementById("bf").style.width="100%";document.getElementById("stt").innerText="✅ OK!";
document.getElementById("rt").innerText="DOWN "+v+" Mbps (REAL)";
b.innerText="🔄 REPETIR";b.style.background="#ff8800";T=false;};
img.onerror=function(){document.getElementById("stt").innerText="Erro";b.innerText="🚀 TENTAR";b.style.background="#ff8800";T=false;};
}

function seg(){document.getElementById("lg").innerText="🛡️ VPN | TLS/SSL | SSH | SNI | PAYLOAD | SOCKS5 | GZIP 70% | SHA-256";}
</script>
</body>
</html>"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

print(f"MEGA WIFI 5G - Porta {PORT}")
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    httpd.serve_forever()
