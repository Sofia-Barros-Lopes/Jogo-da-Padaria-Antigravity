"""
Módulo do Cenário da Padaria Aroma & Trigo (Ultra-Otimizado para 60 FPS)
- Camada Estática Caching: O cenário (piso, paredes, balcões, vitrines) é desenhado UMA ÚNICA VEZ
  ou quando a tela for redimensionada (Zero lag e Zero consumo de CPU).
- Camada Dinâmica: Apenas o boneco, vapor e setas animadas são atualizados por quadro.
- Adaptação Automática para Tela Cheia / Qualquer Resolução.
Paleta fiel ao site https://padariaaromaetrigo.netlify.app/
"""
import math
import random
from config import PALETTE, BRAND

class World:
    def __init__(self, width=760, height=560):
        self.width = width
        self.height = height
        self.animation_tick = 0
        self.needs_redraw_static = True
        self.steam_particles = []
        self._init_particles()
        self.recalculate_layout(width, height)

    def _init_particles(self):
        self.steam_particles = []
        # Quantidade otimizada de partículas de vapor
        for _ in range(8):
            self.steam_particles.append({
                "type": "bread",
                "x": 380,
                "y": random.randint(75, 110),
                "speed": random.uniform(0.7, 1.3),
                "size": random.uniform(3, 6),
                "drift": random.uniform(-0.25, 0.25)
            })
            
        for _ in range(4):
            self.steam_particles.append({
                "type": "coffee",
                "x": 100,
                "y": random.randint(75, 105),
                "speed": random.uniform(0.8, 1.5),
                "size": random.uniform(2, 4),
                "drift": random.uniform(-0.2, 0.2)
            })

    def recalculate_layout(self, width, height):
        """Adapta as coordenadas dos balcões e vitrines para qualquer tamanho de tela"""
        self.width = max(int(width), 680)
        self.height = max(int(height), 480)
        w = self.width
        h = self.height

        self.bounds = (28, 95, w - 28, h - 35)

        # Balcões Superiores Proporcionais
        cafeteria_x1, cafeteria_x2 = 35, int(w * 0.32)
        fornada_x1, fornada_x2 = int(w * 0.36), int(w * 0.64)
        caixa_x1, caixa_x2 = int(w * 0.68), w - 35

        # Vitrines Laterais
        salgados_x1, salgados_x2 = 35, 140
        salgados_y1, salgados_y2 = 195, h - 90

        doces_x1, doces_x2 = w - 140, w - 35
        doces_y1, doces_y2 = 195, h - 90

        # Zonas Interativas
        self.zones = [
            {
                "id": "cafeteria",
                "name": "☕ Balcão da Cafeteria",
                "category": "Bebidas",
                "rect": (cafeteria_x1, 60, cafeteria_x2, 145),
                "interact_pos": ((cafeteria_x1 + cafeteria_x2) // 2, 175),
                "color": PALETTE["primary"],
                "icon": "☕",
                "hint": "Café Espresso, Cappuccino e Sucos"
            },
            {
                "id": "fornada_paes",
                "name": "🥖 Fornada Quentinha de Pães",
                "category": "Salgados",
                "rect": (fornada_x1, 60, fornada_x2, 135),
                "interact_pos": ((fornada_x1 + fornada_x2) // 2, 165),
                "color": PALETTE["accent"],
                "icon": "🥖",
                "hint": "Pão Francês quentinho saído do forno"
            },
            {
                "id": "caixa",
                "name": "💳 Balcão do Caixa (Finalizar)",
                "category": "Caixa",
                "rect": (caixa_x1, 60, caixa_x2, 145),
                "interact_pos": ((caixa_x1 + caixa_x2) // 2, 175),
                "color": PALETTE["success"],
                "icon": "💳",
                "hint": "Pagar itens, emitir cupom e ganhar pontos"
            },
            {
                "id": "vitrine_salgados",
                "name": "🥐 Vitrine de Salgados Artesanais",
                "category": "Salgados",
                "rect": (salgados_x1, salgados_y1, salgados_x2, salgados_y2),
                "interact_pos": (salgados_x2 + 30, (salgados_y1 + salgados_y2) // 2),
                "color": PALETTE["accent"],
                "icon": "🥐",
                "hint": "Croissants, Coxinhas, Empadas e Quiches"
            },
            {
                "id": "vitrine_doces",
                "name": "🍰 Vitrine de Doces & Confeitaria",
                "category": "Doces",
                "rect": (doces_x1, doces_y1, doces_x2, doces_y2),
                "interact_pos": (doces_x1 - 30, (doces_y1 + doces_y2) // 2),
                "color": "#9c27b0",
                "icon": "🍰",
                "hint": "Bolos, Donuts, Sonhos, Pudins e Carolinas"
            }
        ]

        # Mesas Centrais
        mid_x = w // 2
        mid_y = int(h * 0.52)
        self.tables = []
        if w > 880:
            self.tables.append((mid_x - 110, mid_y))
            self.tables.append((mid_x + 110, mid_y))
        else:
            self.tables.append((mid_x, mid_y))

        # Obstáculos Físicos de Colisão
        self.obstacles = [
            {"name": "Balcão Café", "rect": (cafeteria_x1 - 5, 60, cafeteria_x2 + 5, 145)},
            {"name": "Estante Pães", "rect": (fornada_x1 - 5, 60, fornada_x2 + 5, 135)},
            {"name": "Balcão Caixa", "rect": (caixa_x1 - 5, 60, caixa_x2 + 5, 145)},
            {"name": "Vitrine Salgados", "rect": (salgados_x1 - 5, salgados_y1, salgados_x2 + 5, salgados_y2 + 5)},
            {"name": "Vitrine Doces", "rect": (doces_x1 - 5, doces_y1, doces_x2 + 5, doces_y2 + 5)}
        ]

        for tx, ty in self.tables:
            self.obstacles.append({"name": "Mesa", "rect": (tx - 38, ty - 32, tx + 38, ty + 32)})

        self.needs_redraw_static = True

    def resize(self, width, height):
        """Chamado quando a janela é maximizada ou redimensionada"""
        if width > 100 and height > 100:
            if abs(width - self.width) > 10 or abs(height - self.height) > 10:
                self.recalculate_layout(width, height)

    def update_particles(self):
        """Atualiza animação da fumacinha dos pães quentes e do café"""
        self.animation_tick += 1
        for p in self.steam_particles:
            p["y"] -= p["speed"]
            p["x"] += p["drift"]
            if p["y"] < 45:
                if p["type"] == "coffee":
                    z = self.zones[0]
                    cx1, _, cx2, _ = z["rect"]
                    p["x"] = random.randint(cx1 + 40, cx1 + 90)
                    p["y"] = random.randint(85, 105)
                else:
                    z = self.zones[1]
                    fx1, _, fx2, _ = z["rect"]
                    p["x"] = random.randint(fx1 + 30, fx2 - 30)
                    p["y"] = random.randint(85, 110)

    def get_nearby_zone(self, char_x, char_y):
        """Detecta se o jogador está perto de alguma vitrine ou do caixa"""
        closest_zone = None
        min_dist = 85
        for z in self.zones:
            ix, iy = z["interact_pos"]
            dist = math.hypot(char_x - ix, char_y - iy)
            if dist < min_dist:
                min_dist = dist
                closest_zone = z
        return closest_zone

    def _draw_static_world(self, canvas):
        """Desenha a camada de fundo UMA ÚNICA VEZ (Cache de alta performance)"""
        w, h = self.width, self.height

        # 1. Base do chão (1 retângulo gigante para todo o piso)
        canvas.create_rectangle(
            0, 78, w, h,
            fill=PALETTE["floor_tile_1"], outline="", tags="static_world"
        )

        # 2. Azulejos xadrez contrastantes (desenhados uma vez)
        tile_size = 50
        for x in range(0, w, tile_size):
            for y in range(80, h, tile_size):
                if (x // tile_size + y // tile_size) % 2 == 1:
                    canvas.create_rectangle(
                        x, y, x + tile_size, y + tile_size,
                        fill=PALETTE["floor_tile_2"], outline="#e6d7c3", width=1, tags="static_world"
                    )

        # 3. Paredes e Rodapés de Madeira Nobre
        canvas.create_rectangle(0, 0, w, 70, fill=PALETTE["wall_top"], outline="", tags="static_world")
        for x in range(0, w, 35):
            canvas.create_line(x, 0, x, 70, fill="#361b07", width=1, tags="static_world")

        # Letreiro Principal no Topo
        banner_x = w // 2
        canvas.create_rectangle(banner_x - 220, 8, banner_x + 220, 52, fill=PALETTE["dark"], outline=PALETTE["accent_light"], width=2, tags="static_world")
        canvas.create_text(
            banner_x, 22,
            text=f"🍞 {BRAND['name']} 🍞",
            fill=PALETTE["accent_light"], font=("Georgia", 13, "bold"), tags="static_world"
        )
        canvas.create_text(
            banner_x, 40,
            text=f"{BRAND['site_url'].replace('https://', '')} • {BRAND['course_info']}",
            fill="#ffffff", font=("Segoe UI", 8, "italic"), tags="static_world"
        )

        # Rodapé e Bordas
        canvas.create_rectangle(0, 68, w, 78, fill=PALETTE["wall_base"], outline="#5c2c16", tags="static_world")
        canvas.create_rectangle(0, 70, 25, h, fill=PALETTE["wall_top"], outline="#5c2c16", tags="static_world")
        canvas.create_rectangle(w - 25, 70, w, h, fill=PALETTE["wall_top"], outline="#5c2c16", tags="static_world")

        # Tapete de Entrada
        door_x1, door_x2 = w // 2 - 110, w // 2 + 110
        canvas.create_rectangle(
            door_x1, h - 45, door_x2, h - 5,
            fill=PALETTE["primary"], outline=PALETTE["accent_light"], width=2, tags="static_world"
        )
        canvas.create_text(
            w // 2, h - 25,
            text="✨ BEM-VINDO À AROMA & TRIGO ✨",
            fill="#ffffff", font=("Segoe UI", 9, "bold"), tags="static_world"
        )

        # Balcão da Cafeteria
        cx1, cy1, cx2, cy2 = self.zones[0]["rect"]
        self._draw_counter(canvas, cx1, cy1, cx2, cy2, "☕ CAFETERIA & BEBIDAS", PALETTE["primary"])
        cafe_mx = (cx1 + cx2) // 2
        canvas.create_rectangle(cafe_mx - 30, 85, cafe_mx + 10, 125, fill="#90a4ae", outline="#546e7a", width=2, tags="static_world")
        canvas.create_rectangle(cafe_mx - 25, 95, cafe_mx - 10, 120, fill="#37474f", outline="", tags="static_world")
        canvas.create_oval(cafe_mx - 5, 95, cafe_mx + 5, 110, fill="#b0bec5", outline="", tags="static_world")
        canvas.create_oval(cafe_mx + 25, 110, cafe_mx + 40, 122, fill="#ffffff", outline="#b0bec5", tags="static_world")
        canvas.create_rectangle(cafe_mx + 50, 92, cafe_mx + 70, 122, fill="#ff9800", outline="#e65100", width=1, tags="static_world")

        # Estante de Pães
        fx1, fy1, fx2, fy2 = self.zones[1]["rect"]
        self._draw_bread_rack(canvas, fx1, fy1, fx2, fy2)

        # Balcão do Caixa
        kx1, ky1, kx2, ky2 = self.zones[2]["rect"]
        self._draw_counter(canvas, kx1, ky1, kx2, ky2, "💳 CAIXA - PAGUE AQUI", PALETTE["success"])
        caixa_mx = (kx1 + kx2) // 2
        canvas.create_rectangle(caixa_mx - 40, 85, caixa_mx + 10, 125, fill="#37474f", outline="#263238", width=2, tags="static_world")
        canvas.create_rectangle(caixa_mx - 30, 90, caixa_mx, 105, fill="#81c784", outline="", tags="static_world")
        canvas.create_text(caixa_mx - 15, 97, text="R$ 0,00", fill="#1b5e20", font=("Segoe UI", 7, "bold"), tags="static_world")
        canvas.create_rectangle(caixa_mx - 35, 112, caixa_mx + 5, 122, fill="#cfd8dc", outline="", tags="static_world")
        self._draw_npc_attendant(canvas, caixa_mx + 45, 95, "Juliana (Caixa)")

        # Vitrine de Salgados
        sx1, sy1, sx2, sy2 = self.zones[3]["rect"]
        self._draw_display_case(canvas, sx1, sy1, sx2, sy2, "🥐 SALGADOS", PALETTE["accent"], "salgados")

        # Vitrine de Doces
        dx1, dy1, dx2, dy2 = self.zones[4]["rect"]
        self._draw_display_case(canvas, dx1, dy1, dx2, dy2, "🍰 DOCES", "#9c27b0", "doces")

        # Mesas Centrais
        for tx, ty in self.tables:
            self._draw_dining_table(canvas, tx, ty)

    def draw(self, canvas, nearby_zone=None, target_zone_id=None):
        """Atualização Ultra-Rápida a cada quadro (Só redesenha elementos dinâmicos)"""
        # Redesenha o fundo estático apenas se o tamanho mudou
        if self.needs_redraw_static:
            canvas.delete("static_world")
            self._draw_static_world(canvas)
            self.needs_redraw_static = False

        # Remove apenas os elementos dinâmicos do quadro anterior
        canvas.delete("dynamic")

        # 1. Partículas animadas de vapor (apenas pequenos ovals)
        for p in self.steam_particles:
            canvas.create_oval(
                p["x"] - p["size"], p["y"] - p["size"],
                p["x"] + p["size"], p["y"] + p["size"],
                fill="#ffffff", outline="", tags="dynamic"
            )

        # 2. Sinalizador da Missão Diária (Beacon Dourado com Seta Animada)
        if target_zone_id:
            target_zone = next((z for z in self.zones if z["id"] == target_zone_id), None)
            if target_zone:
                self._draw_mission_target_beacon(canvas, target_zone)

        # 3. Destaque e balão de interação quando o jogador estiver próximo
        if nearby_zone:
            self._draw_interaction_prompt(canvas, nearby_zone)

    def _draw_counter(self, canvas, x1, y1, x2, y2, title, accent_color):
        canvas.create_rectangle(x1, y1 + 15, x2, y2, fill=PALETTE["counter_wood"], outline="#4a260b", width=2, tags="static_world")
        canvas.create_rectangle(x1 - 4, y1, x2 + 4, y1 + 20, fill=PALETTE["counter_top"], outline="#c7b29a", width=2, tags="static_world")
        canvas.create_rectangle((x1+x2)//2 - 75, y1 + 25, (x1+x2)//2 + 75, y1 + 45, fill=accent_color, outline="#ffffff", width=1, tags="static_world")
        canvas.create_text((x1+x2)//2, y1 + 35, text=title, fill="#ffffff", font=("Segoe UI", 8, "bold"), tags="static_world")

    def _draw_bread_rack(self, canvas, x1, y1, x2, y2):
        canvas.create_rectangle(x1, y1, x2, y2, fill="#795548", outline="#4e342e", width=2, tags="static_world")
        canvas.create_line(x1, y1 + 25, x2, y1 + 25, fill="#3e2723", width=3, tags="static_world")
        canvas.create_line(x1, y1 + 45, x2, y1 + 45, fill="#3e2723", width=3, tags="static_world")
        for px in range(x1 + 15, x2 - 15, 24):
            canvas.create_oval(px, y1 + 10, px + 18, y1 + 23, fill="#e59866", outline="#a04000", tags="static_world")
            canvas.create_oval(px + 4, y1 + 30, px + 20, y1 + 43, fill="#f0b27a", outline="#a04000", tags="static_world")
        canvas.create_rectangle((x1+x2)//2 - 70, y1 - 2, (x1+x2)//2 + 70, y1 + 15, fill=PALETTE["dark"], outline=PALETTE["accent_light"], tags="static_world")
        canvas.create_text((x1+x2)//2, y1 + 6, text="🥖 FORNADA DE PÃES", fill=PALETTE["accent_light"], font=("Segoe UI", 7, "bold"), tags="static_world")

    def _draw_display_case(self, canvas, x1, y1, x2, y2, title, theme_color, kind):
        canvas.create_rectangle(x1, y1, x2, y2, fill="#eceff1", outline="#78909c", width=2, tags="static_world")
        canvas.create_rectangle(x1 + 6, y1 + 28, x2 - 6, y2 - 10, fill=PALETTE["glass"], outline=PALETTE["glass_border"], width=1, tags="static_world")
        
        h = (y2 - y1 - 38) // 3
        for i in range(1, 3):
            py = y1 + 28 + i * h
            canvas.create_line(x1 + 6, py, x2 - 6, py, fill="#90caf9", width=2, tags="static_world")
            
        cx = (x1 + x2) // 2
        if kind == "salgados":
            canvas.create_oval(cx - 20, y1 + 45, cx - 5, y1 + 60, fill="#e67e22", outline="#a04000", tags="static_world")
            canvas.create_oval(cx + 5, y1 + 45, cx + 22, y1 + 58, fill="#f39c12", outline="#d35400", tags="static_world")
            canvas.create_oval(cx - 15, y1 + 105, cx + 15, y1 + 120, fill="#d35400", outline="#6e2c00", tags="static_world")
            canvas.create_oval(cx - 18, y1 + 165, cx + 18, y1 + 182, fill="#e59866", outline="#873600", tags="static_world")
        else:
            canvas.create_rectangle(cx - 18, y1 + 42, cx + 18, y1 + 62, fill="#4a235a", outline="#6c3483", tags="static_world")
            canvas.create_oval(cx - 14, y1 + 102, cx + 14, y1 + 125, fill="#f06292", outline="#c2185b", tags="static_world")
            canvas.create_oval(cx - 16, y1 + 162, cx + 16, y1 + 182, fill="#ffe082", outline="#f57f17", tags="static_world")

        canvas.create_rectangle(x1 - 2, y1, x2 + 2, y1 + 26, fill=theme_color, outline="#ffffff", width=1, tags="static_world")
        canvas.create_text(cx, y1 + 13, text=title, fill="#ffffff", font=("Segoe UI", 8, "bold"), tags="static_world")

    def _draw_dining_table(self, canvas, cx, cy):
        canvas.create_oval(cx - 40, cy + 15, cx + 40, cy + 35, fill="#d7ccc8", outline="", tags="static_world")
        canvas.create_oval(cx - 45, cy - 10, cx - 25, cy + 10, fill="#8d6e63", outline="#4e342e", tags="static_world")
        canvas.create_oval(cx + 25, cy - 10, cx + 45, cy + 10, fill="#8d6e63", outline="#4e342e", tags="static_world")
        canvas.create_oval(cx - 32, cy - 25, cx + 32, cy + 25, fill=PALETTE["table_cloth"], outline="#78281f", width=2, tags="static_world")
        canvas.create_oval(cx - 24, cy - 18, cx + 24, cy + 18, fill=PALETTE["table_cloth_white"], outline="", tags="static_world")
        canvas.create_oval(cx - 7, cy - 7, cx + 7, cy + 7, fill=PALETTE["accent"], outline="#8B4513", tags="static_world")
        canvas.create_line(cx, cy, cx, cy - 10, fill="#2e7d32", width=2, tags="static_world")
        canvas.create_oval(cx - 4, cy - 14, cx + 4, cy - 8, fill="#f1c40f", outline="", tags="static_world")

    def _draw_npc_attendant(self, canvas, x, y, name):
        canvas.create_oval(x - 9, y - 8, x + 9, y + 8, fill="#ffd8b3", outline="#e6be98", tags="static_world")
        canvas.create_arc(x - 10, y - 10, x + 10, y + 2, start=0, extent=180, fill="#ffffff", outline=PALETTE["primary"], tags="static_world")
        canvas.create_oval(x - 5, y - 1, x - 2, y + 2, fill="#3e2723", outline="", tags="static_world")
        canvas.create_oval(x + 2, y - 1, x + 5, y + 2, fill="#3e2723", outline="", tags="static_world")
        canvas.create_arc(x - 4, y, x + 4, y + 5, start=200, extent=140, style="arc", outline="#8B4513", width=2, tags="static_world")
        canvas.create_text(x, y + 15, text=name, fill="#ffffff", font=("Segoe UI", 7, "bold"), tags="static_world")

    def _draw_mission_target_beacon(self, canvas, target_zone):
        """Desenha sinalizador reluzente e seta animada apontando exatamente onde o jogador deve ir"""
        ix, iy = target_zone["interact_pos"]
        pulse = math.sin(self.animation_tick * 0.22) * 8
        bounce_y = iy - 58 + math.sin(self.animation_tick * 0.25) * 6

        # Halo pulsante no chão
        canvas.create_oval(
            ix - 32 - pulse, iy - 16 - pulse,
            ix + 32 + pulse, iy + 16 + pulse,
            outline=PALETTE["gold"], width=3, tags="dynamic"
        )
        canvas.create_oval(
            ix - 24, iy - 12, ix + 24, iy + 12,
            fill="#fff3cd", outline=PALETTE["gold"], width=1, tags="dynamic"
        )

        is_caixa = (target_zone["id"] == "caixa")
        banner_text = "💳 PAGUE NO CAIXA AQUI! 🌟" if is_caixa else "⭐ ITEM DA MISSÃO AQUI! ⭐"
        banner_bg = PALETTE["success"] if is_caixa else PALETTE["gold"]

        canvas.create_rectangle(
            ix - 90, bounce_y - 12, ix + 90, bounce_y + 12,
            fill=banner_bg, outline="#ffffff", width=2, tags="dynamic"
        )
        canvas.create_text(
            ix, bounce_y,
            text=banner_text,
            fill="#ffffff" if is_caixa else PALETTE["dark"],
            font=("Segoe UI", 8, "bold"), tags="dynamic"
        )

        # Seta apontando para baixo
        arrow_top = bounce_y + 13
        canvas.create_polygon(
            ix - 10, arrow_top,
            ix + 10, arrow_top,
            ix, arrow_top + 10,
            fill=banner_bg, outline="#ffffff", tags="dynamic"
        )

    def _draw_interaction_prompt(self, canvas, zone):
        """Desenha balão iluminado convidando a interagir com tecla [E] ou Espaço"""
        ix, iy = zone["interact_pos"]
        pulse = math.sin(self.animation_tick * 0.15) * 4

        canvas.create_oval(
            ix - 25 - pulse, iy - 12 - pulse,
            ix + 25 + pulse, iy + 12 + pulse,
            outline=zone["color"], width=2, dash=(3, 3), tags="dynamic"
        )

        balloon_y = iy - 32 + pulse * 0.5
        msg = f"[E] Abrir {zone['name']}" if zone["id"] != "caixa" else f"[E] PAGAR NO CAIXA 💳"

        canvas.create_rectangle(ix - 80, balloon_y - 12, ix + 80, balloon_y + 12, fill="#3e2723", outline="", tags="dynamic")
        canvas.create_rectangle(ix - 82, balloon_y - 14, ix + 78, balloon_y + 10, fill=PALETTE["dark"], outline=zone["color"], width=2, tags="dynamic")
        canvas.create_text(ix - 2, balloon_y - 2, text=msg, fill="#ffffff", font=("Segoe UI", 8, "bold"), tags="dynamic")
