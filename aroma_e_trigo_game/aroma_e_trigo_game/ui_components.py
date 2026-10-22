"""
Componentes da Interface de Usuário (HUD, Navbar, Banner de Missão e Barra Lateral do Carrinho)
Inspirado 100% no layout e CSS do site https://padariaaromaetrigo.netlify.app/
Com suporte a Tela Cheia, Guia Passo a Passo da Missão Diária e Controles Ágeis.
"""
import os
import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk

from config import PALETTE, BRAND, PRODUCTS, MISSIONS, ASSETS_DIR
import sound_effects
from dialogs import get_product_image

class HeaderNavbar(tk.Frame):
    """Navbar superior idêntica à do site padariaaromaetrigo.netlify.app"""
    def __init__(self, parent, on_cart_click, on_help_click, on_missions_click):
        super().__init__(parent, bg=PALETTE["primary"], padx=15, pady=8)
        self.on_cart_click = on_cart_click
        self.on_help_click = on_help_click
        self.on_missions_click = on_missions_click
        self._build_ui()

    def _build_ui(self):
        # 1. Logo da Padaria Aroma & Trigo
        logo_path = os.path.join(ASSETS_DIR, "logo_aroma_e_trigo.png")
        if os.path.exists(logo_path):
            try:
                pil_logo = Image.open(logo_path).resize((46, 46), Image.Resampling.LANCZOS)
                self.logo_tk = ImageTk.PhotoImage(pil_logo)
                logo_lbl = tk.Label(self, image=self.logo_tk, bg=PALETTE["primary"])
                logo_lbl.pack(side="left", padx=(0, 10))
            except Exception:
                pass

        # 2. Títulos e Slogan
        titles_frame = tk.Frame(self, bg=PALETTE["primary"])
        titles_frame.pack(side="left")

        title_lbl = tk.Label(
            titles_frame, text=BRAND["name"],
            font=("Georgia", 13, "bold"), fg="#ffffff", bg=PALETTE["primary"]
        )
        title_lbl.pack(anchor="w")

        slogan_lbl = tk.Label(
            titles_frame, text=BRAND["slogan"],
            font=("Segoe UI", 8, "italic"), fg=PALETTE["accent_light"], bg=PALETTE["primary"]
        )
        slogan_lbl.pack(anchor="w")

        # 3. Badge do Projeto Pronatec
        pronatec_badge = tk.Frame(self, bg=PALETTE["dark"], padx=8, pady=3)
        pronatec_badge.pack(side="left", padx=(15, 0))
        tk.Label(
            pronatec_badge, text=f"✨ {BRAND['course_info']}",
            font=("Segoe UI", 8, "bold"), fg=PALETTE["accent_light"], bg=PALETTE["dark"]
        ).pack()

        # 4. Atalhos da Direita: Missão Diária, Site Oficial e Carrinho
        right_frame = tk.Frame(self, bg=PALETTE["primary"])
        right_frame.pack(side="right")

        # Botão Missão Diária em Destaque
        mission_btn = tk.Button(
            right_frame, text="🎯 Missão Diária", font=("Segoe UI", 8, "bold"),
            bg=PALETTE["gold"], fg=PALETTE["dark"], activebackground="#e6c200",
            activeforeground=PALETTE["dark"], relief="flat", padx=9, pady=4, cursor="hand2",
            command=self.on_missions_click
        )
        mission_btn.pack(side="left", padx=4)

        # Botão link do site
        site_btn = tk.Button(
            right_frame, text="🌐 Acessar Site", font=("Segoe UI", 8, "bold"),
            bg=PALETTE["primary_hover"], fg="#ffffff", activebackground=PALETTE["accent"],
            activeforeground="#ffffff", relief="flat", padx=9, pady=4, cursor="hand2",
            command=lambda: webbrowser.open(BRAND["site_url"])
        )
        site_btn.pack(side="left", padx=4)

        # Botão Como Jogar
        help_btn = tk.Button(
            right_frame, text="❓ Ajuda", font=("Segoe UI", 8, "bold"),
            bg=PALETTE["primary_hover"], fg="#ffffff", activebackground=PALETTE["accent"],
            activeforeground="#ffffff", relief="flat", padx=7, pady=4, cursor="hand2",
            command=self.on_help_click
        )
        help_btn.pack(side="left", padx=4)

        # Botão de Carrinho com badge laranja
        self.cart_btn = tk.Button(
            right_frame, text="🛒 Carrinho (0)", font=("Segoe UI", 9, "bold"),
            bg=PALETTE["accent"], fg="#ffffff", activebackground="#b85412",
            activeforeground="#ffffff", relief="flat", padx=11, pady=4, cursor="hand2",
            command=self.on_cart_click
        )
        self.cart_btn.pack(side="left", padx=(4, 0))

    def update_cart_count(self, count):
        self.cart_btn.config(text=f"🛒 Carrinho ({count})")


