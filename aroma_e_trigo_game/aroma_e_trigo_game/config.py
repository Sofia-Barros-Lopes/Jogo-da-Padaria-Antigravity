"""
Configurações, Paleta de Cores e Catálogo de Produtos
Padaria Aroma & Trigo - Jogo Desktop
Site: https://padariaaromaetrigo.netlify.app/
Projeto: Pronatec - Negócios Inovadores com IA
"""
import os

# Caminhos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

# Paleta de Cores Oficial do Site padariaaromaetrigo.netlify.app
PALETTE = {
    "bg": "#fcf8f2",           # Fundo creme suave do site
    "primary": "#8B4513",      # Marrom tradicional da navbar e botões (#8B4513)
    "primary_hover": "#a0522d",# Marrom terracota ao passar o mouse
    "dark": "#3e2723",         # Marrom espresso escuro do banner e footer (#3e2723)
    "accent": "#d2691e",       # Laranja crocante do carrinho e destaques (#d2691e)
    "accent_light": "#ffe0b2", # Tom pêssego/dourado suave do slogan (#ffe0b2)
    "success": "#2e7d32",      # Verde dos preços e finalização (#2e7d32)
    "card_bg": "#ffffff",      # Fundo branco puro dos cards
    "card_border": "#ead9c6",  # Borda suave dos cards
    "text": "#333333",         # Texto principal escuro
    "text_muted": "#777777",   # Texto secundário
    "gold": "#d4af37",         # Dourado para troféus e estrelas
    
    # Cores do Cenário da Padaria
    "floor_tile_1": "#f5ebd8", # Piso cerâmica clara
    "floor_tile_2": "#eedec5", # Piso cerâmica escura
    "wall_top": "#4a2810",     # Parede de tijolinho/madeira topo
    "wall_base": "#8B4513",    # Rodapé de madeira nobre
    "counter_wood": "#6d3710", # Balcão de atendimento
    "counter_top": "#dfcbb5",  # Tampo de mármore/madeira clara do balcão
    "glass": "#d8edf8",        # Vidro das vitrines
    "glass_border": "#9cb8cb", # Moldura das vitrines
    "table_cloth": "#c0392b",  # Toalha de mesa xadrez vermelho
    "table_cloth_white": "#ffffff",
    "bread_gold": "#e59866"    # Pães dourados
}

# Informações da Marca
BRAND = {
    "name": "Padaria Aroma & Trigo",
    "slogan": "Pães artesanais e momentos inesquecíveis todos os dias",
    "site_url": "https://padariaaromaetrigo.netlify.app/",
    "course_info": "Pronatec - Negócios Inovadores com IA",
    "address": "Rua do Trigo, nº 123 - Centro, São Paulo - SP",
    "phone": "(11) 3333-4444",
    "whatsapp": "(11) 98888-7777"
}

