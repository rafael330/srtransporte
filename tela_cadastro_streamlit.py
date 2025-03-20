import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        conn = mysql.connector.connect(
            user='rafael_logitech',  # Usuário do MySQL
            password='admin',  # Senha do MySQL
            host='0.tcp.sa.ngrok.io',  # Endereço público gerado pelo Ngrok
            port=11804,  # Porta gerada pelo Ngrok
            database='bd_srtransporte'  # Nome do banco de dados
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao banco de dados: {err}")
        return None

# Função para buscar clientes e seus códigos
def buscar_clientes():
    conn = conectar_banco()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT cliente, cod_cliente FROM cad_cliente"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()
            return {cliente: cod_cliente for cliente, cod_cliente in resultados}
        except mysql.connector.Error as err:
            st.error(f"Erro ao buscar clientes: {err}")
    return {}

# Função para buscar motoristas e seus CPFs
def buscar_motoristas():
    conn = conectar_banco()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT nome, cpf FROM cad_mot"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()
            return {nome: cpf for nome, cpf in resultados}
        except mysql.connector.Error as err:
            st.error(f"Erro ao buscar motoristas: {err}")
    return {}

# Função para buscar placas e perfis de veículos
def buscar_placas():
    conn = conectar_banco()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT placa, perfil FROM cad_vei"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()
            return {placa: perfil for placa, perfil in resultados}
        except mysql.connector.Error as err:
            st.error(f"Erro ao buscar placas: {err}")
    return {}

# Função para buscar rotas e cidades
def buscar_rotas_cidades():
    conn = conectar_banco()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT rota, cidade FROM cad_rota"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()
            return resultados
        except mysql.connector.Error as err:
            st.error(f"Erro ao buscar rotas e cidades: {err}")
    return []

# Função para buscar todos os lançamentos no banco de dados
def buscar_todos_lancamentos(filtro_id=None, filtro_data=None):
    conn = conectar_banco()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT id, data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, minuta_ot,
                       id_carga_cvia, cubagem, rot_1, rot_2, cid_1, cid_2, mod_1, mod_2, valor_carga, descarga, adiantamento, valor_frete
                FROM tela_inicial
            """
            if filtro_id:
                query += " WHERE id = %s"
                cursor.execute(query, (filtro_id,))
            elif filtro_data:
                # Converte a data para o formato YYYY-MM-DD
                data_formatada = filtro_data.strftime("%Y-%m-%d")
                st.write(f"Data usada no filtro: {data_formatada}")  # Log para depuração
                query += " WHERE data = %s"
                cursor.execute(query, (data_formatada,))
            else:
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
        conn = conectar_banco()
        if conn:
            try:
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
                    st.session_state.update({
                        'data': resultado[0],
                        'cliente': resultado[1],
                        'cod_cliente': resultado[2],
                        'motorista': resultado[3],
                        'cpf_motorista': resultado[4],
                        'placa': resultado[5],
                        'perfil_vei': resultado[6],
                        'minuta_ot': resultado[7],
                        'id_carga_cvia': resultado[8],
                        'cubagem': resultado[9],
                        'rot_1': resultado[10],
                        'rot_2': resultado[11],
                        'cid_1': resultado[12],
                        'cid_2': resultado[13],
                        'mod_1': resultado[14],
                        'mod_2': resultado[15],
                        'valor_carga': resultado[16],
                        'descarga': resultado[17],
                        'adiantamento': resultado[18],
                        'valor_frete': resultado[19]
                    })
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
    campos_obrigatorios = [
        st.session_state.get('data', ''),
        st.session_state.get('cliente', ''),
        st.session_state.get('cod_cliente', ''),
        st.session_state.get('motorista', ''),
        st.session_state.get('cpf_motorista', ''),
        st.session_state.get('placa', ''),
        st.session_state.get('perfil_vei', ''),
        st.session_state.get('minuta_ot', ''),
        st.session_state.get('id_carga_cvia', ''),
        st.session_state.get('cubagem', ''),
        st.session_state.get('valor_carga', ''),
        st.session_state.get('descarga', ''),
        st.session_state.get('adiantamento', ''),
        st.session_state.get('valor_frete', '')
    ]
    
    if all(campos_obrigatorios):
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                id_registro = st.session_state.get('id', '')
                values = (
                    st.session_state['data'], st.session_state['cliente'], st.session_state['cod_cliente'],
                    st.session_state['motorista'], st.session_state['cpf_motorista'], st.session_state['placa'],
                    st.session_state['perfil_vei'], st.session_state['minuta_ot'], st.session_state['id_carga_cvia'],
                    st.session_state['cubagem'], st.session_state['rot_1'], st.session_state['rot_2'],
                    st.session_state['cid_1'], st.session_state['cid_2'], st.session_state['mod_1'],
                    st.session_state['mod_2'], st.session_state['valor_carga'], st.session_state['descarga'],
                    st.session_state['adiantamento'], st.session_state['valor_frete']
                )
                if id_registro:
                    query = """
                        UPDATE tela_inicial 
                        SET data = %s, cliente = %s, cod_cliente = %s, motorista = %s, cpf_motorista = %s, placa = %s, perfil_vei = %s,
                            minuta_ot = %s, id_carga_cvia = %s, cubagem = %s, rot_1 = %s, rot_2 = %s, cid_1 = %s, cid_2 = %s, mod_1 = %s, mod_2 = %s, valor_carga = %s, descarga = %s, adiantamento = %s, valor_frete = %s
                        WHERE id = %s
                    """
                    cursor.execute(query, values + (id_registro,))
                else:
                    query = """
                        INSERT INTO tela_inicial 
                        (data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, minuta_ot, id_carga_cvia, cubagem, rot_1, rot_2, cid_1, cid_2, mod_1, mod_2, valor_carga, descarga, adiantamento, valor_frete) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, values)
                    id_registro = cursor.lastrowid
                conn.commit()
                cursor.close()
                conn.close()
                st.success("Dados salvos com sucesso!")
                st.session_state.clear()  # Limpa os campos após o envio
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Erro ao salvar dados: {str(e)}")
    else:
        st.warning("Por favor, preencha todos os campos obrigatórios.")

