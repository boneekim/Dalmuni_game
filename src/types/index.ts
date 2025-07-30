import type { CardData } from '../constants/cards';

export interface Player {
  id: string;
  name: string;
  hand: CardData[];
  isAI: boolean;
  rank: number | null; // 게임 종료 후 순위
}

export interface Game {
  players: Player[];
  currentPlayerIndex: number;
  lastPlayed: CardData[] | null;
  turnHistory: any[]; // 단순화를 위해 any 사용, 추후 구체화
  passedPlayers: Set<number>; // 패스한 플레이어 인덱스
  lastPlayerWhoPlayed: number | null; // 마지막으로 카드를 낸 플레이어 인덱스
  finishedPlayers: Player[]; // 게임 종료된 플레이어 목록 (순위 포함)
  isRevolution: boolean; // 혁명 상태 여부
}