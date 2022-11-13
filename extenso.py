from num2words import num2words
from decimal import Decimal
import streamlit as st

def numero_por_extenso(numero):
    if numero < 1:
        if 0 < numero%1 < 0.0199:
            valor_extenso = ('Um centavo.')
            return valor_extenso
        else:
            valor_decimal = round(numero * 100,2)
            num_ptbr = num2words(Decimal(valor_decimal), lang='pt_BR')
            valor_extenso = (num_ptbr + ' centavos.').capitalize()
            return valor_extenso

    elif numero == 1:
        valor_extenso = 'Um real.'
        return valor_extenso

    elif (numero > 1.00) and (numero < 1.011):
        valor_extenso = 'Um real e um centavo.'
        return valor_extenso

    elif (numero > 1.011) and (numero < 2):
        valor_x_100 = round(numero * 100,2)
        valor_decimal = round(valor_x_100 % 100,2)
        num_ptbr = num2words(Decimal(valor_decimal), lang='pt_BR')
        valor_extenso = ('Um real e ' + num_ptbr + ' centavos.')
        return valor_extenso

    elif (numero < 1000000) or (numero >= 1000002):
        if numero%1 == 0:
            num_ptbr = num2words(Decimal(numero), lang='pt_BR')
            valor_extenso = (num_ptbr + ' reais.').capitalize()
            return (valor_extenso).replace("Mil,","Mil")

        elif (numero%1 > 0) and (numero%1 < 0.02):
            num_ptbr = num2words(Decimal(numero // 1), lang='pt_BR')
            valor_extenso = (num_ptbr + ' reais e um centavo.').capitalize()
            return (valor_extenso).replace("Mil,","Mil")

        else:

            num_int_extenso = num2words(Decimal(numero // 1), lang='pt_BR')
            num = round((numero % 1*100),2)
            num_dec_extenso = num2words(Decimal(num), lang='pt_BR')
            valor_extenso = ((num_int_extenso + ' reais e ' + num_dec_extenso + ' centavos.')\
                .replace('zero vírgula','').replace('  ', ' ').capitalize())
            return valor_extenso.replace("Mil,","Mil")

    elif (1000000 <= numero < 1000001):
        if numero == 1000000:
            return 'Um milhão de reais.'
        elif 1000000 < numero < 1000000.02:
            return 'Um milhão de reais e um centavo.'
        else:
            num = round((numero % 1 * 100), 2)
            num_dec_extenso = num2words(Decimal(num), lang='pt_BR')
            valor_extenso = 'Um milhão de reais e ' + num_dec_extenso + ' centavos.'
            return valor_extenso

    elif (1000001 <= numero < 1000002):
        if numero == 1000001.00:
            return 'Um milhão e um reais.'
        elif (1000001.00 < numero < 1000001.02):
            return 'Um milhão e um reais e um centavo.'
        else:
            num = round((numero % 1 * 100), 2)
            num_dec_extenso = num2words(Decimal(num), lang='pt_BR')
            valor_extenso = 'Um milhão e um reais e ' + num_dec_extenso + ' centavos.'
            return valor_extenso

print(numero_por_extenso(10.15))