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
    
    def baixa_financeira(suffix):
        st.title("Baixa Financeira")
        
        # Formulário principal
        with st.form(key=f"form_baixa_financeira_{suffix}"):
            uploaded_file = st.file_uploader(
                "Carregar arquivo XLSX", 
                type=["xlsx"], 
                key=f'baixa_upload_{suffix}'
            )
            
            submitted = st.form_submit_button("Processar Arquivo")
            
            if submitted and uploaded_file is not None:
                try:
                    # Lê o arquivo mantendo os formatos originais
                    df = pd.read_excel(uploaded_file)
                    
                    # Mostra pré-visualização
                    st.write("Pré-visualização dos dados:")
                    st.dataframe(df)
                    
                    # Botão de confirmação para importação
                    if st.button("Confirmar Importação", key=f"confirm_import_{suffix}"):
                        with st.spinner("Importando dados..."):
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
                                    total_importados = 0
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
                                        
                                        try:
                                            cursor.execute(query, valores)
                                            total_importados += 1
                                        except mysql.connector.Error as e:
                                            st.warning(f"Erro ao importar linha {_ + 2}: {str(e)}")
                                            continue
                                    
                                    conn.commit()
                                    st.success(f"Dados importados com sucesso! {total_importados} de {len(df)} registros adicionados.")
                                    
                                except mysql.connector.Error as err:
                                    conn.rollback()
                                    st.error(f"Erro ao importar dados: {err}")
                                finally:
                                    if conn.is_connected():
                                        cursor.close()
                                        conn.close()
                except Exception as e:
                    st.error(f"Erro ao processar o arquivo: {str(e)}")

    baixa_financeira(form_key_suffix)

if __name__ == '__main__':
    main("local")