class MissionGuideBanner(tk.Frame):
    """Faixa orientadora no topo mostrando o passo exato da missão em tempo real"""
    def __init__(self, parent, on_banner_click):
        super().__init__(parent, bg="#fff3cd", padx=12, pady=6, highlightbackground=PALETTE["gold"], highlightthickness=1)
        self.on_banner_click = on_banner_click
        self._build_ui()

    def _build_ui(self):
        self.icon_lbl = tk.Label(self, text="🎯", font=("Segoe UI", 12), bg="#fff3cd")
        self.icon_lbl.pack(side="left", padx=(0, 6))

        self.text_lbl = tk.Label(
            self, text="Carregando missão diária...",
            font=("Segoe UI", 9, "bold"), fg=PALETTE["dark"], bg="#fff3cd"
        )
        self.text_lbl.pack(side="left")

        self.action_btn = tk.Button(
            self, text="Ver Roteiro Completo", font=("Segoe UI", 8, "bold"),
            bg=PALETTE["primary"], fg="#ffffff", relief="flat", padx=8, pady=2,
            cursor="hand2", command=self.on_banner_click
        )
        self.action_btn.pack(side="right")

    def update_guide(self, step_text, is_all_collected=False):
        if is_all_collected:
            self.configure(bg="#e8f5e9", highlightbackground=PALETTE["success"])
            self.icon_lbl.configure(text="🎉", bg="#e8f5e9")
            self.text_lbl.configure(
                text=f"TODOS OS ITENS REUNIDOS! {step_text}",
                fg=PALETTE["success"], bg="#e8f5e9"
            )
        else:
            self.configure(bg="#fff3cd", highlightbackground=PALETTE["gold"])
            self.icon_lbl.configure(text="🎯", bg="#fff3cd")
            self.text_lbl.configure(
                text=step_text,
                fg=PALETTE["dark"], bg="#fff3cd"
            )


