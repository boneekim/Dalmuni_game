import streamlit as st
import random

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
        st.experimental_rerun()

elif st.session_state.game_state == "playing":
    st.header("게임 진행 중")

    # AI 턴 처리
    current_player = st.session_state.players[st.session_state.current_player_index]
    if current_player["is_ai"]:
        st.write(f"{current_player["name"]}의 턴입니다...")
        st.session_state.ai_turn_active = True
        # AI 턴은 자동으로 진행되도록 함
        ai_play_turn()
        st.session_state.ai_turn_active = False
        st.experimental_rerun()

    st.write(f"현재 턴: {st.session_state.players[st.session_state.current_player_index]["name"]}")
    if st.session_state.is_revolution:
        st.warning("혁명 상태입니다! 높은 숫자가 강한 카드입니다.")

    st.subheader("중앙에 낸 카드")
    if st.session_state.last_played:
        cols = st.columns(len(st.session_state.last_played))
        for i, card in enumerate(st.session_state.last_played):
            with cols[i]:
                st.image(f"https://via.placeholder.com/100x140?text={card["rank"]}", caption=card["name"], width=100)
    else:
        st.write("아직 낸 카드가 없습니다.")

    st.subheader("내 손패")
    human_player = next((p for p in st.session_state.players if not p["is_ai"]), None)
    if human_player:
        selected_cards = st.multiselect(
            "낼 카드를 선택하세요:",
            options=[f"{card["name"]} ({card["rank"]})" for card in human_player["hand"]],
            format_func=lambda x: x.split(" (")[0] # 이름만 표시
        )
        selected_card_indices = [human_player["hand"].index(next(c for c in human_player["hand"] if f"{c["name"]} ({c["rank"]})" == sc)) for sc in selected_cards]

        col1, col2 = st.columns(2)
        with col1:
            if st.button("내기", disabled=not selected_cards):
                play_turn(selected_card_indices)
                st.experimental_rerun()
        with col2:
            if st.button("패스"):
                pass_turn()
                st.experimental_rerun()

    st.subheader("다른 플레이어")
    for player in st.session_state.players:
        if player["id"] != human_player["id"]:
            st.write(f"{player["name"]}: {len(player["hand"])}장")

elif st.session_state.game_state == "finished":
    st.header("게임 종료!")
    st.subheader("최종 순위")
    sorted_finished_players = sorted(st.session_state.finished_players, key=lambda x: x["rank"])
    for player in sorted_finished_players:
        st.write(f"{player["rank"]}등: {player["name"]}")

    if st.button("새 게임 시작"):
        st.session_state.clear()
        st.experimental_rerun()

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
