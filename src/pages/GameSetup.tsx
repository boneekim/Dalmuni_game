
import { useState } from 'react';
import styled from 'styled-components';
import type { GameSettings } from '../App';

interface GameSetupProps {
  onGameStart: (settings: GameSettings) => void;
}

const GameSetup = ({ onGameStart }: GameSetupProps) => {
  const [playerCount, setPlayerCount] = useState(4);
  const [difficulty, setDifficulty] = useState<'easy' | 'medium' | 'hard'>('easy');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onGameStart({ playerCount, difficulty });
  };

  return (
    <SetupContainer>
      <h2>게임 설정</h2>
      <form onSubmit={handleSubmit}>
        <FormGroup>
          <label htmlFor="player-count">플레이어 수 (AI 포함)</label>
          <select
            id="player-count"
            value={playerCount}
            onChange={(e) => setPlayerCount(Number(e.target.value))}
          >
            <option value="4">4명</option>
            <option value="5">5명</option>
            <option value="6">6명</option>
            <option value="7">7명</option>
            <option value="8">8명</option>
          </select>
        </FormGroup>
        <FormGroup>
          <label>AI 난이도</label>
          <div onChange={(e: any) => setDifficulty(e.target.value)}>
            <input type="radio" id="easy" name="difficulty" value="easy" defaultChecked />
            <label htmlFor="easy">하</label>
            <input type="radio" id="medium" name="difficulty" value="medium" />
            <label htmlFor="medium">중</label>
            <input type="radio" id="hard" name="difficulty" value="hard" />
            <label htmlFor="hard">상</label>
          </div>
        </FormGroup>
        <StartButton type="submit">게임 시작</StartButton>
      </form>
    </SetupContainer>
  );
};

const SetupContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2rem;
`;

const FormGroup = styled.div`
  margin-bottom: 1.5rem;

  label {
    display: block;
    margin-bottom: 0.5rem;
  }

  select, input[type="radio"] + label {
    margin-left: 0.5rem;
  }
`;

const StartButton = styled.button`
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

export default GameSetup;
