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
def create_card_image_html(card, is_selected=False, is_back=False):
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
    
    border_style = "2px solid #61dafb" if is_selected else "1px solid #ccc"
    transform_style = "translateY(-10px)" if is_selected else "none"

    return f"""
    <div style="border: {border_style}; border-radius: 10px; transform: {transform_style}; transition: transform 0.2s, border 0.2s; display: inline-block;">
        {svg_content}
    </div>
    """

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
if st.session_state.game_state == "setup":
    st.header("게임 설정")
    # 플레이어 수 기본값 변경: 2명부터, 디폴트 3명
    player_count = st.slider("플레이어 수 (AI 포함)", 2, 8, 3)
    # AI 난이도 기본값 변경: "중"으로 디폴트
    difficulty = st.radio("AI 난이도", ("하", "중", "상"), index=1)

    if st.button("게임 시작"):
        initialize_game(player_count, difficulty)
        st.rerun()

elif st.session_state.game_state == "playing":
    st.header("게임 진행 중")

    # AI 턴 처리
    current_player = st.session_state.players[st.session_state.current_player_index]
    if current_player["is_ai"]:
        st.write(f"{current_player["name"]}의 턴입니다...")
        time.sleep(1) # AI 턴 딜레이
        ai_play_turn()
        # st.rerun() # AI 턴 처리 후 중복 호출 제거

    st.write(f"현재 턴: {st.session_state.players[st.session_state.current_player_index]["name"]}")
    if st.session_state.is_revolution:
        st.warning("혁명 상태입니다! 높은 숫자가 강한 카드입니다.")

    st.subheader("중앙에 낸 카드")
    if st.session_state.last_played:
        cols = st.columns(len(st.session_state.last_played))
        for i, card in enumerate(st.session_state.last_played):
            with cols[i]:
                st.markdown(create_card_image_html(card), unsafe_allow_html=True)
    else:
        st.write("아직 낸 카드가 없습니다.")

    st.subheader("내 손패")
    human_player = next((p for p in st.session_state.players if not p["is_ai"]), None)
    if human_player:
        # 카드 선택 UI 개선
        hand_cols = st.columns(len(human_player["hand"]))
        for i, card in enumerate(human_player["hand"]):
            with hand_cols[i]:
                is_selected = i in st.session_state.selected_card_indices
                card_html = create_card_image_html(card, is_selected=is_selected)
                # 버튼을 카드 이미지 위에 겹쳐서 클릭 영역으로 사용
                # Streamlit의 버튼은 클릭 시 페이지를 재실행하므로, 버튼을 누르면 선택 상태가 토글되고 페이지가 새로고침됨
                if st.button(f"card_{id(card)}", help=card["name"], use_container_width=True):
                    if is_selected:
                        st.session_state.selected_card_indices.remove(i)
                    else:
                        st.session_state.selected_card_indices.append(i)
                    st.rerun()
                st.markdown(card_html, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("내기", disabled=not st.session_state.selected_card_indices):
                play_turn(st.session_state.selected_card_indices)
                st.session_state.selected_card_indices = [] # 선택 초기화
                st.rerun()
        with col2:
            if st.button("패스"):
                pass_turn()
                st.session_state.selected_card_indices = [] # 선택 초기화
                st.rerun()

    st.subheader("다른 플레이어")
    other_players_cols = st.columns(len(st.session_state.players) - 1)
    other_player_idx = 0
    for player in st.session_state.players:
        if player["id"] != human_player["id"]:
            with other_players_cols[other_player_idx]:
                st.write(f"{player["name"]}")
                st.markdown(create_card_image_html(None, is_back=True), unsafe_allow_html=True) # 카드 뒷면
                st.write(f"{len(player["hand"])}장")
            other_player_idx += 1

elif st.session_state.game_state == "finished":
    st.header("게임 종료!")
    st.subheader("최종 순위")
    sorted_finished_players = sorted(st.session_state.finished_players, key=lambda x: x["rank"])
    for player in sorted_finished_players:
        st.write(f"{player["rank"]}등: {player["name"]}")

    if st.button("새 게임 시작"):
        st.session_state.clear()
        st.rerun()

# --- 저작권 문구 ---
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #282c34; /* 배경색과 맞춤 */
        color: white;
        text-align: right;
        padding: 10px;
        font-size: 0.8em;
    }
    </style>
    <div class="footer">
        © 2025 BnK. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)