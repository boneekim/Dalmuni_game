import streamlit as st
import random
import time # time 모듈 추가
from itertools import combinations # combinations는 AI 로직 개선 후 제거 예정

st.set_page_config(layout="wide")

st.title("달무티 게임")

# --- 카드 정의 ---
CARDS = [
    {"id": 1, "rank": 1, "name": "달무티", "quantity": 1},
    {"id": 2, "rank": 2, "name": "대주교", "quantity": 2},
    {"id": 3, "rank": 3, "name": "총리", "quantity": 3},
    {"id": 4, "rank": 4, "name": "남작부인", "quantity": 4},
    {"id": 5, "rank": 5, "name": "기사", "quantity": 5},
    {"id": 6, "rank": 6, "name": "재봉사", "quantity": 6},
    {"id": 7, "rank": 7, "name": "석공", "quantity": 7},
    {"id": 8, "rank": 8, "name": "요리사", "quantity": 8},
    {"id": 9, "rank": 9, "name": "광부", "quantity": 9},
    {"id": 10, "rank": 10, "name": "농노", "quantity": 10},
    {"id": 11, "rank": 11, "name": "농노", "quantity": 11},
    {"id": 12, "rank": 12, "name": "농노", "quantity": 12},
    {"id": 13, "rank": 13, "name": "어릿광대", "quantity": 2}, # 조커
]

# --- 게임 상태 초기화 ---
if 'game_state' not in st.session_state:
    st.session_state.game_state = "setup" # setup, playing, finished
if 'players' not in st.session_state:
    st.session_state.players = []
if 'current_player_index' not in st.session_state:
    st.session_state.current_player_index = 0
if 'last_played' not in st.session_state:
    st.session_state.last_played = None
if 'passed_players' not in st.session_state:
    st.session_state.passed_players = set()
if 'last_player_who_played' not in st.session_state:
    st.session_state.last_player_who_played = None
if 'finished_players' not in st.session_state:
    st.session_state.finished_players = []
if 'is_revolution' not in st.session_state:
    st.session_state.is_revolution = False
if 'selected_card_indices' not in st.session_state:
    st.session_state.selected_card_indices = []

# --- 카드 이미지 생성 함수 ---
def create_card_image_html(card, is_back=False):
    if is_back:
        # 카드 뒷면 이미지 (파란색)
        svg_content = f"""
        <svg width="100" height="140" viewBox="0 0 100 140" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="100" height="140" rx="10" fill="#4169E1"/>
        <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial" font-size="40" fill="white">DAL</text>
        </svg>
        """
    else:
        # 카드 앞면 이미지 (랭크에 따라 색상 변경)
        colors = {
            1: "#FFD700", 2: "#C0C0C0", 3: "#CD7F32", 4: "#ADD8E6",
            5: "#90EE90", 6: "#FFB6C1", 7: "#DDA0DD", 8: "#FFDAB9",
            9: "#B0E0E6", 10: "#F0E68C", 11: "#F0E68C", 12: "#F0E68C",
            13: "#FF4500" # 조커
        }
        fill_color = colors.get(card["rank"], "#CCCCCC")
        text_color = "black" if card["rank"] != 13 else "white"
        display_text = "J" if card["rank"] == 13 else str(card["rank"])

        svg_content = f"""
        <svg width="100" height="140" viewBox="0 0 100 140" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect width="100" height="140" rx="10" fill="{fill_color}"/>
        <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-family="Arial" font-size="60" fill="{text_color}">{display_text}</text>
        </svg>
        """
    
    return svg_content

