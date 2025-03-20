import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        conn = mysql.connector.connect(
            user='rafael_logitech',  
            password='admin',  
            host='0.tcp.sa.ngrok.io',  
            port=11804,  
            database='bd_srtransporte'  
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao banco de dados: {err}")
        return None

# Função para buscar motoristas e seus CPFs
def buscar_motoristas():
    conn = conectar_banco()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT nome, cpf FROM cad_mot"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()
            return {nome: cpf for nome, cpf in resultados}
        except mysql.connector.Error as err:
            st.error(f"Erro ao buscar motoristas: {err}")
    return {}

# Função para buscar rotas e cidades
def buscar_rotas_cidades():
    conn = conectar_banco()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT DISTINCT rota, cidade FROM cad_rota"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()
            return resultados
        except mysql.connector.Error as err:
            st.error(f"Erro ao buscar rotas e cidades: {err}")
    return []

    # Tela de Novo Cadastro
    elif st.session_state['opcao'] == "Novo Cadastro":
        st.title("Novo Cadastro de Carregamento")
    
        # Buscar motoristas e rotas
        motoristas = buscar_motoristas()
        rotas_cidades = buscar_rotas_cidades()
    
        # Coluna Cliente e Código do Cliente
        col1, col2 = st.columns(2)
        with col1:
            cliente = st.selectbox(
                "Cliente",
                options=[""] + list(clientes.keys()),
                index=0,
                key='cliente'
            )
            if cliente:
                st.session_state['cod_cliente'] = clientes.get(cliente, '')
        with col2:
            cod_cliente = st.text_input(
                "Código do Cliente",
                value=st.session_state.get('cod_cliente', ''),
                key='cod_cliente',
                disabled=True
            )
        
        # Coluna Motorista e CPF do Motorista
        col1, col2 = st.columns(2)
        with col1:
            motorista = st.selectbox(
                "Motorista",
                options=[""] + list(motoristas.keys()),
                key='motorista'
            )
            if motorista:
                st.session_state['cpf_motorista'] = motoristas.get(motorista, '')
        with col2:
            cpf_motorista = st.text_input(
                "CPF do Motorista",
                value=st.session_state.get('cpf_motorista', ''),
                key='cpf_motorista',
                disabled=True
            )
        
        # Coluna de Placa e Perfil do Veículo
        col1, col2 = st.columns(2)
        with col1:
            placa = st.selectbox(
                "Placa",
                options=[""] + list(placas.keys()),
                index=0,
                key='placa'
            )
            if placa:
                st.session_state['perfil_vei'] = placas.get(placa, '')
        with col2:
            perfil_vei = st.text_input(
                "Perfil do Veículo",
                value=st.session_state.get('perfil_vei', ''),
                key='perfil_vei',
                disabled=True
            )
        
        # Coluna Minuta OT e ID Carga CVia
        col1, col2 = st.columns(2)
        with col1:
            minuta_ot = st.text_input("Minuta/OT", value=st.session_state.get('minuta_ot', ''), key='minuta_ot')
        with col2:
            id_carga_cvia = st.text_input("ID carga / CVia", value=st.session_state.get('id_carga_cvia', ''), key='id_carga_cvia')
        
        # Coluna de Valores
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            valor_carga = st.text_input("Valor da Carga", value=st.session_state.get('valor_carga', ''), key='valor_carga')
        with col2:
            valor_frete = st.text_input("Valor do Frete", value=st.session_state.get('valor_frete', ''), key='valor_frete')
        with col3:
            descarga = st.text_input("Descarga", value=st.session_state.get('descarga', ''), key='descarga')
        with col4:
            adiantamento = st.text_input("Adiantamento", value=st.session_state.get('adiantamento', ''), key='adiantamento')
    
        # Coluna Rota, Cidade e Modalidade 1
        col1, col2, col3 = st.columns(3)
        with col1:
            rotas_1 = [r[0] for r in rotas_cidades]
            rota_1 = st.selectbox("Rota 1", options=[""] + rotas_1, key="rot_1")
        with col2:
            cidades_1 = [r[1] for r in rotas_cidades if r[0] == rota_1]
            cidade_1 = st.selectbox("Cidade 1", options=[""] + cidades_1, key="cid_1")
        with col3:
            modalidade_1 = st.selectbox("Modalidade 1", options=["ABA", "VENDA"], key="mod_1")
    
        # Coluna Rota, Cidade e Modalidade 2
        col1, col2, col3 = st.columns(3)
        with col1:
            rota_2 = st.selectbox("Rota 2", options=[""] + rotas_1, key="rot_2")
        with col2:
            cidades_2 = [r[1] for r in rotas_cidades if r[0] == rota_2]
            cidade_2 = st.selectbox("Cidade 2", options=[""] + cidades_2, key="cid_2")
        with col3:
            modalidade_2 = st.selectbox("Modalidade 2", options=["ABA", "VENDA"], key="mod_2")
    
        # Data e Cubagem
        data = st.text_input("Data", value=st.session_state.get('data', ''), key='data')
        cubagem = st.text_input("Cubagem", value=st.session_state.get('cubagem', ''), key='cubagem')
    
        if st.button("Enviar"):
            submit_data()
