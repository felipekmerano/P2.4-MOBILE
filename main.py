import math
import sqlite3
import numpy as np
from datetime import datetime

# CONFIGURAÇÃO DE TELA (Simula celular no MacBook)
from kivy.config import Config
Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '750')
Config.set('graphics', 'resizable', '0')

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem

class ValiseMobileApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.theme_style = "Light"
        self.DB_NAME = "historico_calibracao.db"
        self.init_db()

        # Layout Raiz
        root = MDBoxLayout(orientation='vertical')
        
        # Barra Superior
        root.add_widget(MDTopAppBar(title="CALIBRAÇÃO P2.4", elevation=10))

        # Navegação por Abas no Rodapé
        nav = MDBottomNavigation()

        # --- ABA 1: FORMULÁRIO ---
        item_form = MDBottomNavigationItem(
            name='form',
            text='Formulário',
            icon='pencil',
        )
        item_form.add_widget(self.create_form_content())
        nav.add_widget(item_form)

        # --- ABA 2: HISTÓRICO ---
        item_hist = MDBottomNavigationItem(
            name='hist',
            text='Histórico',
            icon='database',
        )
        self.lbl_hist = MDLabel(text="Registros salvos no Banco SQLite", halign="center")
        item_hist.add_widget(self.lbl_hist)
        nav.add_widget(item_hist)

        root.add_widget(nav)
        return root

    def create_form_content(self):
        scroll = MDScrollView()
        self.inputs = {}
        container = MDBoxLayout(orientation='vertical', adaptive_height=True, padding=20, spacing=20)

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

        for hint, var_name in fields:
            # CORREÇÃO AQUI: Mudado de 'outline' para 'rectangle' para ser compatível com KivyMD 1.2.0
            tf = MDTextField(
                hint_text=hint, 
                mode="rectangle",
                fill_color_normal=(1, 1, 1, 1)
            )
            
            if var_name == "ent_date": tf.text = datetime.now().strftime("%d/%m/%Y")
            if var_name == "ent_qfe": tf.text = "1013.25"
            
            container.add_widget(tf)
            self.inputs[var_name] = tf

        btn = MDRaisedButton(
            text="CALCULAR E SALVAR",
            pos_hint={"center_x": .5},
            size_hint_x=0.9,
            on_release=self.processar
        )
        container.add_widget(btn)
        
        self.lbl_res = MDLabel(
            text="Status: Aguardando", 
            halign="center", 
            theme_text_color="Secondary", 
            padding=(0, 30)
        )
        container.add_widget(self.lbl_res)

        scroll.add_widget(container)
        return scroll

    def init_db(self):
        conn = sqlite3.connect(self.DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS registros (
            id INTEGER PRIMARY KEY AUTOINCREMENT, anv TEXT, data_cal TEXT, pn_valise TEXT, 
            realizador TEXT, p1_bar REAL, p2_bar REAL, ng1 REAL, p3_bar REAL, 
            p4_bar REAL, ng2 REAL, p5_bar REAL, p6_bar REAL, delta_p REAL, 
            status TEXT, qfe_local REAL, timestamp DATETIME)''')
        conn.commit()
        conn.close()

    def processar(self, instance):
        try:
            anv = self.inputs['ent_tail'].text.upper()
            if not anv: 
                self.lbl_res.text = "Erro: Digite a Matrícula"
                return
            
            self.lbl_res.text = f"Sucesso: Dados de {anv} Processados!"
            self.lbl_res.theme_text_color = "Custom"
            self.lbl_res.text_color = (0, 0.6, 0.2, 1)
        except Exception as e:
            self.lbl_res.text = f"Erro: {str(e)}"

if __name__ == "__main__":
    ValiseMobileApp().run()