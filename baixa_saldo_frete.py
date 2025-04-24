import streamlit as st
import mysql.connector

def main(form_key_suffix=""):
    
    st.markdown("""
        <style>
            .stForm {
                border: none !important;
                box-shadow: none !important;
                padding: 0 !important;
            }
            .stForm form {
                border: none !important;
                padding: 0 !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
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
    
    def baixa_saldo(suffix):
        st.title("Baixa de saldo de frete")      
        
        # Inicializa session_state com keys únicas
        defaults = {
            f'id_baixa_frete_{suffix}': "",
            f'saldo_frete_{suffix}': "0.00",  # Inicializa com valor padrão para evitar erro decimal
            f'motorista_{suffix}': "",
            f'proprietario_{suffix}': "",
            f'last_id_baixa_frete_{suffix}': ""            
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
        # Função para buscar todos os dados pelo ID
        def buscar_dados(id_baixa_frete):
            conn = conectar_banco()
            if conn:
                try:
                    cursor = conn.cursor(dictionary=True)
                    # Consulta corrigida para buscar da tela_inicial
                    query = """
                        SELECT 
                            saldo_frete, 
                            motorista, 
                            proprietario_vei as proprietario
                        FROM tela_inicial
                        WHERE id = %s
                    """
                    cursor.execute(query, (id_baixa_frete,))
                    resultado = cursor.fetchone()
                    cursor.close()
                    conn.close()
                    return resultado if resultado else None
                except mysql.connector.Error as err:
                    st.error(f"Erro ao buscar dados: {err}")
            return None
        
        # Formulário principal
        with st.form(key=f"baixa_saldo_{suffix}"):
            # Layout do formulário
            col1, col2 = st.columns(2)
            
            with col1:
                # Campo ID
                id_baixa_frete = st.text_input(
                    "ID* (obrigatório)", 
                    key=f'id_baixa_frete_{suffix}', 
                    value=st.session_state[f'id_baixa_frete_{suffix}']
                )
                
                # Busca automática dos dados quando o ID é alterado
                if id_baixa_frete and id_baixa_frete != st.session_state[f'last_id_baixa_frete_{suffix}']:
                    dados = buscar_dados(id_baixa_frete)
                    if dados:
                        st.session_state[f'saldo_frete_{suffix}'] = dados.get('saldo_frete', "0.00") or "0.00"  # Garante valor padrão
                        st.session_state[f'motorista_{suffix}'] = dados.get('motorista', "")
                        st.session_state[f'proprietario_{suffix}'] = dados.get('proprietario', "")
                    else:
                        st.session_state[f'saldo_frete_{suffix}'] = "0.00"
                        st.session_state[f'motorista_{suffix}'] = ""
                        st.session_state[f'proprietario_{suffix}'] = ""
                        st.warning("Nenhum dado encontrado para este ID")
                    
                    st.session_state[f'last_id_baixa_frete_{suffix}'] = id_baixa_frete
    
            with col2:
                # Campo de saldo (preenchido automaticamente)
                st.text_input(
                    "Saldo de frete", 
                    value=st.session_state[f'saldo_frete_{suffix}'],
                    key=f'display_saldo_frete_{suffix}',
                    disabled=True
                )
    
            # Campos financeiros
            col1, col2 = st.columns(2)
            with col1:
                # Campo de motorista (preenchido automaticamente)
                st.text_input(
                    "Motorista", 
                    value=st.session_state[f'motorista_{suffix}'],
                    key=f'display_motorista_{suffix}',
                    disabled=True
                )
            with col2:
                # Campo de proprietario (preenchido automaticamente)
                st.text_input(
                    "Proprietário", 
                    value=st.session_state[f'proprietario_{suffix}'],
                    key=f'display_proprietario_{suffix}',
                    disabled=True
                )
    
            # Botão de submit dentro do form
            submitted = st.form_submit_button("Salvar Dados Financeiros")
            
            if submitted:
                # Validação dos campos obrigatórios
                if not id_baixa_frete:
                    st.error("O campo ID é obrigatório")
                else:
                    with st.spinner("Salvando dados..."):
                        # Prepara dados para salvar
                        dados = {
                            'id': id_baixa_frete,
                            'saldo': float(st.session_state[f'saldo_frete_{suffix}'] or 0),  # Converte para float
                            'motorista': st.session_state[f'motorista_{suffix}'],
                            'proprietario': st.session_state[f'proprietario_{suffix}']                            
                        }
    
                        # Conecta ao banco e salva
                        conn = conectar_banco()
                        if conn:
                            try:
                                cursor = conn.cursor()
                                
                                # Verifica se é atualização ou inserção
                                cursor.execute("SELECT id FROM baixa_saldo WHERE id = %s", (id_baixa_frete,))
                                existe = cursor.fetchone()
                                
                                if existe:
                                    # Atualiza registro existente
                                    query = """
                                        UPDATE baixa_saldo SET
                                            saldo = %s,
                                            motorista = %s,
                                            proprietario = %s
                                        WHERE id = %s
                                    """
                                    cursor.execute(query, (
                                        dados['saldo'],
                                        dados['motorista'],
                                        dados['proprietario'],
                                        dados['id']
                                    ))
                                else:
                                    # Insere novo registro
                                    query = """
                                        INSERT INTO baixa_saldo (
                                            id, saldo, motorista, proprietario
                                        ) VALUES (%s, %s, %s, %s)
                                    """
                                    cursor.execute(query, (
                                        dados['id'],
                                        dados['saldo'],
                                        dados['motorista'],
                                        dados['proprietario']
                                    ))
                                
                                conn.commit()
                                st.success("Dados salvos com sucesso!")
                                
                                # Limpa os campos do formulário
                                st.session_state[f'id_baixa_frete_{suffix}'] = ""
                                st.session_state[f'saldo_frete_{suffix}'] = "0.00"
                                st.session_state[f'motorista_{suffix}'] = ""
                                st.session_state[f'proprietario_{suffix}'] = ""
                                st.session_state[f'last_id_baixa_frete_{suffix}'] = ""
                                
                                st.rerun()
                                
                            except mysql.connector.Error as err:
                                conn.rollback()
                                st.error(f"Erro ao salvar dados: {err}")
                            except ValueError as ve:
                                conn.rollback()
                                st.error(f"Valor inválido para saldo: {ve}")
                            finally:
                                if conn and conn.is_connected():
                                    cursor.close()
                                    conn.close()
    
    baixa_saldo(form_key_suffix)

if __name__ == '__main__':
    main("local")
