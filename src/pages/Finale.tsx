import styled from 'styled-components';
import type { Player } from '../types';

interface FinaleProps {
  players: Player[];
  onRestart: () => void;
}

const Finale = ({ players, onRestart }: FinaleProps) => {
  const sortedPlayers = [...players].sort((a, b) => (a.rank || 99) - (b.rank || 99));

  return (
    <FinaleContainer>
      <h2>게임 결과</h2>
      <Rankings>
        {sortedPlayers.map(player => (
          <RankItem key={player.id}>
            <span>{player.rank}등:</span>
            <span>{player.name}</span>
          </RankItem>
        ))}
      </Rankings>
      <RestartButton onClick={onRestart}>새 게임 시작</RestartButton>
    </FinaleContainer>
  );
};

const FinaleContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
`;

const Rankings = styled.div`
  margin: 2rem 0;
  width: 200px;
`;

const RankItem = styled.div`
  display: flex;
  justify-content: space-between;
  padding: 0.5rem;
  border-bottom: 1px solid #ccc;

  &:first-child {
    font-weight: bold;
    color: #ffd700; /* Gold */
  }
`;

const RestartButton = styled.button`
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  background-color: #61dafb;
  border: none;
  border-radius: 5px;
  color: #282c34;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    background-color: #21a1f2;
  }
`;

export default Finale;