class SideCartPanel(tk.Frame):
    """Barra lateral com Carrinho de Compras, Status e Detalhes da Missão Diária"""
    def __init__(self, parent, on_checkout_request, on_mission_change_request):
        super().__init__(parent, bg=PALETTE["card_bg"], highlightbackground=PALETTE["card_border"], highlightthickness=1, width=320)
        self.pack_propagate(False)
        self.on_checkout_request = on_checkout_request
        self.on_mission_change_request = on_mission_change_request
        self._build_ui()

    def _build_ui(self):
        # Header da Sidebar
        header = tk.Frame(self, bg=PALETTE["primary"], padx=10, pady=8)
        header.pack(fill="x")

        tk.Label(
            header, text="🛒 Carrinho & Missão Diária",
            font=("Georgia", 11, "bold"), fg="#ffffff", bg=PALETTE["primary"]
        ).pack(side="left")

        # Cartão de Status do Jogador (Saldo e Pontos)
        status_card = tk.Frame(self, bg=PALETTE["bg"], padx=10, pady=7, highlightbackground=PALETTE["card_border"], highlightthickness=1)
        status_card.pack(fill="x", padx=8, pady=6)

        row1 = tk.Frame(status_card, bg=PALETTE["bg"])
        row1.pack(fill="x")
        tk.Label(row1, text="💵 Carteira:", font=("Segoe UI", 8, "bold"), fg=PALETTE["text"], bg=PALETTE["bg"]).pack(side="left")
        self.wallet_lbl = tk.Label(row1, text="R$ 100,00", font=("Segoe UI", 9, "bold"), fg=PALETTE["success"], bg=PALETTE["bg"])
        self.wallet_lbl.pack(side="right")

        row2 = tk.Frame(status_card, bg=PALETTE["bg"])
        row2.pack(fill="x", pady=(2, 0))
        tk.Label(row2, text="🌟 Fidelidade:", font=("Segoe UI", 8, "bold"), fg=PALETTE["text"], bg=PALETTE["bg"]).pack(side="left")
        self.points_lbl = tk.Label(row2, text="0 pts", font=("Segoe UI", 8, "bold"), fg=PALETTE["accent"], bg=PALETTE["bg"])
        self.points_lbl.pack(side="right")

        # PAINEL DETALHADO DA MISSÃO DIÁRIA
        self.mission_box = tk.Frame(self, bg="#fff8e7", padx=8, pady=6, highlightbackground="#ffe0b2", highlightthickness=1)
        self.mission_box.pack(fill="x", padx=8, pady=(0, 6))

        m_header = tk.Frame(self.mission_box, bg="#fff8e7")
        m_header.pack(fill="x")
        tk.Label(m_header, text="🌟 MISSÃO DIÁRIA", font=("Segoe UI", 8, "bold"), fg=PALETTE["primary"], bg="#fff8e7").pack(side="left")

        m_btn = tk.Button(
            m_header, text="Trocar", font=("Segoe UI", 7, "bold"),
            bg=PALETTE["accent_light"], fg=PALETTE["dark"], relief="flat", padx=4, pady=1,
            cursor="hand2", command=self.on_mission_change_request
        )
        m_btn.pack(side="right")

        self.mission_title_lbl = tk.Label(
            self.mission_box, text="", font=("Segoe UI", 8, "bold"),
            fg=PALETTE["dark"], bg="#fff8e7", wraplength=280, justify="left"
        )
        self.mission_title_lbl.pack(fill="x", pady=2)

        # Container dos passos da missão
        self.steps_container = tk.Frame(self.mission_box, bg="#fff8e7")
        self.steps_container.pack(fill="x", pady=2)

        # Instrução do próximo passo
        self.next_action_lbl = tk.Label(
            self.mission_box, text="", font=("Segoe UI", 7, "bold"),
            fg=PALETTE["primary"], bg="#fff8e7", wraplength=280, justify="left"
        )
        self.next_action_lbl.pack(fill="x", pady=(2, 0))

        # CARTÃO DO CLIENTE DA PADARIA (ATENDIMENTO)
        self.customer_box = tk.Frame(self, bg="#f0f7ff", padx=8, pady=6, highlightbackground="#b3d7ff", highlightthickness=1)
        self.customer_box.pack(fill="x", padx=8, pady=(0, 6))

        c_header = tk.Frame(self.customer_box, bg="#f0f7ff")
        c_header.pack(fill="x")
        tk.Label(c_header, text="👤 CLIENTE NO SALÃO", font=("Segoe UI", 8, "bold"), fg="#0277bd", bg="#f0f7ff").pack(side="left")
        self.customer_served_lbl = tk.Label(c_header, text="Atendidos: 0", font=("Segoe UI", 7, "bold"), fg="#0277bd", bg="#f0f7ff")
        self.customer_served_lbl.pack(side="right")

        self.customer_info_lbl = tk.Label(
            self.customer_box, text="Aguardando chegada de cliente...", font=("Segoe UI", 8),
            fg=PALETTE["dark"], bg="#f0f7ff", wraplength=280, justify="left"
        )
        self.customer_info_lbl.pack(fill="x", pady=2)

        self.customer_status_lbl = tk.Label(
            self.customer_box, text="", font=("Segoe UI", 7, "bold"),
            fg="#e65100", bg="#f0f7ff", wraplength=280, justify="left"
        )
        self.customer_status_lbl.pack(fill="x")

        # Lista de Itens no Carrinho (Área com Scroll)
        tk.Label(self, text="Itens Escolhidos no Cesto:", font=("Segoe UI", 8, "bold"), fg=PALETTE["text_muted"], bg=PALETTE["card_bg"]).pack(anchor="w", padx=10, pady=(2, 2))

        cart_container = tk.Frame(self, bg=PALETTE["card_bg"])
        cart_container.pack(fill="both", expand=True, padx=8)

        self.cart_canvas = tk.Canvas(cart_container, bg=PALETTE["card_bg"], highlightthickness=0)
        self.cart_sb = ttk.Scrollbar(cart_container, orient="vertical", command=self.cart_canvas.yview)
        self.cart_items_frame = tk.Frame(self.cart_canvas, bg=PALETTE["card_bg"])

        self.cart_items_frame.bind(
            "<Configure>",
            lambda e: self.cart_canvas.configure(scrollregion=self.cart_canvas.bbox("all"))
        )
        self.cart_canvas.create_window((0, 0), window=self.cart_items_frame, anchor="nw", width=285)
        self.cart_canvas.configure(yscrollcommand=self.cart_sb.set)

        self.cart_canvas.pack(side="left", fill="both", expand=True)
        self.cart_sb.pack(side="right", fill="y")

        # Rodapé do Carrinho
        footer = tk.Frame(self, bg=PALETTE["bg"], padx=10, pady=8, highlightbackground=PALETTE["card_border"], highlightthickness=1)
        footer.pack(fill="x", side="bottom")

        total_row = tk.Frame(footer, bg=PALETTE["bg"])
        total_row.pack(fill="x", pady=(0, 6))
        tk.Label(total_row, text="Total no Cesto:", font=("Segoe UI", 9, "bold"), fg=PALETTE["text"], bg=PALETTE["bg"]).pack(side="left")
        self.total_lbl = tk.Label(total_row, text="R$ 0,00", font=("Segoe UI", 12, "bold"), fg=PALETTE["success"], bg=PALETTE["bg"])
        self.total_lbl.pack(side="right")

        self.checkout_btn = tk.Button(
            footer, text="💳 Pagar no Caixa & Finalizar", font=("Segoe UI", 10, "bold"),
            bg=PALETTE["success"], fg="#ffffff", activebackground="#216425",
            activeforeground="#ffffff", relief="flat", pady=7, cursor="hand2",
            command=self.on_checkout_request
        )
        self.checkout_btn.pack(fill="x")

    def update_data(self, cart, wallet_balance, loyalty_points, active_mission, on_item_change, customer=None, served_count=0):
        """Atualiza dinamicamente a lista de itens, valores, passos da missão e cliente atual"""
        self.wallet_lbl.config(text=f"R$ {wallet_balance:.2f}".replace(".", ","))
        self.points_lbl.config(text=f"{loyalty_points} pts")
        self.customer_served_lbl.config(text=f"Atendidos: {served_count}")

        # Atualizar Cliente Atual
        if customer and customer.state != "done":
            items_desc = " + ".join([f"{it['name']} ({it['icon']})" for it in customer.order])
            self.customer_info_lbl.config(text=f"👤 {customer.name} pediu:\n{items_desc}")
            if customer.state == "waiting":
                has_items = customer.check_has_order(cart)
                if has_items:
                    self.customer_status_lbl.config(
                        text="🎁 Você tem o pedido! Vá até o cliente e aperte [E] para entregar!",
                        fg=PALETTE["success"]
                    )
                else:
                    self.customer_status_lbl.config(
                        text=f"⏳ Pegue nas vitrines (+R$ {customer.total_price + customer.tip:.2f} gorjeta)",
                        fg="#e65100"
                    )
            elif customer.state == "eating":
                self.customer_status_lbl.config(
                    text="😋 Saboreando o pedido satisfeito!",
                    fg=PALETTE["success"]
                )
            elif customer.state == "entering":
                self.customer_status_lbl.config(
                    text="🚶 Chegando à mesa...",
                    fg="#0277bd"
                )
            else:
                self.customer_status_lbl.config(
                    text="👋 Agradecendo e saindo da padaria...",
                    fg=PALETTE["text_muted"]
                )
        else:
            self.customer_info_lbl.config(text="Aguardando chegada do próximo cliente...")
            self.customer_status_lbl.config(text="Novos clientes chegam a cada momento!", fg=PALETTE["text_muted"])

        # Atualizar Passos Detalhados da Missão
        for w in self.steps_container.winfo_children():
            w.destroy()

        if active_mission:
            self.mission_title_lbl.config(text=active_mission["title"])
            steps = active_mission.get("steps", [])
            all_done = True
            first_missing_hint = None

            for i, step in enumerate(steps, 1):
                item_id = step["item_id"]
                have = cart.get(item_id, 0) >= 1
                if not have and all_done:
                    all_done = False
                    first_missing_hint = f"Passo {i}: Vá até [{step['zone_name']}] e pegue 1x {step['name']}!"

                row = tk.Frame(self.steps_container, bg="#fff8e7")
                row.pack(fill="x", pady=1)

                icon_txt = "✅" if have else "⬜"
                color = PALETTE["success"] if have else PALETTE["text"]
                tk.Label(row, text=icon_txt, font=("Segoe UI", 8), bg="#fff8e7").pack(side="left")
                tk.Label(
                    row, text=f"{step['name']}",
                    font=("Segoe UI", 8, "bold" if not have else "normal"),
                    fg=color, bg="#fff8e7"
                ).pack(side="left", padx=(2, 4))
                tk.Label(
                    row, text=f"📍 {step['zone_id'].replace('_', ' ').title()}",
                    font=("Segoe UI", 7), fg=PALETTE["text_muted"], bg="#fff8e7"
                ).pack(side="right")

            if all_done:
                self.next_action_lbl.config(
                    text="🎉 Todos os itens no cesto! Vá até o Balcão do Caixa (Juliana) e aperte [E] para finalizar!",
                    fg=PALETTE["success"]
                )
            else:
                self.next_action_lbl.config(
                    text=f"👉 {first_missing_hint}",
                    fg=PALETTE["primary"]
                )
        else:
            self.mission_title_lbl.config(text="Modo Livre")
            self.next_action_lbl.config(text="Explore a padaria e compre à vontade!")

        # Atualizar Itens do Carrinho
        for widget in self.cart_items_frame.winfo_children():
            widget.destroy()

        total = 0.0
        if not cart:
            empty_lbl = tk.Label(
                self.cart_items_frame, text="Cesto vazio!\nAnde com W, A, S, D\n(Segure Shift para Correr)\ne aperte [E] nas vitrines",
                font=("Segoe UI", 8, "italic"), fg=PALETTE["text_muted"], bg=PALETTE["card_bg"], pady=15
            )
            empty_lbl.pack()
        else:
            for pid, qty in list(cart.items()):
                prod = next((p for p in PRODUCTS if p["id"] == pid), None)
                if not prod:
                    continue

                subtotal = prod["price"] * qty
                total += subtotal

                row = tk.Frame(self.cart_items_frame, bg=PALETTE["card_bg"], highlightbackground="#f0e6d6", highlightthickness=1, padx=4, pady=3)
                row.pack(fill="x", pady=2)

                thumb = get_product_image(prod["image"], size=(26, 26))
                if thumb:
                    t_lbl = tk.Label(row, image=thumb, bg=PALETTE["card_bg"])
                    t_lbl.image = thumb
                    t_lbl.pack(side="left", padx=(0, 4))
                else:
                    tk.Label(row, text=prod["icon"], font=("Segoe UI", 11), bg=PALETTE["card_bg"]).pack(side="left", padx=(0, 4))

                info = tk.Frame(row, bg=PALETTE["card_bg"])
                info.pack(side="left", fill="both", expand=True)
                tk.Label(info, text=prod["name"][:18], font=("Segoe UI", 8, "bold"), fg=PALETTE["text"], bg=PALETTE["card_bg"], anchor="w").pack(fill="x")
                tk.Label(info, text=f"{qty}x R$ {prod['price']:.2f} = R$ {subtotal:.2f}".replace(".", ","), font=("Segoe UI", 7), fg=PALETTE["success"], bg=PALETTE["card_bg"], anchor="w").pack(fill="x")

                btn_f = tk.Frame(row, bg=PALETTE["card_bg"])
                btn_f.pack(side="right")

                p_id = prod["id"]
                tk.Button(
                    btn_f, text="-", font=("Segoe UI", 7, "bold"), width=2,
                    relief="flat", bg="#e0e0e0", cursor="hand2",
                    command=lambda i=p_id: on_item_change(i, -1)
                ).pack(side="left", padx=1)

                tk.Button(
                    btn_f, text="+", font=("Segoe UI", 7, "bold"), width=2,
                    relief="flat", bg=PALETTE["primary"], fg="#ffffff", cursor="hand2",
                    command=lambda i=p_id: on_item_change(i, 1)
                ).pack(side="left", padx=1)

        self.total_lbl.config(text=f"R$ {total:.2f}".replace(".", ","))


