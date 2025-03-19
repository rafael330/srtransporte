import streamlit as st
import mysql.connector
import pandas as pd

# Função para buscar todas as rotas e cidades da tabela cad_rota
def buscar_rotas_cidades():
    try:
        conn = mysql.connector.connect(
            user='rafael_logitech',  # Substitua pelo usuário do MySQL
            password='admin',  # Substitua pela senha do MySQL
            host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
            port=11804,  # Porta gerada pelo Ngrok
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
            user='rafael_logitech',  # Substitua pelo usuário do MySQL
            password='admin',  # Substitua pela senha do MySQL
            host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
            port=11804,  # Porta gerada pelo Ngrok
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
            user='rafael_logitech',  # Substitua pelo usuário do MySQL
            password='admin',  # Substitua pela senha do MySQL
            host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
            port=11804,  # Porta gerada pelo Ngrok
            database='bd_srtransporte'  # Nome do banco de dados
        )
        cursor = conn.cursor()
        
        query = """
            SELECT id, data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, minuta_ot,
                   id_carga_cvia, cubagem, rot_1, rot_2, cid_1, cid_2, mod_1, mod_2, valor_carga, descarga, adiantamento, valor_frete
            FROM tela_inicial
        """
        cursor.execute(query)
        resultados = cursor.fetchall()
        
        colunas = [
            'ID', 'Data', 'Cliente', 'Código do Cliente', 'Motorista', 'CPF do Motorista', 'Placa', 'Perfil do Veículo', 
            'Minuta/OT', 'ID carga / CVia', 'Cubagem', 'rot_1', 'rot_2', 'cid_1', 'cid_2', 'mod_1', 'mod_2', 'Valor da Carga', 
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
                user='rafael_logitech',  # Substitua pelo usuário do MySQL
                password='admin',  # Substitua pela senha do MySQL
                host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
                port=11804,  # Porta gerada pelo Ngrok
                database='bd_srtransporte'  # Nome do banco de dados
            )
            cursor = conn.cursor()
            
            query = """
                SELECT data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, 
                       minuta_ot, id_carga_cvia, cubagem, rot_1, rot_2, cid_1, cid_2, mod_1, mod_2, valor_carga, descarga, adiantamento, valor_frete
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
                st.session_state['cpf_motorista'] = resultado[4]  # Atualiza o CPF do motorista
                st.session_state['placa'] = resultado[5]
                st.session_state['perfil_vei'] = resultado[6]                
                st.session_state['minuta_ot'] = resultado[7]  # Alterado para minuta_ot
                st.session_state['id_carga_cvia'] = resultado[8]  # Alterado para id_carga_cvia
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
    minuta_ot = st.session_state.get('minuta_ot', '')  # Alterado para minuta_ot
    id_carga_cvia = st.session_state.get('id_carga_cvia', '')  # Alterado para id_carga_cvia
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
    
    # Verificando se todos os campos obrigatórios estão preenchidos
    campos_obrigatorios = [
        data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, 
        minuta_ot, id_carga_cvia, cubagem, valor_carga, descarga, adiantamento, valor_frete
    ]
    
    if all(campos_obrigatorios):  # Verifica se todos os campos obrigatórios estão preenchidos
        try:
            conn = mysql.connector.connect(
                user='rafael_logitech',  # Substitua pelo usuário do MySQL
                password='admin',  # Substitua pela senha do MySQL
                host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
                port=11804,  # Porta gerada pelo Ngrok
                database='bd_srtransporte'  # Nome do banco de dados
            )
            cursor = conn.cursor()
            
            if id_registro:
                query = """
                    UPDATE tela_inicial 
                    SET data = %s, cliente = %s, cod_cliente = %s, motorista = %s, cpf_motorista = %s, placa = %s, perfil_vei = %s
                    , minuta_ot = %s, id_carga_cvia = %s, cubagem = %s, rot_1 = %s, rot_2 = %s, cid_1 = %s, cid_2 = %s, mod_1 = %s, mod_2 = %s, valor_carga = %s, descarga = %s, adiantamento = %s, valor_frete = %s
                    WHERE id = %s
                """
                values = (
                    data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, 
                    minuta_ot, id_carga_cvia, cubagem, rot_1, rot_2, cid_1, cid_2, mod_1, mod_2, 
                    valor_carga, descarga, adiantamento, valor_frete, id_registro
                )
            else:
                query = """
                    INSERT INTO tela_inicial 
                    (data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, minuta_ot, id_carga_cvia, cubagem, rot_1, rot_2, cid_1, cid_2, mod_1, mod_2, valor_carga, descarga, adiantamento, valor_frete) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, 
                    minuta_ot, id_carga_cvia, cubagem, rot_1, rot_2, cid_1, cid_2, mod_1, mod_2, 
                    valor_carga, descarga, adiantamento, valor_frete
                )
            
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
        st.warning("Por favor, preencha todos os campos obrigatórios.")

