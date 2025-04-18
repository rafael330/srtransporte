import streamlit as st
import mysql.connector

def main():
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
    
    def cadastro_rota():
        st.title("Cadastro de Rota")
    
        if 'id_registro'not in st.session_state:
            st.session_state.id_registro = ''    
        if 'cidade'not in st.session_state:        
            st.session_state.cidade = ''            
        if 'regiao'not in st.session_state:        
            st.session_state.regiao = ''            
        if 'cep_unico'not in st.session_state:        
            st.session_state.cep_unico = ''
        
        id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id_rota')
        cidade = st.text_input("Cidade", key='cidade')
        regiao = st.text_input("Região", key='regiao')
        cep_unico = st.text_input("CEP Único", key='cep_unico')
    
        if st.button("Salvar", key='salvar_rota'):
            campos = ['cidade', 'regiao', 'cep_unico']
            valores = (cidade, regiao, cep_unico)
            salvar_dados('cad_rota', campos, valores, id_registro)
    
    cadastro_rota() 

if __name__ == '__main__' or 'streamlit' in __import__('sys').modules:
    main()
