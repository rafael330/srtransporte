import streamlit as st
import mysql.connector
import pandas as pd

# Função para buscar todas as rotas e cidades da tabela cad_rota
def buscar_rotas_cidades():
    try:
        conn = mysql.connector.connect(
            user='root',  # Substitua pelo usuário do MySQL
            password='@Kaclju2125.',  # Substitua pela senha do MySQL
            host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
            port=19156,  # Porta gerada pelo Ngrok
            database='bd_srtransporte'  # Nome do banco de dados
        )
        cursor = conn.cursor()
        
        # Buscando todas as rotas e cidades
        query = "SELECT rota, cidade FROM cad_rota"
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Convertendo os resultados em listas únicas
        rotas = list(set([rc[0] for rc in resultados]))  # Valores únicos para rotas
        cidades = list(set([rc[1] for rc in resultados]))  # Valores únicos para cidades
        
        return rotas, cidades
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar rotas e cidades: {err}")
        return [], []

# Função para buscar todos os lançamentos no banco de dados
def buscar_todos_lancamentos():
    try:
        conn = mysql.connector.connect(
            user='root',  # Substitua pelo usuário do MySQL
            password='@Kaclju2125.',  # Substitua pela senha do MySQL
            host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
            port=19156,  # Porta gerada pelo Ngrok
            database='bd_srtransporte'  # Nome do banco de dados
        )
        cursor = conn.cursor()
        
        # Verifique se os nomes das colunas estão corretos (rot_1, cid_1, etc.)
        query = """
            SELECT id, data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, 
                   minuta_cvia, ot_viagem, cubagem, rot_1, rot_2, cid_1, cid_2, valor_carga, descarga, adiantamento, valor_frete
            FROM tela_inicial
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        colunas = [
            'ID', 'Data', 'Cliente', 'Código do Cliente', 'Motorista', 'Placa', 'Perfil do Veículo', 
            'Modalidade', 'Minuta/CVia', 'OT Viagem', 'Cubagem', 'rot_1', 'rot_2', 'cid_1', 'cid_2', 'Valor da Carga', 
            'Descarga', 'Adiantamento', 'Valor do Frete'
        ]
        df = pd.DataFrame(resultados, columns=colunas)
        
        cursor.close()
        conn.close()
        
        return df
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar dados: {err}")
        return pd.DataFrame()

# Função para buscar um lançamento pelo ID
def buscar_lancamento_por_id(id_registro):
    if id_registro:
        try:
            conn = mysql.connector.connect(
                user='root',  # Substitua pelo usuário do MySQL
                password='@Kaclju2125.',  # Substitua pela senha do MySQL
                host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
                port=19156,  # Porta gerada pelo Ngrok
                database='bd_srtransporte'  # Nome do banco de dados
            )
            cursor = conn.cursor()
            
            query = """
                SELECT data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, 
                       minuta_cvia, ot_viagem, cubagem, rot_1, rot_2, cid_1, cid_2, valor_carga, descarga, adiantamento, valor_frete
                FROM tela_inicial 
                WHERE id = %s
            """
            cursor.execute(query, (id_registro,))
            resultado = cursor.fetchone()
            
            if resultado:
                st.session_state['data'] = resultado[0]
                st.session_state['cliente'] = resultado[1]
                st.session_state['cod_cliente'] = resultado[2]
                st.session_state['motorista'] = resultado[3]
                st.session_state['placa'] = resultado[4]
                st.session_state['perfil_vei'] = resultado[5]
                st.session_state['modalidade'] = resultado[6]
                st.session_state['minuta_cvia'] = resultado[7]
                st.session_state['ot_viagem'] = resultado[8]
                st.session_state['cubagem'] = resultado[9]
                st.session_state['rot_1'] = resultado[10]
                st.session_state['rot_2'] = resultado[11]
                st.session_state['cid_1'] = resultado[12]
                st.session_state['cid_2'] = resultado[13]
                st.session_state['valor_carga'] = resultado[15]
                st.session_state['descarga'] = resultado[16]
                st.session_state['adiantamento'] = resultado[17]
                st.session_state['valor_frete'] = resultado[18]
            else:
                st.warning("Nenhum registro encontrado com esse ID.")
            
            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            st.error(f"Erro ao buscar dados: {err}")
    else:
        st.warning("Por favor, informe o ID.")

# Função para enviar dados (inserir ou atualizar)
def submit_data():
    id_registro = st.session_state.get('id', '')
    data = st.session_state.get('data', '')
    cliente = st.session_state.get('cliente', '')
    cod_cliente = st.session_state.get('cod_cliente', '')
    motorista = st.session_state.get('motorista', '')
    placa = st.session_state.get('placa', '')
    perfil_vei = st.session_state.get('perfil_vei', '')
    modalidade = st.session_state.get('modalidade', '')
    minuta_cvia = st.session_state.get('minuta_cvia', '')
    ot_viagem = st.session_state.get('ot_viagem', '')
    cubagem = st.session_state.get('cubagem', '')
    rot_1 = st.session_state.get('rot_1', '')
    rot_2 = st.session_state.get('rot_2', '')
    cid_1 = st.session_state.get('cid_1', '')
    cid_2 = st.session_state.get('cid_2', '')
    valor_carga = st.session_state.get('valor_carga', '')
    descarga = st.session_state.get('descarga', '')
    adiantamento = st.session_state.get('adiantamento', '')
    valor_frete = st.session_state.get('valor_frete', '')
    
    if data and cliente and cod_cliente and motorista and placa and perfil_vei and modalidade and minuta_cvia and ot_viagem and cubagem and rot_1 and rot_2 and cid_1 and cid_2 and valor_carga and descarga and adiantamento and valor_frete:
        try:
            conn = mysql.connector.connect(
                user='root',  # Substitua pelo usuário do MySQL
                password='@Kaclju2125.',  # Substitua pela senha do MySQL
                host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
                port=19156,  # Porta gerada pelo Ngrok
                database='bd_srtransporte'  # Nome do banco de dados
            )
            cursor = conn.cursor()
            
            if id_registro:
                query = """
                    UPDATE tela_inicial 
                    SET data = %s, cliente = %s, cod_cliente = %s, motorista = %s, placa = %s, perfil_vei = %s, 
                    modalidade = %s, minuta_cvia = %s, ot_viagem = %s, cubagem = %s, rot_1 = %s, rot_2 = %s, cid_1 = %s, cid_2 = %s, 
                    valor_carga = %s, descarga = %s, adiantamento = %s, valor_frete = %s
                    WHERE id = %s
                """
                values = (data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, minuta_cvia, ot_viagem, cubagem, rot_1, rot_2, cid_1, cid_2, valor_carga, descarga, adiantamento, valor_frete, id_registro)
            else:
                query = """
                    INSERT INTO tela_inicial 
                    (data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, minuta_cvia, ot_viagem, cubagem, rot_1, rot_2, cid_1, cid_2, valor_carga, descarga, adiantamento, valor_frete) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, minuta_cvia, ot_viagem, cubagem, rot_1, rot_2, cid_1, cid_2, valor_carga, descarga, adiantamento, valor_frete)
            
            cursor.execute(query, values)
            conn.commit()
            
            if not id_registro:
                id_registro = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            st.success("Dados salvos com sucesso!")
            st.session_state.clear()
            st.session_state['id'] = id_registro
            st.experimental_rerun()
        except Exception as e:
            st.error(f"Erro ao salvar dados: {str(e)}")
    else:
        st.warning("Por favor, preencha todos os campos.")

