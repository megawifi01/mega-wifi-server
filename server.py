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
<style>
body{background:#0a0a1a;color:#fff;font-family:Arial;text-align:center;padding:20px;}
h1{color:#ff8800;}
button{padding:15px;margin:10px;font-size:18px;background:#ff8800;color:#fff;border:none;border-radius:8px;width:90%;}
input{padding:12px;margin:8px;font-size:16px;background:#111;color:#fff;border:1px solid #ff8800;border-radius:8px;width:90%;}
.erro{color:red;}
.sucesso{color:green;}
.tela{display:none;}
</style>
</head>
<body>

<div id="t1">
<h1>⚡ MEGA WIFI</h1>
<input type="email" id="email" placeholder="Email">
<br>
<input type="password" id="senha" placeholder="Senha">
<br>
<p class="erro" id="msg"></p>
<button onclick="entrar()">⚡ ENTRAR</button>
<button onclick="document.getElementById('t1').style.display='none';document.getElementById('t2').style.display='block';">🕵️ ADMIN</button>
</div>

<div id="t2" class="tela">
<h1>🕵️ ADMIN</h1>
<input type="password" id="sa" placeholder="Senha Master">
<br>
<p class="erro" id="ma"></p>
<button onclick="admin()">🔐 ACESSAR</button>
<button onclick="document.getElementById('t2').style.display='none';document.getElementById('t1').style.display='block';">⬅ VOLTAR</button>
</div>

<div id="t3" class="tela">
<h1>⚡ MEGA WIFI 5G</h1>
<p class="sucesso" id="ui"></p>
<h2 id="vl" style="color:#ff8800;font-size:3em;">500 Mbps</h2>
<button onclick="c(20)">🇧🇷 BRASIL | 20x</button>
<button onclick="c(10)">🇺🇸 EUA | 10x</button>
<button onclick="c(25)">🚀 5G MAX | 25x</button>
<button onclick="document.getElementById('t3').style.display='none';document.getElementById('t1').style.display='block';">🚪 SAIR</button>
</div>

<script>
function entrar(){
var e=document.getElementById("email").value;
var s=document.getElementById("senha").value;
if(e=="kauan@megawifi.com" && s=="kauan123"){
document.getElementById("t1").style.display="none";
document.getElementById("t3").style.display="block";
document.getElementById("ui").innerText="👤 Kauan | PREMIUM";
}else if(e=="cliente1@megawifi.com" && s=="cliente123"){
document.getElementById("t1").style.display="none";
document.getElementById("t3").style.display="block";
document.getElementById("ui").innerText="👤 Cliente 1 | BASICO";
}else{
document.getElementById("msg").innerText="❌ Email ou senha incorretos!";
}
}

function admin(){
if(document.getElementById("sa").value=="kauanadmin123"){
document.getElementById("t2").style.display="none";
document.getElementById("t3").style.display="block";
document.getElementById("ui").innerText="🕵️ ADMIN: Kauan";
}else{
document.getElementById("ma").innerText="❌ Senha incorreta!";
}
}

function c(m){
var n=500*m;
document.getElementById("vl").innerText=n+" Mbps";
}
</script>
</body>
</html>"""

class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

print(f"OK {PORT}")
with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
    httpd.serve_forever()