class FooterHUD(tk.Frame):
    """Barra inferior com instruções, velocidade, botão tela cheia e som"""
    def __init__(self, parent, on_key_sim, on_toggle_sound, on_open_site, on_toggle_fullscreen):
        super().__init__(parent, bg=PALETTE["dark"], padx=15, pady=6)
        self.on_key_sim = on_key_sim
        self.on_toggle_sound = on_toggle_sound
        self.on_open_site = on_open_site
        self.on_toggle_fullscreen = on_toggle_fullscreen
        self._build_ui()

    def _build_ui(self):
        left_f = tk.Frame(self, bg=PALETTE["dark"])
        left_f.pack(side="left")

        keys_lbl = tk.Label(
            left_f,
            text="🎮 [W][A][S][D] Mover Rápido | [Shift] Correr | [E] ou [Espaço] Interagir | [F11] Tela Cheia",
            font=("Segoe UI", 8, "bold"), fg=PALETTE["accent_light"], bg=PALETTE["dark"]
        )
        keys_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            left_f,
            text=f"Padaria Aroma & Trigo • {BRAND['site_url'].replace('https://', '')} • Pronatec IA",
            font=("Segoe UI", 7, "italic"), fg="#aaaaaa", bg=PALETTE["dark"]
        )
        sub_lbl.pack(anchor="w")

        right_f = tk.Frame(self, bg=PALETTE["dark"])
        right_f.pack(side="right")

        fullscreen_btn = tk.Button(
            right_f, text="⛶ Tela Cheia", font=("Segoe UI", 8, "bold"),
            bg="#5d4037", fg="#ffffff", activebackground=PALETTE["accent"],
            activeforeground="#ffffff", relief="flat", padx=8, pady=3,
            cursor="hand2", command=self.on_toggle_fullscreen
        )
        fullscreen_btn.pack(side="left", padx=3)

        self.sound_btn = tk.Button(
            right_f, text="🔊 Som: ON", font=("Segoe UI", 8, "bold"),
            bg=PALETTE["primary"], fg="#ffffff", relief="flat", padx=8, pady=3,
            cursor="hand2", command=self._toggle_sound_click
        )
        self.sound_btn.pack(side="left", padx=3)

        site_btn = tk.Button(
            right_f, text="🌐 Abrir Site", font=("Segoe UI", 8, "bold"),
            bg=PALETTE["accent"], fg="#ffffff", relief="flat", padx=8, pady=3,
            cursor="hand2", command=self.on_open_site
        )
        site_btn.pack(side="left", padx=3)

    def _toggle_sound_click(self):
        state = self.on_toggle_sound()
        self.sound_btn.config(text=f"🔊 Som: {'ON' if state else 'OFF'}")
