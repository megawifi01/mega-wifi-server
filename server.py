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
.status{background:#111133;padding:12px;border-radius:10px;margin:10px 0;border:2px solid #00ff88;}
.status h2{color:#00ff88;font-size:1em;}
.vel{font-size:2em;font-weight:bold;color:#ff8800;margin:8px 0;}
.log{background:#111133;padding:8px;border-radius:8px;margin-top:10px;font-size:.75em;color:#00ff88;}
.erro{color:#ff4444;font-size:.85em;}
.sucesso{color:#00ff88;font-size:.85em;}
.lista{background:#111133;padding:10px;border-radius:8px;margin:8px 0;font-size:.8em;text-align:left;color:#ccc;max-height:150px;overflow-y:auto;}
</style>
</head>
<body>

<div id="login">
<h1>⚡ MEGA WIFI</h1>
<p class="sub">5G ULTRA | NUVEM 24H</p>
<input type="email" id="email" placeholder="📧 Email">
<input type="password" id="senha" placeholder="🔑 Senha">
<p class="erro" id="msg"></p>
<button class="btn-l" onclick="logar()">⚡ ENTRAR</button>
<button class="btn-c" onclick="mostrarAdminLogin()">🕵️ ADMIN</button>
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
<p class="sub" style="color:#00ff88;">Adicione e visualize seus clientes</p>
<div class="lista" id="listaClientes">Carregando...</div>
<h2>➕ ADICIONAR NOVO CLIENTE</h2>
<input type="text" id="novoNome" placeholder="👤 Nome do cliente">
<input type="email" id="novoEmail" placeholder="📧 Email do cliente">
<input type="password" id="novaSenha" placeholder="🔑 Senha para o cliente">
<select id="novoPlano">
<option value="BASICO">💰 BASICO - R$ 15/mes</option>
<option value="PREMIUM">👑 PREMIUM - R$ 30/mes</option>
</select>
<p class="sucesso" id="msgAdd"></p>
<p class="erro" id="msgErroAdd"></p>
<button class="btn-v" onclick="adicionarCliente()">✅ ADICIONAR CLIENTE</button>
<button class="btn-l" onclick="irParaAppAdmin()">📱 ABRIR MEGA WIFI 5G</button>
<button class="btn-c" onclick="voltarLogin()">⬅ SAIR</button>
</div>

<div id="app" style="display:none;">
<h1>⚡ MEGA WIFI 5G</h1>
<p class="sub" id="ui" style="color:#00ff88;"></p>
<div class="status">
<h2 id="st">🔒 PRONTO</h2>
<p id="pg">📡 5G | Sinal: 5 BARRAS</p>
<p id="cg">🔋 Carga: 100%</p>
</div>
<div class="vel"><span id="vl">300</span> Mbps</div>
<p style="color:#aaa;">⬇️ DOWN = ⬆️ UP</p>
<button class="btn-v" onclick="c(20,'BRASIL')">🇧🇷 SERVIDOR PRIVADO BRASIL | 20x</button>
<button class="btn-a" onclick="c(10,'EUA')">🇺🇸 EUA | 10x</button>
<button class="btn-vm" onclick="c(12,'JAPAO')">🇯🇵 JAPAO | 12x</button>
<button class="btn-r" onclick="c(18,'SATELITE')">🛰️ SATELITE | 18x</button>
<button class="btn-l" onclick="c(25,'5G MAX')" style="font-size:1.1em;">🚀 5G MAX | 25x</button>
<div class="log" id="lg">[LOG] Online 24h.</div>
<div style="display:flex;gap:5px;margin-top:8px;">
<button class="btn-c" onclick="p()" style="flex:1;">📊</button>
<button class="btn-c" onclick="seg()" style="flex:1;">🛡️</button>
<button class="btn-c" onclick="s()" style="flex:1;">🚪</button>
</div>
<p style="color:#aaa;font-size:.7em;margin-top:15px;">☁️ NUVEM 24H</p>
</div>

<script>
var cl = {
"kauan@megawifi.com":{s:"kauan123",n:"Kauan",p:"PREMIUM",ativo:true},
"cliente1@megawifi.com":{s:"cliente123",n:"Cliente 1",p:"BASICO",ativo:true}
};
var ADMIN = "kauanadmin123";
var v = Math.floor(Math.random()*200)+200;
var d = 0;

function atualizarLista(){
var lista = document.getElementById("listaClientes");
var txt = "📋 CLIENTES:\\n\\n";
for(var e in cl){
var status = cl[e].ativo ? "✅ ATIVO" : "❌ INATIVO";
txt += status + " - " + cl[e].n + "\\n   📧 " + e + "\\n   💰 " + cl[e].p + "\\n   🔑 " + cl[e].s + "\\n\\n";
}
lista.innerText = txt;
}

function adicionarCliente(){
var nome = document.getElementById("novoNome").value.trim();
var email = document.getElementById("novoEmail").value.trim();
var senha = document.getElementById("novaSenha").value.trim();
var plano = document.getElementById("novoPlano").value;

document.getElementById("msgAdd").innerText = "";
document.getElementById("msgErroAdd").innerText = "";

if(!nome || !email || !senha){
document.getElementById("msgErroAdd").innerText = "❌ Preencha todos os campos!";
return;
}

if(cl[email]){
document.getElementById("msgErroAdd").innerText = "❌ Email ja cadastrado!";
return;
}

cl[email] = {s:senha, n:nome, p:plano, ativo:true};
document.getElementById("msgAdd").innerText = "✅ " + nome + " adicionado! Senha: " + senha;
document.getElementById("novoNome").value = "";
document.getElementById("novoEmail").value = "";
document.getElementById("novaSenha").value = "";
atualizarLista();
}

function mostrarAdminLogin(){
document.getElementById("login").style.display = "none";
document.getElementById("adminLogin").style.display = "block";
}

function voltarLogin(){
document.getElementById("login").style.display = "block";
document.getElementById("adminLogin").style.display = "none";
document.getElementById("painelAdmin").style.display = "none";
}

function entrarAdmin(){
if(document.getElementById("sa").value == ADMIN){
document.getElementById("adminLogin").style.display = "none";
document.getElementById("painelAdmin").style.display = "block";
atualizarLista();
}else{
document.getElementById("ma").innerText = "❌ Senha master incorreta!";
}
}

function irParaAppAdmin(){
document.getElementById("painelAdmin").style.display = "none";
document.getElementById("app").style.display = "block";
document.getElementById("ui").innerText = "🕵️ ADMIN: Kauan";
}

function logar(){
var e = document.getElementById("email").value.trim();
var s = document.getElementById("senha").value.trim();
if(cl[e] && cl[e].s == s && cl[e].ativo){
document.getElementById("login").style.display = "none";
document.getElementById("app").style.display = "block";
document.getElementById("ui").innerText = "👤 " + cl[e].n + " | 💰 " + cl[e].p;
d = 0;
document.getElementById("vl").innerText = v;
document.getElementById("msg").innerText = "";
}else{
document.getElementById("msg").innerText = "❌ Email ou senha incorretos!";
}
}

function c(m,s){
var n = v*m;
d += Math.floor(Math.random()*200)+100;
document.getElementById("st").innerHTML = "📡 CONECTADO: " + s;
document.getElementById("vl").innerText = n;
document.getElementById("pg").innerText = "⬇️ " + n + " | ⬆️ " + n + " | Ping: " + (m>=20?"1ms":"5ms");
document.getElementById("cg").innerText = "🔋 " + (m>=20?"100%":"85%") + " | ☁️";
document.getElementById("lg").innerText = "[LOG] " + s + ": " + m + "x | " + n + " Mbps | " + d + " KB";
}

function p(){document.getElementById("lg").innerText = "📊 " + v + " Mbps | " + d + " KB | ☁️ 24H";}
function seg(){document.getElementById("lg").innerText = "🛡️ SHA-256 | Firewall ON";}
function s(){document.getElementById("app").style.display = "none";document.getElementById("login").style.display = "block";}
</script>
</body>
</html>"""

class MeuServidor(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

print(f"MEGA WIFI rodando na porta {PORT}")
with socketserver.TCPServer(("0.0.0.0", PORT), MeuServidor) as httpd:
    httpd.serve_forever()