# Inicializando o session_state
if 'opcao' not in st.session_state:
    st.session_state['opcao'] = "Novo Cadastro"
if 'id' not in st.session_state:
    st.session_state['id'] = ''
if 'data' not in st.session_state:
    st.session_state['data'] = ''
if 'cliente' not in st.session_state:
    st.session_state['cliente'] = ''
if 'cod_cliente' not in st.session_state:
    st.session_state['cod_cliente'] = ''
if 'motorista' not in st.session_state:
    st.session_state['motorista'] = ''
if 'cpf_motorista' not in st.session_state:
    st.session_state['cpf_motorista'] = ''
if 'placa' not in st.session_state:
    st.session_state['placa'] = ''
if 'perfil_vei' not in st.session_state:
    st.session_state['perfil_vei'] = ''
if 'minuta_ot' not in st.session_state:
    st.session_state['minuta_ot'] = ''
if 'id_carga_cvia' not in st.session_state:
    st.session_state['id_carga_cvia'] = ''
if 'cubagem' not in st.session_state:
    st.session_state['cubagem'] = ''
if 'rot_1' not in st.session_state:
    st.session_state['rot_1'] = ''
if 'rot_2' not in st.session_state:
    st.session_state['rot_2'] = ''
if 'cid_1' not in st.session_state:
    st.session_state['cid_1'] = ''
if 'cid_2' not in st.session_state:
    st.session_state['cid_2'] = ''
if 'mod_1' not in st.session_state:
    st.session_state['mod_1'] = ''
if 'mod_2' not in st.session_state:
    st.session_state['mod_2'] = ''
if 'valor_carga' not in st.session_state:
    st.session_state['valor_carga'] = ''
if 'descarga' not in st.session_state:
    st.session_state['descarga'] = ''
if 'adiantamento' not in st.session_state:
    st.session_state['adiantamento'] = ''
if 'valor_frete' not in st.session_state:
    st.session_state['valor_frete'] = ''

# Configurando a barra lateral com botões
st.sidebar.title("Menu")
if st.sidebar.button("Novo Cadastro"):
    st.session_state['opcao'] = "Novo Cadastro"
    st.session_state.clear()
    st.session_state['opcao'] = "Novo Cadastro"  # Re-inicializa a opção
if st.sidebar.button("Consulta de Cadastro"):
    st.session_state['opcao'] = "Consulta de Cadastro"
    st.session_state.clear()
    st.session_state['opcao'] = "Consulta de Cadastro"  # Re-inicializa a opção

# Tela de Consulta de Cadastro
if st.session_state['opcao'] == "Consulta de Cadastro":
    st.title("Consulta de Cadastro")
    
    col1, col2 = st.columns(2)
    with col1:
        id_registro = st.text_input("Informe o ID do lançamento", key='id_edicao')
    with col2:
        filtro_data = st.date_input("Filtrar por data de lançamento", value=st.session_state.get('filtro_data', None), key='filtro_data')
    
    if st.button("Buscar"):
        if id_registro:
            df = buscar_todos_lancamentos(filtro_id=id_registro)
        elif filtro_data:
            df = buscar_todos_lancamentos(filtro_data=filtro_data)
        else:
            df = buscar_todos_lancamentos()
        
        if not df.empty:
            st.dataframe(df, height=500, use_container_width=True)
        else:
            st.warning("Nenhum lançamento encontrado.")
            
