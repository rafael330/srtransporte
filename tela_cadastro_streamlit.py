import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

# Função para conectar ao banco de dados
def conectar_banco():
    try:
        conn = mysql.connector.connect(
            user='logitech_rafael',  # Usuário do MySQL
            password='admin000',  # Senha do MySQL
            host='db4free.net',  # Endereço público gerado pelo Ngrok
            port=3306,  # Porta gerada pelo Ngrok
            database= 'srtransporte'  # Nome do banco de dados
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Erro ao conectar ao banco de dados: {err}")
        return None

def salvar_dados(tabela, campos, valores, id_registro):
    conn = conectar_banco()
    if not conn:
        st.error("Erro ao conectar ao banco de dados.")
        return

    try:
        cursor = conn.cursor()
        if id_registro:
            # Atualiza o registro existente
            query = f"UPDATE {tabela} SET {', '.join([f'{campo} = %s' for campo in campos])} WHERE id = %s"
            cursor.execute(query, valores + (id_registro,))
        else:
            # Insere um novo registro
            query = f"INSERT INTO {tabela} ({', '.join(campos)}) VALUES ({', '.join(['%s'] * len(campos))})"
            cursor.execute(query, valores)

        conn.commit()
        cursor.close()
        conn.close()
        st.success("Dados salvos com sucesso!")
        
        # Limpa o session_state após o salvamento
        st.session_state.clear()  # Limpa todos os campos
        st.experimental_rerun()  # Recarrega a página para garantir que os campos fiquem vazios
    except mysql.connector.Error as err:
        st.error(f"Erro ao salvar dados no banco de dados: {err}")
    except Exception as e:
        st.error(f"Erro inesperado: {str(e)}")

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

# Função para buscar placas, perfis e proprietários de veículos
def buscar_placas():
    conn = conectar_banco()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT placa, perfil, proprietario FROM cad_vei"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()
            return {placa: {'perfil': perfil, 'proprietario': proprietario} for placa, perfil, proprietario in resultados}
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
                SELECT id, data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, proprietario_vei, minuta_ot,
                       id_carga_cvia, cubagem, rot_1, cid_1, mod_1
                FROM tela_inicial
            """
            if filtro_id:
                query += " WHERE id = %s"
                cursor.execute(query, (filtro_id,))            
            else:
                cursor.execute(query)
            
            resultados = cursor.fetchall()
            colunas = [
                'ID', 'Data', 'Cliente', 'Código do Cliente', 'Motorista', 'CPF do Motorista', 'Placa', 
                'Perfil do Veículo', 'Proprietário', 'Minuta/OT', 'ID carga / CVia', 'Cubagem', 
                'rot_1', 'cid_1', 'mod_1'
            ]
            df = pd.DataFrame(resultados, columns=colunas)
            df['ID'] = df['ID'].replace(',','')
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
                    SELECT data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, proprietario_vei,
                           minuta_ot, id_carga_cvia, cubagem, rot_1, cid_1, mod_1
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
                        'proprietario_vei': resultado[7],
                        'minuta_ot': resultado[8],
                        'id_carga_cvia': resultado[9],
                        'cubagem': resultado[10],
                        'rot_1': resultado[11],                        
                        'cid_1': resultado[12],                        
                        'mod_1': resultado[13]                        
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
    # Lista de campos obrigatórios
    campos_obrigatorios = {
        'data': st.session_state.get('data', ''),
        'cliente': st.session_state.get('cliente', ''),
        'cod_cliente': st.session_state.get('cod_cliente', ''),
        'motorista': st.session_state.get('motorista', ''),
        'cpf_motorista': st.session_state.get('cpf_motorista', ''),
        'placa': st.session_state.get('placa', ''),
        'perfil_vei': st.session_state.get('perfil_vei', ''),
        'proprietario_vei': st.session_state.get('proprietario_vei', ''),
        'minuta_ot': st.session_state.get('minuta_ot', ''),
        'id_carga_cvia': st.session_state.get('id_carga_cvia', ''),
        'cubagem': st.session_state.get('cubagem', '')
    }

    # Verifica se todos os campos obrigatórios foram preenchidos
    campos_vazios = [campo for campo, valor in campos_obrigatorios.items() if not valor]
    
    if campos_vazios:
        st.warning(f"Os seguintes campos obrigatórios não foram preenchidos: {', '.join(campos_vazios)}")
        return  # Interrompe a execução se houver campos obrigatórios vazios

    # Converte a data do formato brasileiro (dd/mm/aaaa) para o formato MySQL (aaaa-mm-dd)
    try:
        data_brasileira = st.session_state['data']
        data_mysql = datetime.strptime(data_brasileira, "%d/%m/%Y").strftime("%Y-%m-%d")
    except ValueError:
        st.error("Formato de data inválido. Use o formato dd/mm/aaaa.")
        return

    # Conecta ao banco de dados
    conn = conectar_banco()
    if not conn:
        st.error("Erro ao conectar ao banco de dados.")
        return

    try:
        cursor = conn.cursor()
        id_registro = st.session_state.get('id', '')

        # Valores a serem inseridos ou atualizados
        values = (
            data_mysql, st.session_state['cliente'], st.session_state['cod_cliente'],
            st.session_state['motorista'], st.session_state['cpf_motorista'], st.session_state['placa'],
            st.session_state['perfil_vei'], st.session_state['proprietario_vei'], st.session_state['minuta_ot'], 
            st.session_state['id_carga_cvia'], st.session_state['cubagem'], st.session_state['rot_1'], 
            st.session_state['cid_1'], st.session_state['mod_1']
        )

        # Se houver um ID, atualiza o registro existente
        if id_registro:
            query = """
                UPDATE tela_inicial 
                SET data = %s, cliente = %s, cod_cliente = %s, motorista = %s, cpf_motorista = %s, placa = %s, 
                    perfil_vei = %s, proprietario_vei = %s, minuta_ot = %s, id_carga_cvia = %s, cubagem = %s, 
                    rot_1 = %s, cid_1 = %s, mod_1 = %s
                WHERE id = %s
            """
            cursor.execute(query, values + (id_registro,))
        else:
            # Caso contrário, insere um novo registro
            query = """
                INSERT INTO tela_inicial 
                (data, cliente, cod_cliente, motorista, cpf_motorista, placa, perfil_vei, proprietario_vei, 
                 minuta_ot, id_carga_cvia, cubagem, rot_1, cid_1, mod_1) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, values)

        conn.commit()  # Confirma a transação
        cursor.close()
        conn.close()

        st.success("Dados salvos com sucesso!")
        st.session_state.clear()  # Limpa os campos após o envio
        st.experimental_rerun()  # Recarrega a página para limpar o formulário
    except mysql.connector.Error as err:
        st.error(f"Erro ao salvar dados no banco de dados: {err}")
    except Exception as e:
        st.error(f"Erro inesperado: {str(e)}")

