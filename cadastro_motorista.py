import streamlit as st
import mysql.connector

def conectar_banco():
    try:
        conn = mysql.connector.connect(
            user='logitech_rafael',
            password='admin000',
            host='db4free.net',
            port=3306,
            database='srtransporte'
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao banco de dados: {err}")
        return None
    
def salvar_dados(tabela, campos, valores, id_registro):
    with st.spinner("Salvando dados...", show_time=True):
        conn = conectar_banco()
        if not conn:
            st.error("Erro ao conectar ao banco de dados.")
            return

        try:
            cursor = conn.cursor()
            if id_registro:
                query = f"UPDATE {tabela} SET {', '.join([f'{campo} = %s' for campo in campos])} WHERE id_registro = %s"
                cursor.execute(query, valores + (id_registro,))
            else:
                query = f"INSERT INTO {tabela} ({', '.join(campos)}) VALUES ({', '.join(['%s'] * len(campos))})"
                cursor.execute(query, valores)

            conn.commit()
            cursor.close()
            conn.close()
            st.success("Dados salvos com sucesso!")
            
            st.session_state.clear()
            st.rerun()

        except mysql.connector.Error as err:
            st.error(f"Erro ao salvar dados no banco de dados: {err}")
        except Exception as e:
            st.error(f"Erro inesperado: {str(e)}")

def cadastro_motorista():
    st.title("Cadastro de Motorista")

    if 'id_registro'not in st.session_state:
        st.session_state.id_registro = ''    
    if 'motorista_1'not in st.session_state:        
        st.session_state.motorista_1 = ''            
    if 'cpf_1'not in st.session_state:        
        st.session_state.cpf_1 = ''            
    if 'rg'not in st.session_state:        
        st.session_state.rg = ''
    
    id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id_motorista')
    motorista = st.text_input("Motorista", key='motorista_1')
    cpf = st.text_input("CPF", key='cpf_1')
    rg = st.text_input("RG", key='rg')

    if st.button("Salvar", key='salvar_motorista'):
        campos = ['nome', 'cpf_1', 'rg']
        valores = (motorista, cpf, rg)
        salvar_dados('cad_mot', campos, valores, id_registro)

cadastro_motorista()