# Catálogo Oficial extraído fielmente do site
PRODUCTS = [
    # --- SALGADOS ---
    {
        "id": "s1",
        "name": "Croissant de Queijo",
        "category": "Salgados",
        "price": 8.50,
        "desc": "Folhado crocante recheado com queijo derretido.",
        "image": "croissantQueijo.jpg",
        "icon": "🥐",
        "zone": "vitrine_salgados"
    },
    {
        "id": "s2",
        "name": "Pão Francês (Kg)",
        "category": "Salgados",
        "price": 14.90,
        "desc": "Quentinho, casca dourada e crocante, miolo macio.",
        "image": "paoFrances.jpg",
        "icon": "🥖",
        "zone": "fornada_paes"
    },
    {
        "id": "s3",
        "name": "Coxinha de Frango",
        "category": "Salgados",
        "price": 7.50,
        "desc": "Massa dourada recheada com frango e catupiry.",
        "image": "coxinhaFrango.jpg",
        "icon": "🍗",
        "zone": "vitrine_salgados"
    },
    {
        "id": "s4",
        "name": "Enroladinho de Presunto",
        "category": "Salgados",
        "price": 6.50,
        "desc": "Presunto e queijo envoltos em massa macia.",
        "image": "enroladinhoPresuntoQueijo.jpg",
        "icon": "🥟",
        "zone": "vitrine_salgados"
    },
    {
        "id": "s5",
        "name": "Empada de Palmito",
        "category": "Salgados",
        "price": 7.00,
        "desc": "Massa podre que derrete na boca com palmito cremoso.",
        "image": "empadaPalmito.jpg",
        "icon": "🥧",
        "zone": "vitrine_salgados"
    },
    {
        "id": "s6",
        "name": "Pão de Queijo Tradicional",
        "category": "Salgados",
        "price": 4.50,
        "desc": "Receita mineira autêntica com queijo curado.",
        "image": "paoQueijo.jpg",
        "icon": "🧀",
        "zone": "vitrine_salgados"
    },
    {
        "id": "s7",
        "name": "Esfiha Aberta de Carne",
        "category": "Salgados",
        "price": 6.00,
        "desc": "Tempero árabe tradicional com carne moída de primeira.",
        "image": "esfihaAbertaCarne.jpg",
        "icon": "🍕",
        "zone": "vitrine_salgados"
    },
    {
        "id": "s8",
        "name": "Kibe Recheado",
        "category": "Salgados",
        "price": 7.00,
        "desc": "Kibe frito crocante recheado com requeijão cremoso.",
        "image": "kibeRecheado.jpg",
        "icon": "🥩",
        "zone": "vitrine_salgados"
    },
    {
        "id": "s9",
        "name": "Folhado de Frango",
        "category": "Salgados",
        "price": 8.00,
        "desc": "Massa folhada leve com frango desfiado e requeijão.",
        "image": "folhadoFrango.png",
        "icon": "🥐",
        "zone": "vitrine_salgados"
    },
    {
        "id": "s10",
        "name": "Quiche de Alho Poró",
        "category": "Salgados",
        "price": 9.50,
        "desc": "Torta fina francesa recheada com creme e alho-poró.",
        "image": "quicheAlho.png",
        "icon": "🥧",
        "zone": "vitrine_salgados"
    },

    # --- DOCES ---
    {
        "id": "d1",
        "name": "Fatia de Bolo de Chocolate",
        "category": "Doces",
        "price": 9.00,
        "desc": "Massa fofa de cacau nobre com cobertura aveludada.",
        "image": "boloChocolate.jpg",
        "icon": "🍰",
        "zone": "vitrine_doces"
    },
    {
        "id": "d2",
        "name": "Donut Recheado",
        "category": "Doces",
        "price": 7.00,
        "desc": "Donut americano com cobertura colorida e recheio cremoso.",
        "image": "donoutRecheado.jpg",
        "icon": "🍩",
        "zone": "vitrine_doces"
    },
    {
        "id": "d3",
        "name": "Sonho de Creme",
        "category": "Doces",
        "price": 6.00,
        "desc": "O clássico da padaria com recheio farto de baunilha.",
        "image": "sonhoCreme.jpg",
        "icon": "🥯",
        "zone": "vitrine_doces"
    },
    {
        "id": "d5",
        "name": "Carolina de Doce de Leite",
        "category": "Doces",
        "price": 5.00,
        "desc": "Carolinas recheadas com autêntico doce de leite.",
        "image": "carolinaDoceLeite.jpg",
        "icon": "🍮",
        "zone": "vitrine_doces"
    },
    {
        "id": "d6",
        "name": "Croissant de Nutella",
        "category": "Doces",
        "price": 11.00,
        "desc": "Massa folhada amanteigada recheada com pura Nutella.",
        "image": "croissantNutella.jpg",
        "icon": "🥐",
        "zone": "vitrine_doces"
    },
    {
        "id": "d7",
        "name": "Pudim de Leite Condensado",
        "category": "Doces",
        "price": 8.00,
        "desc": "Fatia sedosa e caramelizada sem furinhos.",
        "image": "pudim.png",
        "icon": "🍮",
        "zone": "vitrine_doces"
    },
    {
        "id": "d8",
        "name": "Éclair de Chocolate",
        "category": "Doces",
        "price": 8.50,
        "desc": "Bomba tradicional francesa com calda de chocolate.",
        "image": "eclairChocolate.jpg",
        "icon": "🍫",
        "zone": "vitrine_doces"
    },

    # --- BEBIDAS ---
    {
        "id": "b1",
        "name": "Café Espresso Tradicional",
        "category": "Bebidas",
        "price": 4.50,
        "desc": "Grãos selecionados com crema espessa e aroma marcante.",
        "image": "cafeEspresso.jpg",
        "icon": "☕",
        "zone": "cafeteria"
    },
    {
        "id": "b2",
        "name": "Cappuccino Cremoso",
        "category": "Bebidas",
        "price": 7.50,
        "desc": "Espresso com leite vaporizado e toque suave de canela.",
        "image": "cappuccino.jpg",
        "icon": "☕",
        "zone": "cafeteria"
    },
    {
        "id": "b3",
        "name": "Suco Natural de Laranja",
        "category": "Bebidas",
        "price": 7.00,
        "desc": "Espremido na hora, 100% fruta natural e geladinho.",
        "image": "sucoLaranja.jpg",
        "icon": "🍊",
        "zone": "cafeteria"
    }
]

# Zonas da Loja e seus nomes amigáveis
ZONE_NAMES = {
    "vitrine_salgados": "Vitrine de Salgados (Lado Esquerdo)",
    "fornada_paes": "Fornada Quentinha de Pães (Fundo, Centro)",
    "cafeteria": "Balcão da Cafeteria (Canto Superior Esquerdo)",
    "vitrine_doces": "Vitrine de Doces & Confeitaria (Lado Direito)",
    "caixa": "Balcão do Caixa (Canto Superior Direito)"
}