# Função para gerar um novo ID automaticamente
def gerar_novo_id():
    try:
        conn = mysql.connector.connect(
            user='root',  # Substitua pelo usuário do MySQL
            password='@Kaclju2125.',  # Substitua pela senha do MySQL
            host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
            port=19156,  # Porta gerada pelo Ngrok
            database='bd_srtransporte'  # Nome do banco de dados
        )
        cursor = conn.cursor()
        
        # Busca o último ID inserido na tabela
        cursor.execute("SELECT MAX(id) FROM tela_inicial")
        ultimo_id = cursor.fetchone()[0]
        
        # Gera um novo ID (último ID + 1)
        novo_id = ultimo_id + 1 if ultimo_id else 1
        
        cursor.close()
        conn.close()
        
        return novo_id
    except mysql.connector.Error as err:
        st.error(f"Erro ao gerar novo ID: {err}")
        return None

# Inicialização do session_state
if 'id' not in st.session_state:
    st.session_state['id'] = ''  # ID inicialmente vazio
if 'modo_edicao' not in st.session_state:
    st.session_state['modo_edicao'] = False  # Indica se está em modo de edição

# Configuração da barra lateral
st.sidebar.title("Menu")
if st.sidebar.button("Novo Cadastro"):
    st.session_state['modo_edicao'] = False  # Modo de novo cadastro
    st.session_state['id'] = ''  # Limpa o ID para novo cadastro
if st.sidebar.button("Consulta/Edição"):
    st.session_state['modo_edicao'] = True  # Modo de edição

# Tela de Consulta/Edição
if st.session_state['modo_edicao']:
    st.title("Consulta/Edição de Lançamentos")
    
    # Campo para o usuário inserir o ID do lançamento
    id_registro = st.text_input("Informe o ID do lançamento para edição", key='id_edicao')
    
    # Botão para buscar o lançamento
    if st.button("Buscar Lançamento"):
        if id_registro:
            buscar_lancamento_por_id(id_registro)
            st.session_state['id'] = id_registro  # Atualiza o ID no session_state
        else:
            st.warning("Por favor, informe o ID do lançamento.")

# Tela de Novo Cadastro
else:
    st.title("Novo Cadastro de Carregamento")
    
    # Gera um novo ID automaticamente para novos cadastros
    if not st.session_state['id']:
        novo_id = gerar_novo_id()
        if novo_id:
            st.session_state['id'] = novo_id
    
    # Exibe o ID gerado automaticamente (somente leitura)
    st.text_input("ID (gerado automaticamente)", value=st.session_state['id'], key='id_novo', disabled=True)

# Campos do formulário (compartilhados entre novo cadastro e edição)
col1, col2 = st.columns(2)
with col1:
    cliente = st.text_input("Cliente", value=st.session_state.get('cliente', ''), key='cliente')
with col2:
    cod_cliente = st.text_input("Código do Cliente", value=st.session_state.get('cod_cliente', ''), key='cod_cliente')

# Outros campos do formulário (adicionar conforme necessário)
data = st.text_input("Data", value=st.session_state.get('data', ''), key='data')
motorista = st.text_input("Motorista", value=st.session_state.get('motorista', ''), key='motorista')
cpf_motorista = st.text_input("CPF do Motorista", value=st.session_state.get('cpf_motorista', ''), key='cpf_motorista')
placa = st.text_input("Placa", value=st.session_state.get('placa', ''), key='placa')
perfil_vei = st.selectbox(
    "Perfil do Veículo", 
    options=["", "3/4", "TOCO", "TRUCK"],
    index=safe_index(["", "3/4", "TOCO", "TRUCK"], st.session_state.get('perfil_vei', '')),
    key='perfil_vei'
)
cubagem = st.text_input("Cubagem", value=st.session_state.get('cubagem', ''), key='cubagem')

# Botão para enviar os dados
if st.button("Enviar"):
    submit_data()
