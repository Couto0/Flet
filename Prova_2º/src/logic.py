# logic.py

def validar_peso(peso_str: str):
    """Valida o campo de peso e retorna o valor float ou uma mensagem de erro."""
    if not peso_str.strip():
        return None, "Por favor, preencha o peso com um número válido."

    try:
        peso = float(peso_str)
    except:
        return None, "O peso deve ser um número."

    if peso <= 0:
        return None, "O peso deve ser maior que zero."

    return peso, None


def calcular_consumo(peso: float, multiplicador: float) -> float:
    """Calcula o consumo ideal de água baseado na fórmula."""
    base = peso * 35
    total = base * multiplicador
    return total
