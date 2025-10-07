import math


def calculate_compound_interest(initial_value, monthly_deposit, annual_interest_rate, years):
    """
    Calcula juros compostos com aportes mensais
    """
    try:
        # Converter taxa anual para mensal
        monthly_rate = (1 + annual_interest_rate / 100) ** (1/12) - 1
        
        # Calcular evolução do investimento
        months = years * 12
        current_amount = initial_value
        data_points = []
        monthly_evolution = []
        
        total_invested = initial_value
        
        for month in range(months + 1):
            if month > 0:
                # Adicionar juros
                current_amount *= (1 + monthly_rate)
                # Adicionar aporte mensal
                current_amount += monthly_deposit
                total_invested += monthly_deposit
            
            # Adicionar ponto para o gráfico
            data_points.append((month, current_amount))
            monthly_evolution.append({
                'month': month,
                'amount': current_amount,
                'total_invested': total_invested if month > 0 else initial_value
            })
        
        final_amount = current_amount
        interest_earned = final_amount - total_invested
        
        return {
            'final_amount': final_amount,
            'total_invested': total_invested,
            'interest_earned': interest_earned,
            'monthly_evolution': monthly_evolution,
            'data_points': data_points,
            'months': months
        }
    except Exception as e:
        return {
            'final_amount': 0,
            'total_invested': 0,
            'interest_earned': 0,
            'monthly_evolution': [],
            'data_points': [],
            'months': 0,
            'error': str(e)
        }


def validate_investment_inputs(initial_value, monthly_deposit, interest_rate, time_period):
    """
    Valida os inputs da calculadora de investimentos
    """
    try:
        initial = float(initial_value or 0)
        monthly = float(monthly_deposit or 0)
        rate = float(interest_rate or 0)
        years = int(time_period or 0)
        
        if initial < 0 or monthly < 0 or rate < 0 or years <= 0:
            return False, "Todos os valores devem ser positivos"
        
        if years > 100:
            return False, "Período máximo é de 100 anos"
            
        return True, ""
        
    except ValueError:
        return False, "Por favor, insira valores numéricos válidos"