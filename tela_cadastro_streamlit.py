import streamlit as st 
import requests

def executar_arquivo_remoto(url, form_key_suffix=""):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Cria namespace com variáveis essenciais
            namespace = {
                'form_key_suffix': form_key_suffix,
                'st': st,
                'session_state': st.session_state
            }
            # Executa com escopo isolado
            exec(response.text, namespace)
            
            # Chama main() se existir, passando o sufixo
            if 'main' in namespace:
                namespace['main'](form_key_suffix)
    except Exception as e:
        st.error(f"Erro ao executar {url}: {str(e)}")

# Configuração da página
path = "https://raw.githubusercontent.com/rafael330/srtransporte/main/WhatsApp%20Image%202025-04-09%20at%2021.19.07.png"

with st.sidebar:
    st.image(path, width=280, use_container_width='auto')
    pagina = st.sidebar.selectbox("Selecione a operação:", 
                                ['Cadastros - OPERAÇÃO', 
                                 'Cadastros - FINANCEIRO', 
                                 'Monitoramento'])

# Páginas e abas
if pagina == 'Cadastros - OPERAÇÃO':   
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Cadastro de produção", "Cadastro de cliente", 
                                                  "Cadastro de motorista", "Cadastro de rota", 
                                                  "Cadastro de veículo", "Cadastro de frete extra"])
    
    with tab1:       
        executar_arquivo_remoto("https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_producao.py",
                               form_key_suffix="producao")
        
    
    with tab2:
        executar_arquivo_remoto("https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_cliente.py", 
                               form_key_suffix="cliente_tab")

    with tab3:   
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_motorista.py"
        executar_arquivo_remoto(url,
                               form_key_suffix="motorista_tab")

    with tab4:   
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_rota.py"
        executar_arquivo_remoto(url, 
                               form_key_suffix="rota_tab")

    with tab5:   
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_veiculo.py"
        executar_arquivo_remoto(url,
                               form_key_suffix="veiculo_tab")

    with tab6:   
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_frete_extra.py"
        executar_arquivo_remoto(url,
                               form_key_suffix="frete_extra_tab")

if pagina == 'Cadastros - FINANCEIRO':
    tab1, tab2, tab3 = st.tabs(["Cadastro financeiro", "Cadastro fiscal", "Baixa saldo de frete"])

    with tab1:
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_financeiro.py"
        executar_arquivo_remoto(url,
                               form_key_suffix="financeiro_tab")

    with tab2:
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/cadastro_fiscal.py"
        executar_arquivo_remoto(url,
                               form_key_suffix="fiscal_tab")
    with tab3:
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/baixa_saldo_frete.py"
        executar_arquivo_remoto(url,
                               form_key_suffix="baixa_saldo_tab")

if pagina == 'Monitoramento':
    tab1, tab2 = st.tabs(["Baixa financeira"])

    with tab1:
        url = "https://raw.githubusercontent.com/rafael330/srtransporte/main/baixa_financeira.py"
        executar_arquivo_remoto(url,
                               form_key_suffix="baixa_tab")
