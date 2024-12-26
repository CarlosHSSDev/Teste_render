from flask import Flask, jsonify
import threading
import requests
import datetime

app = Flask(__name__)

# Lista para armazenar informações das requisições
lista_requisicoes = []

# Função para realizar requisições periódicas
def fazer_requisicao():
    while True:
        try:
            response = requests.get("https://plantoesuau.onrender.com/")
            status_code = response.status_code
        except Exception as e:
            status_code = f"Erro: {str(e)}"

        # Adicionar informações da requisição à lista
        lista_requisicoes.append({
            "data_hora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": status_code
        })

        # Dormir por 5 segundos antes da próxima requisição
        threading.Event().wait(5)

# Rota para exibir a última requisição
@app.route("/", methods=["GET"])
def ultima_requisicao():
    if lista_requisicoes:
        return jsonify(lista_requisicoes[-1])
    else:
        return jsonify({"message": "Nenhuma requisição realizada ainda."})

# Iniciar o thread da função de requisição periódica
thread = threading.Thread(target=fazer_requisicao, daemon=True)
thread.start()

if __name__ == "__main__":
    app.run(debug=True)
