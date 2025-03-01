import streamlit as st
import mysql.connector

# Função para limpar todos os campos
def limpar_campos():
    for key in st.session_state:
        if key != 'id':
            st.session_state[key] = ''

# Função para buscar dados no banco de dados
def buscar_dados():
    id_registro = st.session_state['id']
    if id_registro:
        try:
            # Conectando ao banco de dados
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='@Kaclju2125.',
                database='bd_srtransporte'
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

# Campo: ID
id_registro = st.text_input("ID", key='id')

# Botão para buscar dados
if st.button("Buscar"):
    buscar_dados()

# Campo: Data
data = st.text_input("Data", key='data')

# Campo: Cliente
cliente = st.text_input("Cliente", key='cliente')

# Campo: Código do Cliente
cod_cliente = st.text_input("Código do Cliente", key='cod_cliente')

# Campo: Motorista
motorista = st.text_input("Motorista", key='motorista')

# Campo: Placa
placa = st.text_input("Placa", key='placa')

# Campo: Perfil do Veículo (Combobox)
perfil_vei = st.selectbox("Perfil do Veículo", ["3/4", "TOCO", "TRUCK"], key='perfil_vei')

# Campo: Modalidade (Combobox)
modalidade = st.selectbox("Modalidade", ["ABA", "VENDA"], key='modalidade')

# Campo: Minuta/CVia
minuta_cvia = st.text_input("Minuta/CVia", key='minuta_cvia')

# Campo: OT Viagem
ot_viagem = st.text_input("OT Viagem", key='ot_viagem')

# Campo: Cubagem
cubagem = st.text_input("Cubagem", key='cubagem')

# Campo: Rota
rota = st.text_input("Rota", key='rota')

# Campo: Valor da Carga
valor_carga = st.text_input("Valor da Carga", key='valor_carga')

# Campo: Descarga
descarga = st.text_input("Descarga", key='descarga')

# Campo: Adiantamento
adiantamento = st.text_input("Adiantamento", key='adiantamento')

# Botão: Enviar
if st.button("Enviar"):
    submit_data()

# Botão: Limpar Campos
if st.button("Limpar Campos"):
    limpar_campos()