# --- 게임 로직 함수 ---
def initialize_game(player_count, difficulty):
    deck = []
    for card_info in CARDS:
        for _ in range(card_info["quantity"]):
            deck.append({"id": card_info["id"], "rank": card_info["rank"], "name": card_info["name"]})
    random.shuffle(deck)

    players = []
    for i in range(player_count):
        players.append({
            "id": f"player-{i}",
            "name": "나" if i == 0 else f"AI {i}",
            "hand": [],
            "is_ai": i != 0,
            "rank": None
        })

    player_index = 0
    for card in deck:
        players[player_index]["hand"].append(card)
        player_index = (player_index + 1) % player_count

    for player in players:
        player["hand"].sort(key=lambda x: x["rank"])

    # 세금 시스템 (간단화)
    dalmuti_player = next((p for p in players if any(card["rank"] == 1 for card in p["hand"])), None)
    peasant_player = next((p for p in players if any(card["rank"] == 12 for card in p["hand"])), None)

    if dalmuti_player and peasant_player:
        # 농노는 달무티에게 가장 낮은 등급의 카드 2장을 줍니다.
        peasant_low_cards = peasant_player["hand"][:2]
        peasant_player["hand"] = peasant_player["hand"][2:]
        dalmuti_player["hand"].extend(peasant_low_cards)

        # 달무티는 농노에게 가장 높은 등급의 카드 2장을 받습니다.
        dalmuti_high_cards = dalmuti_player["hand"][-2:]
        dalmuti_player["hand"] = dalmuti_player["hand"][:-2]
        peasant_player["hand"].extend(dalmuti_high_cards)

        dalmuti_player["hand"].sort(key=lambda x: x["rank"])
        peasant_player["hand"].sort(key=lambda x: x["rank"])

    st.session_state.players = players
    st.session_state.current_player_index = next((i for i, p in enumerate(players) if any(card["rank"] == 1 for card in p["hand"])), 0)
    st.session_state.game_state = "playing"
    st.session_state.last_played = None
    st.session_state.passed_players = set()
    st.session_state.last_player_who_played = None
    st.session_state.finished_players = []
    st.session_state.is_revolution = False
    st.session_state.selected_card_indices = []

def validate_play(selected_cards):
    if not selected_cards: return False

    first_card_rank = selected_cards[0]["rank"]
    all_same_rank = all(card["rank"] == first_card_rank or card["rank"] == 13 for card in selected_cards)
    if not all_same_rank: return False

    if st.session_state.passed_players and len(st.session_state.passed_players) == len(st.session_state.players) - len(st.session_state.finished_players) - 1:
        return True # 모두 패스했으면 아무거나 낼 수 있음

    if st.session_state.last_played:
        if len(selected_cards) != len(st.session_state.last_played): return False
        
        if st.session_state.is_revolution:
            if selected_cards[0]["rank"] < st.session_state.last_played[0]["rank"]: return False
        else:
            if selected_cards[0]["rank"] >= st.session_state.last_played[0]["rank"]: return False

    return True

def next_turn():
    next_idx = (st.session_state.current_player_index + 1) % len(st.session_state.players)
    while st.session_state.players[next_idx]["rank"] is not None: # 이미 끝난 플레이어는 건너뛰기
        next_idx = (next_idx + 1) % len(st.session_state.players)
    st.session_state.current_player_index = next_idx

def play_turn(selected_card_indices):
    current_player = st.session_state.players[st.session_state.current_player_index]
    selected_cards = [current_player["hand"][i] for i in selected_card_indices]
    selected_cards.sort(key=lambda x: x["rank"])

    if not validate_play(selected_cards):
        st.warning("낼 수 없는 카드입니다.")
        return

    # 카드 제거
    current_player["hand"] = [card for i, card in enumerate(current_player["hand"]) if i not in selected_card_indices]
    st.session_state.last_played = selected_cards
    st.session_state.passed_players = set()
    st.session_state.last_player_who_played = st.session_state.current_player_index

    if not current_player["hand"] and current_player not in st.session_state.finished_players:
        current_player["rank"] = len(st.session_state.finished_players) + 1
        st.session_state.finished_players.append(current_player)

    # 혁명/반란 토글
    if len(selected_cards) == 2 and selected_cards[0]["rank"] == selected_cards[1]["rank"]:
        st.session_state.is_revolution = not st.session_state.is_revolution

    if len(st.session_state.finished_players) == len(st.session_state.players) - 1:
        # 마지막 남은 플레이어의 순위 결정
        last_player = next((p for p in st.session_state.players if p["rank"] is None), None)
        if last_player:
            last_player["rank"] = len(st.session_state.players)
            st.session_state.finished_players.append(last_player)
        st.session_state.game_state = "finished"
    else:
        next_turn()

def pass_turn():
    st.session_state.passed_players.add(st.session_state.current_player_index)

    if len(st.session_state.passed_players) == len(st.session_state.players) - len(st.session_state.finished_players) - 1:
        # 모두 패스함
        st.session_state.last_played = None
        st.session_state.passed_players = set()
        if st.session_state.last_player_who_played is not None:
            st.session_state.current_player_index = st.session_state.last_player_who_played
        else:
            next_turn()
    else:
        next_turn()

