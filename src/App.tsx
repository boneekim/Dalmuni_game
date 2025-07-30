
import { useState } from 'react';
import styled from 'styled-components';
import { GlobalStyle } from './styles/GlobalStyle';
import GameSetup from './pages/GameSetup';
import GameBoard from './pages/GameBoard';
import Finale from './pages/Finale';
import useGameLogic from './hooks/useGameLogic';

export type GameState = 'setup' | 'playing' | 'finished';
export interface GameSettings {
  playerCount: number;
  difficulty: 'easy' | 'medium' | 'hard';
}

function App() {
  const [gameState, setGameState] = useState<GameState>('setup');
  const [gameSettings, setGameSettings] = useState<GameSettings | null>(null);
  const { game, playTurn, passTurn } = useGameLogic(gameSettings, setGameState);

  const handleGameStart = (settings: GameSettings) => {
    setGameSettings(settings);
    setGameState('playing');
  };

  const handleRestart = () => {
    setGameSettings(null);
    setGameState('setup');
  };

  return (
    <>
      <GlobalStyle />
      <Container>
        <h1>달무티 게임</h1>
        <p>테스트 중입니다... 이 텍스트가 보이면 리액트 앱이 정상적으로 로드된 것입니다.</p>
        {gameState === 'setup' && <GameSetup onGameStart={handleGameStart} />}
        {gameState === 'playing' && game && <GameBoard game={game} playTurn={playTurn} passTurn={passTurn} />}
        {gameState === 'finished' && game && <Finale players={game.players} onRestart={handleRestart} />}
      </Container>
    </>
  );
}

const Container = styled.div`
  text-align: center;
  padding: 2rem;
  min-height: 100vh; /* 최소 높이를 뷰포트 높이로 설정 */
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* 내용을 중앙에 배치 */
  background-color: #444; /* 배경색 추가 */
  color: white;
`;

export default App;
