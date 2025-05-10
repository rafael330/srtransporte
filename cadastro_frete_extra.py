import streamlit as st
import mysql.connector
from datetime import datetime
from decimal import Decimal

def main(form_key_suffix=""):
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
    
    def formatar_valor(valor_str):
        """Converte valores com vírgula para formato decimal"""
        if not valor_str:
            return None
        try:
            # Remove pontos de milhar e substitui vírgula por ponto
            valor_str = valor_str.replace('.', '').replace(',', '.')
            return Decimal(valor_str)
        except:
            return None
        
    def salvar_dados(tabela, campos, valores, id_registro):
        with st.spinner("Salvando dados..."):     
            conn = conectar_banco()
            if not conn:
                st.error("Erro ao conectar ao banco de dados.")
                return
    
            try:
                cursor = conn.cursor()
                if id_registro:
                    query = f"UPDATE {tabela} SET {', '.join([f'{campo} = %s' for campo in campos])} WHERE id_registro = %s"
                    cursor.execute(query, valores + (id_registro,))
                else:
                    query = f"INSERT INTO {tabela} ({', '.join(campos)}) VALUES ({', '.join(['%s'] * len(campos))})"
                    cursor.execute(query, valores)
                
                conn.commit()
                st.success("Dados salvos com sucesso!")
                
                # Limpa apenas os campos do formulário
                keys_to_clear = [f'id_frete_extra_{form_key_suffix}',
                                f'cliente_{form_key_suffix}',
                                f'data_{form_key_suffix}',
                                f'id_carga_{form_key_suffix}',
                                f'cidade_{form_key_suffix}',
                                f'entrega_final_{form_key_suffix}',
                                f'valor_{form_key_suffix}']
                for key in keys_to_clear:
                    if key in st.session_state:
                        del st.session_state[key]
                
                st.rerun()
            except mysql.connector.Error as err:
                st.error(f"Erro ao salvar dados: {err}")
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
    
    def buscar_clientes():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT cliente, cod_cliente FROM cad_cliente")
                return {cliente: cod_cliente for cliente, cod_cliente in cursor.fetchall()}
            except mysql.connector.Error as err:
                st.error(f"Erro ao buscar clientes: {err}")
            finally:
                conn.close()
        return {}
    
    def buscar_cargas():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT id_carga_cvia FROM tela_inicial")
                return [carga[0] for carga in cursor.fetchall()]
            except mysql.connector.Error as err:
                st.error(f"Erro ao buscar cargas: {err}")
            finally:
                conn.close()
        return []
    
    def buscar_cidades():
        conn = conectar_banco()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT DISTINCT cidade FROM cad_rota")
                return [cidade[0] for cidade in cursor.fetchall()]
            except mysql.connector.Error as err:
                st.error(f"Erro ao buscar cidades: {err}")
            finally:
                conn.close()
        return []
    
    def cadastro_frete_extra(suffix):
        st.title("Cadastro de Frete Extra")
        
        # Inicializa session_state com valores padrão
        defaults = {
            f'id_frete_extra_{suffix}': '',
            f'cliente_{suffix}': '',
            f'data_{suffix}': '',
            f'id_carga_{suffix}': '',
            f'cidade_{suffix}': '',
            f'entrega_final_{suffix}': '',
            f'valor_{suffix}': ''
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
        
        # Formulário principal
        with st.form(key=f"form_frete_extra_{suffix}"):
            # Busca dados necessários
            clientes = buscar_clientes()
            cargas = buscar_cargas()
            cidades = buscar_cidades()
            
            # Layout em colunas
            col1, col2 = st.columns(2)
            
            with col1:
                # Campo ID
                id_registro = st.text_input(
                    "ID (deixe vazio para novo cadastro)",
                    value=st.session_state[f'id_frete_extra_{suffix}'],
                    key=f"input_id_frete_extra_{suffix}"
                )
                
                # Campo Cliente
                cliente = st.selectbox(
                    "Cliente*",
                    options=[""] + list(clientes.keys()),
                    key=f"select_cliente_{suffix}"
                )
                
                # Campo Data
                data = st.text_input(
                    "Data* (Formato: dd/mm/aaaa)",
                    value=st.session_state[f'data_{suffix}'],
                    key=f"input_data_{suffix}"
                )
                
                # Campo ID Carga
                id_carga = st.selectbox(
                    "ID Carga",
                    options=[""] + cargas,
                    key=f"select_id_carga_{suffix}"
                )
            
            with col2:
                # Campo Cidade
                cidade = st.selectbox(
                    "Cidade*",
                    options=[""] + cidades,
                    key=f"select_cidade_{suffix}"
                )
                
                # Campo Entrega Final
                entrega_final = st.text_input(
                    "Entrega Final",
                    value=st.session_state[f'entrega_final_{suffix}'],
                    key=f"input_entrega_final_{suffix}"
                )
                
                # Campo Valor
                valor = st.text_input(
                    "Valor* (R$)",
                    value=st.session_state[f'valor_{suffix}'],
                    key=f"input_valor_{suffix}",
                    help="Use vírgula para decimais (ex: 1.234,56)"
                )
            
            # Botão de submit dentro do form
            submitted = st.form_submit_button("Salvar Frete Extra")
            
            if submitted:
                try:
                    # Validação dos campos obrigatórios
                    if not cliente or not data or not cidade or not valor:
                        st.error("Preencha todos os campos obrigatórios (*)")
                    else:
                        # Valida formato da data
                        datetime.strptime(data, "%d/%m/%Y")
                        
                        # Formata o valor com vírgula
                        valor_formatado = formatar_valor(valor)
                        if valor_formatado is None:
                            st.error("Valor inválido. Use vírgula para decimais (ex: 1.234,56)")
                            return
                        
                        # Atualiza session_state
                        st.session_state[f'id_frete_extra_{suffix}'] = id_registro
                        st.session_state[f'cliente_{suffix}'] = cliente
                        st.session_state[f'data_{suffix}'] = data
                        st.session_state[f'id_carga_{suffix}'] = id_carga
                        st.session_state[f'cidade_{suffix}'] = cidade
                        st.session_state[f'entrega_final_{suffix}'] = entrega_final
                        st.session_state[f'valor_{suffix}'] = valor
                        
                        # Prepara dados para salvar
                        campos = ['cliente', 'data', 'id_carga', 'cidade', 'entrega_final', 'valor']
                        valores = (cliente, data, id_carga, cidade, entrega_final, valor_formatado)
                        salvar_dados('cad_frete_extra', campos, valores, id_registro)
                except ValueError as e:
                    if "time data" in str(e):
                        st.error("Formato de data inválido. Use dd/mm/aaaa")
                    else:
                        st.error(f"Erro ao processar dados: {str(e)}")
    
    cadastro_frete_extra(form_key_suffix)

if __name__ == '__main__':
    main("local")
