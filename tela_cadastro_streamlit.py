import streamlit as st
import mysql.connector
import pandas as pd

# Função para buscar todas as rotas e cidades da tabela cad_rota
def buscar_rotas_cidades():
    try:
        conn = mysql.connector.connect(
            user='root',  # Substitua pelo usuário do MySQL
            password='admin',  # Substitua pela senha do MySQL
            host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
            port=19250,  # Porta gerada pelo Ngrok
            database='bd_srtransporte'  # Nome do banco de dados
        )
        cursor = conn.cursor()
        
        # Buscando todas as rotas e cidades
        query = "SELECT rota, cidade FROM cad_rota"
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Convertendo os resultados em uma lista de tuplas (rota, cidade)
        return resultados
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar rotas e cidades: {err}")
        return []

# Função para buscar todos os motoristas e seus CPFs da tabela cad_mot
def buscar_motoristas():
    try:
        conn = mysql.connector.connect(
            user='root',  # Substitua pelo usuário do MySQL
            password='admin',  # Substitua pela senha do MySQL
            host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
            port=19250,  # Porta gerada pelo Ngrok
            database='bd_srtransporte'  # Nome do banco de dados
        )
        cursor = conn.cursor()
        
        # Buscando todos os motoristas e seus CPFs
        query = "SELECT nome, cpf FROM cad_mot"
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Convertendo os resultados em um dicionário {nome: cpf}
        return {nome: cpf for nome, cpf in resultados}
    except mysql.connector.Error as err:
        st.error(f"Erro ao buscar motoristas: {err}")
        return {}

