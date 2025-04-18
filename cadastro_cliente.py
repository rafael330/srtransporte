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

def cadastro_cliente():
    st.title("Cadastro de Cliente")

    if 'id_registro'not in st.session_state:
        st.session_state.id_registro = ''    
    if 'cod_cliente_1'not in st.session_state:        
        st.session_state.cod_cliente_1 = ''            
    if 'cliente_1'not in st.session_state:        
        st.session_state.cliente_1 = ''            
    if 'cnpj'not in st.session_state:        
        st.session_state.cnpj = ''
    
    id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id_cliente')
    cod_cliente = st.text_input("Código do Cliente", key='cod_cliente_1')
    cliente = st.text_input("Cliente", key='cliente_1')
    cnpj = st.text_input("CNPJ", key='cnpj')

    if st.button("Salvar", key='salvar_cliente'):        
        campos = ['cod_cliente_1', 'cliente_1', 'cnpj']
        valores = (cod_cliente, cliente, cnpj)
        salvar_dados('cad_cliente', campos, valores, id_registro)

cadastro_cliente()