import streamlit as st
import random
import math

# ─── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="統計大富翁：房價大作戰",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Fredoka+One&display=swap');

*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #fff0f5;
    font-family: 'Nunito', sans-serif;
}

/* Polka-dot background */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image: radial-gradient(circle, #ffb6c1 1.5px, transparent 1.5px);
    background-size: 28px 28px;
    opacity: 0.45;
    pointer-events: none;
    z-index: 0;
}

[data-testid="stAppViewContainer"] > * { position: relative; z-index: 1; }

h1, h2, h3, h4 { font-family: 'Fredoka One', cursive; }

/* Hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #ff6b9d, #ff8fab);
    color: white;
    border: none;
    border-radius: 25px;
    font-family: 'Fredoka One', cursive;
    font-size: 1rem;
    padding: 0.5rem 1.4rem;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(255,107,157,0.4);
    transition: all 0.2s;
}
.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 18px rgba(255,107,157,0.5);
}
.stButton > button:active { transform: translateY(0); }

/* Cards */
.card {
    background: white;
    border-radius: 20px;
    padding: 1rem 1.2rem;
    box-shadow: 0 4px 16px rgba(255,107,157,0.15);
    border: 2px solid #ffd6e0;
    margin-bottom: 0.8rem;
}

.player-card {
    background: linear-gradient(135deg, #fff0f5, #ffe4ec);
    border-radius: 16px;
    padding: 0.8rem 1rem;
    border: 2px solid #ffb6c1;
    text-align: center;
    transition: all 0.2s;
}
.player-card.active {
    border-color: #ff6b9d;
    box-shadow: 0 0 0 3px rgba(255,107,157,0.3);
    transform: scale(1.03);
}

.district-btn {
    display: inline-block;
    padding: 0.25rem 0.6rem;
    border-radius: 12px;
    font-size: 0.78rem;
    font-weight: 700;
    cursor: default;
}

.chance-card {
    background: linear-gradient(135deg, #fff9c4, #fff3e0);
    border: 3px dashed #ffa000;
    border-radius: 18px;
    padding: 1rem;
    text-align: center;
}
.fate-card {
    background: linear-gradient(135deg, #e8f5e9, #f3e5f5);
    border: 3px dashed #7b1fa2;
    border-radius: 18px;
    padding: 1rem;
    text-align: center;
}

.answer-input > div > input {
    border-radius: 12px !important;
    border: 2px solid #ffb6c1 !important;
    font-size: 1.2rem !important;
    text-align: center;
}

.property-tag {
    display: inline-block;
    background: #ff6b9d;
    color: white;
    border-radius: 8px;
    padding: 0.15rem 0.5rem;
    font-size: 0.72rem;
    font-weight: 700;
    margin: 0.1rem;
}

.msg-box {
    background: linear-gradient(135deg, #e3f2fd, #f8bbd0);
    border-radius: 14px;
    padding: 0.8rem 1rem;
    font-size: 0.95rem;
    font-weight: 700;
    color: #333;
    text-align: center;
    border: 2px solid #90caf9;
    margin: 0.5rem 0;
}

/* Dice */
.dice-face {
    font-size: 3.5rem;
    text-align: center;
    animation: diceBounce 0.4s ease;
}
@keyframes diceBounce {
    0% { transform: scale(0.5) rotate(-20deg); opacity: 0; }
    70% { transform: scale(1.2) rotate(5deg); }
    100% { transform: scale(1) rotate(0deg); opacity: 1; }
}

/* Map grid */
.map-cell {
    border-radius: 10px;
    padding: 0.3rem 0.2rem;
    text-align: center;
    font-size: 0.7rem;
    font-weight: 700;
    min-height: 58px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 2px solid;
    position: relative;
    cursor: default;
}
.cell-district { background: #fff0f5; border-color: #ffb6c1; color: #c2185b; }
.cell-chance   { background: #fff9c4; border-color: #fbc02d; color: #e65100; }
.cell-fate     { background: #f3e5f5; border-color: #ab47bc; color: #6a1b9a; }
.cell-tax      { background: #fbe9e7; border-color: #ff5722; color: #bf360c; }
.cell-jail     { background: #e8eaf6; border-color: #5c6bc0; color: #283593; }
.cell-go       { background: #e8f5e9; border-color: #43a047; color: #1b5e20; }

.player-token {
    font-size: 1.1rem;
    line-height: 1;
}
</style>
""", unsafe_allow_html=True)

# ─── Constants ─────────────────────────────────────────────────────────────────
PLAYERS = [
    {"name": "玩家1 豬", "emoji": "🐷", "color": "#ff6b9d"},
    {"name": "玩家2 貓", "emoji": "🐱", "color": "#7c4dff"},
    {"name": "玩家3 狗", "emoji": "🐶", "color": "#00bcd4"},
    {"name": "玩家4 兔", "emoji": "🐰", "color": "#ff9800"},
]

DISTRICTS = {
    "萬華區": {
        "data": [63, 44, 49, 58, 49],
        "task": "由小到大排序並計算平均數",
        "task_type": "sort_mean",
        "answer": round(sum([63,44,49,58,49])/5, 1),
        "price": 500,
        "color": "#e91e63",
    },
    "信義區": {
        "data": [170, 128, 100, 130, 88],
        "task": "計算平均數",
        "task_type": "mean",
        "answer": round(sum([170,128,100,130,88])/5, 1),
        "price": 1200,
        "color": "#9c27b0",
    },
    "大安區": {
        "data": [98, 121, 36, 85, 178],
        "task": "計算中位數",
        "task_type": "median",
        "answer": sorted([98,121,36,85,178])[2],
        "price": 1500,
        "color": "#3f51b5",
    },
    "中和區": {
        "data": [20, 22, 17, 33, 65],
        "task": "計算平均數",
        "task_type": "mean",
        "answer": round(sum([20,22,17,33,65])/5, 1),
        "price": 350,
        "color": "#009688",
    },
    "板橋區": {
        "data": [51, 10, 69, 53, 39],
        "task": "計算平均數",
        "task_type": "mean",
        "answer": round(sum([51,10,69,53,39])/5, 1),
        "price": 400,
        "color": "#ff5722",
    },
    "新莊區": {
        "data": [23, 15, 38, 85, 58],
        "task": "計算中位數",
        "task_type": "median",
        "answer": sorted([23,15,38,85,58])[2],
        "price": 380,
        "color": "#795548",
    },
    "淡水區": {
        "data": [48, 35, 64, 13, 30],
        "task": "由小到大排序並找中位數",
        "task_type": "sort_median",
        "answer": sorted([48,35,64,13,30])[2],
        "price": 420,
        "color": "#607d8b",
    },
    "新店區": {
        "data": [133, 19, 17, 15, 14],
        "task": "避開極端值計算中位數（去掉133）",
        "task_type": "trimmed_median",
        "answer": sorted([19,17,15,14])[len(sorted([19,17,15,14]))//2],
        "price": 450,
        "color": "#4caf50",
    },
    "三重區": {
        "data": [11, 39, 56, 42, 52],
        "task": "計算平均數",
        "task_type": "mean",
        "answer": round(sum([11,39,56,42,52])/5, 1),
        "price": 360,
        "color": "#ff9800",
    },
    "士林區": {
        "data": [36, 67, 90, 96, 45],
        "task": "排序並找中位數",
        "task_type": "sort_median",
        "answer": sorted([36,67,90,96,45])[2],
        "price": 700,
        "color": "#00bcd4",
    },
    "北投區": {
        "data": [13, 65, 80, 38, 40],
        "task": "找中位數",
        "task_type": "median",
        "answer": sorted([13,65,80,38,40])[2],
        "price": 600,
        "color": "#8bc34a",
    },
    "中正區": {
        "data": [73, 152, 151, 154, 157],
        "task": "計算平均數",
        "task_type": "mean",
        "answer": round(sum([73,152,151,154,157])/5, 1),
        "price": 1000,
        "color": "#f44336",
    },
}

CHANCE_CARDS = [
    {"title": "實價登錄上路！", "desc": "市場資訊透明化！下次購買地產享 9 折優惠。", "type": "discount", "value": 0.9},
    {"title": "捷運線開通！", "desc": "交通便利帶動房價！你持有的所有地產價值 +10%。", "type": "property_up", "value": 0.1},
    {"title": "政府補貼青安貸款！", "desc": "房市熱絡！所有玩家向你支付 100 萬租金。", "type": "collect_all", "value": 100},
    {"title": "精準預測趨勢！", "desc": "統計天才！擲骰判定：偶數獲得 200 萬獎金。", "type": "dice_bonus", "value": 200},
]

FATE_CARDS = [
    {"title": "央行宣佈升息！", "desc": "貸款壓力增加！請支付銀行 200 萬利息。", "type": "pay_bank", "value": 200},
    {"title": "出現極端值（豪宅）！", "desc": "數據偏差！你被虛假行情誤導，本回合計算任務難度加倍。", "type": "double_task", "value": 0},
    {"title": "地價稅調整！", "desc": "根據你擁有的地產數量，每棟地產需支付 50 萬稅金。", "type": "property_tax", "value": 50},
    {"title": "區域性地震風險！", "desc": "擲骰判定：若擲出 1 或 6，指定一處地產價值 -20%。", "type": "quake", "value": 0.2},
]

# Board layout: 20 cells total in order
BOARD = [
    {"type": "go",       "label": "出發點 🏁", "key": None},
    {"type": "district", "label": "萬華區",    "key": "萬華區"},
    {"type": "chance",   "label": "機會 🃏",   "key": None},
    {"type": "district", "label": "中和區",    "key": "中和區"},
    {"type": "district", "label": "板橋區",    "key": "板橋區"},
    {"type": "jail",     "label": "監獄 🔒",   "key": None},
    {"type": "district", "label": "新莊區",    "key": "新莊區"},
    {"type": "fate",     "label": "命運 🎴",   "key": None},
    {"type": "district", "label": "淡水區",    "key": "淡水區"},
    {"type": "district", "label": "新店區",    "key": "新店區"},
    {"type": "tax",      "label": "國稅局 💸", "key": None},
    {"type": "district", "label": "三重區",    "key": "三重區"},
    {"type": "chance",   "label": "機會 🃏",   "key": None},
    {"type": "district", "label": "士林區",    "key": "士林區"},
    {"type": "district", "label": "北投區",    "key": "北投區"},
    {"type": "fate",     "label": "命運 🎴",   "key": None},
    {"type": "district", "label": "信義區",    "key": "信義區"},
    {"type": "district", "label": "大安區",    "key": "大安區"},
    {"type": "chance",   "label": "機會 🃏",   "key": None},
    {"type": "district", "label": "中正區",    "key": "中正區"},
]

BOARD_SIZE = len(BOARD)

DICE_FACES = {1:"⚀", 2:"⚁", 3:"⚂", 4:"⚃", 5:"⚄", 6:"⚅"}

def fmt(n): return f"{n:,.0f}"

# ─── Session state init ────────────────────────────────────────────────────────
def init_state():
    if "game_started" not in st.session_state:
        st.session_state.game_started = False
    if "players" not in st.session_state:
        st.session_state.players = [
            {"name": p["name"], "emoji": p["emoji"], "color": p["color"],
             "money": 3000, "pos": 0, "properties": [], "jail": 0,
             "discount": 1.0, "alive": True}
            for p in PLAYERS
        ]
    if "current_player" not in st.session_state:
        st.session_state.current_player = 0
    if "phase" not in st.session_state:
        st.session_state.phase = "roll"          # roll | land | task | card | buy | end_turn
    if "last_dice" not in st.session_state:
        st.session_state.last_dice = None
    if "message" not in st.session_state:
        st.session_state.message = ""
    if "active_card" not in st.session_state:
        st.session_state.active_card = None
    if "active_district" not in st.session_state:
        st.session_state.active_district = None
    if "task_solved" not in st.session_state:
        st.session_state.task_solved = False
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "winner" not in st.session_state:
        st.session_state.winner = None
    if "double_task" not in st.session_state:
        st.session_state.double_task = False
    if "answer_submitted" not in st.session_state:
        st.session_state.answer_submitted = False

init_state()

# ─── Helpers ──────────────────────────────────────────────────────────────────
def current():
    return st.session_state.players[st.session_state.current_player]

def next_alive():
    n = len(st.session_state.players)
    idx = (st.session_state.current_player + 1) % n
    for _ in range(n):
        if st.session_state.players[idx]["alive"]:
            return idx
        idx = (idx + 1) % n
    return st.session_state.current_player

def check_game_over():
    alive = [p for p in st.session_state.players if p["alive"]]
    if len(alive) == 1:
        st.session_state.game_over = True
        st.session_state.winner = alive[0]
        return True
    return False

def check_bankruptcy(p):
    if p["money"] <= 0:
        p["alive"] = False
        p["money"] = 0
        st.session_state.message += f"  💀 {p['emoji']} {p['name']} 破產了！"

def pay(player, amount):
    player["money"] = max(0, player["money"] - amount)
    check_bankruptcy(player)

def apply_card(card, player):
    t = card["type"]
    v = card["value"]
    if t == "discount":
        player["discount"] = 0.9
        st.session_state.message = f"🎉 {player['emoji']} 下次購買享 9 折！"
    elif t == "property_up":
        for prop in player["properties"]:
            if prop in DISTRICTS:
                old = DISTRICTS[prop]["price"]
                DISTRICTS[prop]["price"] = int(old * (1 + v))
        st.session_state.message = f"📈 {player['emoji']} 地產全數增值 10%！"
    elif t == "collect_all":
        for p in st.session_state.players:
            if p is not player and p["alive"]:
                pay(p, v)
                player["money"] += v
        st.session_state.message = f"💰 {player['emoji']} 向所有玩家收取 {fmt(v)} 萬！"
    elif t == "dice_bonus":
        d = random.randint(1,6)
        if d % 2 == 0:
            player["money"] += v
            st.session_state.message = f"🎲 擲出 {d}（偶數）！{player['emoji']} 獲得 {fmt(v)} 萬！"
        else:
            st.session_state.message = f"🎲 擲出 {d}（奇數）。很遺憾，無獎金。"
    elif t == "pay_bank":
        pay(player, v)
        st.session_state.message = f"🏦 {player['emoji']} 支付銀行 {fmt(v)} 萬利息。"
    elif t == "double_task":
        st.session_state.double_task = True
        st.session_state.message = f"😱 {player['emoji']} 下個地產任務難度加倍！"
    elif t == "property_tax":
        tax = len(player["properties"]) * v
        pay(player, tax)
        st.session_state.message = f"🏛️ {player['emoji']} 共持有 {len(player['properties'])} 棟，繳稅 {fmt(tax)} 萬。"
    elif t == "quake":
        d = random.randint(1,6)
        if d in (1,6) and player["properties"]:
            prop = player["properties"][0]
            if prop in DISTRICTS:
                DISTRICTS[prop]["price"] = int(DISTRICTS[prop]["price"] * (1 - v))
            st.session_state.message = f"🌋 擲出 {d}！{player['emoji']} 的 {prop} 價值 -20%！"
        else:
            st.session_state.message = f"🎲 擲出 {d}。地震未波及你的地產！"

# ─── HOME SCREEN ──────────────────────────────────────────────────────────────
if not st.session_state.game_started:
    st.markdown("""
    <div style='text-align:center; padding: 2rem 0 1rem;'>
        <div style='font-size:4rem; margin-bottom:0.3rem;'>🏠🎲🏘️</div>
        <h1 style='font-family: "Fredoka One", cursive; font-size:2.8rem; color:#c2185b;
                   text-shadow: 3px 3px 0 #ffb6c1; margin:0;'>
            統計大富翁
        </h1>
        <h2 style='font-family: "Fredoka One", cursive; font-size:1.8rem; color:#e91e63; margin:0.3rem 0 0.5rem;'>
            房價大作戰 🏡
        </h2>
        <p style='color:#888; font-size:0.95rem; max-width:500px; margin:0 auto;'>
            結合統計概念與台灣房市的趣味大富翁遊戲！
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1,1])
    with col1:
        st.markdown("""
        <div class='card'>
        <h3 style='color:#c2185b; margin-top:0;'>🐾 四位玩家</h3>
        <p>🐷 玩家1 豬 &nbsp;|&nbsp; 🐱 玩家2 貓<br>
           🐶 玩家3 狗 &nbsp;|&nbsp; 🐰 玩家4 兔</p>
        <p>初始資金：<strong>3,000 萬</strong></p>
        </div>
        <div class='card'>
        <h3 style='color:#7b1fa2; margin-top:0;'>📐 統計任務</h3>
        <p>停留在行政區格時需回答統計問題（平均數、中位數），
        答對才能購買地產！</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='card'>
        <h3 style='color:#e65100; margin-top:0;'>🃏 機會 ＆ 命運</h3>
        <p>機會卡帶來好運，命運卡帶來挑戰！<br>
        共 8 張精心設計的卡片。</p>
        </div>
        <div class='card'>
        <h3 style='color:#1565c0; margin-top:0;'>💼 特殊格子</h3>
        <p>🔒 監獄：暫停一回合<br>
        💸 國稅局：繳稅 300 萬<br>
        🏁 出發點：經過獲得 200 萬</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='text-align:center; margin: 1.2rem 0;'>", unsafe_allow_html=True)
    if st.button("🎮  開始遊戲  🎮", key="start_btn", use_container_width=False):
        st.session_state.game_started = True
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align:center; margin-top:2rem; padding:0.8rem;
                background:linear-gradient(135deg,#fff0f5,#f3e5f5);
                border-radius:16px; border:2px solid #ce93d8;'>
        <p style='margin:0; color:#6a1b9a; font-size:0.88rem;'>
        👩‍💻 <strong>開發者資訊 ─ 第 6 組</strong><br>
        413670371 許瑾瑄 ・ 413570098 林庭安 ・ 413570141 胡馨文 ・ 41357015 林育穎
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ─── GAME OVER ────────────────────────────────────────────────────────────────
if st.session_state.game_over:
    w = st.session_state.winner
    st.markdown(f"""
    <div style='text-align:center; padding:3rem 1rem;'>
        <div style='font-size:5rem'>{w['emoji']}</div>
        <h1 style='font-family:"Fredoka One",cursive; color:#c2185b; font-size:3rem;'>
            🏆 {w['name']} 獲勝！🏆
        </h1>
        <p style='font-size:1.3rem; color:#555;'>最終資產：<strong>{fmt(w['money'])} 萬</strong></p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("🔄 重新開始"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.stop()

# ─── MAIN GAME LAYOUT ─────────────────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; padding:0.5rem 0;'>
    <h1 style='font-family:"Fredoka One",cursive; color:#c2185b; font-size:2rem; margin:0;'>
        🏠 統計大富翁：房價大作戰 🎲
    </h1>
</div>
""", unsafe_allow_html=True)

left, mid, right = st.columns([1.3, 2.2, 1.3])

# ─── LEFT: Player info ────────────────────────────────────────────────────────
with left:
    st.markdown("<h3 style='color:#c2185b; text-align:center;'>🐾 玩家狀態</h3>", unsafe_allow_html=True)
    for i, p in enumerate(st.session_state.players):
        active = (i == st.session_state.current_player and st.session_state.phase == "roll")
        status = "active" if active else ""
        alive_style = "opacity:0.4;" if not p["alive"] else ""
        props_html = " ".join([f"<span class='property-tag'>{pr}</span>" for pr in p["properties"]]) or "<span style='color:#ccc;font-size:0.75rem;'>尚無地產</span>"
        turn_arrow = "👈 輪到你！" if active else ""
        st.markdown(f"""
        <div class='player-card {status}' style='{alive_style}'>
            <div style='font-size:1.6rem'>{p['emoji']}</div>
            <div style='font-weight:800; color:{p['color']}; font-size:0.95rem;'>{p['name']}</div>
            <div style='color:#333; font-size:0.9rem;'>💰 <strong>{fmt(p['money'])}</strong> 萬</div>
            <div style='margin-top:0.3rem;'>{props_html}</div>
            {'<div style="color:#ff6b9d; font-size:0.8rem; font-weight:800;">'+turn_arrow+'</div>' if turn_arrow else ''}
        </div>
        """, unsafe_allow_html=True)

# ─── MIDDLE: Board + action ────────────────────────────────────────────────────
with mid:
    # Mini board map
    st.markdown("<h3 style='color:#c2185b; text-align:center;'>🗺️ 遊戲地圖</h3>", unsafe_allow_html=True)

    cell_colors = {
        "go": "#e8f5e9", "district": "#fff0f5", "chance": "#fff9c4",
        "fate": "#f3e5f5", "tax": "#fbe9e7", "jail": "#e8eaf6"
    }
    border_colors = {
        "go": "#43a047", "district": "#ffb6c1", "chance": "#fbc02d",
        "fate": "#ab47bc", "tax": "#ff5722", "jail": "#5c6bc0"
    }

    # Positions of all players on board
    pos_map = {}
    for i, p in enumerate(st.session_state.players):
        if p["alive"]:
            pos_map.setdefault(p["pos"], []).append(p["emoji"])

    # Draw board as 4 rows x 5 cols
    rows = [BOARD[0:5], BOARD[5:10], BOARD[10:15], BOARD[15:20]]
    for row_idx, row in enumerate(rows):
        cols = st.columns(5)
        for col_idx, cell in enumerate(row):
            board_idx = row_idx * 5 + col_idx
            tokens = "".join(pos_map.get(board_idx, []))
            bg = cell_colors.get(cell["type"], "#fff")
            bd = border_colors.get(cell["type"], "#ddd")
            is_current = any(p["pos"] == board_idx and p["alive"] for p in st.session_state.players)
            glow = f"box-shadow: 0 0 0 3px #ff6b9d; transform:scale(1.06);" if is_current else ""
            # Owner indicator
            owner_dot = ""
            if cell["type"] == "district" and cell["key"]:
                for pi, p in enumerate(st.session_state.players):
                    if cell["key"] in p["properties"]:
                        owner_dot = f"<div style='font-size:0.6rem;color:{p['color']};'>●</div>"
            with cols[col_idx]:
                st.markdown(f"""
                <div style='background:{bg}; border:2px solid {bd}; border-radius:10px;
                            padding:0.25rem 0.1rem; text-align:center; font-size:0.68rem;
                            font-weight:700; min-height:56px; {glow}
                            display:flex; flex-direction:column; align-items:center; justify-content:center;'>
                    <div style='font-size:0.75rem;'>{cell['label']}</div>
                    {owner_dot}
                    <div style='font-size:1.1rem;'>{tokens}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("---")

    # ── Action area ──────────────────────────────────────────────────────────
    cp = current()
    st.markdown(f"<h4 style='text-align:center; color:{cp['color']};'>{cp['emoji']} {cp['name']} 的回合</h4>", unsafe_allow_html=True)

    if st.session_state.message:
        st.markdown(f"<div class='msg-box'>{st.session_state.message}</div>", unsafe_allow_html=True)

    phase = st.session_state.phase

    # ── ROLL ─────────────────────────────────────────────────────────────────
    if phase == "roll":
        if cp["jail"] > 0:
            st.markdown(f"<div class='msg-box'>🔒 {cp['emoji']} 在監獄中，還剩 {cp['jail']} 回合。自動跳過。</div>", unsafe_allow_html=True)
            if st.button("⏭️ 跳過回合"):
                cp["jail"] -= 1
                st.session_state.current_player = next_alive()
                st.session_state.message = ""
                st.session_state.phase = "roll"
                st.rerun()
        else:
            c1, c2 = st.columns(2)
            with c1:
                if st.button("🎲 擲骰子！", use_container_width=True):
                    d = random.randint(1, 6)
                    st.session_state.last_dice = d
                    old_pos = cp["pos"]
                    new_pos = (old_pos + d) % BOARD_SIZE
                    # Passed Go?
                    if new_pos < old_pos:
                        cp["money"] += 200
                        st.session_state.message = f"🏁 經過出發點，獲得 200 萬！"
                    else:
                        st.session_state.message = ""
                    cp["pos"] = new_pos
                    cell = BOARD[new_pos]
                    # Handle special cells immediately
                    if cell["type"] == "go":
                        cp["money"] += 200
                        st.session_state.message = "🏁 停在出發點，額外獲得 200 萬！"
                        st.session_state.phase = "end_turn"
                    elif cell["type"] == "jail":
                        cp["jail"] = 2
                        st.session_state.message = f"🔒 {cp['emoji']} 進監獄！暫停 2 回合。"
                        st.session_state.phase = "end_turn"
                    elif cell["type"] == "tax":
                        pay(cp, 300)
                        st.session_state.message = f"💸 {cp['emoji']} 繳國稅 300 萬！"
                        st.session_state.phase = "end_turn"
                    elif cell["type"] == "chance":
                        card = random.choice(CHANCE_CARDS)
                        st.session_state.active_card = ("chance", card)
                        st.session_state.phase = "card"
                    elif cell["type"] == "fate":
                        card = random.choice(FATE_CARDS)
                        st.session_state.active_card = ("fate", card)
                        st.session_state.phase = "card"
                    elif cell["type"] == "district":
                        dist_name = cell["key"]
                        # Check if owned by another player
                        owner = None
                        for pi, p in enumerate(st.session_state.players):
                            if dist_name in p["properties"] and p is not cp:
                                owner = p
                                break
                        if owner:
                            rent = DISTRICTS[dist_name]["price"] // 4
                            pay(cp, rent)
                            owner["money"] += rent
                            st.session_state.message = f"🏠 {dist_name} 屬於 {owner['emoji']}！支付租金 {fmt(rent)} 萬。"
                            st.session_state.phase = "end_turn"
                        elif dist_name in cp["properties"]:
                            st.session_state.message = f"🏠 這是你自己的地產：{dist_name}！"
                            st.session_state.phase = "end_turn"
                        else:
                            st.session_state.active_district = dist_name
                            st.session_state.task_solved = False
                            st.session_state.answer_submitted = False
                            st.session_state.double_task = st.session_state.double_task  # keep flag
                            st.session_state.phase = "task"
                    st.rerun()
            with c2:
                if st.session_state.last_dice:
                    st.markdown(f"<div class='dice-face'>{DICE_FACES[st.session_state.last_dice]}</div>", unsafe_allow_html=True)

    # ── CARD ─────────────────────────────────────────────────────────────────
    elif phase == "card":
        ctype, card = st.session_state.active_card
        if ctype == "chance":
            st.markdown(f"""
            <div class='chance-card'>
                <div style='font-size:2rem;'>🃏</div>
                <h3 style='color:#e65100; margin:0.3rem 0;'>機會卡：{card['title']}</h3>
                <p style='margin:0;'>{card['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='fate-card'>
                <div style='font-size:2rem;'>🎴</div>
                <h3 style='color:#6a1b9a; margin:0.3rem 0;'>命運卡：{card['title']}</h3>
                <p style='margin:0;'>{card['desc']}</p>
            </div>
            """, unsafe_allow_html=True)
        if st.button("✅ 確認並執行"):
            apply_card(card, cp)
            st.session_state.active_card = None
            st.session_state.phase = "end_turn"
            check_game_over()
            st.rerun()

    # ── TASK ─────────────────────────────────────────────────────────────────
    elif phase == "task":
        dn = st.session_state.active_district
        d = DISTRICTS[dn]
        double = st.session_state.double_task

        st.markdown(f"""
        <div class='card' style='border-color:{d['color']};'>
            <h3 style='color:{d['color']}; margin-top:0;'>📐 {dn} 統計任務</h3>
            <p>房價資料（萬/坪）：<strong>{d['data']}</strong></p>
            <p>任務：<strong>{d['task']}</strong>{'<br>⚠️ 難度加倍！同時需計算平均數與中位數' if double else ''}</p>
            <p>地產售價：<strong>{fmt(d['price'])} 萬</strong></p>
        </div>
        """, unsafe_allow_html=True)

        ans_str = st.text_input("請輸入答案（數字）：", key="task_ans", placeholder=f"例：{d['answer']}")

        hint_cols = st.columns(2)
        with hint_cols[0]:
            st.markdown(f"""
            <div style='background:#f5f5f5; border-radius:10px; padding:0.5rem;
                        font-size:0.8rem; color:#555;'>
            💡 提示：<br>
            平均數 = 總和 ÷ 個數<br>
            中位數 = 排序後中間值
            </div>
            """, unsafe_allow_html=True)

        btn1, btn2 = st.columns(2)
        with btn1:
            if st.button("📝 提交答案"):
                try:
                    user_ans = float(ans_str.strip())
                    correct = abs(user_ans - d["answer"]) < 0.6
                    if correct:
                        st.session_state.task_solved = True
                        st.session_state.double_task = False
                        st.session_state.message = f"✅ 答對了！答案是 {d['answer']}。可以選擇購買地產！"
                        st.session_state.phase = "buy"
                    else:
                        st.session_state.message = f"❌ 答錯了！正確答案是 {d['answer']}。無法購買地產。"
                        st.session_state.double_task = False
                        st.session_state.phase = "end_turn"
                except:
                    st.session_state.message = "⚠️ 請輸入有效數字！"
                st.rerun()
        with btn2:
            if st.button("⏭️ 放棄任務"):
                st.session_state.double_task = False
                st.session_state.message = "😞 放棄任務，無法購買地產。"
                st.session_state.phase = "end_turn"
                st.rerun()

    # ── BUY ──────────────────────────────────────────────────────────────────
    elif phase == "buy":
        dn = st.session_state.active_district
        d = DISTRICTS[dn]
        disc = cp.get("discount", 1.0)
        price = int(d["price"] * disc)
        affordable = cp["money"] >= price

        st.markdown(f"""
        <div class='card'>
            <h3 style='color:#c2185b; margin-top:0;'>🏠 購買 {dn}？</h3>
            <p>售價：<strong>{fmt(price)} 萬</strong>{'（享 9 折優惠！）' if disc < 1 else ''}</p>
            <p>你的資金：<strong>{fmt(cp['money'])} 萬</strong></p>
            {'<p style="color:red;">⚠️ 資金不足！</p>' if not affordable else ''}
        </div>
        """, unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ 購買！", disabled=not affordable, use_container_width=True):
                cp["money"] -= price
                cp["properties"].append(dn)
                cp["discount"] = 1.0  # reset discount
                st.session_state.message = f"🎉 {cp['emoji']} 購入 {dn}！剩餘資金 {fmt(cp['money'])} 萬。"
                st.session_state.phase = "end_turn"
                st.session_state.active_district = None
                st.rerun()
        with c2:
            if st.button("❌ 不買", use_container_width=True):
                st.session_state.message = f"🤔 {cp['emoji']} 決定不購買 {dn}。"
                st.session_state.phase = "end_turn"
                st.session_state.active_district = None
                st.rerun()

    # ── END TURN ─────────────────────────────────────────────────────────────
    elif phase == "end_turn":
        check_bankruptcy(cp)
        check_game_over()
        if not st.session_state.game_over:
            if st.button("⏭️ 結束回合，換下一位玩家"):
                st.session_state.current_player = next_alive()
                st.session_state.phase = "roll"
                st.session_state.last_dice = None
                st.session_state.message = ""
                st.session_state.active_card = None
                st.session_state.active_district = None
                st.rerun()

# ─── RIGHT: Info panel ────────────────────────────────────────────────────────
with right:
    st.markdown("<h3 style='color:#c2185b; text-align:center;'>📊 地產總覽</h3>", unsafe_allow_html=True)
    for dn, d in DISTRICTS.items():
        owner_info = ""
        for p in st.session_state.players:
            if dn in p["properties"]:
                owner_info = f" {p['emoji']}"
                break
        color = d["color"]
        st.markdown(f"""
        <div style='background:white; border-left:4px solid {color}; border-radius:8px;
                    padding:0.4rem 0.6rem; margin-bottom:0.35rem; font-size:0.78rem;'>
            <span style='font-weight:800; color:{color};'>{dn}</span>
            {f'<span style="float:right;">{owner_info}</span>' if owner_info else ''}
            <br>
            <span style='color:#888;'>💰 {fmt(d["price"])} 萬</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<h3 style='color:#e65100; margin-top:1rem; text-align:center;'>🃏 圖例</h3>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.8rem; line-height:2;'>
    🏁 出發點：經過+200萬<br>
    🃏 機會：好事降臨<br>
    🎴 命運：挑戰來臨<br>
    💸 國稅局：繳稅300萬<br>
    🔒 監獄：暫停2回合<br>
    🏠 地產：答題才能買<br>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style='margin-top:1.5rem; padding:0.6rem;
                background:linear-gradient(135deg,#fff0f5,#f3e5f5);
                border-radius:12px; border:1.5px solid #ce93d8;
                font-size:0.72rem; text-align:center; color:#6a1b9a;'>
    <strong>第 6 組</strong><br>
    許瑾瑄 ・ 林庭安<br>
    胡馨文 ・ 林育穎
    </div>
    """, unsafe_allow_html=True)