# Função para buscar cargas
def buscar_cargas():
    conn = conectar_banco()
    if conn:
        try:
            cursor = conn.cursor()
            query = "SELECT DISTINCT id_carga_cvia FROM tela_inicial"
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            conn.close()
            return [carga[0] for carga in resultados]
        except mysql.connector.Error as err:
            st.error(f"Erro ao buscar cargas: {err}")
    return []

# Função para cadastro de cliente
def cadastro_cliente():
    st.title("Cadastro de Cliente")
    
    id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id_cliente')
    cod_cliente = st.text_input("Código do Cliente", key='cod_cliente')
    cliente = st.text_input("Cliente", key='cliente')
    cnpj = st.text_input("CNPJ", key='cnpj')

    if st.button("Salvar"):
        campos = ['cod_cliente', 'cliente', 'cnpj']
        valores = (cod_cliente, cliente, cnpj)
        salvar_dados('cad_cliente', campos, valores, id_registro)
        # Limpa os campos após o salvamento
        st.session_state['id_cliente'] = None
        st.session_state['cod_cliente'] = None
        st.session_state['cliente'] = None
        st.session_state['cnpj'] = None

# Função para cadastro de motorista
def cadastro_motorista():
    st.title("Cadastro de Motorista")
    
    id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id_motorista')
    motorista = st.text_input("Motorista", key='motorista')
    cpf = st.text_input("CPF", key='cpf')
    rg = st.text_input("RG", key='rg')

    if st.button("Salvar"):
        campos = ['nome', 'cpf', 'rg']
        valores = (motorista, cpf, rg)
        salvar_dados('cad_mot', campos, valores, id_registro)
        # Limpa os campos após o salvamento
        st.session_state['id_motorista'] = None
        st.session_state['motorista'] = None
        st.session_state['cpf'] = None
        st.session_state['rg'] = None

