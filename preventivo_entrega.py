import streamlit as st
import mysql.connector
import pandas as pd

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
            
            # Colunas obrigatórias (ajuste conforme necessário)
            colunas_obrigatorias = ['PEDIDO CLIENTE', 'PEDIDO GEMGO', 'NUMERO NOTA FISCAL']
            
            # Verifica colunas faltantes
            colunas_faltantes = [col for col in colunas_obrigatorias if col not in df.columns]
            if colunas_faltantes:
                st.error(f"Colunas obrigatórias faltantes: {', '.join(colunas_faltantes)}")
                return
            
            if st.button("Importar para Preventivo"):
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
                                st.error(f"Erro na linha {total_inseridos+1}: {err}")
                                st.error(f"Valores problemáticos: {valores}")
                                conn.rollback()
                                return
                        
                        conn.commit()
                        st.success(f"Dados importados com sucesso! {total_inseridos}/{len(df)} registros inseridos.")
                        
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

preventivo_entrega()    