# Função para buscar todos os lançamentos no banco de dados
def buscar_todos_lancamentos():
    try:
        conn = mysql.connector.connect(
            user='root',  # Substitua pelo usuário do MySQL
            password='admin',  # Substitua pela senha do MySQL
            host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
            port=19250,  # Porta gerada pelo Ngrok
            database='bd_srtransporte'  # Nome do banco de dados
        )
        cursor = conn.cursor()
        
        query = """
            SELECT id, data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, minuta_cvia,
                   ot_viagem, cubagem, rot_1, rot_2, cid_1, cid_2, mod_1, mod_2, valor_carga, descarga, adiantamento, valor_frete
            FROM tela_inicial
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        colunas = [
            'ID', 'Data', 'Cliente', 'Código do Cliente', 'Motorista', 'CPF do Motorista', 'Placa', 'Perfil do Veículo', 
            'Minuta/CVia', 'OT Viagem', 'Cubagem', 'rot_1', 'rot_2', 'cid_1', 'cid_2', 'mod_1', 'mod_2', 'Valor da Carga', 
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
                password='admin',  # Substitua pela senha do MySQL
                host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
                port=19250,  # Porta gerada pelo Ngrok
                database='bd_srtransporte'  # Nome do banco de dados
            )
            cursor = conn.cursor()
            
            query = """
                SELECT data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, 
                       minuta_cvia, ot_viagem, cubagem, rot_1, rot_2, cid_1, cid_2, mod_1, mod_2, valor_carga, descarga, adiantamento, valor_frete
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
                st.session_state['cpf_motorista'] = resultado[4]
                st.session_state['placa'] = resultado[5]
                st.session_state['perfil_vei'] = resultado[6]                
                st.session_state['minuta_cvia'] = resultado[7]
                st.session_state['ot_viagem'] = resultado[8]
                st.session_state['cubagem'] = resultado[9]
                st.session_state['rot_1'] = resultado[10]
                st.session_state['rot_2'] = resultado[11]
                st.session_state['cid_1'] = resultado[12]
                st.session_state['cid_2'] = resultado[13]
                st.session_state['mod_1'] = resultado[14]
                st.session_state['mod_2'] = resultado[15]
                st.session_state['valor_carga'] = resultado[16]
                st.session_state['descarga'] = resultado[17]
                st.session_state['adiantamento'] = resultado[18]
                st.session_state['valor_frete'] = resultado[19]
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
    cpf_motorista = st.session_state.get('cpf_motorista', '')
    placa = st.session_state.get('placa', '')
    perfil_vei = st.session_state.get('perfil_vei', '')    
    minuta_cvia = st.session_state.get('minuta_cvia', '')
    ot_viagem = st.session_state.get('ot_viagem', '')
    cubagem = st.session_state.get('cubagem', '')
    rot_1 = st.session_state.get('rot_1', '')
    rot_2 = st.session_state.get('rot_2', '')
    cid_1 = st.session_state.get('cid_1', '')
    cid_2 = st.session_state.get('cid_2', '')
    mod_1 = st.session_state.get('mod_1', '')
    mod_2 = st.session_state.get('mod_2', '')
    valor_carga = st.session_state.get('valor_carga', '')
    descarga = st.session_state.get('descarga', '')
    adiantamento = st.session_state.get('adiantamento', '')
    valor_frete = st.session_state.get('valor_frete', '')
    
    # Verificando se os campos de rota, cidade e modalidade estão vazios
    rot_1 = rot_1 if rot_1 else None
    rot_2 = rot_2 if rot_2 else None
    cid_1 = cid_1 if cid_1 else None
    cid_2 = cid_2 if cid_2 else None
    mod_1 = mod_1 if mod_1 else None
    mod_2 = mod_2 if mod_2 else None
    
    if data and cliente and cod_cliente and motorista and cpf_motorista and placa and perfil_vei and minuta_cvia and ot_viagem and cubagem and valor_carga and descarga and adiantamento and valor_frete:
        try:
            conn = mysql.connector.connect(
                user='root',  # Substitua pelo usuário do MySQL
                password='admin',  # Substitua pela senha do MySQL
                host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
                port=19250,  # Porta gerada pelo Ngrok
                database='bd_srtransporte'  # Nome do banco de dados
            )
            cursor = conn.cursor()
            
            if id_registro:
                query = """
                    UPDATE tela_inicial 
                    SET data = %s, cliente = %s, cod_cliente = %s, motorista = %s, cpf_motorista = %s, placa = %s, perfil_vei = %s
                    , minuta_cvia = %s, ot_viagem = %s, cubagem = %s, rot_1 = %s, rot_2 = %s, cid_1 = %s, cid_2 = %s, mod_1 = %s, mod_2 = %s, valor_carga = %s, descarga = %s, adiantamento = %s, valor_frete = %s
                    WHERE id = %s
                """
                values = (data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, minuta_cvia, ot_viagem, cubagem, rot_1, rot_2, cid_1, cid_2, mod_1, mod_2, valor_carga, descarga, adiantamento, valor_frete, id_registro)
            else:
                query = """
                    INSERT INTO tela_inicial 
                    (data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, minuta_cvia, ot_viagem, cubagem, rot_1, rot_2, cid_1, cid_2, mod_1, mod_2, valor_carga, descarga, adiantamento, valor_frete) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, minuta_cvia, ot_viagem, cubagem, rot_1, rot_2, cid_1, cid_2, mod_1, mod_2, valor_carga, descarga, adiantamento, valor_frete)
            
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

# Função para encontrar o índice seguro
def safe_index(options, value):
    try:
        return options.index(value) if value in options else 0
    except ValueError:
        return 0

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
    
    # Buscar os motoristas e seus CPFs
    motoristas = buscar_motoristas()
    motorista_nomes = list(motoristas.keys())
    
    col1, col2 = st.columns(2)
    with col1:
        motorista = st.selectbox(
            "Motorista",
            options=[""] + motorista_nomes,  # Adiciona uma opção vazia no início
            index=safe_index(motorista_nomes, st.session_state.get('motorista', '')),
            key='motorista'
        )
    with col2:
        cpf_motorista = st.text_input(
            "CPF do Motorista",
            value=motoristas.get(st.session_state.get('motorista', ''), ''),  # Autopreenche o CPF apenas se for um novo cadastro
            key='cpf_motorista'
        )
    
    placa = st.text_input("Placa", value=st.session_state.get('placa', ''), key='placa')
    perfil_vei = st.selectbox(
        "Perfil do Veículo", 
        options=["", "3/4", "TOCO", "TRUCK"],
        index=safe_index(["", "3/4", "TOCO", "TRUCK"], st.session_state.get('perfil_vei', '')),
        key='perfil_vei'
    )
    cubagem = st.text_input("Cubagem", value=st.session_state.get('cubagem', ''), key='cubagem')
    
    # Buscar as rotas e cidades disponíveis
    rotas_cidades = buscar_rotas_cidades()
    rotas = list(set([rc[0] for rc in rotas_cidades]))  # Valores únicos para rotas
    cidades = list(set([rc[1] for rc in rotas_cidades]))  # Valores únicos para cidades
    
    # Definir as modalidades
    modalidades = ["VENDA", "ABA"]  # Opções de modalidade
    
    # Campos de Rota, Cidade e Modalidade lado a lado
    col1, col2, col3 = st.columns(3)
    with col1:
        rot_1 = st.selectbox(
            "Rota 1",
            options=[""] + rotas,  # Adiciona uma opção vazia no início
            index=0,  # Inicia com a opção vazia
            key='rot_1'
        )
    with col2:
        cid_1 = st.selectbox(
            "Cidade 1",
            options=[""] + cidades,  # Adiciona uma opção vazia no início
            index=0,  # Inicia com a opção vazia
            key='cid_1'
        )
    with col3:
        mod_1 = st.selectbox(
            "Modalidade 1",
            options=[""] + modalidades,  # Adiciona uma opção vazia no início
            index=0,  # Inicia com a opção vazia
            key='mod_1'
        )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        rot_2 = st.selectbox(
            "Rota 2",
            options=[""] + rotas,  # Adiciona uma opção vazia no início
            index=0,  # Inicia com a opção vazia
            key='rot_2'
        )
    with col2:
        cid_2 = st.selectbox(
            "Cidade 2",
            options=[""] + cidades,  # Adiciona uma opção vazia no início
            index=0,  # Inicia com a opção vazia
            key='cid_2'
        )
    with col3:
        mod_2 = st.selectbox(
            "Modalidade 2",
            options=[""] + modalidades,  # Adiciona uma opção vazia no início
            index=0,  # Inicia com a opção vazia
            key='mod_2'
        )
    
    if st.button("Enviar"):
        submit_data()
