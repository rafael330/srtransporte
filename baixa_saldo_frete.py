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
        
        # Chave única para o formulário
        form_key = f"baixa_saldo_{suffix}"
        
        # Inicializa session_state apenas uma vez
        if f'initialized_{form_key}' not in st.session_state:
            st.session_state[f'initialized_{form_key}'] = True
            st.session_state[f'id_baixa_frete_{suffix}'] = ""
            st.session_state[f'saldo_frete_{suffix}'] = "0.00"
            st.session_state[f'motorista_{suffix}'] = ""
            st.session_state[f'proprietario_{suffix}'] = ""
            st.session_state[f'last_id_baixa_frete_{suffix}'] = ""
    
        # Função para buscar todos os dados pelo ID nas tabelas corretas
        def buscar_dados(id_baixa_frete):
            conn = conectar_banco()
            if conn:
                try:
                    cursor = conn.cursor(dictionary=True)
                    # Consulta que busca saldo_frete da tela_fin e motorista/proprietario da tela_inicial
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
                # Campo ID - usa o valor atual do session_state
                id_input = st.text_input(
                    "ID* (obrigatório)", 
                    key=f'id_input_{suffix}',
                    value=st.session_state[f'id_baixa_frete_{suffix}']
                )
                
                # Quando o ID é alterado, busca os dados nas tabelas corretas
                if id_input and id_input != st.session_state[f'last_id_baixa_frete_{suffix}']:
                    dados = buscar_dados(id_input)
                    if dados:
                        # Atualiza os valores conforme especificado:
                        # saldo -> saldo_frete (tela_fin)
                        # motorista -> motorista (tela_inicial)
                        # proprietario -> proprietario_vei (tela_inicial)
                        st.session_state[f'saldo_frete_{suffix}'] = dados.get('saldo_frete', "0.00") or "0.00"
                        st.session_state[f'motorista_{suffix}'] = dados.get('motorista', "")
                        st.session_state[f'proprietario_{suffix}'] = dados.get('proprietario', "")
                    else:
                        st.session_state[f'saldo_frete_{suffix}'] = "0.00"
                        st.session_state[f'motorista_{suffix}'] = ""
                        st.session_state[f'proprietario_{suffix}'] = ""
                        st.warning("Nenhum dado encontrado para este ID")
                    
                    # Atualiza o último ID pesquisado
                    st.session_state[f'last_id_baixa_frete_{suffix}'] = id_input
                    # Atualiza o ID no session_state
                    st.session_state[f'id_baixa_frete_{suffix}'] = id_input
    
            with col2:
                # Campo de saldo (apenas exibição)
                st.text_input(
                    "Saldo de frete", 
                    value=st.session_state[f'saldo_frete_{suffix}'],
                    key=f'display_saldo_frete_{suffix}',
                    disabled=True
                )
    
            # Campos financeiros
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
    
            submitted = st.form_submit_button("Salvar Dados Financeiros")
            
            if submitted:
                if not id_input:
                    st.error("O campo ID é obrigatório")
                else:
                    with st.spinner("Salvando dados..."):
                        try:
                            # Converte o saldo para float
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
                                
                                # Verifica se é atualização ou inserção
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
                                st.success("Dados salvos com sucesso!")
                                
                                # Limpa os campos após salvar
                                st.session_state[f'id_baixa_frete_{suffix}'] = ""
                                st.session_state[f'saldo_frete_{suffix}'] = "0.00"
                                st.session_state[f'motorista_{suffix}'] = ""
                                st.session_state[f'proprietario_{suffix}'] = ""
                                st.session_state[f'last_id_baixa_frete_{suffix}'] = ""
                                
                                # Força o rerun para atualizar os campos
                                st.rerun()
                                
                        except mysql.connector.Error as err:
                            if conn:
                                conn.rollback()
                            st.error(f"Erro ao salvar dados: {err}")
                        except ValueError as ve:
                            if conn:
                                conn.rollback()
                            st.error(f"Valor inválido para saldo: {ve}")
                        finally:
                            if conn and conn.is_connected():
                                cursor.close()
                                conn.close()
    
    baixa_saldo(form_key_suffix)

if __name__ == '__main__':
    main("local")
