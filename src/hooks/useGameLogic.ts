import { useState, useEffect, useCallback } from 'react';
import type { Game, Player } from '../types';
import type { GameSettings, GameState } from '../App';
import type { CardData } from '../constants/cards';
import { CARDS } from '../constants/cards';

const useGameLogic = (settings: GameSettings | null, setGameState: (state: GameState) => void) => {
  const [game, setGame] = useState<Game | null>(null);

  const initializeGame = useCallback((settings: GameSettings) => {
    const deck = CARDS.flatMap(card => Array(card.quantity).fill(card));
    for (let i = deck.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [deck[i], deck[j]] = [deck[j], deck[i]];
    }

    const players: Player[] = Array.from({ length: settings.playerCount }, (_, i) => ({
      id: `player-${i}`,
      name: i === 0 ? '나' : `AI ${i}`,
      hand: [],
      isAI: i !== 0,
      rank: null,
    }));

    let playerIndex = 0;
    deck.forEach(card => {
      players[playerIndex].hand.push(card);
      playerIndex = (playerIndex + 1) % settings.playerCount;
    });

    players.forEach(player => {
      player.hand.sort((a, b) => a.rank - b.rank);
    });

    // 세금 시스템 구현
    const dalmutiPlayer = players.find(p => p.hand.some(card => card.rank === 1));
    const peasantPlayer = players.find(p => p.hand.some(card => card.rank === 12));

    if (dalmutiPlayer && peasantPlayer) {
      const peasantLowCards = peasantPlayer.hand.slice(0, 2);
      peasantPlayer.hand = peasantPlayer.hand.slice(2);
      dalmutiPlayer.hand.push(...peasantLowCards);

      const dalmutiHighCards = dalmutiPlayer.hand.slice(-2);
      dalmutiPlayer.hand = dalmutiPlayer.hand.slice(0, -2);
      peasantPlayer.hand.push(...dalmutiHighCards);

      dalmutiPlayer.hand.sort((a, b) => a.rank - b.rank);
      peasantPlayer.hand.sort((a, b) => a.rank - b.rank);
    }

    const startingPlayerIndex = players.findIndex(p => p.hand.some(c => c.rank === 1));

    setGame({
      players,
      currentPlayerIndex: startingPlayerIndex !== -1 ? startingPlayerIndex : 0,
      lastPlayed: null,
      turnHistory: [],
      passedPlayers: new Set(),
      lastPlayerWhoPlayed: null,
      finishedPlayers: [],
      isRevolution: false,
    });
  }, []);

  const nextTurn = useCallback((currentIndex: number) => {
    let nextIndex = (currentIndex + 1) % game!.players.length;
    while (game!.finishedPlayers.some(p => p.id === game!.players[nextIndex].id)) {
      nextIndex = (nextIndex + 1) % game!.players.length;
    }
    return nextIndex;
  }, [game]);

  const validatePlay = useCallback((selectedCards: CardData[]): boolean => {
    if (!game || selectedCards.length === 0) return false;

    const firstCardRank = selectedCards[0].rank;
    const allSameRank = selectedCards.every(c => c.rank === firstCardRank || c.rank === 13); // 조커 rank 13
    if (!allSameRank) return false;

    const { lastPlayed, passedPlayers, players, isRevolution } = game;
    if (passedPlayers.size === players.length - game.finishedPlayers.length - 1) {
        return true; // 모두 패스했으면 아무거나 낼 수 있음
    }

    if (lastPlayed) {
      if (selectedCards.length !== lastPlayed.length) return false;

      if (isRevolution) {
        // 혁명 상태: 낸 카드의 랭크가 이전 카드보다 높아야 함
        if (selectedCards[0].rank < lastPlayed[0].rank) return false;
      } else {
        // 일반 상태: 낸 카드의 랭크가 이전 카드보다 낮아야 함
        if (selectedCards[0].rank >= lastPlayed[0].rank) return false;
      }
    }

    return true;
  }, [game]);

  const findAllPossiblePlays = useCallback((hand: CardData[]): CardData[][] => {
    const possiblePlays: CardData[][] = [];
    const jokerCard = hand.find(card => card.rank === 13); // 조커 카드
    const nonJokerHand = hand.filter(card => card.rank !== 13);

    const groupedByRank = nonJokerHand.reduce((acc, card) => {
      (acc[card.rank] = acc[card.rank] || []).push(card);
      return acc;
    }, {} as Record<number, CardData[]>);

    for (const rank in groupedByRank) {
      const cardsOfRank = groupedByRank[rank];
      for (let i = 1; i <= cardsOfRank.length; i++) {
        const combination = cardsOfRank.slice(0, i);
        possiblePlays.push(combination);
      }
    }

    if (jokerCard) {
      const jokerPlays: CardData[][] = [];
      jokerPlays.push([jokerCard]);

      for (const play of possiblePlays) {
        const newPlayWithJoker = [...play, jokerCard];
        jokerPlays.push(newPlayWithJoker);
      }
      possiblePlays.push(...jokerPlays);
    }

    const filteredPlays = possiblePlays.filter(play => {
      return validatePlay(play);
    });

    filteredPlays.sort((a, b) => a[0].rank - b[0].rank);

    return filteredPlays;
  }, [validatePlay]);

  const playTurn = useCallback((cardIndices: number[]) => {
    if (!game) return;

    const currentPlayer = game.players[game.currentPlayerIndex];
    const selectedCards = cardIndices.map(i => currentPlayer.hand[i]).sort((a, b) => a.rank - b.rank);

    if (!validatePlay(selectedCards)) {
      alert('낼 수 없는 카드입니다.');
      return;
    }

    const newHand = currentPlayer.hand.filter((_, i) => !cardIndices.includes(i));
    const newPlayers = [...game.players];
    newPlayers[game.currentPlayerIndex] = { ...currentPlayer, hand: newHand };

    const newFinishedPlayers = [...game.finishedPlayers];
    if (newHand.length === 0 && !newFinishedPlayers.some(p => p.id === currentPlayer.id)) {
      const finishedPlayer = { ...currentPlayer, rank: newFinishedPlayers.length + 1 };
      newFinishedPlayers.push(finishedPlayer);
    }

    let newIsRevolution = game.isRevolution;
    if (selectedCards.length === 2 && selectedCards[0].rank === selectedCards[1].rank) {
      newIsRevolution = !newIsRevolution;
    }

    setGame(prevGame => ({
      ...prevGame!,
      players: newPlayers,
      lastPlayed: selectedCards,
      currentPlayerIndex: nextTurn(game.currentPlayerIndex),
      passedPlayers: new Set(),
      lastPlayerWhoPlayed: game.currentPlayerIndex,
      finishedPlayers: newFinishedPlayers,
      isRevolution: newIsRevolution,
    }));

    if (newFinishedPlayers.length === game.players.length - 1) {
      const lastPlayer = game.players.find(p => p.hand.length > 0 && !newFinishedPlayers.some(fp => fp.id === p.id));
      if (lastPlayer) {
        newFinishedPlayers.push({ ...lastPlayer, rank: game.players.length });
      }
      setGameState('finished');
    }
  }, [game, nextTurn, setGameState, validatePlay]);

  const passTurn = useCallback(() => {
    if (!game) return;

    const newPassedPlayers = new Set(game.passedPlayers).add(game.currentPlayerIndex);

    if (newPassedPlayers.size === game.players.length - game.finishedPlayers.length - 1) {
      setGame(prevGame => ({
        ...prevGame!,
        lastPlayed: null,
        passedPlayers: new Set(),
        currentPlayerIndex: prevGame!.lastPlayerWhoPlayed !== null ? prevGame!.lastPlayerWhoPlayed : nextTurn(game.currentPlayerIndex),
      }));
    } else {
      setGame(prevGame => ({
        ...prevGame!,
        passedPlayers: newPassedPlayers,
        currentPlayerIndex: nextTurn(game.currentPlayerIndex),
      }));
    }
  }, [game, nextTurn]);

  useEffect(() => {
    if (settings) {
      initializeGame(settings);
    }
  }, [settings, initializeGame]);

  const aiPlayTurn = useCallback(() => {
    if (!game || !game.players[game.currentPlayerIndex].isAI) return;

    const currentPlayer = game.players[game.currentPlayerIndex];
    const possiblePlays = findAllPossiblePlays(currentPlayer.hand);

    if (possiblePlays.length > 0) {
      let play: CardData[];
      if (settings?.difficulty === 'easy') {
        play = possiblePlays[Math.floor(Math.random() * possiblePlays.length)];
      } else if (settings?.difficulty === 'medium') {
        play = possiblePlays[possiblePlays.length - 1];
      } else { // hard
        play = possiblePlays[0];
      }

      const indices = play.map(card => currentPlayer.hand.indexOf(card));
      playTurn(indices);
    } else {
      passTurn();
    }
  }, [game, settings, playTurn, passTurn, findAllPossiblePlays]);

  useEffect(() => {
    if (game && game.players[game.currentPlayerIndex]?.isAI) {
      const timeoutId = setTimeout(aiPlayTurn, 1000);
      return () => clearTimeout(timeoutId);
    }
  }, [game?.currentPlayerIndex, aiPlayTurn]);

  return { game, playTurn, passTurn };
};

export default useGameLogic;