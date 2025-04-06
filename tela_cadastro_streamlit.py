import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime

# Função para conectar ao banco de dados
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

# Função genérica para salvar dados
def salvar_dados(tabela, campos, valores, id_registro):
    conn = conectar_banco()
    if not conn:
        st.error("Erro ao conectar ao banco de dados.")
        return

    try:
        cursor = conn.cursor()
        if id_registro:
            query = f"UPDATE {tabela} SET {', '.join([f'{campo} = %s' for campo in campos])} WHERE id = %s"
            cursor.execute(query, valores + (id_registro,))
        else:
            query = f"INSERT INTO {tabela} ({', '.join(campos)}) VALUES ({', '.join(['%s'] * len(campos))})"
            cursor.execute(query, valores)

        conn.commit()
        cursor.close()
        conn.close()
        st.success("Dados salvos com sucesso!")
        
        st.session_state.clear()
        st.experimental_rerun()
    except mysql.connector.Error as err:
        st.error(f"Erro ao salvar dados no banco de dados: {err}")
    except Exception as e:
        st.error(f"Erro inesperado: {str(e)}")

# Função para buscar clientes
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

# Função para buscar motoristas
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

# Função para buscar veículos
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

# Função para buscar rotas
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

# Função para buscar lançamentos
def buscar_todos_lancamentos(filtro_id=None):
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

# Função para buscar um lançamento por ID
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

