import locale
import random
from money import Money
from datetime import datetime
from docxtpl import DocxTemplate
import streamlit as st
from extenso import numero_por_extenso
from month_translate import translate_month
import os
from docx import Document
import pandas as pd

keys = 0
random.seed()
import time
import streamlit.components.v1 as components

if "new_row" not in st.session_state:
    st.session_state.new_row = pd.DataFrame(columns=['Lote ID', 'Item ID', 'Item Descricao', 'Item Quantidade',
                                                     'Item Unidade', 'Valor do Item', 'Valor por extenso'])

doc = DocxTemplate("MATRIZ.docx")

col1, col2 = st.columns(2)
with col1:
    date_input = st.date_input("Data do documento:")
    data_documento = translate_month(date_input.strftime("%d de %B de %Y"))
    processo = st.text_input(label='Número do Processo:', key=1)
    interessado = st.text_input(label='Setor interessado:', key=2)
    fls_solicitacao = st.text_input(label='Folhas da solicitação no processo:', key=3)
    descricao = st.text_input(label='Descrição da Solicitação:', key=4)
    mod_num_licitacao = st.text_input(label='Modo e número da Licitação:', key=5)
    fls_ata = st.text_input(label='Folhas da ata no processo:', key=6)
    fls_pregoeiro = st.text_input(label='Folhas da indicação do pregoeiro no processo:', key=7)


with col2:
    id_itens_lote = st.text_input(label='Identificação dos lotes:', key=8)
    ganhadora = st.text_input(label='Nome da empresa ganhadora:', key=10)
    valor_lance = st.number_input(label='Valor do lance ganhador:', key=11)
    valor_lance1 = Money(amount=valor_lance, currency='BRL').format('pt_BR')
    fls_especificacoes = st.text_input(label='Folhas contendo as especificações no processo:', key=12)
    id_compra = st.text_input(label='Identificação da compra:', key=13)
    pregoeiro = st.text_input(label='Nome do Pregoeiro:', key=14)
    cnpj_ganhadora = st.text_input(label='CNPJ da empresa ganhadora:', key=15)
    data_adjudicacao = st.date_input("Data da Adjudicação:")

lote_button = st.button("manda")

if lote_button:
    data = translate_month(data_adjudicacao.strftime("%d de %B de %Y")) + "."
    st.write(data)


def funcao(a, b, c, d):
    df.loc[len(df)] = [a, b, c, d]

def item_description(item_id, item_descricao, item_quantidade, item_unidade, item_value):
    valor_total = Money(amount=item_quantidade * item_value, currency='BRL').format('pt_BR')
    valor_total_full = numero_por_extenso(item_quantidade * item_value)
    return str(f"\n{item_id} - {item_descricao}\nQUANTIDADE: {('%.0f' % item_quantidade)} ({item_unidade})\n"
               f"VALOR UNITÁRIO: {Money(amount=item_value, currency='BRL').format('pt_BR')}"
               f"\nVALOR TOTAL DO {item_id} ............... R$"
               f"{valor_total} ({(valor_total_full).replace('.', '')}).\n")

