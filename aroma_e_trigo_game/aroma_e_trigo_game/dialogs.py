"""
Modais e Telas de Interação da Padaria Aroma & Trigo
- Vitrine de Compras com fotos reais dos produtos
- Caixa Registradora e Cupom Fiscal Eletrônico oficial com identidade visual do site
- Missões e Desafios Pronatec
- Instruções de Controles (W, A, S, D)
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
from datetime import datetime
from PIL import Image, ImageTk

from config import PALETTE, BRAND, PRODUCTS, MISSIONS, ASSETS_DIR
import sound_effects

_image_cache = {}

def get_product_image(image_filename, size=(80, 80)):
    """Carrega e redimensiona imagem do produto com cache para performance"""
    cache_key = (image_filename, size)
    if cache_key in _image_cache:
        return _image_cache[cache_key]

    path = os.path.join(ASSETS_DIR, image_filename)
    if not os.path.exists(path):
        # Fallback caso não exista
        path = os.path.join(ASSETS_DIR, "logo_aroma_e_trigo.png")

    try:
        pil_img = Image.open(path)
        pil_img = pil_img.resize(size, Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(pil_img)
        _image_cache[cache_key] = tk_img
        return tk_img
    except Exception:
        return None

class ShelfDialog(tk.Toplevel):
    """Janela de compras da Vitrine / Balcão"""
    def __init__(self, parent, zone_info, cart, on_cart_change):
        super().__init__(parent)
        self.zone_info = zone_info
        self.cart = cart
        self.on_cart_change = on_cart_change

        self.title(f"Aroma & Trigo - {zone_info['name']}")
        self.geometry("640x520")
        self.resizable(False, False)
        self.configure(bg=PALETTE["bg"])
        self.transient(parent)
        self.grab_set()

        sound_effects.play_interact()
        self._build_ui()
        self.bind("<Escape>", lambda e: self.destroy())

    def _build_ui(self):
        # Header temático com cores do site
        header = tk.Frame(self, bg=PALETTE["primary"], padx=15, pady=12)
        header.pack(fill="x")

        title_lbl = tk.Label(
            header, text=self.zone_info["name"],
            font=("Georgia", 14, "bold"), fg="#ffffff", bg=PALETTE["primary"]
        )
        title_lbl.pack(side="left")

        sub_lbl = tk.Label(
            header, text=f"🌐 {BRAND['site_url'].replace('https://', '')}",
            font=("Segoe UI", 9, "italic"), fg=PALETTE["accent_light"], bg=PALETTE["primary"]
        )
        sub_lbl.pack(side="right")

        # Instrução
        hint_frame = tk.Frame(self, bg=PALETTE["accent_light"], padx=10, pady=6)
        hint_frame.pack(fill="x")
        hint_lbl = tk.Label(
            hint_frame, text=f"🥖 Selecione os itens que deseja levar para sua cesta de compras:",
            font=("Segoe UI", 9), fg=PALETTE["dark"], bg=PALETTE["accent_light"]
        )
        hint_lbl.pack(anchor="w")

        # Área de Rolagem dos Produtos
        container = tk.Frame(self, bg=PALETTE["bg"])
        container.pack(fill="both", expand=True, padx=15, pady=10)

        canvas = tk.Canvas(container, bg=PALETTE["bg"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=PALETTE["bg"])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Filtrar produtos desta seção
        zone_products = [p for p in PRODUCTS if p["zone"] == self.zone_info["id"]]

        for prod in zone_products:
            self._create_product_card(scrollable_frame, prod)

        # Rodapé com botão de fechar
        footer = tk.Frame(self, bg=PALETTE["bg"], padx=15, pady=10)
        footer.pack(fill="x")

        close_btn = tk.Button(
            footer, text="Concluir Escolha e Voltar à Padaria",
            font=("Segoe UI", 10, "bold"), bg=PALETTE["primary"], fg="#ffffff",
            activebackground=PALETTE["primary_hover"], activeforeground="#ffffff",
            relief="flat", padx=15, pady=8, cursor="hand2", command=self.destroy
        )
        close_btn.pack(side="right")

    def _create_product_card(self, parent, prod):
        card = tk.Frame(parent, bg=PALETTE["card_bg"], highlightbackground=PALETTE["card_border"], highlightthickness=1, padx=10, pady=8)
        card.pack(fill="x", pady=6, padx=5)

        # Foto do Produto
        img = get_product_image(prod["image"], size=(75, 75))
        if img:
            img_lbl = tk.Label(card, image=img, bg=PALETTE["card_bg"])
            img_lbl.image = img
            img_lbl.pack(side="left", padx=(0, 12))
        else:
            icon_lbl = tk.Label(card, text=prod["icon"], font=("Segoe UI", 28), bg=PALETTE["card_bg"])
            icon_lbl.pack(side="left", padx=(0, 12))

        # Informações de Texto
        info_frame = tk.Frame(card, bg=PALETTE["card_bg"])
        info_frame.pack(side="left", fill="both", expand=True)

        name_lbl = tk.Label(info_frame, text=prod["name"], font=("Segoe UI", 11, "bold"), fg=PALETTE["text"], bg=PALETTE["card_bg"], anchor="w")
        name_lbl.pack(fill="x")

        desc_lbl = tk.Label(info_frame, text=prod["desc"], font=("Segoe UI", 8), fg=PALETTE["text_muted"], bg=PALETTE["card_bg"], anchor="w", wraplength=280, justify="left")
        desc_lbl.pack(fill="x", pady=(2, 4))

        price_lbl = tk.Label(info_frame, text=f"R$ {prod['price']:.2f}".replace(".", ","), font=("Segoe UI", 11, "bold"), fg=PALETTE["success"], bg=PALETTE["card_bg"], anchor="w")
        price_lbl.pack(fill="x")

        # Controles de Adição / Carrinho
        action_frame = tk.Frame(card, bg=PALETTE["card_bg"])
        action_frame.pack(side="right", padx=5)

        qty_var = tk.StringVar(value=f"No cesto: {self.cart.get(prod['id'], 0)}")

        def add_item():
            current = self.cart.get(prod["id"], 0)
            self.cart[prod["id"]] = current + 1
            qty_var.set(f"No cesto: {self.cart[prod['id']]}")
            sound_effects.play_pickup()
            self.on_cart_change()

        def remove_item():
            current = self.cart.get(prod["id"], 0)
            if current > 0:
                if current == 1:
                    del self.cart[prod["id"]]
                else:
                    self.cart[prod["id"]] = current - 1
                qty_var.set(f"No cesto: {self.cart.get(prod['id'], 0)}")
                sound_effects.play_remove()
                self.on_cart_change()

        qty_lbl = tk.Label(action_frame, textvariable=qty_var, font=("Segoe UI", 8, "bold"), fg=PALETTE["accent"], bg=PALETTE["card_bg"])
        qty_lbl.pack(pady=(0, 4))

        btn_row = tk.Frame(action_frame, bg=PALETTE["card_bg"])
        btn_row.pack()

        rem_btn = tk.Button(
            btn_row, text="-", width=3, font=("Segoe UI", 10, "bold"),
            bg="#f5f5f5", fg=PALETTE["text"], relief="flat", cursor="hand2", command=remove_item
        )
        rem_btn.pack(side="left", padx=2)

        add_btn = tk.Button(
            btn_row, text="+ Adicionar", font=("Segoe UI", 9, "bold"),
            bg=PALETTE["primary"], fg="#ffffff", activebackground=PALETTE["primary_hover"],
            activeforeground="#ffffff", relief="flat", padx=10, pady=3, cursor="hand2", command=add_item
        )
        add_btn.pack(side="left", padx=2)


class CheckoutDialog(tk.Toplevel):
    """Modal de Pagamento no Caixa com Emissão do Cupom Fiscal Oficial"""
    def __init__(self, parent, cart, active_mission, on_checkout_success):
        super().__init__(parent)
        self.cart = cart
        self.active_mission = active_mission
        self.on_checkout_success = on_checkout_success

        self.title("Aroma & Trigo - Finalizar Pedido no Caixa")
        self.geometry("540x630")
        self.resizable(False, False)
        self.configure(bg=PALETTE["bg"])
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self.bind("<Escape>", lambda e: self.destroy())

    def _build_ui(self):
        # Header do Caixa
        header = tk.Frame(self, bg=PALETTE["dark"], padx=15, pady=12)
        header.pack(fill="x")

        tk.Label(
            header, text="💳 CAIXA CENTRAL - PADARIA AROMA & TRIGO",
            font=("Georgia", 12, "bold"), fg=PALETTE["accent_light"], bg=PALETTE["dark"]
        ).pack(anchor="w")

        tk.Label(
            header, text="Atendente Juliana: 'Olá! Vamos fechar suas comprinhas?'",
            font=("Segoe UI", 9, "italic"), fg="#ffffff", bg=PALETTE["dark"]
        ).pack(anchor="w", pady=(3, 0))

        # Totalizar itens
        items_detail = []
        total_price = 0.0

        for pid, qty in self.cart.items():
            prod = next((p for p in PRODUCTS if p["id"] == pid), None)
            if prod:
                subtotal = prod["price"] * qty
                total_price += subtotal
                items_detail.append((prod, qty, subtotal))

        if not items_detail:
            # Carrinho vazio
            empty_frame = tk.Frame(self, bg=PALETTE["bg"], pady=60)
            empty_frame.pack(fill="both", expand=True)

            tk.Label(empty_frame, text="🛒", font=("Segoe UI", 48), bg=PALETTE["bg"]).pack()
            tk.Label(
                empty_frame, text="Seu cesto de compras está vazio!",
                font=("Segoe UI", 13, "bold"), fg=PALETTE["primary"], bg=PALETTE["bg"]
            ).pack(pady=8)
            tk.Label(
                empty_frame, text="Visite as vitrines de Salgados, Doces e Cafeteria\npara escolher produtos fresquinhos!",
                font=("Segoe UI", 10), fg=PALETTE["text_muted"], bg=PALETTE["bg"], justify="center"
            ).pack()

            tk.Button(
                self, text="Voltar e Fazer Compras", font=("Segoe UI", 10, "bold"),
                bg=PALETTE["primary"], fg="#ffffff", relief="flat", padx=20, pady=8,
                cursor="hand2", command=self.destroy
            ).pack(pady=20)
            return

        # Cupom Fiscal Impresso em Estilo Térmico
        receipt_outer = tk.Frame(self, bg="#dcdcdc", padx=3, pady=3)
        receipt_outer.pack(fill="both", expand=True, padx=25, pady=12)

        receipt_frame = tk.Frame(receipt_outer, bg="#ffffff", padx=15, pady=12)
        receipt_frame.pack(fill="both", expand=True)

        tk.Label(
            receipt_frame, text="========================================",
            font=("Courier New", 9), fg="#666666", bg="#ffffff"
        ).pack()
        tk.Label(
            receipt_frame, text="PADARIA AROMA & TRIGO",
            font=("Courier New", 12, "bold"), fg=PALETTE["dark"], bg="#ffffff"
        ).pack()
        tk.Label(
            receipt_frame, text="CNPJ: 45.678.901/0001-23",
            font=("Courier New", 8), fg="#666666", bg="#ffffff"
        ).pack()
        tk.Label(
            receipt_frame, text=BRAND["address"],
            font=("Courier New", 8), fg="#666666", bg="#ffffff"
        ).pack()
        tk.Label(
            receipt_frame, text=BRAND["site_url"],
            font=("Courier New", 8, "underline"), fg=PALETTE["primary"], bg="#ffffff"
        ).pack()
        tk.Label(
            receipt_frame, text=f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}",
            font=("Courier New", 8), fg="#666666", bg="#ffffff"
        ).pack()
        tk.Label(
            receipt_frame, text="========================================",
            font=("Courier New", 9), fg="#666666", bg="#ffffff"
        ).pack()

        # Lista de Itens no Cupom
        items_canvas = tk.Canvas(receipt_frame, bg="#ffffff", highlightthickness=0, height=130)
        items_sb = ttk.Scrollbar(receipt_frame, orient="vertical", command=items_canvas.yview)
        items_scroll_frame = tk.Frame(items_canvas, bg="#ffffff")

        items_scroll_frame.bind(
            "<Configure>",
            lambda e: items_canvas.configure(scrollregion=items_canvas.bbox("all"))
        )
        items_canvas.create_window((0, 0), window=items_scroll_frame, anchor="nw")
        items_canvas.configure(yscrollcommand=items_sb.set)

        items_canvas.pack(fill="both", expand=True)

        for prod, qty, subtotal in items_detail:
            row = tk.Frame(items_scroll_frame, bg="#ffffff")
            row.pack(fill="x", pady=2)
            left_txt = f"{qty}x {prod['name'][:22]}"
            right_txt = f"R$ {subtotal:.2f}".replace(".", ",")
            tk.Label(row, text=f"{left_txt:<25}", font=("Courier New", 9), fg="#222222", bg="#ffffff").pack(side="left")
            tk.Label(row, text=f"{right_txt:>10}", font=("Courier New", 9, "bold"), fg="#222222", bg="#ffffff").pack(side="right")

        tk.Label(
            receipt_frame, text="----------------------------------------",
            font=("Courier New", 9), fg="#666666", bg="#ffffff"
        ).pack()

        # Total Geral
        total_row = tk.Frame(receipt_frame, bg="#ffffff")
        total_row.pack(fill="x")
        tk.Label(total_row, text="VALOR TOTAL:", font=("Courier New", 12, "bold"), fg=PALETTE["dark"], bg="#ffffff").pack(side="left")
        tk.Label(total_row, text=f"R$ {total_price:.2f}".replace(".", ","), font=("Courier New", 13, "bold"), fg=PALETTE["success"], bg="#ffffff").pack(side="right")

        tk.Label(
            receipt_frame, text="Projeto Pronatec - Negócios Inovadores com IA",
            font=("Courier New", 7, "italic"), fg="#888888", bg="#ffffff"
        ).pack(pady=(4, 0))
        tk.Label(
            receipt_frame, text="Obrigado pela preferência! Volte sempre!",
            font=("Courier New", 8, "bold"), fg=PALETTE["primary"], bg="#ffffff"
        ).pack()

        # Verificar se cumpre a missão ativa
        mission_completed = False
        if self.active_mission:
            if "steps" in self.active_mission:
                req_items = [s["item_id"] for s in self.active_mission["steps"]]
            else:
                req_items = self.active_mission.get("items", [])
            if req_items and all(self.cart.get(req_id, 0) >= 1 for req_id in req_items):
                mission_completed = True

        if mission_completed:
            reward_pts = self.active_mission.get("reward_points", 50)
            reward_cash = self.active_mission.get("reward_money", 20.0)
            mission_banner = tk.Frame(self, bg=PALETTE["accent"], padx=10, pady=6)
            mission_banner.pack(fill="x", padx=25, pady=(0, 10))
            tk.Label(
                mission_banner, text=f"🏆 MISSÃO CUMPRIDA: {self.active_mission['title']}!",
                font=("Segoe UI", 9, "bold"), fg="#ffffff", bg=PALETTE["accent"]
            ).pack()
            tk.Label(
                mission_banner, text=f"+{reward_pts} Pontos Fidelidade & +R$ {reward_cash:.2f} Bônus na Carteira!",
                font=("Segoe UI", 8, "bold"), fg=PALETTE["accent_light"], bg=PALETTE["accent"]
            ).pack()

        # Botões de Ação
        btn_frame = tk.Frame(self, bg=PALETTE["bg"], padx=25, pady=8)
        btn_frame.pack(fill="x")

        def finalize_payment():
            sound_effects.play_checkout()
            if mission_completed:
                sound_effects.play_victory()
            self.on_checkout_success(total_price, mission_completed)
            self.destroy()

        cancel_btn = tk.Button(
            btn_frame, text="Continuar Comprando", font=("Segoe UI", 9),
            bg="#e0e0e0", fg=PALETTE["text"], relief="flat", padx=12, pady=7,
            cursor="hand2", command=self.destroy
        )
        cancel_btn.pack(side="left")

        pay_btn = tk.Button(
            btn_frame, text="💵 Pagar e Emitir Cupom", font=("Segoe UI", 10, "bold"),
            bg=PALETTE["success"], fg="#ffffff", activebackground="#388e3c",
            activeforeground="#ffffff", relief="flat", padx=16, pady=7,
            cursor="hand2", command=finalize_payment
        )
        pay_btn.pack(side="right")


class MissionsDialog(tk.Toplevel):
    """Visualizador e Seletor Detalhado de Missões de Compra"""
    def __init__(self, parent, active_mission_idx, cart, on_select_mission):
        super().__init__(parent)
        self.active_mission_idx = active_mission_idx
        self.cart = cart
        self.on_select_mission = on_select_mission

        self.title("Aroma & Trigo - Missões e Roteiros Detalhados do Chef")
        self.geometry("640x550")
        self.resizable(False, False)
        self.configure(bg=PALETTE["bg"])
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self.bind("<Escape>", lambda e: self.destroy())

    def _build_ui(self):
        header = tk.Frame(self, bg=PALETTE["primary"], padx=15, pady=12)
        header.pack(fill="x")

        tk.Label(
            header, text="🎯 Roteiro de Missões Diárias do Chef",
            font=("Georgia", 13, "bold"), fg="#ffffff", bg=PALETTE["primary"]
        ).pack(side="left")

        tk.Label(
            header, text="Siga os passos, complete o pedido e ganhe bônus!",
            font=("Segoe UI", 8, "italic"), fg=PALETTE["accent_light"], bg=PALETTE["primary"]
        ).pack(side="right")

        container = tk.Frame(self, bg=PALETTE["bg"])
        container.pack(fill="both", expand=True, padx=12, pady=8)

        canvas = tk.Canvas(container, bg=PALETTE["bg"], highlightthickness=0)
        sb = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scroll_f = tk.Frame(canvas, bg=PALETTE["bg"])

        scroll_f.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_f, anchor="nw", width=595)
        canvas.configure(yscrollcommand=sb.set)

        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        for i, m in enumerate(MISSIONS):
            is_current = (i == self.active_mission_idx)
            card = tk.Frame(
                scroll_f, bg=PALETTE["card_bg"],
                highlightbackground=PALETTE["gold"] if is_current else PALETTE["card_border"],
                highlightthickness=2 if is_current else 1, padx=12, pady=10
            )
            card.pack(fill="x", pady=6)

            title_row = tk.Frame(card, bg=PALETTE["card_bg"])
            title_row.pack(fill="x")

            badge_txt = " ⭐ MISSÃO ATIVA ⭐" if is_current else ""
            tk.Label(
                title_row, text=m["title"] + badge_txt, font=("Segoe UI", 10, "bold"),
                fg=PALETTE["accent"] if is_current else PALETTE["text"], bg=PALETTE["card_bg"]
            ).pack(side="left")

            reward_pts = m.get("reward_points", 50)
            reward_cash = m.get("reward_money", 20.0)
            tk.Label(
                title_row, text=f"+{reward_pts} pts | +R$ {reward_cash:.2f}",
                font=("Segoe UI", 9, "bold"), fg=PALETTE["success"], bg=PALETTE["card_bg"]
            ).pack(side="right")

            if "story" in m:
                tk.Label(
                    card, text=m["story"], font=("Segoe UI", 8, "italic"),
                    fg=PALETTE["text_muted"], bg=PALETTE["card_bg"], anchor="w", justify="left"
                ).pack(fill="x", pady=(2, 6))

            # Passos detalhados
            steps = m.get("steps", [])
            for j, step in enumerate(steps, 1):
                item_id = step["item_id"]
                have = self.cart.get(item_id, 0) >= 1

                step_row = tk.Frame(card, bg="#fafafa", padx=6, pady=4, highlightbackground="#ebebeb", highlightthickness=1)
                step_row.pack(fill="x", pady=2)

                status_txt = "✅ NO CESTO" if have else "⬜ FALTANDO"
                status_color = PALETTE["success"] if have else "#d9534f"

                top_line = tk.Frame(step_row, bg="#fafafa")
                top_line.pack(fill="x")

                tk.Label(
                    top_line, text=f"Passo {j}: {step['name']}",
                    font=("Segoe UI", 8, "bold"), fg=PALETTE["text"], bg="#fafafa"
                ).pack(side="left")

                tk.Label(
                    top_line, text=status_txt,
                    font=("Segoe UI", 7, "bold"), fg=status_color, bg="#fafafa"
                ).pack(side="right")

                tk.Label(
                    step_row, text=f"📍 Onde encontrar: {step['zone_name']} • {step.get('hint', '')}",
                    font=("Segoe UI", 7), fg=PALETTE["text_muted"], bg="#fafafa", anchor="w"
                ).pack(fill="x")

            # Passo Final: Ir ao Caixa
            final_step = tk.Frame(card, bg="#f1f8e9", padx=6, pady=3, highlightbackground="#c8e6c9", highlightthickness=1)
            final_step.pack(fill="x", pady=(4, 2))
            tk.Label(
                final_step, text="Passo Final: Vá até o Balcão do Caixa (Juliana) e aperte [E] para pagar e receber seu bônus!",
                font=("Segoe UI", 8, "bold"), fg=PALETTE["success"], bg="#f1f8e9", anchor="w"
            ).pack(fill="x")

            if not is_current:
                idx = i
                btn = tk.Button(
                    card, text="Ativar Esta Missão", font=("Segoe UI", 8, "bold"),
                    bg=PALETTE["primary"], fg="#ffffff", relief="flat", padx=10, pady=3,
                    cursor="hand2", command=lambda x=idx: self._select(x)
                )
                btn.pack(anchor="e", pady=(4, 0))

            if not is_current:
                idx = i
                btn = tk.Button(
                    card, text="Ativar Esta Missão", font=("Segoe UI", 8, "bold"),
                    bg=PALETTE["primary"], fg="#ffffff", relief="flat", padx=8, pady=2,
                    cursor="hand2", command=lambda x=idx: self._select(x)
                )
                btn.pack(anchor="e", pady=(3, 0))

        close_btn = tk.Button(
            self, text="Fechar", font=("Segoe UI", 9, "bold"),
            bg="#e0e0e0", fg=PALETTE["text"], relief="flat", padx=15, pady=6,
            cursor="hand2", command=self.destroy
        )
        close_btn.pack(pady=10)

    def _select(self, idx):
        self.on_select_mission(idx)
        self.destroy()


class HelpDialog(tk.Toplevel):
    """Guia de Controles e Informações da Padaria"""
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Aroma & Trigo - Como Jogar e Controles")
        self.geometry("520x440")
        self.resizable(False, False)
        self.configure(bg=PALETTE["bg"])
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self.bind("<Escape>", lambda e: self.destroy())

    def _build_ui(self):
        header = tk.Frame(self, bg=PALETTE["dark"], padx=15, pady=12)
        header.pack(fill="x")

        tk.Label(
            header, text="🥐 GUIA DO JOGADOR - AROMA & TRIGO",
            font=("Georgia", 12, "bold"), fg=PALETTE["accent_light"], bg=PALETTE["dark"]
        ).pack(anchor="w")

        tk.Label(
            header, text="Jogo Desenvolvido no Curso Pronatec de Negócios Inovadores com IA",
            font=("Segoe UI", 8, "italic"), fg="#ffffff", bg=PALETTE["dark"]
        ).pack(anchor="w", pady=(2, 0))

        content = tk.Frame(self, bg=PALETTE["bg"], padx=20, pady=15)
        content.pack(fill="both", expand=True)

        instructions = [
            ("⌨️ Movimentação do Boneco", "Use as teclas [W], [A], [S] e [D] (ou setas do teclado) para andar pela padaria."),
            ("🛒 Fazer Compras", "Aproxime-se das vitrines (Salgados, Doces, Cafeteria ou Fornada de Pães) e pressione [E] ou [ESPAÇO]."),
            ("💳 Pagar no Caixa", "Quando terminar suas compras, vá até o Balcão do Caixa e aperte [E] para emitir seu cupom fiscal e ganhar pontos."),
            ("🎯 Missões do Chef", "Cumpra os combos de compras ativos para ganhar troféus e Pontos Fidelidade."),
            ("🌐 Site Oficial", f"Visite o site do projeto a qualquer momento:\n{BRAND['site_url']}")
        ]

        for title, desc in instructions:
            box = tk.Frame(content, bg=PALETTE["card_bg"], highlightbackground=PALETTE["card_border"], highlightthickness=1, padx=10, pady=6)
            box.pack(fill="x", pady=4)

            tk.Label(box, text=title, font=("Segoe UI", 9, "bold"), fg=PALETTE["primary"], bg=PALETTE["card_bg"]).pack(anchor="w")
            tk.Label(box, text=desc, font=("Segoe UI", 8), fg=PALETTE["text"], bg=PALETTE["card_bg"], wraplength=460, justify="left").pack(anchor="w")

        btn_row = tk.Frame(self, bg=PALETTE["bg"], pady=10)
        btn_row.pack()

        site_btn = tk.Button(
            btn_row, text="🌐 Acessar Nosso Site Oficial", font=("Segoe UI", 9, "bold"),
            bg=PALETTE["accent"], fg="#ffffff", relief="flat", padx=12, pady=6,
            cursor="hand2", command=lambda: webbrowser.open(BRAND["site_url"])
        )
        site_btn.pack(side="left", padx=5)

        close_btn = tk.Button(
            btn_row, text="Entendido!", font=("Segoe UI", 9, "bold"),
            bg=PALETTE["primary"], fg="#ffffff", relief="flat", padx=15, pady=6,
            cursor="hand2", command=self.destroy
        )
        close_btn.pack(side="left", padx=5)