# Função para cadastro fiscal
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
    if st.button("Salvar"):
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
                st.experimental_rerun()
                
            except mysql.connector.Error as err:
                conn.rollback()
                st.error(f"Erro ao salvar dados: {err}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

# Função para cadastro financeiro
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
    if st.button("Salvar"):
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
                st.experimental_rerun()
                
            except mysql.connector.Error as err:
                conn.rollback()
                st.error(f"Erro ao salvar dados: {err}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()

# Função para baixa financeira
def baixa_financeira():
    st.title("Baixa Financeira")
    
    uploaded_file = st.file_uploader("Carregar arquivo XLSX", type=["xlsx"], key='baixa_upload')
    
    if uploaded_file is not None:
        try:
            # Lê o arquivo mantendo os formatos originais
            df = pd.read_excel(uploaded_file)
            
            # Mostra pré-visualização
            st.write("Pré-visualização dos dados:")
            st.dataframe(df)
            
            if st.button("Importar dados"):
                conn = conectar_banco()
                if conn:
                    try:
                        cursor = conn.cursor()
                        
                        # Primeiro verifica a estrutura da tabela
                        cursor.execute("SHOW COLUMNS FROM baixa_financeira")
                        colunas_info = cursor.fetchall()
                        colunas = [col[0] for col in colunas_info if col[0].lower() != 'id']
                        
                        # Verifica se as colunas do arquivo correspondem às da tabela
                        if not all(col in df.columns for col in colunas):
                            st.error(f"Colunas no arquivo não correspondem às da tabela. Esperado: {', '.join(colunas)}")
                            return
                        
                        # Prepara a query
                        placeholders = ', '.join(['%s'] * len(colunas))
                        query = f"INSERT INTO baixa_financeira ({', '.join(colunas)}) VALUES ({placeholders})"
                        
                        # Converte os dados conforme os tipos
                        for _, row in df.iterrows():
                            valores = []
                            for col in colunas:
                                valor = row[col]
                                
                                # Se for NULL ou vazio
                                if pd.isna(valor) or valor == '':
                                    valores.append(None)
                                    continue
                                
                                # Conversão para tipos específicos
                                if isinstance(valor, pd.Timestamp):
                                    valores.append(valor.to_pydatetime())
                                elif 'date' in str(valor).lower():
                                    try:
                                        dt = pd.to_datetime(valor)
                                        valores.append(dt.to_pydatetime())
                                    except:
                                        valores.append(str(valor))
                                elif isinstance(valor, (int, float)):
                                    valores.append(float(valor))
                                else:
                                    valores.append(str(valor))
                            
                            cursor.execute(query, valores)
                        
                        conn.commit()
                        st.success(f"Dados importados com sucesso! {len(df)} registros adicionados.")
                        
                    except mysql.connector.Error as err:
                        conn.rollback()
                        st.error(f"Erro ao importar dados: {err}")
                    finally:
                        if conn.is_connected():
                            cursor.close()
                            conn.close()
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {str(e)}")

# Função para preventivo de entrega
def preventivo_entrega():
    st.title("Preventivo de Entrega")
    
    uploaded_file = st.file_uploader("Carregar arquivo XLSX", type=["xlsx"], key='preventivo_upload')
    
    if uploaded_file is not None:
        try:
            # Lê o arquivo mantendo os formatos originais
            df = pd.read_excel(uploaded_file)
            
            # Mostra pré-visualização
            st.write("Pré-visualização dos dados:")
            st.dataframe(df)
            
            if st.button("Importar para Preventivo"):
                conn = conectar_banco()
                if conn:
                    try:
                        cursor = conn.cursor()
                        
                        # Primeiro verifica a estrutura da tabela
                        cursor.execute("SHOW COLUMNS FROM preventivo")
                        colunas_info = cursor.fetchall()
                        colunas = [col[0] for col in colunas_info if col[0].lower() != 'id']
                        
                        # Verifica se as colunas do arquivo correspondem às da tabela
                        if not all(col in df.columns for col in colunas):
                            st.error(f"Colunas no arquivo não correspondem às da tabela. Esperado: {', '.join(colunas)}")
                            return
                        
                        # Prepara a query
                        placeholders = ', '.join(['%s'] * len(colunas))
                        query = f"INSERT INTO preventivo ({', '.join(colunas)}) VALUES ({placeholders})"
                        
                        # Converte os dados conforme os tipos
                        for _, row in df.iterrows():
                            valores = []
                            for col in colunas:
                                valor = row[col]
                                
                                # Se for NULL ou vazio
                                if pd.isna(valor) or valor == '':
                                    valores.append(None)
                                    continue
                                
                                # Conversão para tipos específicos
                                if isinstance(valor, pd.Timestamp):
                                    valores.append(valor.to_pydatetime())
                                elif 'date' in str(valor).lower():
                                    try:
                                        dt = pd.to_datetime(valor)
                                        valores.append(dt.to_pydatetime())
                                    except:
                                        valores.append(str(valor))
                                elif isinstance(valor, (int, float)):
                                    valores.append(float(valor))
                                else:
                                    valores.append(str(valor))
                            
                            cursor.execute(query, valores)
                        
                        conn.commit()
                        st.success(f"Dados importados com sucesso! {len(df)} registros adicionados à tabela preventivo.")
                        
                    except mysql.connector.Error as err:
                        conn.rollback()
                        st.error(f"Erro ao importar dados: {err}")
                        st.error("Verifique se os tipos de dados correspondem aos da tabela preventivo")
                    finally:
                        if conn.is_connected():
                            cursor.close()
                            conn.close()
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {str(e)}")

# Configuração inicial do session_state
if 'opcao' not in st.session_state:
    st.session_state.opcao = "Novo Cadastro"

# Menu lateral
st.sidebar.title("Menu")
opcao = st.sidebar.radio("Selecione uma opção", [
    "Novo Cadastro", "Consulta de Cadastro", "Cadastro de Cliente", 
    "Cadastro de Motorista", "Cadastro de Rota", "Cadastro de Veículo", 
    "Cadastro de Frete Extra", "Cadastro Fiscal", "Cadastro Financeiro",
    "Baixa Financeira", "Preventivo de Entrega"
])

# Redirecionamento para a tela selecionada
if opcao == "Novo Cadastro":
    # (Manter implementação existente)
    pass
elif opcao == "Consulta de Cadastro":
    # (Manter implementação existente)
    pass
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
elif opcao == "Preventivo de Entrega":
    preventivo_entrega()