# Função para cadastro de rota
def cadastro_rota():
    st.title("Cadastro de Rota")
    
    id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id_rota')
    rota = st.text_input("Rota", key='rota')
    cidade = st.text_input("Cidade", key='cidade')
    regiao = st.text_input("Região", key='regiao')
    cep_unico = st.text_input("CEP Único", key='cep_unico')

    if st.button("Salvar"):
        campos = ['rota', 'cidade', 'regiao', 'cep_unico']
        valores = (rota, cidade, regiao, cep_unico)
        salvar_dados('cad_rota', campos, valores, id_registro)
        # Limpa os campos após o salvamento
        st.session_state['id_rota'] = None
        st.session_state['rota'] = None
        st.session_state['cidade'] = None
        st.session_state['regiao'] = None
        st.session_state['cep_unico'] = None

# Função para cadastro de veículo
def cadastro_veiculo():
    st.title("Cadastro de Veículo")
    
    id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id_veiculo')
    placa = st.text_input("Placa", key='placa')
    perfil = st.text_input("Perfil", key='perfil')
    proprietario = st.text_input("Proprietário", key='proprietario')
    cubagem = st.text_input("Cubagem", key='cubagem')

    if st.button("Salvar"):
        campos = ['placa', 'perfil', 'proprietario', 'cubagem']
        valores = (placa, perfil, proprietario, cubagem)
        salvar_dados('cad_vei', campos, valores, id_registro)
        # Limpa os campos após o salvamento
        st.session_state['id_veiculo'] = None
        st.session_state['placa'] = None
        st.session_state['perfil'] = None
        st.session_state['proprietario'] = None
        st.session_state['cubagem'] = None

# Função para cadastro de frete extra
def cadastro_frete_extra():
    st.title("Cadastro de Frete Extra")
    
    id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id_frete_extra')
    cliente = st.selectbox("Cliente", options=[""] + list(buscar_clientes().keys()), key='cliente_frete')
    data = st.text_input("Data (Formato: dd/mm/aaaa)", key='data_frete')
    id_carga = st.selectbox("ID Carga", options=[""] + buscar_cargas(), key='id_carga_frete')
    rota = st.selectbox("Rota", options=[""] + [rota[1] for rota in buscar_rotas_cidades()], key='rota_frete')
    entrega_final = st.text_input("Entrega Final", key='entrega_final')
    valor = st.text_input("Valor", key='valor_frete')

    if st.button("Salvar"):
        campos = ['cliente', 'data', 'id_carga', 'rota', 'entrega_final', 'valor']
        valores = (cliente, data, id_carga, rota, entrega_final, valor)
        salvar_dados('cad_frete_extra', campos, valores, id_registro)
        # Limpa os campos após o salvamento
        st.session_state['id_frete_extra'] = None
        st.session_state['cliente_frete'] = None
        st.session_state['data_frete'] = None
        st.session_state['id_carga_frete'] = None
        st.session_state['rota_frete'] = None
        st.session_state['entrega_final'] = None
        st.session_state['valor_frete'] = None