def ai_play_turn():
    current_player = st.session_state.players[st.session_state.current_player_index]
    
    # AI 로직 (간단화: 낼 수 있는 첫 번째 유효한 조합을 찾아서 냄)
    possible_plays = []
    # 모든 카드 조합을 시도 (매우 비효율적이지만 예시를 위해)
    from itertools import combinations
    for i in range(1, len(current_player["hand"]) + 1):
        for combo in combinations(current_player["hand"], i):
            if validate_play(list(combo)):
                possible_plays.append(list(combo))
    
    if possible_plays:
        # 가장 낮은 등급(rank가 높은)의 카드 조합을 선택 (간단한 AI)
        play = sorted(possible_plays, key=lambda x: x[0]["rank"], reverse=True)[0]
        selected_card_indices = [current_player["hand"].index(card) for card in play]
        play_turn(selected_card_indices)
    else:
        pass_turn()

# --- UI 렌더링 --- 
# 전역 CSS 스타일
st.markdown(
    """
    <style>
    /* 전체 배경색 및 폰트 */
    body {
        background-color: #1a1a1a; /* 어두운 배경 */
        color: #f0f0f0; /* 밝은 텍스트 */
        font-family: 'Arial', sans-serif;
    }
    /* Streamlit 기본 위젯 스타일 오버라이드 */
    .stApp {
        background-color: #1a1a1a;
    }
    .stButton>button {
        background-color: #4CAF50; /* 녹색 버튼 */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stButton>button:disabled {
        background-color: #cccccc;
        cursor: not-allowed;
    }
    .stSlider .stSliderHandle {
        background-color: #4CAF50;
    }
    .stRadio > label > div {
        color: #f0f0f0;
    }
    /* 카드 컨테이너 스타일 */
    .card-container {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin-top: 20px;
    }
    /* 카드 자체 스타일 */
    .card-item {
        border: 1px solid #555;
        border-radius: 10px;
        box-shadow: 3px 3px 8px rgba(0,0,0,0.5);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        cursor: pointer;
    }
    .card-item:hover {
        transform: translateY(-5px);
        box-shadow: 5px 5px 12px rgba(0,0,0,0.7);
    }
    .card-item.selected {
        border: 3px solid #61dafb; /* 선택된 카드 테두리 */
        transform: translateY(-15px); /* 선택 시 더 많이 올라오도록 */
        box-shadow: 5px 5px 15px rgba(97, 218, 251, 0.8); /* 선택 시 그림자 강조 */
    }
    /* 중앙 낸 카드 스타일 */
    .played-cards-container {
        min-height: 160px;
        border: 2px dashed #555;
        border-radius: 15px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
        padding: 10px;
        margin-bottom: 20px;
        background-color: #2a2a2a;
    }
    /* 플레이어 정보 스타일 */
    .player-info {
        border: 1px solid #777;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        background-color: #3a3a3a;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    .player-info.current-turn {
        border-color: #61dafb;
        box-shadow: 0 0 15px rgba(97, 218, 251, 0.8);
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 15px rgba(97, 218, 251, 0.8); }
        50% { box-shadow: 0 0 25px rgba(97, 218, 251, 1); }
        100% { box-shadow: 0 0 15px rgba(97, 218, 251, 0.8); }
    }
    /* 저작권 푸터 */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #1a1a1a;
        color: #777;
        text-align: right;
        padding: 10px;
        font-size: 0.8em;
        z-index: 1000;
    }

    /* Streamlit 체크박스 커스텀 스타일 */
    .stCheckbox > label {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 0;
        margin: 0;
        cursor: pointer;
        width: 100px; /* 카드 너비 */
        height: 140px; /* 카드 높이 */
        border: 1px solid #555;
        border-radius: 10px;
        box-shadow: 3px 3px 8px rgba(0,0,0,0.5);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border 0.2s ease;
    }
    .stCheckbox > label:hover {
        transform: translateY(-5px);
        box-shadow: 5px 5px 12px rgba(0,0,0,0.7);
    }
    .stCheckbox > label > div:first-child { /* 체크박스 아이콘 숨기기 */
        display: none;
    }
    .stCheckbox > label > div:last-child { /* 라벨 텍스트 (SVG) */
        padding: 0;
        margin: 0;
        width: 100%;
        height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .stCheckbox input[type="checkbox"]:checked + div > div:last-child > div > svg {
        border: 3px solid #61dafb; /* 선택된 카드 테두리 */
        transform: translateY(-15px); /* 선택 시 더 많이 올라오도록 */
        box-shadow: 5px 5px 15px rgba(97, 218, 251, 0.8); /* 선택 시 그림자 강조 */
    }
    </style>
    """
    , unsafe_allow_html=True
)

