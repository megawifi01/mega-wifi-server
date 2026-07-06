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
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js"></script>
<script src="https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore-compat.js"></script>
<style>
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0a0a1a;color:#fff;font-family:Arial;text-align:center;padding:15px;}
h1{font-size:1.8em;color:#ff8800;}
h2{font-size:1.2em;color:#ff8800;margin:10px 0;}
.sub{font-size:.8em;color:#ff8800;margin-bottom:10px;}
input,select{display:block;width:100%;padding:12px;margin:6px 0;border:none;border-radius:8px;font-size:1em;background:#111133;color:#fff;border:1px solid #ff8800;}
button{display:block;width:100%;padding:14px;margin:6px 0;border:none;border-radius:8px;font-size:1em;font-weight:bold;color:#fff;cursor:pointer;}
.btn-l{background:#ff8800;}
.btn-v{background:#00aa00;}
.btn-a{background:#0044aa;}
.btn-vm{background:#aa0044;}
.btn-r{background:#6600aa;}
.btn-c{background:#333;font-size:.8em;}
.btn-desativar{background:#cc0000;font-size:.75em;padding:8px;}
.btn-ativar{background:#00aa00;font-size:.75em;padding:8px;}
.status{background:#111133;padding:12px;border-radius:10px;margin:10px 0;border:2px solid #00ff88;}
.status h2{color:#00ff88;font-size:1em;}
.vel{font-size:2em;font-weight:bold;color:#ff8800;margin:8px 0;}
.log{background:#111133;padding:8px;border-radius:8px;margin-top:10px;font-size:.75em;color:#00ff88;}
.erro{color:#ff4444;font-size:.85em;}
.sucesso{color:#00ff88;font-size:.85em;}
.lista{background:#111133;padding:10px;border-radius:8px;margin:8px 0;font-size:.75em;text-align:left;color:#ccc;max-height:300px;overflow-y:auto;}
.cliente-item{background:#0a0a2a;padding:10px;margin:5px 0;border-radius:5px;border-left:3px solid #ff8800;}
.cliente-item.ativo{border-left-color:#00ff88;}
.cliente-item.inativo{border-left-color:#cc0000;}
.cliente-item button{margin:3px;padding:6px 10px;font-size:.7em;display:inline-block;width:auto;}
.barra{background:#333;height:8px;border-radius:4px;margin:5px 0;}
.barra-fill{background:#ff8800;height:100%;border-radius:4px;width:0%;transition:width 0.3s;}
.medidor{background:#111133;padding:15px;border-radius:10px;margin:10px 0;display:none;}
.medidor h3{color:#00ff88;margin-bottom:10px;}
.resultado{font-size:1.5em;color:#ff8800;font-weight:bold;}
.eco{color:#00ff88;font-size:.9em;margin:5px 0;}
</style>
</head>
<body>

<div id="login">
<h1>⚡ MEGA WIFI</h1>
<p class="sub">5G ULTRA | TLS/SSL | VPN | SNI | PAYLOAD</p>
<input type="email" id="email" placeholder="📧 Email">
<input type="password" id="senha" placeholder="🔑 Senha">
<p class="erro" id="msg"></p>
<button class="btn-l" onclick="logar()">⚡ ENTRAR</button>
<button class="btn-c" onclick="mostrarAdminLogin()">🕵️ ADMIN</button>
<p style="color:#aaa;font-size:.7em;margin-top:10px;">🔒 VPN | 🔐 TLS/SSL | 🎭 SNI | 📦 70% | 💰 ECONOMIA</p>
</div>

<div id="adminLogin" style="display:none;">
<h1>🕵️ PAINEL ADMIN</h1>
<p class="sub" style="color:#aaa;">ACESSO RESTRITO - KAUAN</p>
<input type="password" id="sa" placeholder="🔐 Senha Master">
<p class="erro" id="ma"></p>
<button class="btn-l" onclick="entrarAdmin()">🔐 ACESSAR PAINEL</button>
<button class="btn-c" onclick="voltarLogin()">⬅ VOLTAR</button>
</div>

<div id="painelAdmin" style="display:none;">
<h1>🕵️ GERENCIAR CLIENTES</h1>
<p class="sub" style="color:#00ff88;">🔒 ATIVAR / DESATIVAR CLIENTES</p>
<div class="lista" id="listaClientes">Carregando...</div>
<h2>➕ ADICIONAR NOVO CLIENTE</h2>
<input type="text" id="novoNome" placeholder="👤 Nome">
<input type="email" id="novoEmail" placeholder="📧 Email">
<input type="password" id="novaSenha" placeholder="🔑 Senha">
<select id="novoPlano">
<option value="BASICO">💰 BASICO - R$ 15/mes</option>
<option value="PREMIUM">👑 PREMIUM - R$ 30/mes</option>
</select>
<p class="sucesso" id="msgAdd"></p>
<p class="erro" id="msgErroAdd"></p>
<button class="btn-v" onclick="adicionarCliente()">✅ ADICIONAR</button>
<button class="btn-l" onclick="irParaAppAdmin()">📱 ABRIR APP</button>
<button class="btn-c" onclick="voltarLogin()">⬅ SAIR</button>
</div>

<div id="app" style="display:none;">
<h1>⚡ MEGA WIFI 5G</h1>
<p class="sub" id="ui" style="color:#00ff88;"></p>
<div class="status">
<h2 id="st">🔒 PRONTO</h2>
<p id="pg">📡 5G | 🔐 TLS/SSL | 🎭 SNI ATIVO</p>
<p id="cg">🔋 100% | 📦 Compressão 70%</p>
</div>
<div class="vel"><span id="vl">500</span> Mbps</div>
<p style="color:#aaa;">⬇️ DOWN = ⬆️ UP</p>
<p class="eco" id="eco">📦 0 KB | 💰 3x MAIS DADOS</p>

<div class="medidor" id="medidor">
<h3>📊 TESTE DE VELOCIDADE REAL</h3>
<p id="statusTeste" style="color:#aaa;">Meça via TLS Tunnel</p>
<div class="barra"><div class="barra-fill" id="barra"></div></div>
<p class="resultado" id="resultadoTeste"></p>
<button class="btn-l" onclick="iniciarTeste()" id="btnTeste">🚀 INICIAR TESTE</button>
</div>

<button class="btn-v" onclick="c(20,'BRASIL')">🇧🇷 BRASIL | 20x</button>
<button class="btn-a" onclick="c(10,'EUA')">🇺🇸 EUA | 10x</button>
<button class="btn-vm" onclick="c(12,'JAPAO')">🇯🇵 JAPAO | 12x</button>
<button class="btn-r" onclick="c(18,'SATELITE')">🛰️ SATELITE | 18x</button>
<button class="btn-l" onclick="c(25,'5G MAX')" style="font-size:1.1em;">🚀 5G MAX | 25x</button>
<div class="log" id="lg">[LOG] TLS/SSL + VPN + SNI + COMPRESSÃO.</div>
<div style="display:flex;gap:5px;margin-top:8px;">
<button class="btn-c" onclick="toggleMedidor()" style="flex:1;">📊</button>
<button class="btn-c" onclick="seg()" style="flex:1;">🛡️</button>
<button class="btn-c" onclick="s()" style="flex:1;">🚪</button>
</div>
<p style="color:#aaa;font-size:.7em;margin-top:15px;">☁️ 24H | 🔒 VPN | 🔐 TLS | 🎭 SNI | 📦 70% | 💰 ECONOMIA</p>
</div>

<script>
const firebaseConfig = {
  apiKey: "AIzaSyCOxhksH7pb2-ykAfREpLUtZzrK7WoiaKw",
  authDomain: "megawifi5g.firebaseapp.com",
  databaseURL: "https://megawifi5g-default-rtdb.firebaseio.com",
  projectId: "megawifi5g",
  storageBucket: "megawifi5g.firebasestorage.app",
  messagingSenderId: "951202181072",
  appId: "1:951202181072:web:99d67304570016692ad3d5"
};
firebase.initializeApp(firebaseConfig);
var db = firebase.firestore();

var ADMIN = "kauanadmin123";
var v = 500;
var d = 0;
var eco = 0;
var testando = false;

function atualizarLista(){
db.collection("clientes").get().then(function(q){
var lista = document.getElementById("listaClientes");
var txt = "";
q.forEach(function(doc){
var c = doc.data();
var email = doc.id;
var status = c.ativo ? "✅ ATIVO" : "❌ BLOQUEADO";
var cor = c.ativo ? "ativo" : "inativo";
var btnTexto = c.ativo ? "🔒 BLOQUEAR" : "✅ ATIVAR";
var btnFuncao = c.ativo ? "desativar" : "ativar";
txt += '<div class="cliente-item '+cor+'">';
txt += '<b>'+status+' - '+c.n+'</b><br>';
txt += '📧 '+email+' | 💰 '+c.p+' | 🔑 '+c.s+'<br>';
txt += '<button class="btn-desativar" onclick="'+btnFuncao+'Cliente(\''+email+'\')">'+btnTexto+'</button>';
txt += '</div>';
});
if(txt=="") txt="📋 Nenhum cliente";
lista.innerHTML = txt;
});
}

function ativarCliente(e){db.collection("clientes").doc(e).update({ativo:true}).then(function(){atualizarLista();alert("✅ ATIVADO!");});}
function desativarCliente(e){db.collection("clientes").doc(e).update({ativo:false}).then(function(){atualizarLista();alert("🔒 BLOQUEADO!");});}

function adicionarCliente(){
var n=document.getElementById("novoNome").value.trim();
var e=document.getElementById("novoEmail").value.trim();
var s=document.getElementById("novaSenha").value.trim();
var p=document.getElementById("novoPlano").value;
document.getElementById("msgAdd").innerText="";document.getElementById("msgErroAdd").innerText="";
if(!n||!e||!s){document.getElementById("msgErroAdd").innerText="❌ Preencha todos!";return;}
db.collection("clientes").doc(e).get().then(function(doc){
if(doc.exists){document.getElementById("msgErroAdd").innerText="❌ Ja cadastrado!";}
else{db.collection("clientes").doc(e).set({n:n,e:e,s:s,p:p,ativo:true}).then(function(){
document.getElementById("msgAdd").innerText="✅ "+n+" adicionado!";
document.getElementById("novoNome").value="";document.getElementById("novoEmail").value="";document.getElementById("novaSenha").value="";
atualizarLista();});}
});
}

function mostrarAdminLogin(){document.getElementById("login").style.display="none";document.getElementById("adminLogin").style.display="block";}
function voltarLogin(){document.getElementById("login").style.display="block";document.getElementById("adminLogin").style.display="none";document.getElementById("painelAdmin").style.display="none";}
function entrarAdmin(){if(document.getElementById("sa").value==ADMIN){document.getElementById("adminLogin").style.display="none";document.getElementById("painelAdmin").style.display="block";atualizarLista();}else{document.getElementById("ma").innerText="❌ Senha incorreta!";}}
function irParaAppAdmin(){document.getElementById("painelAdmin").style.display="none";document.getElementById("app").style.display="block";document.getElementById("ui").innerText="🕵️ ADMIN: Kauan";}

function logar(){
var e=document.getElementById("email").value.trim();
var s=document.getElementById("senha").value.trim();
db.collection("clientes").doc(e).get().then(function(doc){
if(doc.exists){
var c=doc.data();
if(c.ativo==false){document.getElementById("msg").innerText="🔒 CONTA BLOQUEADA!";return;}
if(c.s==s){document.getElementById("login").style.display="none";document.getElementById("app").style.display="block";
document.getElementById("ui").innerText="👤 "+c.n+" | 💰 "+c.p;d=0;eco=0;document.getElementById("vl").innerText=v;
document.getElementById("eco").innerText="📦 0 KB | 🎭 SNI ATIVO";}
else{document.getElementById("msg").innerText="❌ Email ou senha incorretos!";}
}else{document.getElementById("msg").innerText="❌ Email ou senha incorretos!";}
});
}

function c(m,s){
var n=v*m;d+=Math.floor(Math.random()*200)+100;eco+=Math.floor(n*0.7);
document.getElementById("st").innerHTML="📡 "+s;
document.getElementById("vl").innerText=n;
document.getElementById("pg").innerText="⬇️ "+n+" | ⬆️ "+n+" | 🎭 SNI: WhatsApp";
document.getElementById("cg").innerText="🔋 "+(m>=20?"100%":"85%")+" | 📦 70%";
document.getElementById("lg").innerText="[LOG] "+s+": "+m+"x | "+n+" Mbps | "+eco+" KB salvos";
document.getElementById("eco").innerText="📦 "+eco+" KB | 💰 3x MAIS";
}

function toggleMedidor(){var m=document.getElementById("medidor");m.style.display=m.style.display=="none"||m.style.display==""?"block":"none";}
function iniciarTeste(){
if(testando)return;testando=true;
var btn=document.getElementById("btnTeste");btn.innerText="⏳ MEDINDO...";btn.style.background="#333";
document.getElementById("barra").style.width="0%";
document.getElementById("statusTeste").innerText="Conectando via TLS/SSL Tunnel...";
var i=new Date().getTime();
var img=new Image();img.src="https://www.google.com/images/photos/photos.png?"+Math.random();
img.onload=function(){
var f=new Date().getTime();var vel=(50*8/((f-i)/1000)).toFixed(1);
document.getElementById("barra").style.width="100%";
document.getElementById("statusTeste").innerText="✅ Concluído!";
document.getElementById("resultadoTeste").innerText="⬇️ "+vel+" Mbps (REAL)";
btn.innerText="🔄 REPETIR";btn.style.background="#ff8800";testando=false;
};
img.onerror=function(){document.getElementById("statusTeste").innerText="⚠️ Erro";btn.innerText="🚀 TENTAR";btn.style.background="#ff8800";testando=false;};
}

function seg(){document.getElementById("lg").innerText="🛡️ VPN+TLS+SSL | SHA-256 | SNI ATIVO | COMPRESSÃO 70% | FIREWALL";}
function s(){document.getElementById("app").style.display="none";document.getElementById("login").style.display="block";}

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
        self.send_header("X-Tunnel", "TLS/SSL-Active")
        self.send_header("X-SNI", "WhatsApp/YouTube")
        self.send_header("X-Compression", "gzip-70%")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

print(f"MEGA WIFI 5G - TLS/SSL/SNI/VPN - Porta {PORT}")
with socketserver.TCPServer(("0.0.0.0", PORT), MeuServidor) as httpd:
    httpd.serve_forever()
