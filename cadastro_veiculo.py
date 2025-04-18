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

def cadastro_veiculo():
    st.title("Cadastro de Veículo")

    if 'id_registro'not in st.session_state:
        st.session_state.id_registro = ''    
    if 'placa_1'not in st.session_state:        
        st.session_state.placa_1 = ''            
    if 'perfil_1'not in st.session_state:        
        st.session_state.perfil_1 = ''            
    if 'proprietario_1'not in st.session_state:        
        st.session_state.proprietario_1 = ''
    if 'cubagem_1'not in st.session_state:        
        st.session_state.cubagem_1 = ''
    
    id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id_veiculo')
    placa = st.text_input("Placa", key='placa_1')
    perfil = st.text_input("Perfil", key='perfil_1')
    proprietario = st.text_input("Proprietário", key='proprietario_1')
    cubagem = st.text_input("Cubagem", key='cubagem_1')

    if st.button("Salvar", key='salvar_veiculo'):
        campos = ['placa_1', 'perfil_1', 'proprietario_1', 'cubagem_1']
        valores = (placa, perfil, proprietario, cubagem)
        salvar_dados('cad_vei', campos, valores, id_registro)

cadastro_veiculo()  