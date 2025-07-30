
import { CardData } from '../constants/cards';

export interface Player {
  id: string;
  name: string;
  hand: CardData[];
  isAI: boolean;
}

export interface Game {
  players: Player[];
  currentPlayerIndex: number;
  lastPlayed: CardData[] | null;
  turnHistory: any[]; // 단순화를 위해 any 사용, 추후 구체화
}
