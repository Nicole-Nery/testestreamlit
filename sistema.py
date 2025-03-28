import streamlit as st
import pandas as pd

# Inicializa session state para armazenar dados temporários
if "atas" not in st.session_state:
    st.session_state.atas = []
if "fornecedores" not in st.session_state:
    st.session_state.fornecedores = []
if "empenhos" not in st.session_state:
    st.session_state.empenhos = []

# Layout com abas
tabs = st.tabs(["Registro de Atas", "Cadastro de Fornecedores", "Registro de Empenhos", "Histórico de Empenhos"])

# Registro de Atas
with tabs[0]:
    st.header("Registro de Atas")

    # Formulário para cadastrar nova ATA
    with st.form("nova_ata"):
        nome_ata = st.text_input("Nome da ATA")
        data_ata = st.date_input("Data da ATA")
        fornecedor = st.selectbox("Fornecedor", ["Selecione"] + [f["nome"] for f in st.session_state.fornecedores])

        # Lista de equipamentos da ATA
        equipamentos_ata = []

        # Adicionar equipamentos à ATA
        st.subheader("Equipamentos")

        with st.form("equipamento_ata"):
            especificacao = st.text_input("Especificação")
            marca_modelo = st.text_input("Marca/Modelo")
            codigo = st.text_input("Código")
            unidade = st.selectbox("Unidade", ["Unidade", "Caixa", "Pacote", "Outro"])
            quantidade = st.number_input("Quantidade", min_value=1, step=1)
            valor_unitario = st.number_input("Valor Unitário", min_value=0.0, format="%.2f")
            valor_total = valor_unitario * quantidade if valor_unitario > 0 and quantidade > 0 else 0.0
            adicionar_equipamento = st.form_submit_button("Adicionar Equipamento")

            if adicionar_equipamento:
                equipamentos_ata.append({
                    "especificacao": especificacao,
                    "marca_modelo": marca_modelo,
                    "codigo": codigo,
                    "unidade": unidade,
                    "quantidade": quantidade,
                    "valor_unitario": valor_unitario,
                    "valor_total": valor_total
                })
                st.success(f"Equipamento '{especificacao}' adicionado!")

        # Botão para cadastrar ATA com equipamentos
        submit_ata = st.form_submit_button("Cadastrar ATA")

        if submit_ata and nome_ata and data_ata and fornecedor != "Selecione":
            st.session_state.atas.append({
                "nome": nome_ata,
                "data": data_ata,
                "fornecedor": fornecedor,
                "equipamentos": equipamentos_ata
            })
            st.success(f"ATA '{nome_ata}' cadastrada com sucesso!")

    # Listagem de ATAs cadastradas
    st.subheader("ATAs organizadas por data")
    if st.session_state.atas:
        atas_df = pd.DataFrame(st.session_state.atas)
        st.dataframe(atas_df.sort_values(by="data"))
    else:
        st.info("Nenhuma ATA cadastrada ainda.")

# Cadastro de Fornecedores
with tabs[1]:
    st.header("Cadastro de Fornecedor")

    # Formulário para cadastrar fornecedor
    with st.form("novo_fornecedor"):
        nome_fornecedor = st.text_input("Nome do Fornecedor")
        cnpj = st.text_input("CNPJ")
        info1 = st.text_input("Informação 1")
        info2 = st.text_input("Informação 2")
        observacao = st.text_area("Observação")
        submit_fornecedor = st.form_submit_button("Cadastrar Fornecedor")

        if submit_fornecedor and nome_fornecedor and cnpj:
            st.session_state.fornecedores.append({
                "nome": nome_fornecedor, "cnpj": cnpj, "info1": info1, "info2": info2, "observacao": observacao
            })
            st.success(f"Fornecedor '{nome_fornecedor}' cadastrado!")

    # Listagem de fornecedores
    st.subheader("Fornecedores cadastrados")
    if st.session_state.fornecedores:
        fornecedores_df = pd.DataFrame(st.session_state.fornecedores)
        st.dataframe(fornecedores_df)
    else:
        st.info("Nenhum fornecedor cadastrado ainda.")

# Registro de Empenhos
with tabs[2]:
    st.header("Registro de Empenhos")

    # Seleção da ATA e equipamento
    ata_selecionada = st.selectbox("Selecione a ATA", ["Selecione"] + [a["nome"] for a in st.session_state.atas])
    equipamento = st.text_input("Nome do Equipamento")
    quantidade = st.number_input("Quantidade", min_value=1, step=1)
    registrar_empenho = st.button("Registrar Empenho")

    if registrar_empenho and ata_selecionada != "Selecione" and equipamento:
        st.session_state.empenhos.append({"ata": ata_selecionada, "equipamento": equipamento, "quantidade": quantidade})
        st.success("Empenho registrado!")

# Histórico de Empenhos
with tabs[3]:
    st.header("Histórico de Empenhos")

    # Seleção de ATA para filtrar empenhos
    ata_filtro = st.selectbox("Filtrar por ATA", ["Todas"] + [a["nome"] for a in st.session_state.atas])
    
    if st.session_state.empenhos:
        df_empenhos = pd.DataFrame(st.session_state.empenhos)
        
        if ata_filtro != "Todas":
            df_empenhos = df_empenhos[df_empenhos["ata"] == ata_filtro]
        
        st.dataframe(df_empenhos)
    else:
        st.info("Nenhum empenho registrado ainda.")

        
        st.dataframe(df_empenhos)
    else:
        st.info("Nenhum empenho registrado ainda.")

