import streamlit as st
import mysql.connector
from datetime import datetime
import time
import pymysql

def main(form_key_suffix=""):
    # Configuração inicial
    if 'pagina' not in st.session_state:
        st.session_state.pagina = 'formulario'
    
    # CSS para remover a borda do formulário
    st.markdown("""
        <style>
            .stForm {
                border: none !important;
                box-shadow: none !important;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # Funções do banco de dados usando PyMySQL como alternativa
    def conectar_banco():
        try:
            return pymysql.connect(
                user='logitech_rafael',
                password='admin000',
                host='db4free.net',
                port=3306,
                database='srtransporte',
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.Error as err:
            st.error(f"Erro ao conectar ao banco de dados: {err}")
            return None
    
    def buscar_clientes():
        conn = conectar_banco()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT cliente, cod_cliente FROM cad_cliente")
                    return {cliente: cod_cliente for cliente, cod_cliente in cursor.fetchall()}
            except pymysql.Error as err:
                st.error(f"Erro ao buscar clientes: {err}")
            finally:
                conn.close()
        return {}
    
    def buscar_motoristas():
        conn = conectar_banco()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT nome, cpf FROM cad_mot")
                    return {nome: cpf for nome, cpf in cursor.fetchall()}
            except pymysql.Error as err:
                st.error(f"Erro ao buscar motoristas: {err}")
            finally:
                conn.close()
        return {}
    
    def buscar_placas():
        conn = conectar_banco()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT placa, perfil, proprietario FROM cad_vei")
                    return {placa: {'perfil': perfil, 'proprietario': proprietario} for placa, perfil, proprietario in cursor.fetchall()}
            except pymysql.Error as err:
                st.error(f"Erro ao buscar placas: {err}")
            finally:
                conn.close()
        return {}
    
    def buscar_cidades():
        conn = conectar_banco()
        if conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT DISTINCT cidade FROM cad_rota")
                    return [cidade[0] for cidade in cursor.fetchall()]
            except pymysql.Error as err:
                st.error(f"Erro ao buscar cidades: {err}")
            finally:
                conn.close()
        return []
    
    def excluir_registro(id_registro):
        conn = conectar_banco()
        if not conn:
            return False
        
        try:
            with conn.cursor() as cursor:
                query = "DELETE FROM tela_inicial WHERE id = %s"
                cursor.execute(query, (id_registro,))
                conn.commit()
                return cursor.rowcount > 0
        except pymysql.Error as err:
            st.error(f"Erro ao excluir registro: {err}")
            return False
        finally:
            if conn.open:
                conn.close()
    
    def salvar_dados(dados):
        conn = conectar_banco()
        if not conn:
            return False
    
        try:
            with conn.cursor() as cursor:
                campos = [
                    'data', 'cliente', 'cod_cliente', 'motorista', 'cpf_motorista',
                    'placa', 'perfil_vei', 'proprietario_vei',
                    'id_carga_cvia', 'cubagem', 'cid_1', 'mod_1', 'filial'
                ]
                
                valores = (
                    dados['data_mysql'],
                    dados['cliente'],
                    dados['cod_cliente'],
                    dados['motorista'],
                    dados['cpf_motorista'],
                    dados['placa'],
                    dados['perfil_vei'],
                    dados['proprietario_vei'],
                    dados['id_carga_cvia'],
                    dados['cubagem'],
                    dados['cid_1'],
                    dados['mod_1'],
                    dados['filial']
                )
    
                if dados['id_registro']:
                    query = f"UPDATE tela_inicial SET {', '.join([f'{campo} = %s' for campo in campos])} WHERE id = %s"
                    cursor.execute(query, valores + (dados['id_registro'],))
                else:
                    query = f"INSERT INTO tela_inicial ({', '.join(campos)}) VALUES ({', '.join(['%s'] * len(campos))})"
                    cursor.execute(query, valores)
    
                conn.commit()
                return True
        except pymysql.Error as err:
            st.error(f"Erro ao salvar dados: {err}")
            return False
        finally:
            if conn.open:
                conn.close()
    
    # Página do formulário
    def mostrar_formulario(suffix):
        st.title("Novo Cadastro de Carregamento")
        
        clientes = buscar_clientes()
        motoristas = buscar_motoristas()
        placas_info = buscar_placas()
        cidades = buscar_cidades()
        
        # Formulário principal
        with st.form(key=f"form_producao_{suffix}", clear_on_submit=True):
            id_registro = st.text_input(
                "ID (para edição, deixe vazio para novo cadastro)",
                key=f"id_registro_{suffix}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                cliente = st.selectbox(
                    "Cliente*", 
                    [""] + list(clientes.keys()),
                    key=f"cliente_{suffix}"
                )
                cod_cliente = st.text_input(
                    "Código do Cliente", 
                    value=clientes.get(cliente, ""), 
                    disabled=True,
                    key=f"cod_cliente_{suffix}"
                )
            with col2:
                motorista = st.selectbox(
                    "Motorista*", 
                    [""] + list(motoristas.keys()),
                    key=f"motorista_{suffix}"
                )
                cpf_motorista = st.text_input(
                    "CPF do Motorista", 
                    value=motoristas.get(motorista, ""), 
                    disabled=True,
                    key=f"cpf_motorista_{suffix}"
                )

            col1, col2, col3 = st.columns(3)
            with col1:
                placa = st.selectbox(
                    "Placa*", 
                    [""] + list(placas_info.keys()),
                    key=f"placa_{suffix}"
                )
            with col2:
                perfil_vei = st.text_input(
                    "Perfil do Veículo", 
                    value=placas_info.get(placa, {}).get('perfil', ''), 
                    disabled=True,
                    key=f"perfil_vei_{suffix}"
                )
            with col3:
                proprietario_vei = st.text_input(
                    "Proprietário", 
                    value=placas_info.get(placa, {}).get('proprietario', ''), 
                    disabled=True,
                    key=f"proprietario_vei_{suffix}"
                )

            col1, col2 = st.columns(2)
            with col1:
                id_carga_cvia = st.text_input(
                    "ID carga / CVia",
                    key=f"id_carga_cvia_{suffix}"
                )
            with col2:
                filial = st.text_input(
                    "Filial",
                    key=f"filial_{suffix}"
                )

            data = st.text_input(
                "Data* (Formato: dd/mm/aaaa)",
                key=f"data_{suffix}"
            )

            col1, col2 = st.columns(2)
            with col1:
                cid_1 = st.selectbox(
                    "Cidade*", 
                    [""] + cidades,
                    key=f"cid_1_{suffix}"
                )
            with col2:
                mod_1 = st.selectbox(
                    "Modalidade", 
                    ["", "ABA", "VENDA"],
                    key=f"mod_1_{suffix}"
                )

            cubagem = st.text_input(
                "Cubagem",
                key=f"cubagem_{suffix}"
            )

            submitted = st.form_submit_button("Enviar")
            if submitted:
                if not all([cliente, motorista, placa, data, cid_1]):
                    st.error("Preencha todos os campos obrigatórios (*)")
                else:
                    try:
                        dados = {
                            'id_registro': id_registro if id_registro else None,
                            'data_mysql': datetime.strptime(data, "%d/%m/%Y").strftime("%Y-%m-%d"),
                            'cliente': cliente,
                            'cod_cliente': clientes.get(cliente, ""),
                            'motorista': motorista,
                            'cpf_motorista': motoristas.get(motorista, ""),
                            'placa': placa,
                            'perfil_vei': placas_info.get(placa, {}).get('perfil', ''),
                            'proprietario_vei': placas_info.get(placa, {}).get('proprietario', ''),
                            'id_carga_cvia': id_carga_cvia,
                            'cubagem': cubagem,
                            'cid_1': cid_1,
                            'mod_1': mod_1,
                            'filial': filial
                        }
                        
                        st.session_state.dados = dados
                        st.session_state.pagina = 'progresso'
                        st.rerun()
                    except ValueError:
                        st.error("Formato de data inválido. Use dd/mm/aaaa")

        # Seção de exclusão de registro (fora do formulário)
        st.markdown("---")
        with st.expander("Excluir Registro Existente"):
            id_para_excluir = st.text_input(
                "ID do registro a ser excluído:",
                key=f"id_excluir_{suffix}"
            )
            
            if st.button("Excluir Registro", key=f"btn_excluir_{suffix}"):
                if id_para_excluir:
                    if excluir_registro(id_para_excluir):
                        st.success(f"✅ Registro ID {id_para_excluir} excluído com sucesso!")
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.error("❌ Falha ao excluir registro ou registro não encontrado")
                else:
                    st.warning("⚠️ Por favor, informe o ID do registro a ser excluído")

    # Página de progresso
    def mostrar_progresso():
        st.empty()
        barra = st.progress(0)
        for i in range(100):
            time.sleep(0.03)
            barra.progress(i + 1)
        
        if salvar_dados(st.session_state.dados):
            st.session_state.pagina = 'sucesso'
        else:
            st.session_state.pagina = 'formulario'
        st.rerun()
    
    # Página de sucesso
    def mostrar_sucesso():
        st.empty()
        st.success("✅ Dados salvos com sucesso!")
        
        if st.button("🆕 Novo Cadastro", key="novo_cadastro"):
            for key in list(st.session_state.keys()):
                if key != 'pagina':
                    del st.session_state[key]
            st.session_state.pagina = 'formulario'
            st.rerun()

    # Controle de páginas
    if st.session_state.pagina == 'formulario':
        mostrar_formulario(form_key_suffix)
    elif st.session_state.pagina == 'progresso':
        mostrar_progresso()
    elif st.session_state.pagina == 'sucesso':
        mostrar_sucesso()

if __name__ == '__main__':
    main("local")
