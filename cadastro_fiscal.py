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

def cadastro_fiscal():
    st.title("Cadastro Fiscal")
    
    # Inicializa session_state
    if 'minuta_ot_fiscal' not in st.session_state:
        st.session_state.minuta_ot_fiscal = ""
    if 'cliente_fiscal' not in st.session_state:
        st.session_state.cliente_fiscal = ""
    if 'cod_cliente_fiscal' not in st.session_state:
        st.session_state.cod_cliente_fiscal = ""
    if 'valor_carga_fiscal' not in st.session_state:
        st.session_state.valor_carga_fiscal = ""
    if 'valor_frete_fiscal' not in st.session_state:
        st.session_state.valor_frete_fiscal = ""

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

    # Função para buscar clientes e códigos
    def buscar_clientes_e_codigos():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                query = "SELECT cliente, cod_cliente FROM cad_cliente"
                cursor.execute(query)
                resultados = cursor.fetchall()
                cursor.close()
                conn.close()
                return resultados
            except mysql.connector.Error as err:
                st.error(f"Erro ao buscar clientes: {err}")
        return []

    # Busca clientes e códigos
    clientes_e_codigos = buscar_clientes_e_codigos()
    clientes = [""] + [cliente[0] for cliente in clientes_e_codigos]
    cliente_para_codigo = {cliente[0]: cliente[1] for cliente in clientes_e_codigos}

    # Layout do formulário
    col1, col2 = st.columns(2)
    
    with col1:
        # Campo ID
        id_registro = st.text_input("ID* (obrigatório)", key='id_fiscal', value=st.session_state.get('id_fiscal', ''))
        
        # Busca automática da Minuta/OT quando o ID é alterado
        if id_registro and id_registro != st.session_state.get('last_id_fiscal', ''):
            st.session_state.minuta_ot_fiscal = buscar_minuta_por_id(id_registro)
            st.session_state.last_id_fiscal = id_registro
            if id_registro and not st.session_state.minuta_ot_fiscal:
                st.warning("Nenhuma minuta encontrada para este ID")

    with col2:
        # Campo Minuta/OT (preenchido automaticamente)
        st.text_input(
            "Minuta/OT", 
            value=st.session_state.minuta_ot_fiscal,
            key='display_minuta_ot',
            disabled=True
        )

    # Selectbox para cliente
    cliente_selecionado = st.selectbox(
        "Cliente",
        options=clientes,
        index=clientes.index(st.session_state.cliente_fiscal) if st.session_state.cliente_fiscal in clientes else 0,
        key='select_cliente'
    )
    
    # Atualiza código do cliente quando o cliente muda
    if cliente_selecionado != st.session_state.get('last_cliente', ''):
        st.session_state.cod_cliente_fiscal = cliente_para_codigo.get(cliente_selecionado, "")
        st.session_state.last_cliente = cliente_selecionado

    # Código do cliente (preenchido automaticamente)
    st.text_input(
        "Código do Cliente",
        value=st.session_state.cod_cliente_fiscal,
        key='display_cod_cliente',
        disabled=True
    )

    # Campos de valores
    col1, col2 = st.columns(2)
    with col1:
        valor_carga = st.text_input("Valor da Carga", key='valor_carga_fiscal', value=st.session_state.valor_carga_fiscal)
    with col2:
        valor_frete = st.text_input("Valor do Frete", key='valor_frete_fiscal', value=st.session_state.valor_frete_fiscal)

    # Botão de salvar
    if st.button("Salvar_fiscal"):
        with st.spinner("Salvando dados...", show_time=True):
            # Validação dos campos obrigatórios
            if not id_registro:
                st.error("O campo ID é obrigatório")
                return
                
            # Prepara dados para salvar
            dados = {
                'id': id_registro,
                'minuta_ot': st.session_state.minuta_ot_fiscal,
                'cliente': cliente_selecionado,
                'cod_cliente': st.session_state.cod_cliente_fiscal,
                'valor_carga': valor_carga,
                'valor_frete': valor_frete
            }

            # Conecta ao banco e salva
            conn = conectar_banco()
            if conn:
                try:
                    cursor = conn.cursor()
                    
                    # Verifica se é atualização ou inserção
                    cursor.execute("SELECT id FROM tela_fis WHERE id = %s", (id_registro,))
                    existe = cursor.fetchone()
                    
                    if existe:
                        # Atualiza registro existente
                        query = """
                            UPDATE tela_fis SET
                                minuta_ot = %s,
                                cliente = %s,
                                cod_cliente = %s,
                                valor_carga = %s,
                                valor_frete = %s
                            WHERE id = %s
                        """
                        cursor.execute(query, (
                            dados['minuta_ot'],
                            dados['cliente'],
                            dados['cod_cliente'],
                            dados['valor_carga'],
                            dados['valor_frete'],
                            dados['id']
                        ))
                    else:
                        # Insere novo registro
                        query = """
                            INSERT INTO tela_fis (
                                id, minuta_ot, cliente, cod_cliente, valor_carga, valor_frete
                            ) VALUES (%s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(query, (
                            dados['id'],
                            dados['minuta_ot'],
                            dados['cliente'],
                            dados['cod_cliente'],
                            dados['valor_carga'],
                            dados['valor_frete']
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

cadastro_fiscal()   