import streamlit as st
import mysql.connector

def main(form_key_suffix=""):
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
        with st.spinner("Salvando dados..."):     
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
                st.success("Dados salvos com sucesso!")
                
                # Limpa apenas os campos do formulário, mantendo outras variáveis de sessão
                keys_to_clear = [f'id_cliente_{form_key_suffix}', 
                                f'cod_cliente_{form_key_suffix}',
                                f'cliente_{form_key_suffix}',
                                f'cnpj_{form_key_suffix}']
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                
                st.rerun()
            except mysql.connector.Error as err:
                st.error(f"Erro ao salvar dados: {err}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
    
    def cadastro_cliente(suffix):
        st.title("Cadastro de Cliente")
        
        # Inicializa session_state com valores padrão se não existirem
        defaults = {
            f'id_cliente_{suffix}': '',
            f'cod_cliente_{suffix}': '',
            f'cliente_{suffix}': '',
            f'cnpj_{suffix}': ''
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
        
        # Formulário principal com submit button
        with st.form(key=f"form_cliente_{suffix}"):
            # Campo ID
            id_registro = st.text_input(
                "ID (deixe vazio para novo cadastro)",
                value=st.session_state[f'id_cliente_{suffix}'],
                key=f"input_id_cliente_{suffix}"
            )
            
            # Campo Código do Cliente
            cod_cliente = st.text_input(
                "Código do Cliente*",
                value=st.session_state[f'cod_cliente_{suffix}'],
                key=f"input_cod_cliente_{suffix}"
            )
            
            # Campo Nome do Cliente
            cliente = st.text_input(
                "Cliente*",
                value=st.session_state[f'cliente_{suffix}'],
                key=f"input_cliente_{suffix}"
            )
            
            # Campo CNPJ
            cnpj = st.text_input(
                "CNPJ",
                value=st.session_state[f'cnpj_{suffix}'],
                key=f"input_cnpj_{suffix}"
            )
            
            # Botão de submit dentro do form
            submitted = st.form_submit_button("Salvar")
            
            if submitted:
                if not cod_cliente or not cliente:
                    st.error("Os campos marcados com * são obrigatórios!")
                else:
                    # Atualiza session_state
                    st.session_state[f'id_cliente_{suffix}'] = id_registro
                    st.session_state[f'cod_cliente_{suffix}'] = cod_cliente
                    st.session_state[f'cliente_{suffix}'] = cliente
                    st.session_state[f'cnpj_{suffix}'] = cnpj
                    
                    # Prepara dados para salvar
                    campos = ['cod_cliente', 'cliente', 'cnpj']
                    valores = (cod_cliente, cliente, cnpj)
                    salvar_dados('cad_cliente', campos, valores, id_registro)
    
    cadastro_cliente(form_key_suffix)

if __name__ == '__main__':
    main("local")
