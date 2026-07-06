import http.server
import socketserver
import os

PORT = int(os.environ.get("PORT", 8080))

HTML = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TESTE MEGA WIFI</title>
<style>
body{background:#0a0a1a;color:#fff;font-family:Arial;text-align:center;padding:20px;}
button{display:block;width:100%;padding:15px;margin:10px 0;font-size:18px;background:#ff8800;color:#fff;border:none;border-radius:8px;cursor:pointer;}
input{display:block;width:100%;padding:15px;margin:10px 0;font-size:16px;background:#111;color:#fff;border:1px solid #ff8800;border-radius:8px;}
h1{color:#ff8800;}
.erro{color:red;}
.sucesso{color:green;}
</style>
</head>
<body>

<h1>⚡ TESTE MEGA WIFI</h1>

<div id="tela1">
<p>Clique nos botões para testar:</p>
<button onclick="irTela2()">🕵️ IR PARA ADMIN</button>
<button onclick="mostrarAlerta()">📢 MOSTRAR ALERTA</button>
<p id="resultado" style="margin-top:20px;"></p>
</div>

<div id="tela2" style="display:none;">
<h2>🕵️ TELA ADMIN</h2>
<p>Se você está vendo isso, o botão FUNCIONOU!</p>
<button onclick="irTela1()">⬅ VOLTAR</button>
</div>

<script>
function irTela2(){
document.getElementById("tela1").style.display="none";
document.getElementById("tela2").style.display="block";
document.getElementById("resultado").innerText="✅ Botão funcionou!";
}

function irTela1(){
document.getElementById("tela2").style.display="none";
document.getElementById("tela1").style.display="block";
}

function mostrarAlerta(){
alert("✅ BOTÃO FUNCIONANDO!");
document.getElementById("resultado").innerText="✅ Alerta mostrado!";
}
</script>
</body>
</html>"""

class MeuServidor(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

print(f"TESTE rodando na porta {PORT}")
with socketserver.TCPServer(("0.0.0.0", PORT), MeuServidor) as httpd:
    httpd.serve_forever()