numero_lotes = st.slider("Número de Lotes:", min_value=1, max_value=10, value=1)
if numero_lotes == 1:
    with st.form(key="a"):
        lote_id = st.text_input("Identificação do lote")
        item_id = st.text_input("Identificação do Item:")
        item_descricao = st.text_input("Descrição do Item")
        item_quantidade = st.number_input("Quantidade:")
        item_unidade = st.text_input("Unidade:")
        item_value = st.number_input("Valor do Item:")
        item_full_value = numero_por_extenso(item_value)
        btn_form = st.form_submit_button('Manda de novo')
        df_new = pd.DataFrame({'Lote ID': lote_id,
                               'Item ID': item_id,
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

if numero_lotes > 1:
    lote_id = st.text_input("Identificação do Lote:")
    with st.form(key='1'):

        st.write(lote_id)
        item_id = st.text_input("Identificação do item:")
        item_descricao = st.text_input("Descrição do Item")
        item_quantidade = st.number_input("Quantidade:")
        item_unidade = st.text_input("Unidade:")
        item_value = st.number_input("Valor do Item:")
        item_full_value = numero_por_extenso(item_value)
        btn_form = st.form_submit_button('Manda de novo')
        df_new = pd.DataFrame({'Lote ID': lote_id,
                               'Item ID': item_id,
                               'Item Descricao': item_descricao,
                               'Item Quantidade': item_quantidade,
                               'Item Unidade': item_unidade,
                               'Valor do Item': item_value,
                               'Valor por extenso': item_full_value}, index=[len(st.session_state.new_row)])

        if btn_form:

            df_check = st.session_state.new_row[(st.session_state.new_row['Lote ID'] == lote_id) &
                                                (st.session_state.new_row['Item ID'] == item_id)]
            if len(df_check) > 0:
                for c in range (len(st.session_state.new_row)):
                    if (st.session_state.new_row['Lote ID'][c] == lote_id) & \
                            (st.session_state.new_row['Item ID'][c] == item_id):
                        st.session_state.new_row.drop(index=c, inplace=True)
                        st.session_state.new_row.sort_values(by=['Lote ID', 'Item ID'], inplace=True)
                        st.session_state.new_row.reset_index(drop=True, inplace=True)
                        st.session_state.new_row = pd.concat([st.session_state.new_row, df_new], axis=0)
                        st.write(st.session_state.new_row)
                        st.write(df_new)
                        break
            else:
                st.session_state.new_row = pd.concat([st.session_state.new_row, df_new], axis=0)
                df_new.drop(df_new.tail(1).index, inplace=True)
                df_new = pd.concat([st.session_state.new_row, df_new], axis=0)
                df_new.sort_values(by=['Lote ID', 'Item ID'], inplace=True)
                df_new.reset_index(drop=True, inplace=True)



            st.session_state.new_row.reset_index(drop=True, inplace=True)
            st.session_state.new_row.sort_values(by=['Lote ID', 'Item ID'], inplace=True)
            st.write(df_check)
            st.write(st.session_state.new_row)
            st.write(df_new)




            #st.dataframe(df_new)
options = list()
options.append('...')
for z in range(len(st.session_state.new_row)):
    options.append(st.session_state.new_row.loc[z, 'Lote ID'] + ' - '
                   + st.session_state.new_row.loc[z, 'Item ID'] + ' - '
                   + st.session_state.new_row.loc[z, 'Item Descricao'] + 'index:' + str(z))
col3, col4 = st.columns(2)
with col3:

    select_reg = st.selectbox("Selecione um registro para removê-lo:", options)
    remover = st.button("Remover registro")
    if select_reg != '...' and remover:
        removido = select_reg
        select_reg_titulo = int(select_reg.split(sep=':')[1].lstrip())
        st.session_state.new_row.drop(index=select_reg_titulo, inplace=True)
        st.session_state.new_row.sort_values(by=['Lote ID', 'Item ID'], inplace=True)
        st.session_state.new_row.reset_index(drop=True, inplace=True)

with col4:
    st.empty()



finaliza = st.button("Acabou?")
if finaliza:
    df_new = pd.concat([st.session_state.new_row, df_new], axis=0)
    df_new.drop(df_new.tail(1).index, inplace=True)
    df_new.sort_values(by=['Lote ID', 'Item ID']).reset_index(drop=True)
    st.dataframe(df_new)
    st.dataframe(st.session_state.new_row)
    # st.write(df_new.loc[len(df_new)-1,'Valor do Item'])
    # st.dataframe(df_new.loc['2'].at['Valor do Item'])
    list_dfs = []
    lotes = df_new['Lote ID'].unique()
    for y in range(len(lotes)):
        list_dfs.append(y)
        list_dfs[y] = df_new[df_new['Lote ID'] == lotes[y]].reset_index(drop=True)

    list_item = {}
    list_lote = {}
    list_total_lote = {}
    #for z in range(len(lotes)):
    #    st.dataframe(list_dfs[z])
    #st.write(list_dfs[0].loc[0, 'Item ID'])


    for x in range(len(lotes)):
        lote_atual = 'lote' + str(x)
        list_lote['lote{0}'.format(x)] = (str(lotes[x]))

        total_lote = round((list_dfs[x]['Item Quantidade'] * list_dfs[x]['Valor do Item']).sum(),2)
        total_lote_money = Money(amount=total_lote, currency='BRL').format('pt_BR')
        list_total_lote['total_lote{0}'.format(x)] = str(f'\nTOTAL DO {lotes[x]} .... R${total_lote_money} '
                                                         f'({numero_por_extenso(total_lote)}).')

        for i in range(len(list_dfs[x])):
            list_item[(lote_atual + ('item{0}'.format(i)))] = \
                (item_description(list_dfs[x].loc[i, 'Item ID'],
                                  list_dfs[x].loc[i, 'Item Descricao'],
                                  list_dfs[x].loc[i, 'Item Quantidade'],
                                  list_dfs[x].loc[i, 'Item Unidade'],
                                  list_dfs[x].loc[i, 'Valor do Item']))

    context = {'processo': processo, 'interessado': interessado, 'fls_solicitacao': fls_solicitacao,
               'descricao': descricao, 'data_documento': data_documento,
               'mod_num_licitacao': mod_num_licitacao, 'fls_ata': fls_ata, 'fls_pregoeiro': fls_pregoeiro,
               'id_itens_lote': id_itens_lote, 'ganhadora': ganhadora,
               'valor_lance': valor_lance1,
               'fls_especificacoes': fls_especificacoes, 'id_compra': id_compra, 'pregoeiro': pregoeiro,
               'cnpj_ganhadora': cnpj_ganhadora, 'data_adjudicacao':
                   translate_month(data_adjudicacao.strftime("%d de %B de %Y"))}

    context.update(list_item)
    context.update(list_lote)
    context.update(list_total_lote)

    df = pd.DataFrame.from_dict([context])
    st.dataframe(df)
    st.write(list_lote)
    st.write(list_item)
    st.write(list_total_lote)
    print(type(context))
    doc.render(context)
    doc.save("generated_doc_2.docx")

with open("generated_doc_2.docx", "rb") as myfile:
    btn = st.download_button(
        label="Download do documento",
        data=myfile,
        file_name='new_file.docx',
        mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )
