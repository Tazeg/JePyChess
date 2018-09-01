JePyChess
=========

Introducing "JeffProd Simple Python Chess Program" running in command line.
You can play a full game versus it.
Run it with the command : ./main.py

It supports actually :
- promote
- under-promote
- capture "en passant"

Commands are :
- **new** to start a new game
- **e2e4** or **e7e8q** for example to move a piece. Promotes are q,r,n,b for queen, rook, knight, bishop
- **undomove** to cancel the last move
- **legalmoves** to show legal moves for side to move
- **go** requests the engine to play now
- **setboard fen** to set the board as the FEN position given
- **getboard** to export the current FEN position
- **sd x** to set the depth search
- **perft x** to test the move generator (x = search depth)
- **quit**... to quit

Things to do :
- move ordering
- quiescent search
- 50 moves rule
- 3 repetitions rule
- time settings
- opening book

Requirements :
- Python 3

More information on :
https://fr.jeffprod.com/blog/2014/comment-programmer-un-jeu-dechecs/