# Função para cadastro fiscal
def cadastro_fiscal():
    st.title("Cadastro Fiscal")
    
    id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id_fiscal')
    minuta_ot = st.text_input("Minuta/OT", key='minuta_ot_fiscal')
    valor_carga = st.text_input("Valor da Carga", key='valor_carga_fiscal')
    valor_frete = st.text_input("Valor do Frete", key='valor_frete_fiscal')

    if st.button("Salvar"):
        campos = ['minuta_ot', 'valor_carga', 'valor_frete']
        valores = (minuta_ot, valor_carga, valor_frete)
        salvar_dados('tela_fis', campos, valores, id_registro)
        # Limpa os campos após o salvamento
        st.session_state['id_fiscal'] = None
        st.session_state['minuta_ot_fiscal'] = None
        st.session_state['valor_carga_fiscal'] = None
        st.session_state['valor_frete_fiscal'] = None

# Função para cadastro financeiro
def cadastro_financeiro():
    st.title("Cadastro Financeiro")
    
    id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id_financeiro')
    minuta_ot = st.text_input("Minuta/OT", key='minuta_ot_financeiro')
    valor_frete_pago = st.text_input("Valor do Frete (pago)", key='valor_frete_pago')
    descontos = st.text_input("Descontos", key='descontos')
    acerto = st.text_input("Acerto (Despesa extra)", key='acerto')
    observacoes = st.text_area("Observações gerais", key='observacoes')

    if st.button("Salvar"):
        campos = ['minuta_ot', 'valor_frete_pago', 'descontos', 'acerto', 'observacoes']
        valores = (minuta_ot, valor_frete_pago, descontos, acerto, observacoes)
        salvar_dados('tela_fin', campos, valores, id_registro)
        # Limpa os campos após o salvamento
        st.session_state['id_financeiro'] = None
        st.session_state['minuta_ot_financeiro'] = None
        st.session_state['valor_frete_pago'] = None
        st.session_state['descontos'] = None
        st.session_state['acerto'] = None
        st.session_state['observacoes'] = None

