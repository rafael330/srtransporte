import streamlit as st
import mysql.connector

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

def cadastro_financeiro():
    st.title("Cadastro Financeiro")
    
    # Inicializa session_state
    if 'minuta_ot_financeiro' not in st.session_state:
        st.session_state.minuta_ot_financeiro = ""
    if 'valor_frete_pago' not in st.session_state:
        st.session_state.valor_frete_pago = ""
    if 'descontos' not in st.session_state:
        st.session_state.descontos = ""
    if 'acerto' not in st.session_state:
        st.session_state.acerto = ""
    if 'adiantamento' not in st.session_state:
        st.session_state.adiantamento = ""
    if 'observacoes' not in st.session_state:
        st.session_state.observacoes = ""

    # Função para buscar minuta_ot pelo ID
    def buscar_minuta_por_id(id_registro):
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT minuta_ot FROM tela_inicial WHERE id = %s"
                cursor.execute(query, (id_registro,))
                resultado = cursor.fetchone()
                cursor.close()
                conn.close()
                return resultado[0] if resultado else ""
            except mysql.connector.Error as err:
                st.error(f"Erro ao buscar minuta: {err}")
        return ""

    # Layout do formulário
    col1, col2 = st.columns(2)
    
    with col1:
        # Campo ID
        id_registro = st.text_input("ID* (obrigatório)", key='id_financeiro', value=st.session_state.get('id_financeiro', ''))
        
        # Busca automática da Minuta/OT quando o ID é alterado
        if id_registro and id_registro != st.session_state.get('last_id_financeiro', ''):
            st.session_state.minuta_ot_financeiro = buscar_minuta_por_id(id_registro)
            st.session_state.last_id_financeiro = id_registro
            if id_registro and not st.session_state.minuta_ot_financeiro:
                st.warning("Nenhuma minuta encontrada para este ID")

    with col2:
        # Campo Minuta/OT (preenchido automaticamente)
        st.text_input(
            "Minuta/OT", 
            value=st.session_state.minuta_ot_financeiro,
            key='display_minuta_ot_financeiro',
            disabled=True
        )

    # Campos financeiros
    col1, col2 = st.columns(2)
    with col1:
        valor_frete_pago = st.text_input("Valor do Frete (pago)", key='valor_frete_pago', value=st.session_state.valor_frete_pago)
    with col2:
        descontos = st.text_input("Descontos", key='descontos', value=st.session_state.descontos)

    # Campos Acerto e Adiantamento lado a lado
    col1, col2 = st.columns(2)
    with col1:
        acerto = st.text_input("Acerto (Despesa extra)", key='acerto', value=st.session_state.acerto)
    with col2:
        adiantamento = st.text_input("Adiantamento", key='adiantamento', value=st.session_state.adiantamento)

    observacoes = st.text_area("Observações gerais", key='observacoes', value=st.session_state.observacoes)

    # Botão de salvar
    if st.button("Salvar_financeiro"):
        with st.spinner("Salvando dados...", show_time=True):
            # Validação dos campos obrigatórios
            if not id_registro:
                st.error("O campo ID é obrigatório")
                return
            
            # Prepara dados para salvar
            dados = {
                'id': id_registro,
                'minuta_ot': st.session_state.minuta_ot_financeiro,
                'valor_frete_pago': valor_frete_pago,
                'descontos': descontos,
                'acerto': acerto,
                'adiantamento': adiantamento,
                'observacoes': observacoes
            }

            # Conecta ao banco e salva
            conn = conectar_banco()
            if conn:
                try:
                    cursor = conn.cursor()
                    
                    # Verifica se é atualização ou inserção
                    cursor.execute("SELECT id FROM tela_fin WHERE id = %s", (id_registro,))
                    existe = cursor.fetchone()
                    
                    if existe:
                        # Atualiza registro existente
                        query = """
                            UPDATE tela_fin SET
                                minuta_ot = %s,
                                valor_frete_pago = %s,
                                descontos = %s,
                                acerto = %s,
                                adiantamento = %s,
                                observacoes = %s
                            WHERE id = %s
                        """
                        cursor.execute(query, (
                            dados['minuta_ot'],
                            dados['valor_frete_pago'],
                            dados['descontos'],
                            dados['acerto'],
                            dados['adiantamento'],
                            dados['observacoes'],
                            dados['id']
                        ))
                    else:
                        # Insere novo registro
                        query = """
                            INSERT INTO tela_fin (
                                id, minuta_ot, valor_frete_pago, descontos, acerto, adiantamento, observacoes
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(query, (
                            dados['id'],
                            dados['minuta_ot'],
                            dados['valor_frete_pago'],
                            dados['descontos'],
                            dados['acerto'],
                            dados['adiantamento'],
                            dados['observacoes']
                        ))
                    
                    conn.commit()
                    st.success("Dados salvos com sucesso!")
                    
                    # Limpa todos os campos após salvar
                    st.session_state.clear()
                    st.rerun()
                    
                except mysql.connector.Error as err:
                    conn.rollback()
                    st.error(f"Erro ao salvar dados: {err}")
                finally:
                    if conn.is_connected():
                        cursor.close()
                        conn.close()

cadastro_financeiro()   