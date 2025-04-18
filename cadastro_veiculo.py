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
                keys_to_clear = [f'id_veiculo_{form_key_suffix}',
                                f'placa_{form_key_suffix}',
                                f'perfil_{form_key_suffix}',
                                f'proprietario_{form_key_suffix}',
                                f'cubagem_{form_key_suffix}']
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
    
    def cadastro_veiculo(suffix):
        st.title("Cadastro de Veículo")
        
        # Inicializa session_state com valores padrão
        defaults = {
            f'id_veiculo_{suffix}': '',
            f'placa_{suffix}': '',
            f'perfil_{suffix}': '',
            f'proprietario_{suffix}': '',
            f'cubagem_{suffix}': ''
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
        
        # Formulário principal
        with st.form(key=f"form_veiculo_{suffix}"):
            # Layout em colunas para melhor organização
            col1, col2 = st.columns(2)
            
            with col1:
                # Campo ID
                id_registro = st.text_input(
                    "ID (deixe vazio para novo cadastro)",
                    value=st.session_state[f'id_veiculo_{suffix}'],
                    key=f"input_id_veiculo_{suffix}"
                )
                
                # Campo Placa
                placa = st.text_input(
                    "Placa*",
                    value=st.session_state[f'placa_{suffix}'],
                    key=f"input_placa_{suffix}"
                )
                
                # Campo Perfil
                perfil = st.text_input(
                    "Perfil",
                    value=st.session_state[f'perfil_{suffix}'],
                    key=f"input_perfil_{suffix}"
                )
            
            with col2:
                # Campo Proprietário
                proprietario = st.text_input(
                    "Proprietário",
                    value=st.session_state[f'proprietario_{suffix}'],
                    key=f"input_proprietario_{suffix}"
                )
                
                # Campo Cubagem
                cubagem = st.text_input(
                    "Cubagem (m³)",
                    value=st.session_state[f'cubagem_{suffix}'],
                    key=f"input_cubagem_{suffix}"
                )
            
            # Botão de submit dentro do form
            submitted = st.form_submit_button("Salvar Cadastro")
            
            if submitted:
                if not placa:  # Validação do campo obrigatório
                    st.error("O campo Placa é obrigatório!")
                else:
                    # Atualiza session_state
                    st.session_state[f'id_veiculo_{suffix}'] = id_registro
                    st.session_state[f'placa_{suffix}'] = placa
                    st.session_state[f'perfil_{suffix}'] = perfil
                    st.session_state[f'proprietario_{suffix}'] = proprietario
                    st.session_state[f'cubagem_{suffix}'] = cubagem
                    
                    # Prepara dados para salvar
                    campos = ['placa', 'perfil', 'proprietario', 'cubagem']
                    valores = (placa, perfil, proprietario, cubagem)
                    salvar_dados('cad_vei', campos, valores, id_registro)
    
    cadastro_veiculo(form_key_suffix)

if __name__ == '__main__':
    main("local")
