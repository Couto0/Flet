# teste_api.py
import requests

def busca_clima(cidade: str):
    API_KEY = "6cef74c4347b6e6022d27957f34c91fb"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            return {
                "cidade": cidade,
                "descricao": dados['weather'][0]['description'],
                "temperatura": dados['main']['temp'],
                "umidade": dados['main']['humidity'],
            }
        else:
            return None
    except Exception as e:
        print("Erro na requisição HTTP:", e)
        return None