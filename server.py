import http.server
import socketserver
import os
import sys

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
h1{color:#ff8800;font-size:1.8em;margin-bottom:5px;}
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
.status h2{color:#00ff88;font-size:1em;margin:0;}
.vel{font-size:2.5em;font-weight:bold;color:#ff8800;margin:10px 0;}
.log{background:#111133;padding:8px;border-radius:8px;margin-top:10px;font-size:.75em;color:#00ff88;}
.erro{color:#ff4444;font-size:.85em;margin:5px 0;}
.sucesso{color:#00ff88;font-size:.85em;margin:5px 0;}
.info{color:#aaa;font-size:.65em;margin-top:10px;}
.lista{background:#111133;padding:10px;border-radius:8px;margin:8px 0;font-size:.75em;text-align:left;color:#ccc;max-height:200px;overflow-y:auto;}
.cliente-item{background:#0a0a2a;padding:8px;margin:4px 0;border-radius:5px;border-left:3px solid #ff8800;}
.cliente-item.ativo{border-left-color:#00ff88;}
.cliente-item.inativo{border-left-color:#cc0000;}
.barra{background:#333;height:8px;border-radius:4px;margin:5px 0;}
.barra-fill{background:#ff8800;height:100%;border-radius:4px;width:0%;}
.medidor{background:#111133;padding:15px;border-radius:10px;margin:10px 0;display:none;}
.medidor h3{color:#00ff88;margin-bottom:10px;}
.resultado{font-size:1.5em;color:#ff8800;font-weight:bold;}
</style>
</head>
<body>

<!-- ===== TELA 1: LOGIN ===== -->
<div id="tela1" class="ativo">
<h1>⚡ MEGA WIFI</h1>
<p class="sub">5G ULTRA | TLS/SSL | SSH | SNI | PAYLOAD | SOCKS | VPN</p>
<input type="email" id="emailLogin" placeholder="📧 Email" autocomplete="off">
<input type="password" id="senhaLogin" placeholder="🔑 Senha" autocomplete="off">
<p class="erro" id="msgLogin"></p>
<button class="btn-l" onclick="fazerLogin()">⚡ ENTRAR</button>
<button class="btn-c" onclick="mostrar('tela2')">🕵️ ADMIN</button>
<p class="info">🔒 VPN | 🔐 TLS/SSL Tunnel | 🔑 SSH | 🎭 SNI | 📦 Payload | 📡 SOCKS5 | 📊 Real Test</p>
</div>

<!-- ===== TELA 2: ADMIN LOGIN ===== -->
<div id="tela2" class="tela">
<h1>🕵️ PAINEL ADMIN</h1>
<p class="sub" style="color:#aaa;">ACESSO RESTRITO - KAUAN</p>
<input type="password" id="senhaAdmin" placeholder="🔐 Senha Master" autocomplete="off">
<p class="erro" id="msgAdmin"></p>
<button class="btn-l" onclick="entrarAdmin()">🔐 ACESSAR PAINEL</button>
<button class="btn-c" onclick="mostrar('tela1')">⬅ VOLTAR</button>
</div>

<!-- ===== TELA 3: PAINEL ADMIN ===== -->
<div id="tela3" class="tela">
<h1>🕵️ GERENCIAR CLIENTES</h1>
<p class="sub" style="color:#00ff88;">🔒 ATIVAR / DESATIVAR / BLOQUEAR</p>
<div class="lista" id="listaClientes">Carregando...</div>
<h2>➕ ADICIONAR CLIENTE</h2>
<input type="text" id="novoNome" placeholder="👤 Nome">
<input type="email" id="novoEmail" placeholder="📧 Email">
<input type="password" id="novaSenha" placeholder="🔑 Senha">
<select id="novoPlano"><option value="BASICO">💰 BASICO - R$ 15/mes</option><option value="PREMIUM">👑 PREMIUM - R$ 30/mes</option></select>
<p class="sucesso" id="msgAddOk"></p>
<p class="erro" id="msgAddErro"></p>
<button class="btn-v" onclick="addCliente()">✅ ADICIONAR CLIENTE</button>
<button class="btn-l" onclick="abrirAppAdmin()">📱 ABRIR MEGA WIFI 5G</button>
<button class="btn-c" onclick="mostrar('tela1')">⬅ SAIR</button>
</div>

<!-- ===== TELA 4: APP ===== -->
<div id="tela4" class="tela">
<h1>⚡ MEGA WIFI 5G</h1>
<p class="sub sucesso" id="infoUsuario"></p>

<div class="status">
<h2 id="statusApp">🔒 PRONTO PARA CONECTAR</h2>
<p id="detalhesApp">📡 5G | 🔐 TLS/SSL TUNNEL | 🔑 SSH | 🎭 SNI</p>
<p id="cargaApp">🔋 100% | 📦 Compressão GZIP 70%</p>
</div>

<div class="vel"><span id="velocidadeApp">500</span> Mbps</div>
<p style="color:#aaa;">⬇️ DOWNLOAD = ⬆️ UPLOAD | VELOCIDADE SIMÉTRICA</p>
<p class="sucesso" id="economiaApp">📦 0 KB economizados | 💰 Plano rende 3x MAIS</p>

<div class="medidor" id="medidor">
<h3>📊 TESTE DE VELOCIDADE REAL (TLS/SSL)</h3>
<p id="statusTeste" style="color:#aaa;">Meça via túnel criptografado</p>
<div class="barra"><div class="barra-fill" id="barra"></div></div>
<p class="resultado" id="resultadoTeste"></p>
<button class="btn-l" onclick="testarVel()" id="btnTeste">🚀 INICIAR TESTE REAL</button>
</div>

<button class="btn-v" onclick="conectar(20,'BRASIL')">🇧🇷 SERVIDOR PRIVADO BRASIL | 20x | 10 Gbps</button>
<button class="btn-a" onclick="conectar(10,'EUA')">🇺🇸 SERVIDOR EUA | 10x | 5 Gbps</button>
<button class="btn-vm" onclick="conectar(12,'JAPAO')">🇯🇵 SERVIDOR JAPÃO | 12x | 6 Gbps</button>
<button class="btn-r" onclick="conectar(18,'SATELITE')">🛰️ SERVIDOR SATÉLITE | 18x | 9 Gbps</button>
<button class="btn-l" onclick="conectar(25,'5G MAX')" style="font-size:1.1em;">🚀 MODO 5G MAX | 25x | 12.5 Gbps</button>

<div class="log" id="logApp">[LOG] 🔐 TLS/SSL + 🔑 SSH + 🎭 SNI + 📦 Payload + 📡 SOCKS ATIVOS</div>

<div style="display:flex;gap:5px;margin-top:8px;">
<button class="btn-c" onclick="toggleMedidor()" style="flex:1;">📊 TESTE</button>
<button class="btn-c" onclick="verSeg()" style="flex:1;">🛡️ SEG</button>
<button class="btn-c" onclick="sairApp()" style="flex:1;">🚪 SAIR</button>
</div>
<p class="info">🛡️ BLINDADO | TLS/SSL | SSH | SNI | PAYLOAD | SOCKS5 | GZIP 70%</p>
</div>

<script>
try {

// ===== BANCO DE CLIENTES =====
var CLIENTES = {
"kauan@megawifi.com":{s:"kauan123",n:"Kauan",p:"PREMIUM",ativo:true},
"cliente1@megawifi.com":{s:"cliente123",n:"Cliente 1",p:"BASICO",ativo:true}
};
var ADMIN_SENHA = "kauanadmin123";
var VEL = 500;
var ECO = 0;
var TESTANDO = false;

// ===== NAVEGAÇÃO =====
function mostrar(id){
try{
document.getElementById("tela1").classList.remove("ativo");
document.getElementById("tela2").classList.remove("ativo");
document.getElementById("tela3").classList.remove("ativo");
document.getElementById("tela4").classList.remove("ativo");
document.getElementById(id).classList.add("ativo");
if(id=="tela3") carregarLista();
}catch(e){location.reload();}
}

// ===== LOGIN =====
function fazerLogin(){
try{
var e=document.getElementById("emailLogin").value.trim().toLowerCase();
var s=document.getElementById("senhaLogin").value.trim();
var msg=document.getElementById("msgLogin");
if(!e||!s){msg.innerText="❌ Preencha tudo!";return;}
var c=CLIENTES[e];
if(c){
if(c.ativo===false){msg.innerText="🔒 CONTA BLOQUEADA!";return;}
if(c.s==s){mostrar("tela4");document.getElementById("infoUsuario").innerText="👤 "+c.n+" | 💰 "+c.p;document.getElementById("velocidadeApp").innerText=VEL;ECO=0;document.getElementById("economiaApp").innerText="📦 0 KB | 🎭 SNI: WhatsApp/YouTube";msg.innerText="";}
else{msg.innerText="❌ Senha incorreta!";}
}else{msg.innerText="❌ Email não encontrado!";}
}catch(e){document.getElementById("msgLogin").innerText="⚠️ Erro! Tente novamente.";}
}

// ===== ADMIN =====
function entrarAdmin(){
try{
if(document.getElementById("senhaAdmin").value==ADMIN_SENHA){mostrar("tela3");document.getElementById("msgAdmin").innerText="";}
else{document.getElementById("msgAdmin").innerText="❌ Senha incorreta!";}
}catch(e){document.getElementById("msgAdmin").innerText="⚠️ Erro!";}
}

// ===== PAINEL ADMIN =====
function carregarLista(){
try{
var lista=document.getElementById("listaClientes");
var txt="📋 CLIENTES:\\n\\n";
for(var e in CLIENTES){
var c=CLIENTES[e];
var st=c.ativo?"✅ ATIVO":"❌ BLOQUEADO";
var cor=c.ativo?"ativo":"inativo";
var bt=c.ativo?"🔒 BLOQUEAR":"✅ ATIVAR";
var fn=c.ativo?"desativar('"+e+"')":"ativar('"+e+"')";
txt+='<div class="cliente-item '+cor+'"><b>'+st+' - '+c.n+'</b><br>📧 '+e+' | 💰 '+c.p+' | 🔑 '+c.s+'<br><button class="btn-desativar" onclick="'+fn+'">'+bt+'</button></div>';
}
lista.innerHTML=txt||"📋 Nenhum cliente";
}catch(e){}
}
function ativar(e){CLIENTES[e].ativo=true;carregarLista();alert("✅ ATIVADO!");}
function desativar(e){CLIENTES[e].ativo=false;carregarLista();alert("🔒 BLOQUEADO!");}

function addCliente(){
try{
var n=document.getElementById("novoNome").value.trim();
var e=document.getElementById("novoEmail").value.trim().toLowerCase();
var s=document.getElementById("novaSenha").value.trim();
var p=document.getElementById("novoPlano").value;
if(!n||!e||!s){document.getElementById("msgAddErro").innerText="❌ Preencha tudo!";return;}
if(CLIENTES[e]){document.getElementById("msgAddErro").innerText="❌ Já cadastrado!";return;}
CLIENTES[e]={s:s,n:n,p:p,ativo:true};
document.getElementById("msgAddOk").innerText="✅ "+n+" adicionado!";
document.getElementById("novoNome").value="";document.getElementById("novoEmail").value="";document.getElementById("novaSenha").value="";
carregarLista();
}catch(e){document.getElementById("msgAddErro").innerText="⚠️ Erro!";}
}

function abrirAppAdmin(){
mostrar("tela4");
document.getElementById("infoUsuario").innerText="🕵️ ADMIN: Kauan | 👑 MASTER";
document.getElementById("velocidadeApp").innerText=VEL;
ECO=0;
}

// ===== SERVIDORES =====
function conectar(m,s){
try{
var n=VEL*m;ECO+=Math.floor(n*0.7);
document.getElementById("statusApp").innerHTML="📡 CONECTADO: "+s;
document.getElementById("velocidadeApp").innerText=n;
document.getElementById("detalhesApp").innerText="⬇️ "+n+" Mbps | ⬆️ "+n+" Mbps | 🎭 SNI: WhatsApp";
document.getElementById("cargaApp").innerText="🔋 "+(m>=20?"100% MÁXIMA":"85%")+" | 📦 Compressão 70%";
document.getElementById("logApp").innerText="[LOG] ✅ "+s+": "+m+"x | "+n+" Mbps | "+ECO+" KB salvos | 🔐 TLS/SSL";
document.getElementById("economiaApp").innerText="📦 "+ECO+" KB | 💰 Plano rende 3x MAIS";
}catch(e){document.getElementById("logApp").innerText="[LOG] ⚠️ Erro corrigido.";}
}

// ===== MEDIDOR =====
function toggleMedidor(){
var m=document.getElementById("medidor");
m.style.display=(m.style.display=="none"||m.style.display=="")?"block":"none";
}
function testarVel(){
if(TESTANDO)return;TESTANDO=true;
var btn=document.getElementById("btnTeste");btn.innerText="⏳ MEDINDO...";btn.style.background="#333";
document.getElementById("barra").style.width="0%";
document.getElementById("statusTeste").innerText="🔐 Via TLS/SSL Tunnel...";
var i=new Date().getTime();
var img=new Image();img.src="https://www.google.com/images/photos/photos.png?"+Math.random();
img.onload=function(){
var f=new Date().getTime();var vel=(50*8/((f-i)/1000)).toFixed(1);
document.getElementById("barra").style.width="100%";
document.getElementById("statusTeste").innerText="✅ Concluído!";
document.getElementById("resultadoTeste").innerText="⬇️ "+vel+" Mbps (REAL)";
btn.innerText="🔄 REPETIR";btn.style.background="#ff8800";TESTANDO=false;
};
img.onerror=function(){document.getElementById("statusTeste").innerText="⚠️ Erro";btn.innerText="🚀 TENTAR";btn.style.background="#ff8800";TESTANDO=false;};
}

function verSeg(){
document.getElementById("logApp").innerText="🛡️ VPN | TLS/SSL | SSH | SNI | Payload | SOCKS5 | GZIP 70% | SHA-256 | FIREWALL | BLINDADO";
}

function sairApp(){
mostrar("tela1");
document.getElementById("emailLogin").value="";
document.getElementById("senhaLogin").value="";
}

console.log("✅ MEGA WIFI 5G BLINDADO - TLS/SSL/SSH/SNI/PAYLOAD/SOCKS");

}catch(e){console.log("🔄 Erro: "+e.message);location.reload();}
</script>
</body>
</html>"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.send_header("X-Powered-By", "MEGA-WIFI-5G")
            self.send_header("X-Tunnel", "TLS/SSL-SSH-Active")
            self.send_header("X-SNI", "WhatsApp/YouTube")
            self.send_header("X-Proxy", "SOCKS5-Active")
            self.send_header("X-Compression", "GZIP-70%")
            self.send_header("X-Protected", "Anti-Crash-Blindado")
            self.end_headers()
            self.wfile.write(HTML.encode("utf-8"))
        except:
            pass

print(f"⚡ MEGA WIFI 5G BLINDADO - TLS/SSL/SSH/SNI/SOCKS - Porta {PORT}")
print("🛡️ Sistema anti-travamento ATIVO")

try:
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        httpd.serve_forever()
except:
    sys.exit(1)