# Função para baixa financeira
def baixa_financeira():
    st.title("Baixa Financeira")
    
    uploaded_file = st.file_uploader("Carregar arquivo XLSX", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.write("Pré-visualização dos dados:")
            st.dataframe(df)
            
            if st.button("Importar dados"):
                conn = conectar_banco()
                if conn:
                    try:
                        cursor = conn.cursor()
                        for _, row in df.iterrows():
                            query = """
                                INSERT INTO baixa_financeira 
                                (campo1, campo2, campo3) 
                                VALUES (%s, %s, %s)
                            """
                            # Ajuste os campos e valores conforme a estrutura do seu arquivo
                            cursor.execute(query, (row[0], row[1], row[2]))
                        
                        conn.commit()
                        cursor.close()
                        conn.close()
                        st.success("Dados importados com sucesso!")
                    except mysql.connector.Error as err:
                        st.error(f"Erro ao importar dados: {err}")
        except Exception as e:
            st.error(f"Erro ao ler o arquivo: {str(e)}")

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
if 'proprietario_vei' not in st.session_state:
    st.session_state['proprietario_vei'] = ''
if 'minuta_ot' not in st.session_state:
    st.session_state['minuta_ot'] = ''
if 'id_carga_cvia' not in st.session_state:
    st.session_state['id_carga_cvia'] = ''
if 'cubagem' not in st.session_state:
    st.session_state['cubagem'] = ''
if 'rot_1' not in st.session_state:
    st.session_state['rot_1'] = ''
if 'cid_1' not in st.session_state:
    st.session_state['cid_1'] = ''
if 'mod_1' not in st.session_state:
    st.session_state['mod_1'] = ''

# Configurando a barra lateral com botões
st.sidebar.title("Menu")
opcao = st.sidebar.radio("Selecione uma opção", [
    "Novo Cadastro", "Consulta de Cadastro", "Cadastro de Cliente", 
    "Cadastro de Motorista", "Cadastro de Rota", "Cadastro de Veículo", 
    "Cadastro de Frete Extra", "Cadastro Fiscal", "Cadastro Financeiro",
    "Baixa Financeira"
])

# Redirecionamento para a tela selecionada
if opcao == "Novo Cadastro":
    st.title("Novo Cadastro de Carregamento")
    
    # Campo ID (para correções)
    id_registro = st.text_input("ID (deixe vazio para novo cadastro)", key='id')
    
    # Buscar clientes, motoristas, placas e rotas
    clientes = buscar_clientes()
    motoristas = buscar_motoristas()
    placas_info = buscar_placas()
    placas = list(placas_info.keys())
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
    
    col1, col2, col3 = st.columns(3)
    with col1:
        placa = st.selectbox(
            "Placa",
            options=[""] + placas,
            index=0,
            key='placa'
        )
        if placa:
            st.session_state['perfil_vei'] = placas_info.get(placa, {}).get('perfil', '')
            st.session_state['proprietario_vei'] = placas_info.get(placa, {}).get('proprietario', '')
    with col2:
        perfil_vei = st.text_input(
            "Perfil do Veículo",
            value=st.session_state.get('perfil_vei', ''),
            key='perfil_vei',
            disabled=True
        )
    with col3:
        proprietario_vei = st.text_input(
            "Proprietário do Veículo",
            value=st.session_state.get('proprietario_vei', ''),
            key='proprietario_vei',
            disabled=True
        )
    
    col1, col2 = st.columns(2)
    with col1:
        minuta_ot = st.text_input("Minuta/OT", value=st.session_state.get('minuta_ot', ''), key='minuta_ot')
    with col2:
        id_carga_cvia = st.text_input("ID carga / CVia", value=st.session_state.get('id_carga_cvia', ''), key='id_carga_cvia')
    
    # Campo de data no formato brasileiro (dd/mm/aaaa)
    data = st.text_input("Data (Formato: dd/mm/aaaa)", key='data')
    
    col1, col2, col3 = st.columns(3)
    with col1:
        rot_1 = st.selectbox(
            "Rota",
            options=[""] + rotas,
            index=0,
            key='rot_1'
        )
    with col2:
        cid_1 = st.selectbox(
            "Cidade",
            options=[""] + cidades,
            index=0,
            key='cid_1'
        )
    with col3:
        mod_1 = st.selectbox(
            "Modalidade",
            options=["", "ABA", "VENDA"],
            index=0,
            key='mod_1'
        )
        
    cubagem = st.text_input("Cubagem", value=st.session_state.get('cubagem', ''), key='cubagem')
    
    if st.button("Enviar"):
        submit_data()

elif opcao == "Consulta de Cadastro":
    st.title("Consulta de Cadastro")
    
    # Campo para inserir o ID do lançamento
    id_registro = st.text_input("Informe o ID do lançamento", key='id_edicao')
    
    # Botão para buscar os lançamentos
    if st.button("Buscar"):
        if id_registro:
            # Busca pelo ID do lançamento
            df = buscar_todos_lancamentos(filtro_id=id_registro)
        else:
            # Busca todos os lançamentos
            df = buscar_todos_lancamentos()
        
        # Exibe os resultados
        if not df.empty:
            st.dataframe(df, height=500, use_container_width=True)
        else:
            st.warning("Nenhum lançamento encontrado.")

elif opcao == "Cadastro de Cliente":
    cadastro_cliente()

elif opcao == "Cadastro de Motorista":
    cadastro_motorista()

elif opcao == "Cadastro de Rota":
    cadastro_rota()

elif opcao == "Cadastro de Veículo":
    cadastro_veiculo()

elif opcao == "Cadastro de Frete Extra":
    cadastro_frete_extra()

elif opcao == "Cadastro Fiscal":
    cadastro_fiscal()

elif opcao == "Cadastro Financeiro":
    cadastro_financeiro()

elif opcao == "Baixa Financeira":
    baixa_financeira()
