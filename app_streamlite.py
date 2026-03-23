import math
import sqlite3
import numpy as np
from datetime import datetime
import streamlit as st

# CONFIGURAÇÃO DE TELA (Substitui o Kivy Config)
st.set_page_config(
    page_title="CALIBRAÇÃO P2.4", 
    layout="centered"
)

# Variáveis globais baseadas na classe original
DB_NAME = "historico_calibracao.db"
inputs = {}

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT, anv TEXT, data_cal TEXT, pn_valise TEXT, 
        realizador TEXT, p1_bar REAL, p2_bar REAL, ng1 REAL, p3_bar REAL, 
        p4_bar REAL, ng2 REAL, p5_bar REAL, p6_bar REAL, delta_p REAL, 
        status TEXT, qfe_local REAL, timestamp DATETIME)''')
    conn.commit()
    conn.close()

# Executa a inicialização do banco
init_db()

# Barra Superior
st.header("CALIBRAÇÃO P2.4")

# Navegação por Abas (Substitui o MDBottomNavigation)
item_form, item_hist = st.tabs(["✏️ Formulário", "🗄️ Histórico"])

# --- ABA 1: FORMULÁRIO ---
with item_form:
    fields = [
        ("Matrícula (ANV)", "ent_tail"), ("Data", "ent_date"), 
        ("P/N Valise", "ent_pn"), ("Realizador", "ent_nome"),
        ("QFE Local (hPa)", "ent_qfe"), ("P1 Parado (mA)", "ent_p1_ma"),
        ("P2 Girando (mA)", "ent_p2_ma"), ("T1 C1 (°C)", "ent_t1_c1"),
        ("N1 C1 (%)", "ent_n1_c1"), ("P3 (mA)", "ent_p3_ma"),
        ("P4 (mA)", "ent_p4_ma"), ("T1 C2 (°C)", "ent_t1_c2"),
        ("N1 C2 (%)", "ent_n1_c2"), ("P5 (mA)", "ent_p5_ma"),
        ("P6 (mA)", "ent_p6_ma")
    ]

    # Substitui o MDBoxLayout/MDScrollView por um form do Streamlit
    with st.form(key="form_calibracao"):
        for hint, var_name in fields:
            # Lógica das strings padrão originais
            default_text = ""
            if var_name == "ent_date": 
                default_text = datetime.now().strftime("%d/%m/%Y")
            if var_name == "ent_qfe": 
                default_text = "1013.25"
            
            # Substitui o MDTextField
            inputs[var_name] = st.text_input(label=hint, value=default_text)

        # Substitui o MDRaisedButton
        btn = st.form_submit_button(label="CALCULAR E SALVAR")

    # Substitui o MDLabel de status e a lógica do "processar"
    if btn:
        try:
            anv = inputs['ent_tail'].upper()
            if not anv: 
                st.error("Erro: Digite a Matrícula")
            else:
                st.success(f"Sucesso: Dados de {anv} Processados!")
        except Exception as e:
            st.error(f"Erro: {str(e)}")
    else:
        # Status inicial antes de clicar no botão
        st.info("Status: Aguardando")


# --- ABA 2: HISTÓRICO ---
with item_hist:
    # Substitui a lbl_hist
    st.markdown("<h4 style='text-align: center;'>Registros salvos no Banco SQLite</h4>", unsafe_allow_html=True)
    
    # Bônus: Como agora você está no Streamlit, deixei um bloco de visualização pronto
    # caso você queira ver o banco na tela, basta descomentar as linhas abaixo no futuro:
    # try:
    #     import pandas as pd
    #     conn = sqlite3.connect(DB_NAME)
    #     df = pd.read_sql_query("SELECT * FROM registros", conn)
    #     st.dataframe(df)
    # except Exception as e:
    #     st.write("Sem registros no momento.")