# Missões de Compra Detalhadas (Desafios Pronatec com Guia Passo a Passo)
MISSIONS = [
    {
        "id": "m1",
        "title": "☕ Missão Diária: Combo Café da Manhã Tradicional",
        "story": "O dia acabou de amanhecer na Aroma & Trigo! Um cliente fiel fez um pedido clássico de café da manhã. Siga o roteiro abaixo:",
        "steps": [
            {
                "item_id": "s2",
                "name": "Pão Francês (Kg)",
                "zone_id": "fornada_paes",
                "zone_name": "Estante de Pães (Fundo, Centro)",
                "hint": "Ande para o fundo da loja até a estante com fumaça aromática de pães."
            },
            {
                "item_id": "b1",
                "name": "Café Espresso Tradicional",
                "zone_id": "cafeteria",
                "zone_name": "Balcão da Cafeteria (Superior Esquerdo)",
                "hint": "Vá ao balcão com a cafeteira italiana no canto superior esquerdo."
            },
            {
                "item_id": "s6",
                "name": "Pão de Queijo Tradicional",
                "zone_id": "vitrine_salgados",
                "zone_name": "Vitrine de Salgados (Lateral Esquerda)",
                "hint": "Visite a grande vitrine iluminada de salgados no lado esquerdo."
            }
        ],
        "reward_points": 50,
        "reward_money": 20.0,
        "bonus_msg": "Sensacional! Você montou o melhor café da manhã artesanal de São Paulo!"
    },
    {
        "id": "m2",
        "title": "🥐 Missão Diária: Lanche da Tarde Gourmet",
        "story": "Às 16h o movimento na padaria esquenta! Prepare este lanche sofisticado e saboroso:",
        "steps": [
            {
                "item_id": "s1",
                "name": "Croissant de Queijo",
                "zone_id": "vitrine_salgados",
                "zone_name": "Vitrine de Salgados (Lateral Esquerda)",
                "hint": "Procure os croissants folhados na vitrine de salgados."
            },
            {
                "item_id": "b2",
                "name": "Cappuccino Cremoso",
                "zone_id": "cafeteria",
                "zone_name": "Balcão da Cafeteria (Superior Esquerdo)",
                "hint": "Peça um cappuccino com espuma e canela na cafeteria."
            },
            {
                "item_id": "d3",
                "name": "Sonho de Creme",
                "zone_id": "vitrine_doces",
                "zone_name": "Vitrine de Doces (Lateral Direita)",
                "hint": "Vá até a vitrine de doces do lado direito e pegue o sonho com creme de baunilha."
            }
        ],
        "reward_points": 75,
        "reward_money": 25.0,
        "bonus_msg": "Que lanche espetacular! O aroma de café e croissant encantou a todos!"
    },
    {
        "id": "m3",
        "title": "🍰 Missão Diária: Banquete de Doces da Casa",
        "story": "Uma festa de aniversário vai acontecer hoje! Monte uma seleção com os melhores doces artesanais:",
        "steps": [
            {
                "item_id": "d1",
                "name": "Fatia de Bolo de Chocolate",
                "zone_id": "vitrine_doces",
                "zone_name": "Vitrine de Doces (Lateral Direita)",
                "hint": "Pegue o bolo fofinho de chocolate na vitrine de doces."
            },
            {
                "item_id": "d2",
                "name": "Donut Recheado",
                "zone_id": "vitrine_doces",
                "zone_name": "Vitrine de Doces (Lateral Direita)",
                "hint": "Escolha o donut recheado com cobertura colorida."
            },
            {
                "item_id": "d7",
                "name": "Pudim de Leite Condensado",
                "zone_id": "vitrine_doces",
                "zone_name": "Vitrine de Doces (Lateral Direita)",
                "hint": "Pegue a fatia dourada de pudim caramelizado."
            }
        ],
        "reward_points": 100,
        "reward_money": 35.0,
        "bonus_msg": "Banquete dos deuses! Você é o mestre da confeitaria Aroma & Trigo!"
    },
    {
        "id": "m4",
        "title": "🥟 Missão Diária: Festa dos Salgados & Suco",
        "story": "Hora do almoço rápido e reforçado! Reúna salgados fritos na hora com suco natural:",
        "steps": [
            {
                "item_id": "s3",
                "name": "Coxinha de Frango",
                "zone_id": "vitrine_salgados",
                "zone_name": "Vitrine de Salgados (Lateral Esquerda)",
                "hint": "Pegue a famosa coxinha de frango com catupiry."
            },
            {
                "item_id": "s7",
                "name": "Esfiha Aberta de Carne",
                "zone_id": "vitrine_salgados",
                "zone_name": "Vitrine de Salgados (Lateral Esquerda)",
                "hint": "Escolha a esfiha aberta temperada na vitrine de salgados."
            },
            {
                "item_id": "b3",
                "name": "Suco Natural de Laranja",
                "zone_id": "cafeteria",
                "zone_name": "Balcão da Cafeteria (Superior Esquerdo)",
                "hint": "Pegue um suco de laranja natural e geladinho na cafeteria."
            }
        ],
        "reward_points": 60,
        "reward_money": 20.0,
        "bonus_msg": "Delícia de combinação! Salgados crocantes e suco fresquinho!"
    }
]
