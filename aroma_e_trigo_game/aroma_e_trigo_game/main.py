"""
Aplicação Principal - Padaria Aroma & Trigo (Jogo Desktop)
Controles: W, A, S, D para movimentar o boneco com alta velocidade (Shift para Correr)
Adaptação Automática para Tela Cheia em qualquer aparelho/resolução (F11 ou Maximizado)
Guia Visual Passo a Passo da Missão Diária (Seta Dourada e Banner Orientador)
Sistema de Clientes com Pedidos em Balão de Fala e Entrega Interativa na Mesa
Cenário e interface baseados na paleta do site https://padariaaromaetrigo.netlify.app/
Projeto Desenvolvido no Curso Pronatec - Negócios Inovadores com IA
"""
import math
import os
import sys
import tkinter as tk
from tkinter import messagebox
import webbrowser

from config import PALETTE, BRAND, PRODUCTS, MISSIONS, ASSETS_DIR
import sound_effects
from character import Character
from world import World
from customer import CustomerManager
from ui_components import HeaderNavbar, MissionGuideBanner, SideCartPanel, FooterHUD
from dialogs import ShelfDialog, CheckoutDialog, MissionsDialog, HelpDialog

class AromaETrigoApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{BRAND['name']} - Jogo de Compras Desktop | {BRAND['course_info']}")
        self.root.configure(bg=PALETTE["bg"])

        # Ícone da Janela
        logo_path = os.path.join(ASSETS_DIR, "logo_aroma_e_trigo.png")
        if os.path.exists(logo_path):
            try:
                from PIL import Image, ImageTk
                ico = ImageTk.PhotoImage(file=logo_path)
                self.root.iconphoto(False, ico)
            except Exception:
                pass

        # 1. ADAPTAÇÃO PARA TELA CHEIA INDEPENDENTE DO APARELHO
        self.is_fullscreen = False
        self._apply_fullscreen_or_maximized()

        # Estado do Jogo
        self.cart = {}
        self.wallet_balance = 100.00
        self.loyalty_points = 0
        self.active_mission_idx = 0
        self.keys_pressed = {}
        self.last_banner_text = None
        self.last_banner_done = None

        # Criar Cenário e Personagem com velocidade aprimorada (base 9.5, sprint 14.5)
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        init_w = max(screen_w - 360, 800)
        init_h = max(screen_h - 180, 560)

        self.world = World(width=init_w, height=init_h)
        self.character = Character(x=init_w // 2, y=int(init_h * 0.75), base_speed=9.5, sprint_speed=14.5)
        
        # Gerenciador de Clientes com Pedidos
        self.customer_manager = CustomerManager()

        self._build_layout()
        self._bind_events()

        # Iniciar Game Loop
        self.is_running = True
        self.root.after(30, self.game_loop)

    def _apply_fullscreen_or_maximized(self):
        """Maximiza e ajusta o jogo à tela inteira do dispositivo"""
        try:
            self.root.state('zoomed')
        except Exception:
            try:
                self.root.attributes('-zoomed', True)
            except Exception:
                w = self.root.winfo_screenwidth()
                h = self.root.winfo_screenheight()
                self.root.geometry(f"{w}x{h}+0+0")

    def toggle_fullscreen(self):
        """Alterna entre Tela Cheia Total (sem bordas) e Janela Maximizada (F11)"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)
        if not self.is_fullscreen:
            try:
                self.root.state('zoomed')
            except Exception:
                pass

    def _build_layout(self):
        # 1. Navbar Superior
        self.navbar = HeaderNavbar(
            self.root,
            on_cart_click=self.open_checkout,
            on_help_click=self.open_help,
            on_missions_click=self.open_missions
        )
        self.navbar.pack(fill="x", side="top")

        # 2. Faixa Orientadora da Missão Diária (Passo a Passo em tempo real)
        self.mission_banner = MissionGuideBanner(
            self.root,
            on_banner_click=self.open_missions
        )
        self.mission_banner.pack(fill="x", side="top")

        # 3. Barra Inferior HUD
        self.footer = FooterHUD(
            self.root,
            on_key_sim=self._simulate_key,
            on_toggle_sound=sound_effects.toggle_sound,
            on_open_site=lambda: webbrowser.open(BRAND["site_url"]),
            on_toggle_fullscreen=self.toggle_fullscreen
        )
        self.footer.pack(fill="x", side="bottom")

        # 4. Corpo Central (Canvas do Jogo responsivo + Painel Lateral de Missão/Carrinho)
        main_body = tk.Frame(self.root, bg=PALETTE["bg"])
        main_body.pack(fill="both", expand=True)

        # Painel Lateral do Carrinho e Missão
        self.sidebar = SideCartPanel(
            main_body,
            on_checkout_request=self.open_checkout,
            on_mission_change_request=self.open_missions
        )
        self.sidebar.pack(side="right", fill="y", padx=(0, 5), pady=5)

        # Container do Canvas que se expande para qualquer resolução
        canvas_frame = tk.Frame(main_body, bg=PALETTE["bg"], padx=5, pady=5)
        canvas_frame.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(
            canvas_frame,
            bg=PALETTE["floor_tile_1"],
            highlightbackground=PALETTE["primary"],
            highlightthickness=2
        )
        self.canvas.pack(fill="both", expand=True)

        # Evento de Redimensionamento Automático da Tela
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.refresh_ui()

    def _on_canvas_configure(self, event):
        """Redimensiona o mundo da padaria dinamicamente apenas quando necessário"""
        if event.width > 200 and event.height > 200:
            self.world.resize(event.width, event.height)

    def _bind_events(self):
        self.root.bind("<KeyPress>", self._on_key_press)
        self.root.bind("<KeyRelease>", self._on_key_release)
        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())
        self.canvas.bind("<Button-1>", lambda e: self.canvas.focus_set())
        self.canvas.focus_set()

    def _on_key_press(self, event):
        key = event.keysym.lower()

        # Movimentação W, A, S, D e Setas
        if key in ("w", "s", "a", "d", "up", "down", "left", "right"):
            self.keys_pressed[key] = True

        # Correr rápido com Shift
        elif key in ("shift_l", "shift_r", "shift"):
            self.keys_pressed["shift"] = True

        # Interação com Vitrines / Balcão ou Clientes com E ou Espaço
        elif key in ("e", "space"):
            self.interact()

        # Atalhos
        elif key == "c":
            self.open_checkout()
        elif key == "m":
            self.open_missions()
        elif key == "f11":
            self.toggle_fullscreen()

    def _on_key_release(self, event):
        key = event.keysym.lower()
        if key in self.keys_pressed:
            self.keys_pressed[key] = False
        if key in ("shift_l", "shift_r", "shift"):
            self.keys_pressed["shift"] = False

    def _simulate_key(self, key_name):
        self.keys_pressed[key_name] = True
        self.root.after(100, lambda: self.keys_pressed.update({key_name: False}))

    def get_mission_status(self):
        """Calcula o passo atual detalhado da missão diária para guiar o jogador"""
        if not (0 <= self.active_mission_idx < len(MISSIONS)):
            return {"all_done": True, "target_zone": None, "banner_text": "Modo Livre Ativado"}

        m = MISSIONS[self.active_mission_idx]
        steps = m.get("steps", [])
        
        # Encontrar o primeiro item que ainda não está no carrinho
        for i, step in enumerate(steps, 1):
            if self.cart.get(step["item_id"], 0) < 1:
                return {
                    "all_done": False,
                    "target_zone": step["zone_id"],
                    "step_num": i,
                    "total_steps": len(steps),
                    "item_name": step["name"],
                    "zone_name": step["zone_name"],
                    "banner_text": f"Passo {i} de {len(steps)}: Vá até a [{step['zone_name']}] e pegue 1x {step['name']}! (Aperte [E])"
                }

        # Todos os itens já estão no carrinho! Próximo passo: Caixa
        return {
            "all_done": True,
            "target_zone": "caixa",
            "banner_text": "Todos os itens reunidos! Vá até o [Balcão do Caixa (Juliana)] e aperte [E] para pagar e receber seu bônus!"
        }

    def game_loop(self):
        if not self.is_running:
            return

        # 1. Atualizar Personagem (Velocidade e Shift)
        self.character.update(self.keys_pressed, self.world.obstacles, self.world.bounds)
        self.character.cart_item_count = sum(self.cart.values())

        # 2. Atualizar Fumacinha aromática
        self.world.update_particles()

        # 3. Atualizar Cliente NPC e Mesa de Atendimento
        table_pos = self.world.tables[0] if self.world.tables else (self.world.width // 2, int(self.world.height * 0.52))
        self.customer_manager.update(self.world.width, self.world.height, table_pos)

        # 4. Identificar passo da missão e zona alvo (Beacon Dourado)
        mission_info = self.get_mission_status()
        target_zone_id = mission_info["target_zone"]

        # 5. Atualizar faixa superior apenas quando o texto ou status mudar
        b_text = mission_info["banner_text"]
        b_done = mission_info["all_done"]
        if b_text != self.last_banner_text or b_done != self.last_banner_done:
            self.mission_banner.update_guide(b_text, is_all_collected=b_done)
            self.last_banner_text = b_text
            self.last_banner_done = b_done

        # 6. Detectar proximidade com vitrines/caixa e com o cliente
        nearby_zone = self.world.get_nearby_zone(self.character.x, self.character.y)

        # 7. Desenhar Cenário
        self.world.draw(self.canvas, nearby_zone=nearby_zone, target_zone_id=target_zone_id)

        # 8. Desenhar Cliente NPC com Balão de Pedido
        self.customer_manager.draw(self.canvas)

        # 9. Desenhar Prompt de Interação com o Cliente caso esteja perto
        cust = self.customer_manager.current_customer
        if cust and cust.state == "waiting":
            dist = math.hypot(self.character.x - cust.x, self.character.y - cust.y)
            if dist < 75:
                has_items = cust.check_has_order(self.cart)
                p_text = f"[E] Entregar Pedido para {cust.name}! 🎁" if has_items else f"[E] Ver Pedido de {cust.name} 💬"
                p_bg = PALETTE["success"] if has_items else PALETTE["primary"]
                py = cust.y - 105
                self.canvas.create_rectangle(cust.x - 110, py - 12, cust.x + 110, py + 12, fill=p_bg, outline="#ffffff", width=2, tags="dynamic")
                self.canvas.create_text(cust.x, py, text=p_text, fill="#ffffff", font=("Segoe UI", 8, "bold"), tags="dynamic")

        # 10. Desenhar Boneco
        self.character.draw(self.canvas)

        # Agendar próximo quadro (16ms = 60 FPS fluido e sem engasgos)
        self.root.after(16, self.game_loop)

    def interact(self):
        """Disparado ao apertar [E] ou [Espaço]"""
        # 1. Primeiro checa se está interagindo com o Cliente NPC
        cust = self.customer_manager.current_customer
        if cust and cust.state == "waiting":
            dist = math.hypot(self.character.x - cust.x, self.character.y - cust.y)
            if dist < 85:
                if cust.check_has_order(self.cart):
                    earnings, points = cust.deliver_order(self.cart)
                    self.wallet_balance += earnings
                    self.loyalty_points += points
                    self.customer_manager.served_count += 1
                    messagebox.showinfo(
                        "🎉 Pedido Entregue com Sucesso!",
                        f"O cliente {cust.name} adorou o atendimento na Aroma & Trigo!\n\n"
                        f"💰 Preço dos produtos: R$ {cust.total_price:.2f}\n"
                        f"💖 Gorjeta Especial: R$ {cust.tip:.2f}\n"
                        f"🌟 Pontos Fidelidade: +{points} pts\n\n"
                        f"Total recebido na carteira: R$ {earnings:.2f}!"
                    )
                    self.refresh_ui()
                    return
                else:
                    items_needed = " + ".join([f"{it['name']} ({it['icon']})" for it in cust.order if self.cart.get(it['id'], 0) < 1])
                    messagebox.showinfo(
                        f"Pedido de {cust.name}",
                        f"Olá! O cliente {cust.name} está aguardando:\n\n"
                        f"👉 {items_needed}\n\n"
                        f"Vá até as vitrines da padaria, adicione os itens ao seu cesto e volte aqui para entregar e receber sua recompensa!"
                    )
                    return

        # 2. Interação com Vitrines ou Balcão do Caixa
        nearby_zone = self.world.get_nearby_zone(self.character.x, self.character.y)
        if not nearby_zone:
            return

        if nearby_zone["id"] == "caixa":
            self.open_checkout()
        else:
            ShelfDialog(
                self.root,
                zone_info=nearby_zone,
                cart=self.cart,
                on_cart_change=self.refresh_ui
            )

    def refresh_ui(self):
        """Atualiza a sidebar, navbar e contador do carrinho"""
        active_m = MISSIONS[self.active_mission_idx] if 0 <= self.active_mission_idx < len(MISSIONS) else None
        cust = self.customer_manager.current_customer
        served = self.customer_manager.served_count

        self.sidebar.update_data(
            cart=self.cart,
            wallet_balance=self.wallet_balance,
            loyalty_points=self.loyalty_points,
            active_mission=active_m,
            on_item_change=self._on_cart_item_change,
            customer=cust,
            served_count=served
        )
        total_items = sum(self.cart.values())
        self.navbar.update_cart_count(total_items)

    def _on_cart_item_change(self, product_id, delta):
        current = self.cart.get(product_id, 0)
        new_val = current + delta
        if new_val <= 0:
            if product_id in self.cart:
                del self.cart[product_id]
                sound_effects.play_remove()
        else:
            self.cart[product_id] = new_val
            if delta > 0:
                sound_effects.play_pickup()
            else:
                sound_effects.play_remove()
        self.refresh_ui()

    def open_checkout(self):
        active_m = MISSIONS[self.active_mission_idx] if 0 <= self.active_mission_idx < len(MISSIONS) else None
        CheckoutDialog(
            self.root,
            cart=self.cart,
            active_mission=active_m,
            on_checkout_success=self._on_checkout_success
        )

    def _on_checkout_success(self, total_paid, mission_completed):
        if self.wallet_balance >= total_paid:
            self.wallet_balance -= total_paid
        else:
            self.wallet_balance = 50.0

        if mission_completed and 0 <= self.active_mission_idx < len(MISSIONS):
            m = MISSIONS[self.active_mission_idx]
            reward_pts = m.get("reward_points", 50)
            reward_cash = m.get("reward_money", 20.0)

            self.loyalty_points += reward_pts
            self.wallet_balance += reward_cash

            # Próxima missão
            self.active_mission_idx = (self.active_mission_idx + 1) % len(MISSIONS)
            next_m = MISSIONS[self.active_mission_idx]

            messagebox.showinfo(
                "🎉 Parabéns! Missão Diária Cumprida!",
                f"Você concluiu: {m['title']}!\n"
                f"{m.get('bonus_msg', '')}\n\n"
                f"🎁 RECOMPENSAS:\n"
                f"• +{reward_pts} Pontos Fidelidade Aroma & Trigo\n"
                f"• +R$ {reward_cash:.2f} Bônus em dinheiro adicionado à carteira!\n\n"
                f"🌟 Próxima Missão Liberada:\n{next_m['title']}"
            )

        self.cart.clear()
        self.refresh_ui()

    def open_missions(self):
        MissionsDialog(
            self.root,
            active_mission_idx=self.active_mission_idx,
            cart=self.cart,
            on_select_mission=self._on_select_mission
        )

    def _on_select_mission(self, new_idx):
        self.active_mission_idx = new_idx
        self.refresh_ui()

    def open_help(self):
        HelpDialog(self.root)


def main():
    root = tk.Tk()
    app = AromaETrigoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
