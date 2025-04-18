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
                
                # Limpa apenas os campos do formulário
                keys_to_clear = [f'id_motorista_{form_key_suffix}',
                                f'motorista_{form_key_suffix}',
                                f'cpf_{form_key_suffix}',
                                f'rg_{form_key_suffix}']
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
    
    def cadastro_motorista(suffix):
        st.title("Cadastro de Motorista")
        
        # Inicializa session_state com valores padrão
        defaults = {
            f'id_motorista_{suffix}': '',
            f'motorista_{suffix}': '',
            f'cpf_{suffix}': '',
            f'rg_{suffix}': ''
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
        
        # Formulário principal
        with st.form(key=f"form_motorista_{suffix}"):
            # Campo ID
            id_registro = st.text_input(
                "ID (deixe vazio para novo cadastro)",
                value=st.session_state[f'id_motorista_{suffix}'],
                key=f"input_id_motorista_{suffix}"
            )
            
            # Campo Nome do Motorista
            motorista = st.text_input(
                "Motorista*",
                value=st.session_state[f'motorista_{suffix}'],
                key=f"input_motorista_{suffix}"
            )
            
            # Campo CPF
            cpf = st.text_input(
                "CPF*",
                value=st.session_state[f'cpf_{suffix}'],
                key=f"input_cpf_{suffix}"
            )
            
            # Campo RG
            rg = st.text_input(
                "RG",
                value=st.session_state[f'rg_{suffix}'],
                key=f"input_rg_{suffix}"
            )
            
            # Botão de submit dentro do form
            submitted = st.form_submit_button("Salvar")
            
            if submitted:
                if not motorista or not cpf:
                    st.error("Os campos marcados com * são obrigatórios!")
                else:
                    # Atualiza session_state
                    st.session_state[f'id_motorista_{suffix}'] = id_registro
                    st.session_state[f'motorista_{suffix}'] = motorista
                    st.session_state[f'cpf_{suffix}'] = cpf
                    st.session_state[f'rg_{suffix}'] = rg
                    
                    # Prepara dados para salvar
                    campos = ['nome', 'cpf', 'rg']
                    valores = (motorista, cpf, rg)
                    salvar_dados('cad_mot', campos, valores, id_registro)
    
    cadastro_motorista(form_key_suffix)

if __name__ == '__main__':
    main("local")
