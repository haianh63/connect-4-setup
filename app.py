from fastapi import FastAPI, HTTPException
import random
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from game import get_connect_four_move
import numpy as np

app = FastAPI()
def my_agent(board, mark): 
    move = get_connect_four_move(board, mark)
    return move
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GameState(BaseModel):
    board: List[List[int]]
    current_player: int
    valid_moves: List[int]

class AIResponse(BaseModel):
    move: int

@app.post("/api/connect4-move")
async def make_move(game_state: GameState) -> AIResponse:
    try:
        if not game_state.valid_moves:
            raise ValueError("Không có nước đi hợp lệ")
            
        selected_move = my_agent(np.array(game_state.board).astype(np.int64).flatten(), game_state.current_player)
        
        return AIResponse(move=selected_move)
    except Exception as e:
        print(f"Error in AI: {str(e)}")
        if game_state.valid_moves:
            return AIResponse(move=game_state.valid_moves[0])
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)