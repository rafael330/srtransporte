import streamlit as st
import mysql.connector
import pandas as pd

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
    
    def preventivo_entrega(suffix):
        st.title("Preventivo de Entrega")
        
        # Formulário principal
        with st.form(key=f"form_preventivo_{suffix}"):
            uploaded_file = st.file_uploader(
                "Carregar arquivo XLSX", 
                type=["xlsx"], 
                key=f'preventivo_upload_{suffix}'
            )
            
            submitted = st.form_submit_button("Verificar Arquivo")
            
            if submitted and uploaded_file is not None:
                try:
                    # Lê o arquivo mantendo os formatos originais
                    df = pd.read_excel(uploaded_file)
                    
                    # Mostra pré-visualização
                    st.write("Pré-visualização dos dados:")
                    st.dataframe(df)
                    
                    # Colunas obrigatórias (ajuste conforme necessário)
                    colunas_obrigatorias = ['PEDIDO CLIENTE', 'PEDIDO GEMGO', 'NUMERO NOTA FISCAL']
                    
                    # Verifica colunas faltantes
                    colunas_faltantes = [col for col in colunas_obrigatorias if col not in df.columns]
                    if colunas_faltantes:
                        st.error(f"Colunas obrigatórias faltantes: {', '.join(colunas_faltantes)}")
                        return
                    
                    # Botão de confirmação para importação
                    if st.button("Confirmar Importação", key=f"confirm_import_{suffix}"):
                        with st.spinner("Importando dados para o preventivo..."):
                            conn = conectar_banco()
                            if conn:
                                try:
                                    cursor = conn.cursor()
                                    
                                    # Remove colunas que não existem na tabela
                                    cursor.execute("SHOW COLUMNS FROM preventivo")
                                    colunas_tabela = [column[0] for column in cursor.fetchall() if column[0] != 'id']
                                    
                                    # Filtra apenas colunas que existem tanto no arquivo quanto na tabela
                                    colunas_validas = [col for col in df.columns if col in colunas_tabela]
                                    
                                    if not colunas_validas:
                                        st.error("Nenhuma coluna correspondente encontrada entre o arquivo e a tabela")
                                        return
                                    
                                    # Prepara a query SQL com nomes entre backticks
                                    colunas_sql = ', '.join([f"`{col}`" for col in colunas_validas])
                                    placeholders = ', '.join(['%s'] * len(colunas_validas))
                                    query = f"INSERT INTO preventivo ({colunas_sql}) VALUES ({placeholders})"
                                    
                                    # Processa cada linha
                                    total_inseridos = 0
                                    erros = 0
                                    for _, row in df.iterrows():
                                        valores = []
                                        for col in colunas_validas:
                                            valor = row[col]
                                            
                                            # Trata valores nulos
                                            if pd.isna(valor):
                                                valores.append(None)
                                                continue
                                            
                                            # Conversão de datas/timestamps
                                            if isinstance(valor, pd.Timestamp):
                                                valores.append(valor.to_pydatetime())
                                            elif 'DT.' in col or 'DATA' in col.upper():
                                                try:
                                                    dt = pd.to_datetime(valor)
                                                    valores.append(dt.to_pydatetime())
                                                except:
                                                    valores.append(str(valor))
                                            # Conversão de números
                                            elif isinstance(valor, (int, float)):
                                                valores.append(float(valor))
                                            # Strings
                                            else:
                                                valores.append(str(valor))
                                        
                                        try:
                                            cursor.execute(query, valores)
                                            total_inseridos += 1
                                        except mysql.connector.Error as err:
                                            erros += 1
                                            st.warning(f"Linha {_+2} ignorada: {str(err)}")
                                            continue
                                    
                                    conn.commit()
                                    if erros == 0:
                                        st.success(f"✅ Importação concluída! {total_inseridos} registros inseridos com sucesso.")
                                    else:
                                        st.warning(f"⚠️ Importação parcial: {total_inseridos} registros inseridos, {erros} registros com erro.")
                                    
                                except mysql.connector.Error as err:
                                    conn.rollback()
                                    st.error(f"Erro no banco de dados: {err}")
                                except Exception as e:
                                    conn.rollback()
                                    st.error(f"Erro inesperado: {str(e)}")
                                finally:
                                    if conn.is_connected():
                                        cursor.close()
                                        conn.close()
                except Exception as e:
                    st.error(f"Erro ao ler o arquivo: {str(e)}")

    preventivo_entrega(form_key_suffix)

if __name__ == '__main__':
    main("local")
