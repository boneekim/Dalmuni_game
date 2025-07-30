
export interface CardData {
  id: number;
  rank: number;
  name: string;
  quantity: number;
  image: string;
}

export const CARDS: CardData[] = [
  { id: 1, rank: 1, name: '달무티', quantity: 1, image: '/cards/1.svg' },
  { id: 2, rank: 2, name: '대주교', quantity: 2, image: '/cards/2.svg' },
  { id: 3, rank: 3, name: '총리', quantity: 3, image: '/cards/3.svg' },
  { id: 4, rank: 4, name: '남작부인', quantity: 4, image: '/cards/4.svg' },
  { id: 5, rank: 5, name: '기사', quantity: 5, image: '/cards/5.svg' },
  { id: 6, rank: 6, name: '재봉사', quantity: 6, image: '/cards/6.svg' },
  { id: 7, rank: 7, name: '석공', quantity: 7, image: '/cards/7.svg' },
  { id: 8, rank: 8, name: '요리사', quantity: 8, image: '/cards/8.svg' },
  { id: 9, rank: 9, name: '광부', quantity: 9, image: '/cards/9.svg' },
  { id: 10, rank: 10, name: '농노', quantity: 10, image: '/cards/10.svg' },
  { id: 11, rank: 11, name: '농노', quantity: 11, image: '/cards/11.svg' },
  { id: 12, rank: 12, name: '농노', quantity: 12, image: '/cards/12.svg' },
  { id: 13, rank: 13, name: '어릿광대', quantity: 2, image: '/cards/13.svg' }, // 조커
];