if st.session_state.game_state == "setup":
    st.header("게임 설정")
    player_count = st.slider("플레이어 수 (AI 포함)", 2, 8, 3)
    difficulty = st.radio("AI 난이도", ("하", "중", "상"), index=1)

    if st.button("게임 시작", use_container_width=True):
        initialize_game(player_count, difficulty)
        st.rerun()

elif st.session_state.game_state == "playing":
    st.header("게임 진행 중")

    # AI 턴 처리
    current_player = st.session_state.players[st.session_state.current_player_index]
    if current_player["is_ai"]:
        st.info(f"{current_player["name"]}의 턴입니다...")
        time.sleep(1) # AI 턴 딜레이
        ai_play_turn()
        st.rerun() # AI 턴 처리 후 재실행

    # 상단 플레이어 정보
    other_players_container = st.container() # st.container()로 감싸서 독립적인 공간 확보
    with other_players_container:
        cols = st.columns(len(st.session_state.players))
        for i, player in enumerate(st.session_state.players):
            with cols[i]:
                is_current = (i == st.session_state.current_player_index)
                player_class = "player-info current-turn" if is_current else "player-info"
                st.markdown(f"<div class='{player_class}'>", unsafe_allow_html=True)
                st.write(f"**{player['name']}**")
                if player["id"] != next((p for p in st.session_state.players if not p["is_ai"]), None)["id"]:
                    st.markdown(create_card_image_html(None, is_back=True), unsafe_allow_html=True)
                    st.write(f"{len(player['hand'])}장")
                else:
                    st.write(f"{len(player['hand'])}장 (내 카드)")
                st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-top: 1px solid #444; margin: 20px 0;'>", unsafe_allow_html=True) # 구분선

    # 중앙에 낸 카드
    st.subheader("중앙에 낸 카드")
    played_cards_container = st.container()
    with played_cards_container:
        st.markdown("<div class='played-cards-container'>", unsafe_allow_html=True)
        if st.session_state.last_played:
            for card in st.session_state.last_played:
                st.markdown(create_card_image_html(card), unsafe_allow_html=True)
        else:
            st.write("아직 낸 카드가 없습니다.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-top: 1px solid #444; margin: 20px 0;'>", unsafe_allow_html=True) # 구분선

    # 내 손패
    st.subheader("내 손패")
    human_player = next((p for p in st.session_state.players if not p["is_ai"]), None)
    if human_player:
        hand_container = st.container()
        with hand_container:
            st.markdown("<div class='card-container'>", unsafe_allow_html=True)
            for i, card in enumerate(human_player["hand"]):
                # Streamlit 체크박스로 카드 선택 구현
                # 체크박스의 라벨에 카드 이미지를 넣고, 체크박스 자체는 CSS로 숨김
                checked = st.checkbox(
                    create_card_image_html(card), 
                    value=i in st.session_state.selected_card_indices, 
                    key=f"card_checkbox_{id(card)}", 
                    help=card["name"], 
                    label_visibility="hidden"
                )
                if checked and i not in st.session_state.selected_card_indices:
                    st.session_state.selected_card_indices.append(i)
                    st.rerun()
                elif not checked and i in st.session_state.selected_card_indices:
                    st.session_state.selected_card_indices.remove(i)
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        # 액션 버튼
        action_cols = st.columns(2)
        with action_cols[0]:
            if st.button("내기", disabled=not st.session_state.selected_card_indices or st.session_state.current_player_index != st.session_state.players.index(human_player), use_container_width=True):
                play_turn(st.session_state.selected_card_indices)
                st.session_state.selected_card_indices = [] # 선택 초기화
                st.rerun()
        with action_cols[1]:
            if st.button("패스", disabled=st.session_state.current_player_index != st.session_state.players.index(human_player), use_container_width=True):
                pass_turn()
                st.session_state.selected_card_indices = [] # 선택 초기화
                st.rerun()

elif st.session_state.game_state == "finished":
    st.header("게임 종료!")
    st.subheader("최종 순위")
    sorted_finished_players = sorted(st.session_state.finished_players, key=lambda x: x["rank"])
    for player in sorted_finished_players:
        st.write(f"{player["rank"]}등: {player["name"]}")

    if st.button("새 게임 시작", use_container_width=True):
        st.session_state.clear()
        st.rerun()

# --- 저작권 문구 ---
st.markdown(
    """
    <div class="footer">
        © 2025 BnK. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)
