import locale
import random

locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
from datetime import datetime
from docxtpl import DocxTemplate
import streamlit as st
from extenso import numero_por_extenso
import os
from docx import Document
import pandas as pd
keys=0
random.seed()
import time
import streamlit.components.v1 as components

if "new_row" not in st.session_state:
    st.session_state.new_row = pd.DataFrame(columns=['Item ID', 'Item Descricao', 'Item Quantidade',
                                                     'Item Unidade','Valor do Item', 'Valor por extenso'])

doc = DocxTemplate("MATRIZ.docx")

col1, col2 = st.columns(2)
with col1:
    processo = st.text_input(label = 'Número do Processo:', key=1)
    interessado = st.text_input(label = 'Setor interessado:', key=2)
    fls_solicitacao = st.text_input(label = 'Folhas da solicitação no processo:', key=3)
    descricao = st.text_input(label = 'Descrição da Solicitação:', key=4)
    mod_num_licitacao = st.text_input(label = 'Modo e número da Licitação:', key=5)
    fls_ata = st.text_input(label = 'Folhas da ata no processo:', key=6)
    fls_pregoeiro = st.text_input(label = 'Folhas da indicação do pregoeiro no processo:', key=7)
    id_itens_lote = st.text_input(label = 'Identificação dos lotes:', key=8)

with col2:
    data_adjudicacao = datetime.today().strftime("%d de %B de %Y")
    ganhadora = st.text_input(label = 'Nome da empresa ganhadora:', key=10)
    valor_lance = st.number_input(label = 'Valor do lance ganhador:', key=11)
    fls_especificacoes = st.text_input(label = 'Folhas contendo as especificações no processo:', key=12)
    id_compra = st.text_input(label = 'Identificação da compra:', key=13)
    pregoeiro = st.text_input(label = 'Nome do Pregoeiro:', key=14)
    cnpj_ganhadora = st.text_input(label = 'CNPJ da empresa ganhadora:', key=15)

lote1 = ('1 item\n2 itens\n3 itens.')
mydict ={}
print(mydict)
inicial = [['teste1', 'teste2', 2, 'Dois reais.']]
df = pd.DataFrame(inicial, columns=['Item ID', 'Item Descricao', 'Valor do Item', 'Valor por extenso'])
df.loc[len(df)] = ['teste2', 'teste3', 4, 'Quatro reais.']
lote_button = st.button("manda")
st.session_state['dataframe']=keys
st.dataframe(df)

def funcao(a,b,c,d):
    df.loc[len(df)] = [a, b, c, d]

with st.form(key="1"):
    item_id = st.text_input("Identificação do item:")
    item_descricao = st.text_input("Descrição do Item")
    item_quantidade = st.number_input("Quantidade:")
    item_unidade = st.text_input("Unidade:")
    item_value = st.number_input("Valor do Item:")
    item_full_value = numero_por_extenso(item_value)
    btn_form = st.form_submit_button('Manda de novo')
    df_new = pd.DataFrame({'Item ID': item_id,
                           'Item Descricao': item_descricao,
                           'Item Quantidade': item_quantidade,
                           'Item Unidade': item_unidade,
                           'Valor do Item': item_value,
                           'Valor por extenso': item_full_value}, index=[len(st.session_state.new_row)])


    if btn_form:


        st.session_state.new_row = pd.concat([st.session_state.new_row, df_new], axis=0)
        df_new.drop(df_new.tail(1).index, inplace=True)
        df_new = pd.concat([st.session_state.new_row, df_new], axis=0)

        st.dataframe(df_new)

def item_description (item_id, item_descricao, item_quantidade, item_unidade, item_value, item_full_value):
    valor_total = item_quantidade * item_value
    valor_total_full = numero_por_extenso(valor_total)
    return str(f"{item_id} - {item_descricao}\nQUANTIDADE: {('%.0f' % item_quantidade)} ({item_unidade})\n"
                f"VALOR UNITÁRIO: R${('%.2f' % item_value).replace('.',',')}\nVALOR TOTAL DO {item_id} ............... R$"
                f"{('%.2f' % valor_total).replace('.',',')} ({(valor_total_full).replace('.','')}).\n")



finaliza = st.button("Acabou?")
if finaliza:
    df_new = pd.concat([st.session_state.new_row, df_new], axis=0)
    df_new.drop(df_new.tail(1).index, inplace=True)
    st.dataframe(df_new)
    #st.write(df_new.loc[len(df_new)-1,'Valor do Item'])
    #st.dataframe(df_new.loc['2'].at['Valor do Item'])
    list = {}
    for i in range(len(df_new)):
        list['lote{0}'.format(i)] = (item_description(df_new.loc[i, 'Item ID'], df_new.loc[i, 'Item Descricao'],
                                         df_new.loc[i, 'Item Quantidade'], df_new.loc[i, 'Item Unidade'],
                                         df_new.loc[i, 'Valor do Item'], df_new.loc[i, 'Valor por extenso']))

    context = {'processo': processo, 'interessado': interessado, 'fls_solicitacao': fls_solicitacao,
               'descricao': descricao,
               'mod_num_licitacao': mod_num_licitacao, 'fls_ata': fls_ata, 'fls_pregoeiro': fls_pregoeiro,
               'id_itens_lote': id_itens_lote, 'ganhadora': ganhadora, 'valor_lance': valor_lance,
               'fls_especificacoes': fls_especificacoes, 'id_compra': id_compra, 'pregoeiro': pregoeiro,
               'cnpj_ganhadora': cnpj_ganhadora, 'data_adjudicacao': data_adjudicacao}

    context.update(list)

    df = pd.DataFrame.from_dict([context])
    st.dataframe(df)
    print(type(context))
    doc.render(context)
    doc.save("generated_doc_2.docx")



with open("generated_doc_2.docx", "rb") as myfile:
    btn = st.download_button(
        label="Download do documento",
        data = myfile,
        file_name = 'new_file.docx',
        mime = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )