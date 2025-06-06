import streamlit as st
import mysql.connector
import time

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
            .success-message {
                color: green;
                font-weight: bold;
                margin: 10px 0;
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
    
    def limpar_formulario(suffix):
        """Função para limpar todos os campos do formulário"""
        st.session_state[f'id_baixa_frete_{suffix}'] = ""
        st.session_state[f'saldo_frete_{suffix}'] = "0.00"
        st.session_state[f'motorista_{suffix}'] = ""
        st.session_state[f'proprietario_{suffix}'] = ""
        st.session_state[f'last_id_baixa_frete_{suffix}'] = ""
        st.session_state[f'show_success_{suffix}'] = False
        st.rerun()
    
    def baixa_saldo(suffix):
        st.title("Baixa de saldo de frete")
        
        # Chave única para o formulário
        form_key = f"baixa_saldo_{suffix}"
        
        # Inicializa todas as chaves necessárias no session_state
        required_keys = [
            f'id_baixa_frete_{suffix}',
            f'saldo_frete_{suffix}',
            f'motorista_{suffix}',
            f'proprietario_{suffix}',
            f'last_id_baixa_frete_{suffix}',
            f'show_success_{suffix}'
        ]
        
        for key in required_keys:
            if key not in st.session_state:
                if 'saldo' in key:
                    st.session_state[key] = "0.00"
                elif key == f'show_success_{suffix}':
                    st.session_state[key] = False
                else:
                    st.session_state[key] = ""
        
        # Se houver mensagem de sucesso para mostrar
        if st.session_state.get(f'show_success_{suffix}', False):
            st.markdown('<p class="success-message">Dados salvos com sucesso!</p>', unsafe_allow_html=True)
            if st.button("Novo Lançamento", key=f"novo_lancamento_{suffix}"):
                limpar_formulario(suffix)
            return
    
        # Função para buscar todos os dados pelo ID nas tabelas corretas
        def buscar_dados(id_baixa_frete):
            conn = conectar_banco()
            if conn:
                try:
                    cursor = conn.cursor(dictionary=True)
                    query = """
                        SELECT 
                            f.saldo_frete,
                            i.motorista,
                            i.proprietario_vei as proprietario
                        FROM tela_inicial i
                        LEFT JOIN tela_fin f ON i.id = f.id
                        WHERE i.id = %s
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
        with st.form(key=form_key):
            # Layout do formulário
            col1, col2 = st.columns(2)
            
            with col1:
                # Campo ID
                id_input = st.text_input(
                    "ID* (obrigatório)", 
                    key=f'id_input_{suffix}',
                    value=st.session_state[f'id_baixa_frete_{suffix}']
                )
                
                # Busca automática quando o ID é alterado
                if id_input and id_input != st.session_state[f'last_id_baixa_frete_{suffix}']:
                    dados = buscar_dados(id_input)
                    if dados:
                        st.session_state[f'saldo_frete_{suffix}'] = dados.get('saldo_frete', "0.00") or "0.00"
                        st.session_state[f'motorista_{suffix}'] = dados.get('motorista', "")
                        st.session_state[f'proprietario_{suffix}'] = dados.get('proprietario', "")
                    else:
                        st.session_state[f'saldo_frete_{suffix}'] = "0.00"
                        st.session_state[f'motorista_{suffix}'] = ""
                        st.session_state[f'proprietario_{suffix}'] = ""
                        st.warning("Nenhum dado encontrado para este ID")
                    
                    st.session_state[f'last_id_baixa_frete_{suffix}'] = id_input
                    st.session_state[f'id_baixa_frete_{suffix}'] = id_input
    
            with col2:
                st.text_input(
                    "Saldo de frete", 
                    value=st.session_state[f'saldo_frete_{suffix}'],
                    key=f'display_saldo_frete_{suffix}',
                    disabled=True
                )
    
            col1, col2 = st.columns(2)
            with col1:
                st.text_input(
                    "Motorista", 
                    value=st.session_state[f'motorista_{suffix}'],
                    key=f'display_motorista_{suffix}',
                    disabled=True
                )
            with col2:
                st.text_input(
                    "Proprietário", 
                    value=st.session_state[f'proprietario_{suffix}'],
                    key=f'display_proprietario_{suffix}',
                    disabled=True
                )
            
            # Botão de submit
            submitted = st.form_submit_button("Salvar Dados Financeiros")
            
            if submitted:
                if not id_input:
                    st.error("O campo ID é obrigatório")
                else:
                    # Barra de progresso
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for percent_complete in range(100):
                        time.sleep(0.02)  # Simula o processamento
                        progress_bar.progress(percent_complete + 1)
                        status_text.text(f"Salvando... {percent_complete + 1}%")
                    
                    try:
                        saldo = float(st.session_state[f'saldo_frete_{suffix}'] or 0)
                        
                        dados = {
                            'id': id_input,
                            'saldo': saldo,
                            'motorista': st.session_state[f'motorista_{suffix}'],
                            'proprietario': st.session_state[f'proprietario_{suffix}']                            
                        }
    
                        conn = conectar_banco()
                        if conn:
                            cursor = conn.cursor()
                            cursor.execute("SELECT id FROM baixa_saldo WHERE id = %s", (id_input,))
                            existe = cursor.fetchone()
                            
                            if existe:
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
                            
                            # Esconde a barra de progresso
                            progress_bar.empty()
                            status_text.empty()
                            
                            # Mostra mensagem de sucesso e botão "Novo Lançamento"
                            st.session_state[f'show_success_{suffix}'] = True
                            st.rerun()
                            
                    except mysql.connector.Error as err:
                        if conn:
                            conn.rollback()
                        progress_bar.empty()
                        status_text.empty()
                        st.error(f"Erro ao salvar dados: {err}")
                    except ValueError as ve:
                        if conn:
                            conn.rollback()
                        progress_bar.empty()
                        status_text.empty()
                        st.error(f"Valor inválido para saldo: {ve}")
                    finally:
                        if conn and conn.is_connected():
                            cursor.close()
                            conn.close()
    
    baixa_saldo(form_key_suffix)

if __name__ == '__main__':
    main("local")
