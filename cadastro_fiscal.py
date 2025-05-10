import streamlit as st
import mysql.connector

def main(form_key_suffix=""):
    # CSS para remover a borda do formulário
    st.markdown("""
        <style>
            .stForm {
                border: none !important;
                box-shadow: none !important;
            }
        </style>
    """, unsafe_allow_html=True)

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
    
    def cadastro_fiscal(suffix):
        st.title("Cadastro Fiscal")
        
        # Inicializa session_state com keys únicas
        defaults = {
            f'minuta_ot_fiscal_{suffix}': "",
            f'cliente_fiscal_{suffix}': "",
            f'cod_cliente_fiscal_{suffix}': "",
            f'valor_carga_fiscal_{suffix}': "",
            f'valor_frete_fiscal_{suffix}': "",
            f'icms_{suffix}': "",
            f'gris_{suffix}': "",
            f'adv_{suffix}': "",
            f'seguro_{suffix}': "",
            f'id_fiscal_{suffix}': "",
            f'last_cliente_{suffix}': ""
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
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
    
        # Formulário principal
        with st.form(key=f"form_fiscal_{suffix}"):
            # Layout do formulário
            col1, col2 = st.columns(2)
            
            with col1:
                # Campo ID
                id_registro = st.text_input(
                    "ID* (obrigatório)", 
                    key=f'id_fiscal_{suffix}', 
                    value=st.session_state[f'id_fiscal_{suffix}']
                )
                
            with col2:
                # Campo Minuta/OT (agora manual)
                st.session_state[f'minuta_ot_fiscal_{suffix}'] = st.text_input(
                    "Minuta/OT* (obrigatório)", 
                    value=st.session_state[f'minuta_ot_fiscal_{suffix}'],
                    key=f'minuta_ot_{suffix}'
                )
    
            # Selectbox para cliente
            cliente_selecionado = st.selectbox(
                "Cliente",
                options=clientes,
                index=clientes.index(st.session_state[f'cliente_fiscal_{suffix}']) if st.session_state[f'cliente_fiscal_{suffix}'] in clientes else 0,
                key=f'select_cliente_{suffix}'
            )
            
            # Atualiza código do cliente quando o cliente muda
            if cliente_selecionado != st.session_state.get(f'last_cliente_{suffix}', ''):
                st.session_state[f'cod_cliente_fiscal_{suffix}'] = cliente_para_codigo.get(cliente_selecionado, "")
                st.session_state[f'last_cliente_{suffix}'] = cliente_selecionado
    
            # Código do cliente (preenchido automaticamente)
            st.text_input(
                "Código do Cliente",
                value=st.session_state[f'cod_cliente_fiscal_{suffix}'],
                key=f'display_cod_cliente_{suffix}',
                disabled=True
            )
    
            # Campos de valores principais
            col1, col2 = st.columns(2)
            with col1:
                valor_carga = st.text_input(
                    "Valor da Carga", 
                    key=f'valor_carga_fiscal_{suffix}', 
                    value=st.session_state[f'valor_carga_fiscal_{suffix}']
                )
            with col2:
                valor_frete = st.text_input(
                    "Valor do Frete", 
                    key=f'valor_frete_fiscal_{suffix}', 
                    value=st.session_state[f'valor_frete_fiscal_{suffix}']
                )
            
            # Novos campos adicionais
            st.subheader("Tributos e Adicionais")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                icms = st.text_input(
                    "ICMS (R$)",
                    key=f'icms_{suffix}',
                    value=st.session_state[f'icms_{suffix}']
                )
            with col2:
                gris = st.text_input(
                    "GRIS (R$)",
                    key=f'gris_{suffix}',
                    value=st.session_state[f'gris_{suffix}']
                )
            with col3:
                adv = st.text_input(
                    "ADV (R$)",
                    key=f'adv_{suffix}',
                    value=st.session_state[f'adv_{suffix}']
                )
            with col4:
                seguro = st.text_input(
                    "Seguro (R$)",
                    key=f'seguro_{suffix}',
                    value=st.session_state[f'seguro_{suffix}']
                )
    
            # Botão de submit dentro do form
            submitted = st.form_submit_button("Salvar Dados Fiscais")
            
            if submitted:
                with st.spinner("Salvando dados..."):
                    # Validação dos campos obrigatórios
                    if not id_registro or not st.session_state[f'minuta_ot_fiscal_{suffix}']:
                        st.error("Os campos ID e Minuta/OT são obrigatórios")
                    else:
                        # Prepara dados para salvar
                        dados = {
                            'id': id_registro,
                            'minuta_ot': st.session_state[f'minuta_ot_fiscal_{suffix}'],
                            'cliente': cliente_selecionado,
                            'cod_cliente': st.session_state[f'cod_cliente_fiscal_{suffix}'],
                            'valor_carga': valor_carga,
                            'valor_frete': valor_frete,
                            'icms': icms,
                            'gris': gris,
                            'adv': adv,
                            'seguro': seguro
                        }
    
                        # Conecta ao banco e salva
                        conn = conectar_banco()
                        if conn:
                            try:
                                cursor = conn.cursor()
                                
                                # Verifica se a tabela tem os novos campos
                                cursor.execute("SHOW COLUMNS FROM tela_fis LIKE 'icms'")
                                tem_novos_campos = cursor.fetchone()
                                
                                # Verifica se é atualização ou inserção
                                cursor.execute("SELECT id FROM tela_fis WHERE id = %s", (id_registro,))
                                existe = cursor.fetchone()
                                
                                if existe:
                                    # Atualiza registro existente
                                    if tem_novos_campos:
                                        query = """
                                            UPDATE tela_fis SET
                                                minuta_ot = %s,
                                                cliente = %s,
                                                cod_cliente = %s,
                                                valor_carga = %s,
                                                valor_frete = %s,
                                                icms = %s,
                                                gris = %s,
                                                adv = %s,
                                                seguro = %s
                                            WHERE id = %s
                                        """
                                        cursor.execute(query, (
                                            dados['minuta_ot'],
                                            dados['cliente'],
                                            dados['cod_cliente'],
                                            dados['valor_carga'],
                                            dados['valor_frete'],
                                            dados['icms'],
                                            dados['gris'],
                                            dados['adv'],
                                            dados['seguro'],
                                            dados['id']
                                        ))
                                    else:
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
                                    if tem_novos_campos:
                                        query = """
                                            INSERT INTO tela_fis (
                                                id, minuta_ot, cliente, cod_cliente, 
                                                valor_carga, valor_frete, icms, gris, adv, seguro
                                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                        """
                                        cursor.execute(query, (
                                            dados['id'],
                                            dados['minuta_ot'],
                                            dados['cliente'],
                                            dados['cod_cliente'],
                                            dados['valor_carga'],
                                            dados['valor_frete'],
                                            dados['icms'],
                                            dados['gris'],
                                            dados['adv'],
                                            dados['seguro']
                                        ))
                                    else:
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
                                
                                # Limpa apenas os campos do formulário
                                keys_to_clear = [f'minuta_ot_fiscal_{suffix}',
                                                f'cliente_fiscal_{suffix}',
                                                f'cod_cliente_fiscal_{suffix}',
                                                f'valor_carga_fiscal_{suffix}',
                                                f'valor_frete_fiscal_{suffix}',
                                                f'icms_{suffix}',
                                                f'gris_{suffix}',
                                                f'adv_{suffix}',
                                                f'seguro_{suffix}',
                                                f'id_fiscal_{suffix}',
                                                f'last_cliente_{suffix}']
                                for key in keys_to_clear:
                                    if key in st.session_state:
                                        del st.session_state[key]
                                
                                st.rerun()
                                
                            except mysql.connector.Error as err:
                                conn.rollback()
                                st.error(f"Erro ao salvar dados: {err}")
                            finally:
                                if conn.is_connected():
                                    cursor.close()
                                    conn.close()
    
    cadastro_fiscal(form_key_suffix)

if __name__ == '__main__':
    main("local")
