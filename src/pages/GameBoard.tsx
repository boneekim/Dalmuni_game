import { useState } from 'react';
import styled, { css, keyframes } from 'styled-components';
import type { Game, CardData } from '../types';
import Card from '../components/Card';

interface GameBoardProps {
  game: Game;
  playTurn: (cardIndices: number[]) => void;
  passTurn: () => void;
}

const GameBoard = ({ game, playTurn, passTurn }: GameBoardProps) => {
  const [selectedCardIndices, setSelectedCardIndices] = useState<number[]>([]);
  const [animatingCards, setAnimatingCards] = useState<CardData[]>([]);

  const humanPlayer = game.players.find(p => !p.isAI);
  const isMyTurn = game.players[game.currentPlayerIndex].id === humanPlayer?.id;

  const handleCardClick = (index: number) => {
    if (!isMyTurn) return;
    setSelectedCardIndices(prev =>
      prev.includes(index)
        ? prev.filter(i => i !== index)
        : [...prev, index]
    );
  };

  const handlePlayClick = () => {
    if (selectedCardIndices.length > 0) {
      const cardsToAnimate = selectedCardIndices.map(i => humanPlayer!.hand[i]);
      setAnimatingCards(cardsToAnimate);

      setTimeout(() => {
        playTurn(selectedCardIndices);
        setSelectedCardIndices([]);
        setAnimatingCards([]);
      }, 500); // 0.5초 애니메이션
    }
  };

  const handlePassClick = () => {
    passTurn();
    setSelectedCardIndices([]);
  };

  return (
    <BoardContainer>
      <OpponentsContainer>
        {game.players.map((player, index) => (
          <PlayerInfo key={player.id} isCurrent={index === game.currentPlayerIndex}>
            <div>{player.name}</div>
            <div>카드: {player.hand.length}장</div>
          </PlayerInfo>
        ))}
      </OpponentsContainer>

      <PlayArea>
        {game.lastPlayed ? (
          <CardGrid>
            {game.lastPlayed.map((card, index) => <Card key={index} card={card} />)}
          </CardGrid>
        ) : (
          <div>{game.passedPlayers.size > 0 ? '모두 패스했습니다.' : '카드를 내세요'}</div>
        )}
        {animatingCards.length > 0 && (
          <AnimatingCardContainer>
            {animatingCards.map((card, index) => (
              <Card key={index} card={card} />
            ))}
          </AnimatingCardContainer>
        )}
      </PlayArea>

      <HumanPlayerContainer>
        <h3>{humanPlayer?.name} {isMyTurn && '(내 차례)'}</h3>
        <HandContainer>
          {humanPlayer?.hand.map((card, index) => (
            <CardWrapper
              key={index}
              onClick={() => handleCardClick(index)}
              isSelected={selectedCardIndices.includes(index)}
              isMyTurn={isMyTurn}
              isAnimating={animatingCards.includes(card)}
            >
              <Card card={card} />
            </CardWrapper>
          ))}
        </HandContainer>
        <ActionButtons>
          <button onClick={handlePlayClick} disabled={!isMyTurn || selectedCardIndices.length === 0}>내기</button>
          <button onClick={handlePassClick} disabled={!isMyTurn}>패스</button>
        </ActionButtons>
      </HumanPlayerContainer>
    </BoardContainer>
  );
};

const BoardContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: calc(100vh - 100px);
  padding: 1rem;
`;

const OpponentsContainer = styled.div`
  display: flex;
  justify-content: space-around;
  margin-bottom: 1rem;
`;

const blinkAnimation = keyframes`
  0% { box-shadow: 0 0 10px #61dafb; }
  50% { box-shadow: 0 0 20px #61dafb, 0 0 30px #61dafb; }
  100% { box-shadow: 0 0 10px #61dafb; }
`;

const PlayerInfo = styled.div<{ isCurrent: boolean }>`
  border: 1px solid #fff;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  ${({ isCurrent }) => isCurrent && css`
    border-color: #61dafb;
    animation: ${blinkAnimation} 1.5s infinite ease-in-out;
  `}
`;

const PlayArea = styled.div`
  flex-grow: 1;
  border: 2px dashed #fff;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  min-height: 180px;
  position: relative;
`;

const CardGrid = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const HumanPlayerContainer = styled.div``;

const HandContainer = styled.div`
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-top: 1rem;
`;

const CardWrapper = styled.div<{ isSelected: boolean; isMyTurn: boolean; isAnimating: boolean }>`
  cursor: ${({ isMyTurn }) => (isMyTurn ? 'pointer' : 'default')};
  transition: transform 0.2s, box-shadow 0.2s;

  ${({ isSelected }) => isSelected && css`
    transform: translateY(-10px);
    box-shadow: 0 0 15px #61dafb;
  `}

  ${({ isAnimating }) => isAnimating && css`
    opacity: 0;
    transition: opacity 0.5s ease-out;
  `}
`;

const ActionButtons = styled.div`
  margin-top: 1.5rem;
  display: flex;
  justify-content: center;
  gap: 1rem;

  button {
    padding: 0.75rem 1.5rem;
    font-size: 1rem;
    background-color: #61dafb;
    border: none;
    border-radius: 5px;
    color: #282c34;
    cursor: pointer;
    transition: background-color 0.2s;

    &:hover:not(:disabled) {
      background-color: #21a1f2;
    }

    &:disabled {
      background-color: #ccc;
      cursor: not-allowed;
    }
  }
`;

const animateToCenter = keyframes`
  from {
    transform: translate(0, 0) scale(1);
    opacity: 1;
  }
  to {
    transform: translate(0, -150px) scale(1.2); /* 중앙으로 이동 및 확대 */
    opacity: 0;
  }
`;

const AnimatingCardContainer = styled.div`
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 0.5rem;

  & > div {
    animation: ${animateToCenter} 0.5s forwards;
  }
`;

export default GameBoard;