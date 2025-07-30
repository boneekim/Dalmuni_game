
import styled from 'styled-components';
import type { CardData } from '../constants/cards';

interface CardProps {
  card: CardData;
}

const Card = ({ card }: CardProps) => {
  return (
    <CardWrapper>
      <CardImage src={card.image} alt={card.name} />
      <CardName>{card.name}</CardName>
    </CardWrapper>
  );
};

const CardWrapper = styled.div`
  border: 1px solid #fff;
  border-radius: 10px;
  width: 100px;
  height: 140px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  background-color: #f0f0f0;
  color: #333;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
`;

const CardImage = styled.img`
  width: 80px;
  height: 80px;
  object-fit: contain;
  border-radius: 5px;
`;

const CardName = styled.div`
  font-size: 0.9rem;
  font-weight: bold;
`;

export default Card;
