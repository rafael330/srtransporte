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
                keys_to_clear = [f'id_rota_{form_key_suffix}',
                                f'cidade_{form_key_suffix}',
                                f'regiao_{form_key_suffix}',
                                f'cep_unico_{form_key_suffix}']
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
    
    def cadastro_rota(suffix):
        st.title("Cadastro de Rota")
        
        # Inicializa session_state com valores padrão
        defaults = {
            f'id_rota_{suffix}': '',
            f'cidade_{suffix}': '',
            f'regiao_{suffix}': '',
            f'cep_unico_{suffix}': ''
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
        
        # Formulário principal
        with st.form(key=f"form_rota_{suffix}"):
            # Campo ID
            id_registro = st.text_input(
                "ID (deixe vazio para novo cadastro)",
                value=st.session_state[f'id_rota_{suffix}'],
                key=f"input_id_rota_{suffix}"
            )
            
            # Campo Cidade
            cidade = st.text_input(
                "Cidade*",
                value=st.session_state[f'cidade_{suffix}'],
                key=f"input_cidade_{suffix}"
            )
            
            # Campo Região
            regiao = st.text_input(
                "Região",
                value=st.session_state[f'regiao_{suffix}'],
                key=f"input_regiao_{suffix}"
            )
            
            # Campo CEP Único
            cep_unico = st.text_input(
                "CEP Único",
                value=st.session_state[f'cep_unico_{suffix}'],
                key=f"input_cep_unico_{suffix}"
            )
            
            # Botão de submit dentro do form
            submitted = st.form_submit_button("Salvar")
            
            if submitted:
                if not cidade:  # Validação do campo obrigatório
                    st.error("O campo Cidade é obrigatório!")
                else:
                    # Atualiza session_state
                    st.session_state[f'id_rota_{suffix}'] = id_registro
                    st.session_state[f'cidade_{suffix}'] = cidade
                    st.session_state[f'regiao_{suffix}'] = regiao
                    st.session_state[f'cep_unico_{suffix}'] = cep_unico
                    
                    # Prepara dados para salvar
                    campos = ['cidade', 'regiao', 'cep_unico']
                    valores = (cidade, regiao, cep_unico)
                    salvar_dados('cad_rota', campos, valores, id_registro)
    
    cadastro_rota(form_key_suffix)

if __name__ == '__main__':
    main("local")
