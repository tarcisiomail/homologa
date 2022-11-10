import streamlit as st
from decimal import Decimal
import num2words
from extenso import numero_por_extenso

valor = st.number_input(label = "shit")
nome = st.text_input(label = 'merde')

st.write(numero_por_extenso(valor))