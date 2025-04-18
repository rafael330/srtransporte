import streamlit as st
import mysql.connector

def main(form_key_suffix=""):  # Adicionado parâmetro para sufixo único
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
    
    def cadastro_cliente(suffix):  # Adicionado parâmetro suffix
        st.title("Cadastro de Cliente")
    
        # Inicializa session_state com keys únicas
        if f'id_registro_{suffix}' not in st.session_state:
            st.session_state[f'id_registro_{suffix}'] = ''    
        if f'cod_cliente_{suffix}' not in st.session_state:        
            st.session_state[f'cod_cliente_{suffix}'] = ''            
        if f'cliente_{suffix}' not in st.session_state:        
            st.session_state[f'cliente_{suffix}'] = ''            
        if f'cnpj_{suffix}' not in st.session_state:        
            st.session_state[f'cnpj_{suffix}'] = ''
        
        # Formulário com keys únicas
        with st.form(key=f"form_cliente_{suffix}"):
            id_registro = st.text_input(
                "ID (deixe vazio para novo cadastro)", 
                key=f'id_cliente_{suffix}'
            )
            cod_cliente = st.text_input(
                "Código do Cliente", 
                key=f'cod_cliente_{suffix}'
            )
            cliente = st.text_input(
                "Cliente", 
                key=f'cliente_{suffix}'
            )
            cnpj = st.text_input(
                "CNPJ", 
                key=f'cnpj_{suffix}'
            )
    
            submitted = st.form_submit_button("Salvar")
            if submitted:
                campos = ['cod_cliente_1', 'cliente_1', 'cnpj']
                valores = (
                    st.session_state[f'cod_cliente_{suffix}'],
                    st.session_state[f'cliente_{suffix}'],
                    st.session_state[f'cnpj_{suffix}']
                )
                salvar_dados('cad_cliente', campos, valores, id_registro)
    
    cadastro_cliente(form_key_suffix)  # Passa o sufixo para a função

if __name__ == '__main__' or 'streamlit' in __import__('sys').modules:
    main("local")  # Para execução direta usa "local" como sufixo
