import streamlit as st
import mysql.connector
from decimal import Decimal

def main(form_key_suffix=""):
    st.markdown("""
        <style>
            .stForm {
                border: none !important;
                box-shadow: none !important;
                padding: 0 !important;
            }
            .stForm form {
                border: none !important;
                padding: 0 !important;
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
    
    def cadastro_financeiro(suffix):
        st.title("Cadastro Financeiro")      
        
        # Inicializa session_state com keys únicas
        defaults = {
            f'minuta_ot_financeiro_{suffix}': "",
            f'valor_frete_pago_{suffix}': "",
            f'descontos_{suffix}': "",
            f'acerto_{suffix}': "",
            f'adiantamento_{suffix}': "",
            f'observacoes_{suffix}': "",
            f'id_financeiro_{suffix}': "",
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
        # Formulário principal
        with st.form(key=f"form_financeiro_{suffix}"):
            # Layout do formulário
            col1, col2 = st.columns(2)
            
            with col1:
                # Campo ID
                id_registro = st.text_input(
                    "ID* (obrigatório)", 
                    key=f'id_financeiro_{suffix}', 
                    value=st.session_state[f'id_financeiro_{suffix}']
                )
                
            with col2:
                # Campo Minuta/OT (agora manual)
                st.session_state[f'minuta_ot_financeiro_{suffix}'] = st.text_input(
                    "Minuta/OT* (obrigatório)", 
                    value=st.session_state[f'minuta_ot_financeiro_{suffix}'],
                    key=f'minuta_ot_{suffix}'
                )
    
            # Campos financeiros
            col1, col2 = st.columns(2)
            with col1:
                valor_frete_pago = st.text_input(
                    "Valor do Frete (pago) (R$)", 
                    key=f'valor_frete_pago_{suffix}', 
                    value=st.session_state[f'valor_frete_pago_{suffix}'],
                    help="Use vírgula para decimais (ex: 1.234,56)"
                )
            with col2:
                descontos = st.text_input(
                    "Descontos (R$)", 
                    key=f'descontos_{suffix}', 
                    value=st.session_state[f'descontos_{suffix}'],
                    help="Use vírgula para decimais (ex: 123,45)"
                )
    
            # Campos Acerto e Adiantamento lado a lado
            col1, col2 = st.columns(2)
            with col1:
                acerto = st.text_input(
                    "Acerto (Despesa extra) (R$)", 
                    key=f'acerto_{suffix}', 
                    value=st.session_state[f'acerto_{suffix}'],
                    help="Use vírgula para decimais (ex: 234,56)"
                )
            with col2:
                adiantamento = st.text_input(
                    "Adiantamento (R$)", 
                    key=f'adiantamento_{suffix}', 
                    value=st.session_state[f'adiantamento_{suffix}'],
                    help="Use vírgula para decimais (ex: 345,67)"
                )
    
            observacoes = st.text_area(
                "Observações gerais", 
                key=f'observacoes_{suffix}', 
                value=st.session_state[f'observacoes_{suffix}']
            )
    
            # Botão de submit dentro do form
            submitted = st.form_submit_button("Salvar Dados Financeiros")
            
            if submitted:
                # Validação dos campos obrigatórios
                if not id_registro or not st.session_state[f'minuta_ot_financeiro_{suffix}']:
                    st.error("Os campos ID e Minuta/OT são obrigatórios")
                else:
                    # Formata os valores monetários
                    valor_frete_pago_formatado = formatar_valor(valor_frete_pago)
                    descontos_formatado = formatar_valor(descontos)
                    acerto_formatado = formatar_valor(acerto)
                    adiantamento_formatado = formatar_valor(adiantamento)
                    
                    # Verifica se os valores são válidos (apenas para campos preenchidos)
                    if valor_frete_pago and valor_frete_pago_formatado is None:
                        st.error("Valor do Frete inválido. Use vírgula para decimais (ex: 1.234,56)")
                    elif descontos and descontos_formatado is None:
                        st.error("Descontos inválidos. Use vírgula para decimais (ex: 123,45)")
                    elif acerto and acerto_formatado is None:
                        st.error("Acerto inválido. Use vírgula para decimais (ex: 234,56)")
                    elif adiantamento and adiantamento_formatado is None:
                        st.error("Adiantamento inválido. Use vírgula para decimais (ex: 345,67)")
                    else:
                        with st.spinner("Salvando dados..."):
                            # Prepara dados para salvar
                            dados = {
                                'id': id_registro,
                                'minuta_ot': st.session_state[f'minuta_ot_financeiro_{suffix}'],
                                'valor_frete_pago': valor_frete_pago_formatado,
                                'descontos': descontos_formatado,
                                'acerto': acerto_formatado,
                                'adiantamento': adiantamento_formatado,
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
                                    
                                    # Limpa apenas os campos do formulário
                                    keys_to_clear = [f'minuta_ot_financeiro_{suffix}',
                                                    f'valor_frete_pago_{suffix}',
                                                    f'descontos_{suffix}',
                                                    f'acerto_{suffix}',
                                                    f'adiantamento_{suffix}',
                                                    f'observacoes_{suffix}',
                                                    f'id_financeiro_{suffix}']
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
    
    cadastro_financeiro(form_key_suffix)

if __name__ == '__main__':
    main("local")
