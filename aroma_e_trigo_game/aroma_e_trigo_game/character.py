"""
Módulo do Personagem Jogável (Boneco)
Controles: W (Cima), A (Esquerda), S (Baixo), D (Direita)
Animação de caminhada, cesto de compras dinâmico e detecção de direção.
"""
import math
from config import PALETTE
import sound_effects

class Character:
    def __init__(self, x=380, y=420, base_speed=9.5, sprint_speed=14.5):
        self.x = x
        self.y = y
        self.radius = 16
        self.base_speed = base_speed
        self.sprint_speed = sprint_speed
        self.speed = base_speed
        self.is_sprinting = False
        self.direction = "down"  # "up", "down", "left", "right"
        self.is_moving = False
        self.walk_frame = 0
        self.walk_timer = 0
        self.step_sound_timer = 0
        self.cart_item_count = 0

    def update(self, keys_pressed, obstacles, bounds):
        dx = 0
        dy = 0

        # Verificar se está correndo com Shift
        self.is_sprinting = bool(
            keys_pressed.get("shift") or
            keys_pressed.get("shift_l") or
            keys_pressed.get("shift_r")
        )
        current_speed = self.sprint_speed if self.is_sprinting else self.base_speed
        self.speed = current_speed

        # W, A, S, D e Setas direcionais
        if keys_pressed.get("w") or keys_pressed.get("up"):
            dy -= current_speed
            self.direction = "up"
        if keys_pressed.get("s") or keys_pressed.get("down"):
            dy += current_speed
            self.direction = "down"
        if keys_pressed.get("a") or keys_pressed.get("left"):
            dx -= current_speed
            self.direction = "left"
        if keys_pressed.get("d") or keys_pressed.get("right"):
            dx += current_speed
            self.direction = "right"

        # Normalizar velocidade na diagonal
        if dx != 0 and dy != 0:
            factor = 1.0 / math.sqrt(2)
            dx *= factor
            dy *= factor

        self.is_moving = (dx != 0 or dy != 0)

        if self.is_moving:
            # Animação de passos (mais ágil e fluida)
            self.walk_timer += 1
            frame_delay = 2 if self.is_sprinting else 3
            if self.walk_timer >= frame_delay:
                self.walk_frame = (self.walk_frame + 1) % 4
                self.walk_timer = 0

            # Efeito sonoro sutil de passos
            self.step_sound_timer += 1
            step_sound_interval = 8 if self.is_sprinting else 12
            if self.step_sound_timer >= step_sound_interval:
                sound_effects.play_step()
                self.step_sound_timer = 0

            # Testar movimentação com colisão eixo X
            new_x = self.x + dx
            if not self.check_collision(new_x, self.y, obstacles, bounds):
                self.x = new_x

            # Testar movimentação com colisão eixo Y
            new_y = self.y + dy
            if not self.check_collision(self.x, new_y, obstacles, bounds):
                self.y = new_y
        else:
            self.walk_frame = 0

    def check_collision(self, x, y, obstacles, bounds):
        # Limites da sala da padaria (bounds = min_x, min_y, max_x, max_y)
        min_x, min_y, max_x, max_y = bounds
        r = self.radius
        if x - r < min_x or x + r > max_x or y - r < min_y or y + r > max_y:
            return True

        # Colisão com caixas delimitadoras de obstáculos (móveis, balcões)
        char_box = (x - r + 3, y - r + 3, x + r - 3, y + r - 3)
        for obs in obstacles:
            ox1, oy1, ox2, oy2 = obs["rect"]
            if not (char_box[2] < ox1 or char_box[0] > ox2 or char_box[3] < oy1 or char_box[1] > oy2):
                return True
        return False

    def get_interaction_point(self):
        """Retorna as coordenadas do ponto focal à frente do boneco para interação"""
        dist = 30
        if self.direction == "up":
            return (self.x, self.y - dist)
        elif self.direction == "down":
            return (self.x, self.y + dist)
        elif self.direction == "left":
            return (self.x - dist, self.y)
        else:
            return (self.x + dist, self.y)

    def draw(self, canvas):
        """Desenha o boneco na tela com animações e roupas da paleta do site"""
        canvas.delete("character")
        x = self.x
        y = self.y
        r = self.radius

        # Sombra no chão
        canvas.create_oval(
            x - 14, y + 12, x + 14, y + 20,
            fill="#d0beaa", outline="", tags="character"
        )

        # Balanço dos pés ao caminhar
        foot_offset = 0
        if self.is_moving:
            if self.walk_frame in (1, 3):
                foot_offset = 4 if self.walk_frame == 1 else -4

        # Pés / Sapatos marrons escuros (#3e2723)
        if self.direction in ("up", "down"):
            canvas.create_oval(x - 9, y + 10 + foot_offset, x - 3, y + 18 + foot_offset, fill="#3e2723", outline="", tags="character")
            canvas.create_oval(x + 3, y + 10 - foot_offset, x + 9, y + 18 - foot_offset, fill="#3e2723", outline="", tags="character")
        elif self.direction == "left":
            canvas.create_oval(x - 10 + foot_offset, y + 12, x - 2 + foot_offset, y + 18, fill="#3e2723", outline="", tags="character")
        elif self.direction == "right":
            canvas.create_oval(x + 2 - foot_offset, y + 12, x + 10 - foot_offset, y + 18, fill="#3e2723", outline="", tags="character")

        # Corpo / Avental da Padaria Aroma & Trigo (#8B4513 e branco)
        body_y = y - 4
        # Camisa branca
        canvas.create_oval(x - 12, body_y - 8, x + 12, body_y + 14, fill="#ffffff", outline="#cfc3b5", width=1, tags="character")
        
        # Avental marrom da marca (#8B4513)
        canvas.create_rectangle(x - 8, body_y - 2, x + 8, body_y + 13, fill=PALETTE["primary"], outline="", tags="character")
        # Alça do avental
        canvas.create_line(x - 5, body_y - 7, x - 5, body_y - 2, fill=PALETTE["primary"], width=2, tags="character")
        canvas.create_line(x + 5, body_y - 7, x + 5, body_y - 2, fill=PALETTE["primary"], width=2, tags="character")
        # Logotipo / detalhe de trigo dourado no avental
        canvas.create_line(x, body_y + 2, x, body_y + 8, fill=PALETTE["accent_light"], width=1, tags="character")

        # Cabeça
        head_y = y - 16
        # Rosto (tom de pele quente)
        canvas.create_oval(x - 11, head_y - 11, x + 11, head_y + 11, fill="#ffd8b3", outline="#e6be98", tags="character")

        # Cabelo castanho
        canvas.create_arc(x - 12, head_y - 13, x + 12, head_y + 7, start=0, extent=180, fill="#5c3821", outline="", tags="character")

        # Boné / Boina de Padeiro ou Faixa Aroma & Trigo
        canvas.create_rectangle(x - 10, head_y - 13, x + 10, head_y - 8, fill=PALETTE["accent"], outline="", tags="character")
        canvas.create_oval(x - 11, head_y - 17, x + 11, head_y - 10, fill="#ffffff", outline=PALETTE["accent"], width=1, tags="character")

        # Detalhes do Rosto conforme a direção
        if self.direction == "down":
            # Olhos sorridentes
            canvas.create_oval(x - 6, head_y - 1, x - 3, head_y + 2, fill="#3e2723", outline="", tags="character")
            canvas.create_oval(x + 3, head_y - 1, x + 6, head_y + 2, fill="#3e2723", outline="", tags="character")
            # Bochechas coradas
            canvas.create_oval(x - 8, head_y + 2, x - 5, head_y + 4, fill="#ffb4a2", outline="", tags="character")
            canvas.create_oval(x + 5, head_y + 2, x + 8, head_y + 4, fill="#ffb4a2", outline="", tags="character")
            # Sorriso
            canvas.create_arc(x - 4, head_y + 1, x + 4, head_y + 7, start=200, extent=140, style="arc", outline="#8B4513", width=2, tags="character")
        elif self.direction == "up":
            # Parte de trás da cabeça (só cabelo)
            canvas.create_oval(x - 11, head_y - 10, x + 11, head_y + 9, fill="#5c3821", outline="", tags="character")
        elif self.direction == "left":
            # Perfil esquerdo
            canvas.create_oval(x - 8, head_y - 1, x - 5, head_y + 2, fill="#3e2723", outline="", tags="character")
            canvas.create_line(x - 9, head_y + 4, x - 6, head_y + 5, fill="#8B4513", width=2, tags="character")
        elif self.direction == "right":
            # Perfil direito
            canvas.create_oval(x + 5, head_y - 1, x + 8, head_y + 2, fill="#3e2723", outline="", tags="character")
            canvas.create_line(x + 6, head_y + 5, x + 9, head_y + 4, fill="#8B4513", width=2, tags="character")

        # Cesto de Compras na Mão (Wicker Basket)
        basket_x = x + 13 if self.direction != "left" else x - 13
        basket_y = y + 2
        # Alça da cesta
        canvas.create_arc(basket_x - 6, basket_y - 10, basket_x + 6, basket_y - 1, start=0, extent=180, style="arc", outline="#a0522d", width=2, tags="character")
        # Corpo da cesta trançada em tom quente de trigo/vime
        canvas.create_rectangle(basket_x - 7, basket_y - 2, basket_x + 7, basket_y + 7, fill=PALETTE["accent"], outline="#8B4513", tags="character")
        # Padrão trançado
        canvas.create_line(basket_x - 4, basket_y - 2, basket_x - 4, basket_y + 7, fill="#8B4513", tags="character")
        canvas.create_line(basket_x + 2, basket_y - 2, basket_x + 2, basket_y + 7, fill="#8B4513", tags="character")

        # Se tiver produtos no carrinho, desenha uma baguete ou pãozinho saindo da cesta!
        if self.cart_item_count > 0:
            canvas.create_oval(basket_x - 3, basket_y - 7, basket_x + 3, basket_y - 2, fill="#e59866", outline="#8B4513", tags="character")
            # Indicador numérico flutuante sobre a cesta
            canvas.create_oval(basket_x + 4, basket_y - 12, basket_x + 14, basket_y - 2, fill=PALETTE["success"], outline="#ffffff", width=1, tags="character")
            canvas.create_text(basket_x + 9, basket_y - 7, text=str(min(self.cart_item_count, 99)), fill="#ffffff", font=("Segoe UI", 7, "bold"), tags="character")
