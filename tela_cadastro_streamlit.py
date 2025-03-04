import streamlit as st
import mysql.connector
import pandas as pd

# Função para buscar todos os lançamentos no banco de dados
def buscar_todos_lancamentos():
    try:
        # Conectando ao banco de dados
        conn = mysql.connector.connect(
            user='root',  # Substitua pelo usuário do MySQL
            password='@Kaclju2125.',  # Substitua pela senha do MySQL
            host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
            port=19152,  # Porta gerada pelo Ngrok
            database='bd_srtransporte'  # Nome do banco de dados
        )
        cursor = conn.cursor()
        
        # Buscando todos os lançamentos no banco de dados
        query = """
            SELECT id, data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, 
                   minuta_cvia, ot_viagem, cubagem, rota, valor_carga, descarga, adiantamento, valor_frete
            FROM tela_inicial
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        # Convertendo os resultados em um DataFrame
        colunas = [
            'ID', 'Data', 'Cliente', 'Código do Cliente', 'Motorista', 'Placa', 'Perfil do Veículo', 
            'Modalidade', 'Minuta/CVia', 'OT Viagem', 'Cubagem', 'Rota', 'Valor da Carga', 
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
            # Conectando ao banco de dados
            conn = mysql.connector.connect(
                user='root',  # Substitua pelo usuário do MySQL
                password='@Kaclju2125.',  # Substitua pela senha do MySQL
                host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
                port=19152,  # Porta gerada pelo Ngrok
                database='bd_srtransporte'  # Nome do banco de dados
            )
            cursor = conn.cursor()
            
            # Buscando o lançamento no banco de dados
            query = """
                SELECT data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, 
                       minuta_cvia, ot_viagem, cubagem, rota, valor_carga, descarga, adiantamento, valor_frete
                FROM tela_inicial 
                WHERE id = %s
            """
            cursor.execute(query, (id_registro,))
            resultado = cursor.fetchone()
            
            if resultado:
                # Armazenando os dados encontrados no session_state
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
                st.session_state['rota'] = resultado[10]
                st.session_state['valor_carga'] = resultado[11]
                st.session_state['descarga'] = resultado[12]
                st.session_state['adiantamento'] = resultado[13]
                st.session_state['valor_frete'] = resultado[14]
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
    # Obtendo os valores dos campos
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
    rota = st.session_state.get('rota', '')
    valor_carga = st.session_state.get('valor_carga', '')
    descarga = st.session_state.get('descarga', '')
    adiantamento = st.session_state.get('adiantamento', '')
    valor_frete = st.session_state.get('valor_frete', '')
    
    # Verificando se todos os campos foram preenchidos
    if data and cliente and cod_cliente and motorista and placa and perfil_vei and modalidade and minuta_cvia and ot_viagem and cubagem and rota and valor_carga and descarga and adiantamento and valor_frete:
        try:
            # Conectando ao banco de dados
            conn = mysql.connector.connect(
                user='root',  # Substitua pelo usuário do MySQL
                password='@Kaclju2125.',  # Substitua pela senha do MySQL
                host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
                port=19152,  # Porta gerada pelo Ngrok
                database='bd_srtransporte'  # Nome do banco de dados
            )
            cursor = conn.cursor()
            
            # Verificando se o ID já existe (edição)
            if id_registro:
                query = """
                    UPDATE tela_inicial 
                    SET data = %s, cliente = %s, cod_cliente = %s, motorista = %s, placa = %s, perfil_vei = %s, 
                    modalidade = %s, minuta_cvia = %s, ot_viagem = %s, cubagem = %s, rota = %s, 
                    valor_carga = %s, descarga = %s, adiantamento = %s, valor_frete = %s
                    WHERE id = %s
                """
                values = (data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, minuta_cvia, ot_viagem, cubagem, rota, valor_carga, descarga, adiantamento, valor_frete, id_registro)
            else:
                # Inserindo um novo registro
                query = """
                    INSERT INTO tela_inicial 
                    (data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, minuta_cvia, ot_viagem, cubagem, rota, valor_carga, descarga, adiantamento, valor_frete) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, minuta_cvia, ot_viagem, cubagem, rota, valor_carga, descarga, adiantamento, valor_frete)
            
            cursor.execute(query, values)
            conn.commit()
            
            # Se for um novo registro, obter o ID gerado
            if not id_registro:
                id_registro = cursor.lastrowid
            
            cursor.close()
            conn.close()
            
            # Exibindo mensagem de sucesso
            st.success("Dados salvos com sucesso!")
            
            # Limpando os campos após o envio
            st.session_state.clear()  # Limpa o session_state
            st.session_state['id'] = id_registro  # Atualiza o ID no session_state
            st.experimental_rerun()  # Recarrega a página
        except Exception as e:
            st.error(f"Erro ao salvar dados: {str(e)}")  # Exibe o erro completo
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
    
    # Campo de consulta acima da tabela
    id_filtro = st.text_input("Filtrar por ID")
    
    # Busca todos os lançamentos
    df = buscar_todos_lancamentos()
    
    # Filtra a tabela se um ID for fornecido
    if id_filtro:
        df = df[df['ID'] == int(id_filtro)]
    
    # Exibe a tabela com todos os lançamentos
    if not df.empty:
        st.dataframe(df, height=500, use_container_width=True)  # Aumenta o tamanho da tabela
    else:
        st.warning("Nenhum lançamento encontrado.")

# Tela de Novo Cadastro
elif st.session_state['opcao'] == "Novo Cadastro":
    st.title("Cadastro de carregamento")
    
    # Campo: ID e Botão Buscar
    col1, col2 = st.columns([4, 1])  # Divide a linha em duas colunas
    with col1:
        id_registro = st.text_input("ID", key='id')
    with col2:
        st.write("")  # Espaçamento para alinhar o botão
        if st.button("Buscar"):
            buscar_lancamento_por_id(id_registro)
    
    # Campos lado a lado
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
    
    # Outros campos
    data = st.text_input("Data", value=st.session_state.get('data', ''), key='data')
    motorista = st.text_input("Motorista", value=st.session_state.get('motorista', ''), key='motorista')
    placa = st.text_input("Placa", value=st.session_state.get('placa', ''), key='placa')
    perfil_vei = st.selectbox(
        "Perfil do Veículo", 
        options=["", "3/4", "TOCO", "TRUCK"],  # Adiciona uma opção vazia
        index=0 if not st.session_state.get('perfil_vei') else ["", "3/4", "TOCO", "TRUCK"].index(st.session_state.get('perfil_vei')),
        key='perfil_vei'
    )
    modalidade = st.selectbox(
        "Modalidade", 
        options=["", "ABA", "VENDA"],  # Adiciona uma opção vazia
        index=0 if not st.session_state.get('modalidade') else ["", "ABA", "VENDA"].index(st.session_state.get('modalidade')),
        key='modalidade'
    )
    cubagem = st.text_input("Cubagem", value=st.session_state.get('cubagem', ''), key='cubagem')
    rota = st.text_input("Rota", value=st.session_state.get('rota', ''), key='rota')

    # Botão: Enviar
    if st.button("Enviar"):
        submit_data()
