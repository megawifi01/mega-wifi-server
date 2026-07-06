    httpd.serve_forever()
from http.server import HTTPServer, BaseHTTPRequestHandler
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
.sub{font-size:.8em;color:#ff8800;margin-bottom:10px;}
input{display:block;width:100%;padding:12px;margin:6px 0;border:none;border-radius:8px;font-size:1em;background:#111133;color:#fff;border:1px solid #ff8800;}
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
</style>
</head>
<body>
<div id="login">
<h1>⚡ MEGA WIFI</h1>
<p class="sub">5G ULTRA | NUVEM 24H</p>
<input type="email" id="email" placeholder="Email">
<input type="password" id="senha" placeholder="Senha">
<p class="erro" id="msg"></p>
<button class="btn-l" onclick="logar()">⚡ ENTRAR</button>
<button class="btn-c" onclick="admin()">🕵️ ADMIN</button>
</div>
<div id="ad" style="display:none;">
<h1>🕵️ ADMIN</h1>
<input type="password" id="sa" placeholder="Senha Master">
<p class="erro" id="ma"></p>
<button class="btn-l" onclick="va()">🔐 ACESSAR</button>
<button class="btn-c" onclick="vl()">⬅ VOLTAR</button>
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
var cl={"kauan@megawifi.com":{s:"kauan123",n:"Kauan",p:"PREMIUM"},"cliente1@megawifi.com":{s:"cliente123",n:"Cliente 1",p:"BASICO"}};
var AD="kauanadmin123";
var v=Math.floor(Math.random()*200)+200;
var d=0;
function logar(){
var e=document.getElementById("email").value.trim().toLowerCase();
var s=document.getElementById("senha").value.trim();
if(cl[e]&&cl[e].s==s){document.getElementById("login").style.display="none";document.getElementById("app").style.display="block";document.getElementById("ui").innerText="👤 "+cl[e].n+" | "+cl[e].p;d=0;document.getElementById("vl").innerText=v;}
else{document.getElementById("msg").innerText="❌ Email ou senha incorretos!";}
}
function admin(){document.getElementById("login").style.display="none";document.getElementById("ad").style.display="block";}
function vl(){document.getElementById("ad").style.display="none";document.getElementById("login").style.display="block";}
function va(){if(document.getElementById("sa").value==AD){document.getElementById("ad").style.display="none";document.getElementById("app").style.display="block";document.getElementById("ui").innerText="🕵️ ADMIN";}else{document.getElementById("ma").innerText="❌ Senha incorreta!";}}
function c(m,s){var n=v*m;d+=Math.floor(Math.random()*200)+100;document.getElementById("st").innerHTML="📡 CONECTADO: "+s;document.getElementById("vl").innerText=n;document.getElementById("pg").innerText="⬇️ "+n+" | ⬆️ "+n+" | Ping: "+(m>=20?"1ms":"5ms");document.getElementById("cg").innerText="🔋 "+(m>=20?"100%":"85%")+" | ☁️";document.getElementById("lg").innerText="[LOG] "+s+": "+m+"x | "+n+" Mbps | "+d+" KB";}
function p(){document.getElementById("lg").innerText="📊 "+v+" Mbps | "+d+" KB | ☁️ 24H";}
function seg(){document.getElementById("lg").innerText="🛡️ SHA-256 | Firewall ON";}
function s(){document.getElementById("app").style.display="none";document.getElementById("login").style.display="block";}
</script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

print(f"MEGA WIFI 5G rodando na porta {PORT}")
HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
