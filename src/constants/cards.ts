
export interface CardData {
  id: number;
  rank: number;
  name: string;
  quantity: number;
  image: string;
}

export const CARDS: CardData[] = [
  { id: 1, rank: 1, name: '달무티', quantity: 1, image: '/assets/cards/1.png' },
  { id: 2, rank: 2, name: '대주교', quantity: 2, image: '/assets/cards/2.png' },
  { id: 3, rank: 3, name: '총리', quantity: 3, image: '/assets/cards/3.png' },
  { id: 4, rank: 4, name: '남작부인', quantity: 4, image: '/assets/cards/4.png' },
  { id: 5, rank: 5, name: '기사', quantity: 5, image: '/assets/cards/5.png' },
  { id: 6, rank: 6, name: '재봉사', quantity: 6, image: '/assets/cards/6.png' },
  { id: 7, rank: 7, name: '석공', quantity: 7, image: '/assets/cards/7.png' },
  { id: 8, rank: 8, name: '요리사', quantity: 8, image: '/assets/cards/8.png' },
  { id: 9, rank: 9, name: '광부', quantity: 9, image: '/assets/cards/9.png' },
  { id: 10, rank: 10, name: '농노', quantity: 10, image: '/assets/cards/10.png' },
  { id: 11, rank: 11, name: '어릿광대', quantity: 2, image: '/assets/cards/11.png' }, // 조커
];
