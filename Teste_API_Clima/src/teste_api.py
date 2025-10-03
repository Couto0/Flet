import requests

def busca_clima(cidade):
    API_KEY = "6cef74c4347b6e6022d27957f34c91fb"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={API_KEY}&units=metric&lang=pt_br"
    
    response = requests.get(url)
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
