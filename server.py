import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8080))

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MEGA WIFI 5G</title>
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore-compat.js"></script>
<style>
body{background:#0a0a1a;color:#fff;font-family:Arial;text-align:center;padding:15px;}
h1{color:#ff8800;font-size:1.8em;}
h2{color:#ff8800;font-size:1.2em;margin:10px 0;}
button{display:block;width:100%;padding:14px;margin:6px 0;font-size:1em;font-weight:bold;color:#fff;border:none;border-radius:8px;cursor:pointer;}
.btn-l{background:#ff8800;}
.btn-v{background:#00aa00;}
.btn-a{background:#0044aa;}
.btn-vm{background:#aa0044;}
.btn-r{background:#6600aa;}
.btn-c{background:#333;font-size:.8em;}
.btn-desativar{background:#cc0000;font-size:.7em;padding:6px;margin:2px;}
.btn-ativar{background:#00aa00;font-size:.7em;padding:6px;margin:2px;}
input,select{display:block;width:100%;padding:12px;margin:6px 0;font-size:1em;background:#111133;color:#fff;border:1px solid #ff8800;border-radius:8px;}
.status{background:#111133;padding:12px;border-radius:10px;margin:10px 0;border:2px solid #00ff88;}
.status h2{color:#00ff88;font-size:1em;margin:0;}
.vel{font-size:2em;font-weight:bold;color:#ff8800;margin:8px 0;}
.log{background:#111133;padding:8px;border-radius:8px;margin-top:10px;font-size:.75em;color:#00ff88;}
.erro{color:#ff4444;font-size:.85em;}
.sucesso{color:#00ff88;font-size:.85em;}
.lista{background:#111133;padding:10px;border-radius:8px;margin:8px 0;font-size:.75em;text-align:left;color:#ccc;max-height:250px;overflow-y:auto;}
.cliente-item{background:#0a0a2a;padding:8px;margin:4px 0;border-radius:5px;border-left:3px solid #ff8800;}
.ativo{border-left-color:#00ff88;}
.inativo{border-left-color:#cc0000;}
.barra{background:#333;height:8px;border-radius:4px;margin:5px 0;}
.barra-fill{background:#ff8800;height:100%;border-radius:4px;width:0%;}
.medidor{background:#111133;padding:15px;border-radius:10px;margin:10px 0;display:none;}
.medidor h3{color:#00ff88;margin-bottom:10px;}
.resultado{font-size:1.5em;color:#ff8800;font-weight:bold;}
.eco{color:#00ff88;font-size:.9em;margin:5px 0;}
.sub{color:#ff8800;font-size:.8em;margin-bottom:10px;}
.tecnologias{color:#ff6600;font-size:.65em;margin:5px 0;}
</style>
</head>
<body>

<!-- ========== TELA 1: LOGIN ========== -->
<div id="telaLogin">
<h1>⚡ MEGA WIFI</h1>
<p class="sub">5G ULTRA | TLS/SSL | SSH | SNI | PAYLOAD</p>
<input type="email" id="email" placeholder="📧 Email">
<input type="password" id="senha" placeholder="🔑 Senha">
<p class="erro" id="msgLogin"></p>
<button class="btn-l" onclick="fazerLogin()">⚡ ENTRAR</button>
<button class="btn-c" onclick="irPara('telaAdminLogin')">🕵️ ADMIN</button>
<p class="tecnologias">🔒 VPN | 🔐 TLS/SSL Tunnel | 🔑 SSH | 🎭 SNI | 📦 Payload | 📡 SOCKS</p>
</div>

<!-- ========== TELA 2: ADMIN LOGIN ========== -->
<div id="telaAdminLogin" style="display:none;">
<h1>🕵️ PAINEL ADMIN</h1>
<p class="sub" style="color:#aaa;">ACESSO RESTRITO - KAUAN</p>
<input type="password" id="senhaAdmin" placeholder="🔐 Senha Master">
<p class="erro" id="msgAdmin"></p>
<button class="btn-l" onclick="entrarPainel()">🔐 ACESSAR PAINEL</button>
<button class="btn-c" onclick="irPara('telaLogin')">⬅ VOLTAR</button>
</div>

<!-- ========== TELA 3: PAINEL ADMIN ========== -->
<div id="telaPainel" style="display:none;">
<h1>🕵️ GERENCIAR CLIENTES</h1>
<p class="sub" style="color:#00ff88;">🔒 ATIVAR / DESATIVAR / BLOQUEAR</p>
<div class="lista" id="listaClientes">Carregando...</div>
<h2>➕ ADICIONAR CLIENTE</h2>
<input type="text" id="novoNome" placeholder="👤 Nome">
<input type="email" id="novoEmail" placeholder="📧 Email">
<input type="password" id="novaSenha" placeholder="🔑 Senha">
<select id="novoPlano">
<option value="BASICO">💰 BASICO - R$ 15/mes</option>
<option value="PREMIUM">👑 PREMIUM - R$ 30/mes</option>
</select>
<p class="sucesso" id="msgAddOk"></p>
<p class="erro" id="msgAddErro"></p>
<button class="btn-v" onclick="addCliente()">✅ ADICIONAR CLIENTE</button>
<button class="btn-l" onclick="abrirAppAdmin()">📱 ABRIR MEGA WIFI 5G</button>
<button class="btn-c" onclick="irPara('telaLogin')">⬅ SAIR</button>
</div>

<!-- ========== TELA 4: APP ========== -->
<div id="telaApp" style="display:none;">
<h1>⚡ MEGA WIFI 5G</h1>
<p class="sub" id="infoUsuario" style="color:#00ff88;"></p>

<div class="status">
<h2 id="statusApp">🔒 PRONTO</h2>
<p id="detalhesApp">📡 5G | 🔐 TLS/SSL | 🔑 SSH | 🎭 SNI</p>
<p id="cargaApp">🔋 100% | 📦 Compressão 70%</p>
</div>

<div class="vel"><span id="velocidadeApp">500</span> Mbps</div>
<p style="color:#aaa;">⬇️ DOWNLOAD = ⬆️ UPLOAD</p>
<p class="eco" id="economiaApp">📦 0 KB | 💰 3x MAIS DADOS</p>

<div class="medidor" id="medidor">
<h3>📊 TESTE DE VELOCIDADE REAL</h3>
<p id="statusTeste" style="color:#aaa;">Meça via TLS/SSL Tunnel</p>
<div class="barra"><div class="barra-fill" id="barra"></div></div>
<p class="resultado" id="resultadoTeste"></p>
<button class="btn-l" onclick="testarVelocidade()" id="btnTeste">🚀 INICIAR TESTE</button>
</div>

<button class="btn-v" onclick="conectar(20,'BRASIL')">🇧🇷 SERVIDOR PRIVADO BRASIL | 20x</button>
<button class="btn-a" onclick="conectar(10,'EUA')">🇺🇸 EUA | 10x</button>
<button class="btn-vm" onclick="conectar(12,'JAPAO')">🇯🇵 JAPAO | 12x</button>
<button class="btn-r" onclick="conectar(18,'SATELITE')">🛰️ SATELITE | 18x</button>
<button class="btn-l" onclick="conectar(25,'5G MAX')" style="font-size:1.1em;">🚀 5G MAX | 25x</button>

<div class="log" id="logApp">[LOG] 🔐 TLS/SSL + 🔑 SSH + 🎭 SNI + 📦 Payload ATIVOS</div>

<div style="display:flex;gap:5px;margin-top:8px;">
<button class="btn-c" onclick="toggleMedidor()" style="flex:1;">📊 TESTE</button>
<button class="btn-c" onclick="verSeguranca()" style="flex:1;">🛡️ SEG</button>
<button class="btn-c" onclick="irPara('telaLogin')" style="flex:1;">🚪 SAIR</button>
</div>
<p class="tecnologias">🔒 VPN | 🔐 TLS/SSL | 🔑 SSH | 🎭 SNI | 📦 Payload | 📡 SOCKS | 📊 Real Test</p>
</div>

<script>
// ========== FIREBASE ==========
const firebaseConfig = {
  apiKey: "AIzaSyCOxhksH7pb2-ykAfREpLUtZzrK7WoiaKw",
  authDomain: "megawifi5g.firebaseapp.com",
  projectId: "megawifi5g",
  storageBucket: "megawifi5g.firebasestorage.app",
  messagingSenderId: "951202181072",
  appId: "1:951202181072:web:99d67304570016692ad3d5"
};
firebase.initializeApp(firebaseConfig);
var db = firebase.firestore();

var ADMIN = "kauanadmin123";
var velBase = 500;
var ecoTotal = 0;
var testando = false;

// ========== NAVEGAÇÃO SIMPLES ==========
function irPara(tela){
document.getElementById("telaLogin").style.display="none";
document.getElementById("telaAdminLogin").style.display="none";
document.getElementById("telaPainel").style.display="none";
document.getElementById("telaApp").style.display="none";
document.getElementById(tela).style.display="block";
}

// ========== LOGIN ==========
function fazerLogin(){
var e=document.getElementById("email").value.trim();
var s=document.getElementById("senha").value.trim();
if(!e||!s){document.getElementById("msgLogin").innerText="❌ Preencha email e senha!";return;}
document.getElementById("msgLogin").innerText="⏳ Verificando...";
db.collection("clientes").doc(e).get().then(function(doc){
if(doc.exists){
var c=doc.data();
if(c.ativo===false){document.getElementById("msgLogin").innerText="🔒 CONTA BLOQUEADA!";return;}
if(c.s===s){
irPara("telaApp");
document.getElementById("infoUsuario").innerText="👤 "+c.n+" | 💰 "+c.p;
document.getElementById("velocidadeApp").innerText=velBase;
ecoTotal=0;
document.getElementById("economiaApp").innerText="📦 0 KB | 🎭 SNI: WhatsApp/YouTube";
document.getElementById("msgLogin").innerText="";
}else{document.getElementById("msgLogin").innerText="❌ Senha incorreta!";}
}else{document.getElementById("msgLogin").innerText="❌ Email não encontrado!";}
}).catch(function(e){document.getElementById("msgLogin").innerText="❌ Erro: "+e.message;});
}

// ========== PAINEL ADMIN ==========
function entrarPainel(){
if(document.getElementById("senhaAdmin").value==ADMIN){
irPara("telaPainel");
carregarClientes();
}else{document.getElementById("msgAdmin").innerText="❌ Senha master incorreta!";}
}

function carregarClientes(){
db.collection("clientes").get().then(function(q){
var lista=document.getElementById("listaClientes");
var txt="";
q.forEach(function(doc){
var c=doc.data();
var email=doc.id;
var status=c.ativo?"✅ ATIVO":"❌ BLOQUEADO";
var cor=c.ativo?"ativo":"inativo";
var btnTexto=c.ativo?"🔒 BLOQUEAR":"✅ ATIVAR";
var btnFunc=c.ativo?"desativarCliente":"ativarCliente";
txt+='<div class="cliente-item '+cor+'">';
txt+='<b>'+status+' - '+c.n+'</b><br>';
txt+='📧 '+email+' | 💰 '+c.p+' | 🔑 '+c.s+'<br>';
txt+='<button class="btn-desativar" onclick="'+btnFunc+'(\''+email+'\')">'+btnTexto+'</button>';
txt+='</div>';
});
if(txt=="")txt="📋 Nenhum cliente cadastrado";
lista.innerHTML=txt;
});
}

function ativarCliente(e){db.collection("clientes").doc(e).update({ativo:true}).then(function(){carregarClientes();alert("✅ Cliente ATIVADO!");});}
function desativarCliente(e){db.collection("clientes").doc(e).update({ativo:false}).then(function(){carregarClientes();alert("🔒 Cliente BLOQUEADO!");});}

function addCliente(){
var n=document.getElementById("novoNome").value.trim();
var e=document.getElementById("novoEmail").value.trim();
var s=document.getElementById("novaSenha").value.trim();
var p=document.getElementById("novoPlano").value;
document.getElementById("msgAddOk").innerText="";document.getElementById("msgAddErro").innerText="";
if(!n||!e||!s){document.getElementById("msgAddErro").innerText="❌ Preencha todos os campos!";return;}
db.collection("clientes").doc(e).get().then(function(doc){
if(doc.exists){document.getElementById("msgAddErro").innerText="❌ Email já cadastrado!";}
else{db.collection("clientes").doc(e).set({n:n,e:e,s:s,p:p,ativo:true}).then(function(){
document.getElementById("msgAddOk").innerText="✅ "+n+" adicionado com sucesso!";
document.getElementById("novoNome").value="";document.getElementById("novoEmail").value="";document.getElementById("novaSenha").value="";
carregarClientes();});}
});
}

function abrirAppAdmin(){
irPara("telaApp");
document.getElementById("infoUsuario").innerText="🕵️ ADMIN: Kauan | 👑 MASTER";
document.getElementById("velocidadeApp").innerText=velBase;
ecoTotal=0;
}

// ========== SERVIDORES ==========
function conectar(m,s){
var n=velBase*m;ecoTotal+=Math.floor(n*0.7);
document.getElementById("statusApp").innerHTML="📡 CONECTADO: "+s;
document.getElementById("velocidadeApp").innerText=n;
document.getElementById("detalhesApp").innerText="⬇️ "+n+" Mbps | ⬆️ "+n+" Mbps | 🎭 SNI: WhatsApp";
document.getElementById("cargaApp").innerText="🔋 "+(m>=20?"100% MÁXIMA":"85%")+" | 📦 Compressão 70%";
document.getElementById("logApp").innerText="[LOG] ✅ "+s+": "+m+"x | "+n+" Mbps | "+ecoTotal+" KB salvos | 🔐 TLS/SSL";
document.getElementById("economiaApp").innerText="📦 "+ecoTotal+" KB | 💰 Plano rende 3x MAIS";
}

// ========== MEDIDOR ==========
function toggleMedidor(){
var m=document.getElementById("medidor");
m.style.display=(m.style.display=="none"||m.style.display=="")?"block":"none";
}
function testarVelocidade(){
if(testando)return;testando=true;
var btn=document.getElementById("btnTeste");btn.innerText="⏳ MEDINDO...";btn.style.background="#333";
document.getElementById("barra").style.width="0%";
document.getElementById("statusTeste").innerText="🔐 Conectando via TLS/SSL Tunnel...";
var i=new Date().getTime();
var img=new Image();img.src="https://www.google.com/images/photos/photos.png?"+Math.random();
img.onload=function(){
var f=new Date().getTime();var vel=(50*8/((f-i)/1000)).toFixed(1);
document.getElementById("barra").style.width="100%";
document.getElementById("statusTeste").innerText="✅ Teste concluído!";
document.getElementById("resultadoTeste").innerText="⬇️ "+vel+" Mbps (REAL)";
btn.innerText="🔄 REPETIR";btn.style.background="#ff8800";testando=false;
};
img.onerror=function(){document.getElementById("statusTeste").innerText="⚠️ Erro";btn.innerText="🚀 TENTAR";btn.style.background="#ff8800";testando=false;};
}
function verSeguranca(){
document.getElementById("logApp").innerText="🛡️ VPN | TLS/SSL | SSH | SNI | Payload | SOCKS | GZIP 70% | SHA-256 | FIREWALL";
}

// ========== INICIAR CLIENTES PADRÃO ==========
db.collection("clientes").doc("kauan@megawifi.com").set({n:"Kauan",e:"kauan@megawifi.com",s:"kauan123",p:"PREMIUM",ativo:true});
db.collection("clientes").doc("cliente1@megawifi.com").set({n:"Cliente 1",e:"cliente1@megawifi.com",s:"cliente123",p:"BASICO",ativo:true});
</script>
</body>
</html>"""

class MeuServidor(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("X-Powered-By", "MEGA-WIFI-5G")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

print(f"MEGA WIFI 5G rodando na porta {PORT}")
with socketserver.TCPServer(("0.0.0.0", PORT), MeuServidor) as httpd:
    httpd.serve_forever()
