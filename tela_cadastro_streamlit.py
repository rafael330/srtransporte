import streamlit as st 
import os
import requests

path = "https://raw.githubusercontent.com/rafael330/srtransporte/main/WhatsApp%20Image%202025-04-09%20at%2021.19.07.png"

with st.sidebar:
    st.image(
        path,
        width=280,  
        use_container_width='auto'  
    )

pagina = st.sidebar.selectbox("Selecione a operação:", 
                              ['Cadastros - OPERAÇÃO', 
                               'Cadastros - FINANCEIRO', 
                               'Monitoramento'],
                              key="cadastro")

def executar_arquivo_remoto(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Cria um namespace local para execução
            local_vars = {}
            exec(response.text, globals(), local_vars)
            
            # Chama a função principal se existir
            if 'cadastro_producao' in local_vars:
                local_vars['cadastro_producao']()
            else:
                st.error("Função principal não encontrada no arquivo remoto")
        else:
            st.error(f"Arquivo não encontrado no repositório: {url}")
    except Exception as e:
        st.error(f"Erro ao executar o arquivo: {str(e)}")

if pagina == 'Cadastros - OPERAÇÃO':   
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Cadastro de produção", "Cadastro de cliente", "Cadastro de motorista", "Cadastro de rota", "Cadastro de veículo", "Cadastro de frete extra"])    
    
    with tab1:
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_producao.py"
        executar_arquivo_remoto(url)

    with tab2:
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_cliente.py"
        executar_arquivo_remoto(url)

    with tab3:   
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_motorista.py"
        executar_arquivo_remoto(url)

    with tab4:   
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_rota.py"
        executar_arquivo_remoto(url)

    with tab5:   
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_veiculo.py"
        executar_arquivo_remoto(url)

    with tab6:   
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_frete_extra.py"
        executar_arquivo_remoto(url)

if pagina == 'Cadastros - FINANCEIRO':
    tab1, tab2 = st.tabs(["Cadastro financeiro", "Cadastro fiscal"])

    with tab1:
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_financeiro.py"
        executar_arquivo_remoto(url)

    with tab2:
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_fiscal.py"
        executar_arquivo_remoto(url)

if pagina == 'Monitoramento':
    tab1, tab2 = st.tabs(["Baixa financeira", "Preventivo de entrega"])

    with tab1:
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/baixa_financeira.py"
        executar_arquivo_remoto(url)

    with tab2:
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/preventivo_entrega.py"
        executar_arquivo_remoto(url)
