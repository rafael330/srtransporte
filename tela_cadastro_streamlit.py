import streamlit as st
import mysql.connector

# Função para limpar todos os campos
def limpar_campos():
    # Lista de todas as chaves no session_state que devem ser limpas
    campos_para_limpar = [
        'id', 'data', 'cliente', 'cod_cliente', 'motorista', 'placa',
        'perfil_vei', 'modalidade', 'minuta_cvia', 'ot_viagem', 'cubagem',
        'rota', 'valor_carga', 'descarga', 'adiantamento'
    ]
    
    # Limpa os valores dos campos no session_state
    for campo in campos_para_limpar:
        st.session_state[campo] = ""  # Define o valor como vazio

# Função para buscar dados no banco de dados
def buscar_dados():
    id_registro = st.session_state['id']
    if id_registro:
        try:
            # Conectando ao banco de dados
            conn = mysql.connector.connect(
                user='root',  # Substitua pelo usuário do MySQL
                password='@Kaclju2125.',  # Substitua pela senha do MySQL
                host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
                port=11658,  # Porta gerada pelo Ngrok
                database='bd_srtransporte',  # Adicionei uma vírgula aqui
                unix_socket=None  # Força a conexão TCP/IP
            )
            cursor = conn.cursor()
            
            # Buscando os dados no banco de dados
            query = """
                SELECT data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, 
                       minuta_cvia, ot_viagem, cubagem, rota, valor_carga, descarga, adiantamento
                FROM tela_inicial 
                WHERE id = %s
            """
            cursor.execute(query, (id_registro,))
            resultado = cursor.fetchone()
            
            if resultado:
                # Preenchendo os campos com os dados encontrados
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
    id_registro = st.session_state['id']
    data = st.session_state['data']
    cliente = st.session_state['cliente']
    cod_cliente = st.session_state['cod_cliente']
    motorista = st.session_state['motorista']
    placa = st.session_state['placa']
    perfil_vei = st.session_state['perfil_vei']
    modalidade = st.session_state['modalidade']
    minuta_cvia = st.session_state['minuta_cvia']
    ot_viagem = st.session_state['ot_viagem']
    cubagem = st.session_state['cubagem']
    rota = st.session_state['rota']
    valor_carga = st.session_state['valor_carga']
    descarga = st.session_state['descarga']
    adiantamento = st.session_state['adiantamento']
    
    # Verificando se todos os campos foram preenchidos
    if data and cliente and cod_cliente and motorista and placa and perfil_vei and modalidade and minuta_cvia and ot_viagem and cubagem and rota and valor_carga and descarga and adiantamento:
        try:
            # Conectando ao banco de dados
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='@Kaclju2125.',
                database='bd_srtransporte'
            )
            cursor = conn.cursor()
            
            # Verificando se o ID já existe (edição)
            if id_registro:
                query = """
                    UPDATE tela_inicial 
                    SET data = %s, cliente = %s, cod_cliente = %s, motorista = %s, placa = %s, perfil_vei = %s, 
                    modalidade = %s, minuta_cvia = %s, ot_viagem = %s, cubagem = %s, rota = %s, 
                    valor_carga = %s, descarga = %s, adiantamento = %s
                    WHERE id = %s
                """
                values = (data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, minuta_cvia, ot_viagem, cubagem, rota, valor_carga, descarga, adiantamento, id_registro)
            else:
                # Inserindo um novo registro
                query = """
                    INSERT INTO tela_inicial 
                    (data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, minuta_cvia, ot_viagem, cubagem, rota, valor_carga, descarga, adiantamento) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (data, cliente, cod_cliente, motorista, placa, perfil_vei, modalidade, minuta_cvia, ot_viagem, cubagem, rota, valor_carga, descarga, adiantamento)
            
            cursor.execute(query, values)
            conn.commit()
            
            # Se for um novo registro, obter o ID gerado
            if not id_registro:
                id_registro = cursor.lastrowid
                st.session_state['id'] = id_registro
            
            cursor.close()
            conn.close()
            
            # Exibindo mensagem de sucesso
            st.success("Dados salvos com sucesso!")
            
            # Limpando os campos após o envio
            limpar_campos()
        except mysql.connector.Error as err:
            st.error(f"Erro ao salvar dados: {err}")
    else:
        st.warning("Por favor, preencha todos os campos.")

# Configurando a interface gráfica no Streamlit
st.title("Cadastro de carregamento")

# Campo: ID e Botão Buscar
col1, col2 = st.columns([4, 1])  # Divide a linha em duas colunas
with col1:
    id_registro = st.text_input("ID", key='id')
with col2:
    st.write("")  # Espaçamento para alinhar o botão
    if st.button("Buscar"):
        buscar_dados()

# Campo: Data
data = st.text_input("Data", key='data')

# Campos: Cliente e Código do Cliente (lado a lado)
col3, col4 = st.columns(2)  # Divide a linha em duas colunas
with col3:
    cliente = st.text_input("Cliente", key='cliente')
with col4:
    cod_cliente = st.text_input("Código do Cliente", key='cod_cliente')

# Campo: Motorista
motorista = st.text_input("Motorista", key='motorista')

# Campo: Placa
placa = st.text_input("Placa", key='placa')

# Campo: Perfil do Veículo (Combobox)
perfil_vei = st.selectbox(
    "Perfil do Veículo", 
    options=["", "3/4", "TOCO", "TRUCK"],  # Adiciona uma opção vazia
    key='perfil_vei',
    index=0  # Nenhuma opção selecionada por padrão
)

# Campo: Modalidade (Combobox)
modalidade = st.selectbox(
    "Modalidade", 
    options=["", "ABA", "VENDA"],  # Adiciona uma opção vazia
    key='modalidade',
    index=0  # Nenhuma opção selecionada por padrão
)

# Campos: Minuta/CVia e OT Viagem (lado a lado)
col5, col6 = st.columns(2)  # Divide a linha em duas colunas
with col5:
    minuta_cvia = st.text_input("Minuta/CVia", key='minuta_cvia')
with col6:
    ot_viagem = st.text_input("OT Viagem", key='ot_viagem')

# Campo: Cubagem
cubagem = st.text_input("Cubagem", key='cubagem')

# Campo: Rota
rota = st.text_input("Rota", key='rota')

# Campo: Valor da Carga
valor_carga = st.text_input("Valor da Carga", key='valor_carga')

# Campos: Descarga e Adiantamento (lado a lado)
col7, col8 = st.columns(2)  # Divide a linha em duas colunas
with col7:
    descarga = st.text_input("Descarga", key='descarga')
with col8:
    adiantamento = st.text_input("Adiantamento", key='adiantamento')

# Botão: Enviar
if st.button("Enviar"):
    submit_data()

# Botão: Limpar Campos
if st.button("Limpar Campos"):
    limpar_campos()
