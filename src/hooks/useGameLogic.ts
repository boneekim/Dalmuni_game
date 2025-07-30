
import { useState, useEffect, useCallback } from 'react';
import { Game, Player } from '../types';
import { GameSettings, GameState } from '../App';
import { CARDS, CardData } from '../constants/cards';

const useGameLogic = (settings: GameSettings | null, setGameState: (state: GameState) => void) => {
  const [game, setGame] = useState<Game | null>(null);

  const initializeGame = useCallback((settings: GameSettings) => {
    // ... (이전과 동일)
  }, []);

  useEffect(() => {
    if (settings) {
      initializeGame(settings);
    }
  }, [settings, initializeGame]);

  const aiPlayTurn = useCallback(() => {
    if (!game || !game.players[game.currentPlayerIndex].isAI) return;

    // AI 로직 (간소화)
    // 낼 수 있는 가장 약한 카드를 찾아서 냄
    const currentPlayer = game.players[game.currentPlayerIndex];
    const possiblePlays = findAllPossiblePlays(currentPlayer.hand, game.lastPlayed);

    if (possiblePlays.length > 0) {
      // 가장 약한 카드(rank가 높은) 조합을 선택
      const bestPlay = possiblePlays[possiblePlays.length - 1];
      const indices = bestPlay.map(card => currentPlayer.hand.indexOf(card));
      playTurn(indices);
    } else {
      passTurn();
    }
  }, [game]);

  useEffect(() => {
    if (game && game.players[game.currentPlayerIndex]?.isAI) {
      const timeoutId = setTimeout(aiPlayTurn, 1000);
      return () => clearTimeout(timeoutId);
    }
  }, [game?.currentPlayerIndex, aiPlayTurn]);

  const playTurn = (cardIndices: number[]) => {
    // ... (이전 로직과 유사)
    // 카드 낸 후, 손패가 0이 된 플레이어 순위 기록
    const currentPlayer = game!.players[game!.currentPlayerIndex];
    if (newHand.length === 0 && !game!.finishedPlayers.some(p => p.id === currentPlayer.id)) {
      const finishedPlayer = { ...currentPlayer, rank: game!.finishedPlayers.length + 1 };
      newFinishedPlayers.push(finishedPlayer);
    }
    // ...
    // 게임 종료 조건 확인
    if (newFinishedPlayers.length >= game!.players.length - 1) {
      setGameState('finished');
    }
  };

  const passTurn = () => {
    // ... (이전과 동일)
  };

  // ... (validatePlay, findAllPossiblePlays 등 헬퍼 함수)

  return { game, playTurn, passTurn };
};

// 헬퍼 함수 예시 (실제로는 더 복잡함)
const findAllPossiblePlays = (hand: CardData[], lastPlayed: CardData[] | null): CardData[][] => {
  // ...
  return [];
}

export default useGameLogic;