# Tela de Novo Cadastro
elif st.session_state['opcao'] == "Novo Cadastro":
    st.title("Novo Cadastro de Carregamento")
    
    # Campo ID (para correções)
    id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id')
    
    # Buscar clientes, motoristas, placas e rotas
    clientes = buscar_clientes()
    motoristas = buscar_motoristas()
    placas = buscar_placas()
    rotas_cidades = buscar_rotas_cidades()
    rotas = list(set([rc[0] for rc in rotas_cidades]))
    cidades = list(set([rc[1] for rc in rotas_cidades]))
    
    col1, col2 = st.columns(2)
    with col1:
        cliente = st.selectbox(
            "Cliente",
            options=[""] + list(clientes.keys()),
            index=0,
            key='cliente'
        )
        if cliente:
            st.session_state['cod_cliente'] = clientes.get(cliente, '')
    with col2:
        cod_cliente = st.text_input(
            "Código do Cliente",
            value=st.session_state.get('cod_cliente', ''),
            key='cod_cliente',
            disabled=True
        )
    
    col1, col2 = st.columns(2)
    with col1:
        motorista = st.selectbox(
            "Motorista",
            options=[""] + list(motoristas.keys()),
            index=0,
            key='motorista'
        )
        if motorista:
            st.session_state['cpf_motorista'] = motoristas.get(motorista, '')
    with col2:
        cpf_motorista = st.text_input(
            "CPF do Motorista",
            value=st.session_state.get('cpf_motorista', ''),
            key='cpf_motorista',
            disabled=True
        )
    
    col1, col2 = st.columns(2)
    with col1:
        placa = st.selectbox(
            "Placa",
            options=[""] + list(placas.keys()),
            index=0,
            key='placa'
        )
        if placa:
            st.session_state['perfil_vei'] = placas.get(placa, '')
    with col2:
        perfil_vei = st.text_input(
            "Perfil do Veículo",
            value=st.session_state.get('perfil_vei', ''),
            key='perfil_vei',
            disabled=True
        )
    
    col1, col2 = st.columns(2)
    with col1:
        minuta_ot = st.text_input("Minuta/OT", value=st.session_state.get('minuta_ot', ''), key='minuta_ot')
    with col2:
        id_carga_cvia = st.text_input("ID carga / CVia", value=st.session_state.get('id_carga_cvia', ''), key='id_carga_cvia')
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        valor_carga = st.text_input("Valor da Carga", value=st.session_state.get('valor_carga', ''), key='valor_carga')
    with col2:
        valor_frete = st.text_input("Valor do Frete", value=st.session_state.get('valor_frete', ''), key='valor_frete')
    with col3:
        descarga = st.text_input("Descarga", value=st.session_state.get('descarga', ''), key='descarga')
    with col4:
        adiantamento = st.text_input("Adiantamento", value=st.session_state.get('adiantamento', ''), key='adiantamento')
    
    #data = st.text_input("Data", value=st.session_state.get('data', ''), key='data')
    data = st.date_input("Data", value=datetime.now().date(), key='filtro_data')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        rot_1 = st.selectbox(
            "Rota 1",
            options=[""] + rotas,
            index=0,
            key='rot_1'
        )
    with col2:
        cid_1 = st.selectbox(
            "Cidade 1",
            options=[""] + cidades,
            index=0,
            key='cid_1'
        )
    with col3:
        mod_1 = st.selectbox(
            "Modalidade 1",
            options=["", "ABA", "VENDA"],
            index=0,
            key='mod_1'
        )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        rot_2 = st.selectbox(
            "Rota 2",
            options=[""] + rotas,
            index=0,
            key='rot_2'
        )
    with col2:
        cid_2 = st.selectbox(
            "Cidade 2",
            options=[""] + cidades,
            index=0,
            key='cid_2'
        )
    with col3:
        mod_2 = st.selectbox(
            "Modalidade 2",
            options=["", "ABA", "VENDA"],
            index=0,
            key='mod_2'
        )
    
    cubagem = st.text_input("Cubagem", value=st.session_state.get('cubagem', ''), key='cubagem')
    
    if st.button("Enviar"):
        submit_data()
