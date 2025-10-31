# cálculo da Taxa Metabólica Basal
def tmb_homem(peso: float, altura: float, idade: int):
    #Homens

    return 88.362 + (13.397 * peso) + (4.799 * altura) - (5.677 * idade)


def tmb_mulher(peso: float, altura: float, idade: int):
    #Mulhesres
    
    return 447.593 + (9.247 * peso) + (3.098 * altura) - (4.330 * idade)
