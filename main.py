from logic.game import Game

g = Game(5, 5, 5)

while not g.isEnd():
    coords = input("Podaj koordynaty: ").split()
    
    g.leftClick(int(coords[0]) - 1, int(coords[1]) - 1)
    g._board.printBoard()