# Inicializando o session_state
if 'opcao' not in st.session_state:
    st.session_state['opcao'] = "Consulta"

# Configurando a barra lateral com botões
st.sidebar.title("Menu")
if st.sidebar.button("Novo Cadastro"):
    st.session_state['opcao'] = "Novo Cadastro"
if st.sidebar.button("Consulta"):
    st.session_state['opcao'] = "Consulta"

# Tela de Consulta
if st.session_state['opcao'] == "Consulta":
    st.title("Consulta de Lançamentos")
    
    id_filtro = st.text_input("Filtrar por ID")
    
    df = buscar_todos_lancamentos()
    
    if id_filtro:
        df = df[df['ID'] == int(id_filtro)]
    
    if not df.empty:
        st.dataframe(df, height=500, use_container_width=True)
    else:
        st.warning("Nenhum lançamento encontrado.")

# Tela de Novo Cadastro
elif st.session_state['opcao'] == "Novo Cadastro":
    st.title("Cadastro de carregamento")
    
    col1, col2 = st.columns([4, 1])
    with col1:
        id_registro = st.text_input("ID", key='id')
    with col2:
        st.write("")
        if st.button("Buscar"):
            buscar_lancamento_por_id(id_registro)
    
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.text_input("Cliente", value=st.session_state.get('cliente', ''), key='cliente')
    with col2:
        cod_cliente = st.text_input("Código do Cliente", value=st.session_state.get('cod_cliente', ''), key='cod_cliente')
    
    col1, col2 = st.columns(2)
    with col1:
        minuta_cvia = st.text_input("Minuta/CVia", value=st.session_state.get('minuta_cvia', ''), key='minuta_cvia')
    with col2:
        ot_viagem = st.text_input("OT Viagem", value=st.session_state.get('ot_viagem', ''), key='ot_viagem')
    
    col1, col2 = st.columns(2)
    with col1:
        valor_carga = st.text_input("Valor da Carga", value=st.session_state.get('valor_carga', ''), key='valor_carga')
    with col2:
        valor_frete = st.text_input("Valor do Frete", value=st.session_state.get('valor_frete', ''), key='valor_frete')
    
    col1, col2 = st.columns(2)
    with col1:
        descarga = st.text_input("Descarga", value=st.session_state.get('descarga', ''), key='descarga')
    with col2:
        adiantamento = st.text_input("Adiantamento", value=st.session_state.get('adiantamento', ''), key='adiantamento')
    
    data = st.text_input("Data", value=st.session_state.get('data', ''), key='data')
    motorista = st.text_input("Motorista", value=st.session_state.get('motorista', ''), key='motorista')
    placa = st.text_input("Placa", value=st.session_state.get('placa', ''), key='placa')
    perfil_vei = st.selectbox(
        "Perfil do Veículo", 
        options=["", "3/4", "TOCO", "TRUCK"],
        index=0 if not st.session_state.get('perfil_vei') else ["", "3/4", "TOCO", "TRUCK"].index(st.session_state.get('perfil_vei')),
        key='perfil_vei'
    )
    modalidade = st.selectbox(
        "Modalidade", 
        options=["", "ABA", "VENDA"],
        index=0 if not st.session_state.get('modalidade') else ["", "ABA", "VENDA"].index(st.session_state.get('modalidade')),
        key='modalidade'
    )
    cubagem = st.text_input("Cubagem", value=st.session_state.get('cubagem', ''), key='cubagem')
    
    # Buscar as rotas e cidades disponíveis
    rotas, cidades = buscar_rotas_cidades()
    
    # Campos de Rota e Cidade lado a lado
    col1, col2 = st.columns(2)
    with col1:
        rot_1 = st.selectbox("Rota 1", options=rotas, index=None, key='rot_1')
    with col2:
        cid_1 = st.selectbox("Cidade 1", options=cidades, index=None, key='cid_1')
    
    col1, col2 = st.columns(2)
    with col1:
        rot_2 = st.selectbox("Rota 2", options=rotas, index=None, key='rot_2')
    with col2:
        cid_2 = st.selectbox("Cidade 2", options=cidades, index=None, key='cid_2')

    if st.button("Enviar"):
        submit_data()
