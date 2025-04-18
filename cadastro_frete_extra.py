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
    
    # Função para buscar clientes
    def buscar_clientes():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT cliente, cod_cliente FROM cad_cliente"
                cursor.execute(query)
                resultados = cursor.fetchall()
                cursor.close()
                conn.close()
                return {cliente: cod_cliente for cliente, cod_cliente in resultados}
            except mysql.connector.Error as err:
                st.error(f"Erro ao buscar clientes: {err}")
        return {}
    
    # Função para buscar cargas
    def buscar_cargas():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT DISTINCT id_carga_cvia FROM tela_inicial"
                cursor.execute(query)
                resultados = cursor.fetchall()
                cursor.close()
                conn.close()
                return [carga[0] for carga in resultados]
            except mysql.connector.Error as err:
                st.error(f"Erro ao buscar cargas: {err}")
        return []
    
    # Função para buscar cidades
    def buscar_cidades():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT DISTINCT cidade FROM cad_rota"
                cursor.execute(query)
                resultados = cursor.fetchall()
                cursor.close()
                conn.close()
                return [cidade[0] for cidade in resultados]
            except mysql.connector.Error as err:
                st.error(f"Erro ao buscar cidades: {err}")
        return []
    
    def cadastro_frete_extra():
        st.title("Cadastro de Frete Extra")
    
        if 'id_registro'not in st.session_state:
            st.session_state.id_registro = ''    
        if 'cliente'not in st.session_state:        
            st.session_state.cliente = ''            
        if 'data'not in st.session_state:        
            st.session_state.data = ''            
        if 'id_carga'not in st.session_state:        
            st.session_state.id_carga = ''
        if 'cidade'not in st.session_state:        
            st.session_state.cidade = ''
        if 'entrega_final'not in st.session_state:        
            st.session_state.entrega_final = ''
        if 'valor'not in st.session_state:        
            st.session_state.valor = ''
    
        id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id_frete_extra')
        cliente = st.selectbox("Cliente", options=[""] + list(buscar_clientes().keys()), key='cliente_frete')
        data = st.text_input("Data (Formato: dd/mm/aaaa)", key='data_frete')
        id_carga = st.selectbox("ID Carga", options=[""] + buscar_cargas(), key='id_carga_frete')
        cidade = st.selectbox("Cidade", options=[""] + buscar_cidades(), key='cidade_frete')
        entrega_final = st.text_input("Entrega Final", key='entrega_final')
        valor = st.text_input("Valor", key='valor_frete')
    
        if st.button("Salvar", key='salvar_frete_extra'):
            campos = ['cliente', 'data', 'id_carga', 'cidade', 'entrega_final', 'valor']
            valores = (cliente, data, id_carga, cidade, entrega_final, valor)
            salvar_dados('cad_frete_extra', campos, valores, id_registro)
    
    cadastro_frete_extra() 

if __name__ == '__main__' or 'streamlit' in __import__('sys').modules:
    main()
