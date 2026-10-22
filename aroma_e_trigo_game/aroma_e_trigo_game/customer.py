"""
Módulo do Cliente NPC (Atendimento e Pedidos na Padaria)
O cliente entra pela porta, caminha até a mesa, faz o pedido em um balão de fala,
aguarda o jogador trazer os itens e recompensa com gorjeta e pontos de fidelidade!
"""
import math
import random
from config import PALETTE, BRAND, PRODUCTS
import sound_effects

CUSTOMER_NAMES = [
    ("Dona Clara", "#e91e63", "#f8bbd0"),
    ("Seu Marcos", "#1976d2", "#bbdefb"),
    ("Mariana", "#9c27b0", "#e1bee7"),
    ("Lucas", "#388e3c", "#c8e6c9"),
    ("Dona Neide", "#f57c00", "#ffe0b2"),
    ("Pedro", "#00796b", "#b2dfdb"),
    ("Camila", "#d81b60", "#f48fb1")
]

class Customer:
    def __init__(self, spawn_x=380, spawn_y=540, target_x=380, target_y=325):
        self.x = spawn_x
        self.y = spawn_y
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.target_x = target_x
        self.target_y = target_y

        # Escolhe nome e visual
        name, shirt_col, hair_acc = random.choice(CUSTOMER_NAMES)
        self.name = name
        self.shirt_color = shirt_col
        self.hair_accent = hair_acc

        # Estado: "entering", "waiting", "eating", "leaving", "done"
        self.state = "entering"
        self.speed = 3.5
        self.walk_frame = 0
        self.walk_timer = 0
        self.animation_tick = 0
        self.eating_timer = 0

        # Partículas de satisfação (corações flutuantes)
        self.hearts = []

        # Gerar Pedido Aleatório (1 ou 2 itens da padaria)
        self._generate_order()

    def _generate_order(self):
        """Gera um pedido realista combinando salgado/doce com bebida"""
        num_items = random.choice([1, 2])
        chosen = random.sample(PRODUCTS, num_items)
        self.order = []
        for p in chosen:
            self.order.append({
                "id": p["id"],
                "name": p["name"],
                "price": p["price"],
                "icon": p["icon"],
                "zone": p["zone"]
            })
        self.total_price = sum(item["price"] for item in self.order)
        self.tip = round(random.uniform(3.0, 7.50), 2)

    def update(self):
        """Atualiza a movimentação do cliente e animações"""
        self.animation_tick += 1

        # Atualizar corações flutuantes
        for h in self.hearts:
            h["y"] -= 0.8
            h["alpha"] -= 0.02
        self.hearts = [h for h in self.hearts if h["alpha"] > 0]

        if self.state == "entering":
            # Caminhar até a mesa
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.hypot(dx, dy)

            if dist > 4:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed
                self.walk_timer += 1
                if self.walk_timer >= 4:
                    self.walk_frame = (self.walk_frame + 1) % 4
                    self.walk_timer = 0
            else:
                self.x = self.target_x
                self.y = self.target_y
                self.state = "waiting"
                self.walk_frame = 0

        elif self.state == "eating":
            self.eating_timer -= 1
            if self.eating_timer % 15 == 0:
                self.hearts.append({
                    "x": self.x + random.randint(-15, 15),
                    "y": self.y - 25,
                    "alpha": 1.0,
                    "size": random.randint(8, 14)
                })
            if self.eating_timer <= 0:
                self.state = "leaving"

        elif self.state == "leaving":
            # Caminhar até a saída (porta de entrada)
            dx = self.spawn_x - self.x
            dy = (self.spawn_y + 30) - self.y
            dist = math.hypot(dx, dy)

            if dist > 6:
                self.x += (dx / dist) * self.speed
                self.y += (dy / dist) * self.speed
                self.walk_timer += 1
                if self.walk_timer >= 4:
                    self.walk_frame = (self.walk_frame + 1) % 4
                    self.walk_timer = 0
            else:
                self.state = "done"

    def check_has_order(self, cart):
        """Verifica se o jogador tem no carrinho todos os itens pedidos pelo cliente"""
        for item in self.order:
            if cart.get(item["id"], 0) < 1:
                return False
        return True

    def deliver_order(self, cart):
        """Entrega o pedido, consome os itens do carrinho e ativa estado de comer"""
        for item in self.order:
            item_id = item["id"]
            if item_id in cart:
                if cart[item_id] <= 1:
                    del cart[item_id]
                else:
                    cart[item_id] -= 1

        self.state = "eating"
        self.eating_timer = 120 # ~3 a 4 segundos comendo feliz
        sound_effects.play_checkout()
        sound_effects.play_victory()

        # Retorna total arrecadado (preço dos itens + gorjeta) e pontos
        earnings = self.total_price + self.tip
        points = 40 + len(self.order) * 10
        return earnings, points

    def draw(self, canvas):
        """Desenha o cliente e seu balão de pedido com alta performance"""
        if self.state == "done":
            return

        x = self.x
        y = self.y

        # Sombra no chão
        canvas.create_oval(
            x - 12, y + 10, x + 12, y + 18,
            fill="#d0beaa", outline="", tags="customer"
        )

        # Balanço dos pés
        foot_offset = 3 if (self.state in ("entering", "leaving") and self.walk_frame in (1, 3)) else 0

        # Pés
        canvas.create_oval(x - 7, y + 9 + foot_offset, x - 2, y + 15 + foot_offset, fill="#37474f", outline="", tags="customer")
        canvas.create_oval(x + 2, y + 9 - foot_offset, x + 7, y + 15 - foot_offset, fill="#37474f", outline="", tags="customer")

        # Corpo / Roupa do Cliente
        body_y = y - 4
        canvas.create_oval(x - 10, body_y - 6, x + 10, body_y + 12, fill=self.shirt_color, outline="#263238", width=1, tags="customer")

        # Cabeça
        head_y = y - 16
        canvas.create_oval(x - 10, head_y - 10, x + 10, head_y + 10, fill="#ffd8b3", outline="#e6be98", tags="customer")
        # Cabelo
        canvas.create_arc(x - 11, head_y - 12, x + 11, head_y + 6, start=0, extent=180, fill="#4e342e", outline="", tags="customer")

        # Rosto expressivo
        if self.state == "eating":
            # Olhos fechados de felicidade (^^)
            canvas.create_arc(x - 6, head_y - 2, x - 2, head_y + 3, start=0, extent=180, style="arc", outline="#3e2723", width=2, tags="customer")
            canvas.create_arc(x + 2, head_y - 2, x + 6, head_y + 3, start=0, extent=180, style="arc", outline="#3e2723", width=2, tags="customer")
            # Bochechas rosadas
            canvas.create_oval(x - 7, head_y + 2, x - 4, head_y + 5, fill="#ff80ab", outline="", tags="customer")
            canvas.create_oval(x + 4, head_y + 2, x + 7, head_y + 5, fill="#ff80ab", outline="", tags="customer")
            # Sorriso aberto
            canvas.create_arc(x - 4, head_y + 2, x + 4, head_y + 7, start=200, extent=140, fill="#c2185b", outline="#8B4513", tags="customer")
        else:
            # Olhos abertos atentos
            canvas.create_oval(x - 5, head_y - 1, x - 2, head_y + 2, fill="#3e2723", outline="", tags="customer")
            canvas.create_oval(x + 2, head_y - 1, x + 5, head_y + 2, fill="#3e2723", outline="", tags="customer")
            # Sorriso simpático
            canvas.create_arc(x - 4, head_y + 2, x + 4, head_y + 6, start=200, extent=140, style="arc", outline="#8B4513", width=2, tags="customer")

        # Nome sobre a cabeça
        canvas.create_text(x, y + 20, text=self.name, fill="#ffffff", font=("Segoe UI", 7, "bold"), tags="customer")

        # Corações flutuantes ao comer
        for h in self.hearts:
            canvas.create_text(h["x"], h["y"], text="❤️", font=("Segoe UI", h["size"]), fill="#e91e63", tags="customer")

        # BALÃO DE FALA COM O PEDIDO (Quando estiver aguardando na padaria)
        if self.state == "waiting":
            self._draw_speech_bubble(canvas, x, y)
        elif self.state == "eating":
            self._draw_eating_bubble(canvas, x, y)

    def _draw_speech_bubble(self, canvas, cx, cy):
        """Desenha balão de fala fofinho com os itens pedidos e ícones"""
        pulse = math.sin(self.animation_tick * 0.18) * 3
        bubble_y = cy - 65 + pulse

        # Montar texto do pedido
        items_str = " + ".join([f"{it['icon']} {it['name']}" for it in self.order])
        total_str = f"R$ {self.total_price:.2f}".replace(".", ",")

        box_w = max(len(items_str) * 6.8 + 24, 160)
        bx1, bx2 = cx - box_w // 2, cx + box_w // 2
        by1, by2 = bubble_y - 20, bubble_y + 16

        # Rabicho do balão apontando para a cabeça do cliente
        canvas.create_polygon(
            cx - 6, by2,
            cx + 6, by2,
            cx, cy - 26,
            fill="#ffffff", outline=PALETTE["primary"], tags="customer"
        )

        # Fundo do balão
        canvas.create_rectangle(
            bx1, by1, bx2, by2,
            fill="#ffffff", outline=PALETTE["primary"], width=2, tags="customer"
        )
        # Faixa superior do balão
        canvas.create_rectangle(
            bx1 + 1, by1 + 1, bx2 - 1, by1 + 13,
            fill=PALETTE["accent_light"], outline="", tags="customer"
        )
        canvas.create_text(
            cx, by1 + 7,
            text=f"💬 {self.name}: 'Por favor, me vê:'",
            fill=PALETTE["dark"], font=("Segoe UI", 7, "bold"), tags="customer"
        )

        # Texto dos itens pedidos
        canvas.create_text(
            cx, by1 + 24,
            text=f"{items_str} ({total_str})",
            fill=PALETTE["text"], font=("Segoe UI", 8, "bold"), tags="customer"
        )

    def _draw_eating_bubble(self, canvas, cx, cy):
        """Balão quando o cliente recebe o pedido e está saboreando"""
        bubble_y = cy - 58
        canvas.create_rectangle(
            cx - 95, bubble_y - 12, cx + 95, bubble_y + 12,
            fill="#e8f5e9", outline=PALETTE["success"], width=2, tags="customer"
        )
        canvas.create_text(
            cx, bubble_y,
            text="😋 'Mmm, que delícia! Obrigado!'",
            fill=PALETTE["success"], font=("Segoe UI", 8, "bold"), tags="customer"
        )


class CustomerManager:
    """Gerencia a chegada de novos clientes e fila de pedidos"""
    def __init__(self):
        self.current_customer = None
        self.spawn_timer = 20 # Primeiro cliente chega logo aos primeiros segundos!
        self.served_count = 0

    def update(self, world_width, world_height, table_pos):
        """Atualiza o cliente atual ou agenda a chegada do próximo"""
        if self.current_customer is not None:
            self.current_customer.update()
            if self.current_customer.state == "done":
                self.current_customer = None
                self.spawn_timer = 90 # Novo cliente chega ~3 segundos após o anterior sair
        else:
            self.spawn_timer -= 1
            if self.spawn_timer <= 0:
                # Gerar novo cliente entrando pela porta principal
                door_x = world_width // 2
                door_y = world_height - 35
                tx, ty = table_pos
                self.current_customer = Customer(
                    spawn_x=door_x, spawn_y=door_y,
                    target_x=tx, target_y=ty
                )

    def draw(self, canvas):
        """Desenha o cliente na tela"""
        canvas.delete("customer")
        if self.current_customer:
            self.current_customer.draw(canvas)
