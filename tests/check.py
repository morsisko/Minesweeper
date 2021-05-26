#python -m unittest tests.check
import unittest
from logic.game import Game
from logic.exceptions import MinesweeperException, BoardTooSmallException, BoardTooBigException, TooManyMinesException, TooLittleMinesException

class TestIncorrectBoardDimensions(unittest.TestCase):
    def test_1x1x1(self):
        """Próba rozpoczęcia gry z planszą 1x1 i z 1 miną"""
        WIDTH = 1
        HEIGHT = 1
        MINES = 1
        
        self.assertRaises(BoardTooSmallException, Game, WIDTH, HEIGHT, MINES)
        
    def test_5x1x2(self):
        """Próba rozpoczęcia gry z planszą 5x1 i z 2 minami"""
        WIDTH = 5
        HEIGHT = 1
        MINES = 2
        
        self.assertRaises(BoardTooSmallException, Game, WIDTH, HEIGHT, MINES)
        
    def test_4x1x2(self):
        """Próba rozpoczęcia gry z planszą 4x1 i z 2 minami"""
        WIDTH = 4
        HEIGHT = 1
        MINES = 2
        
        self.assertRaises(BoardTooSmallException, Game, WIDTH, HEIGHT, MINES)
        
    def test_20x500x12(self):
        """Próba rozpoczęcia gry z planszą 20x500 i z 12 minami"""
        WIDTH = 20
        HEIGHT = 500
        MINES = 12
        
        self.assertRaises(BoardTooBigException, Game, WIDTH, HEIGHT, MINES)
        
    def test_5x6xminus4(self):
        """Próba rozpoczęcia gry z planszą 5x6 i z -4 minami"""
        WIDTH = 5
        HEIGHT = 6
        MINES = -4
        
        self.assertRaises(TooLittleMinesException, Game, WIDTH, HEIGHT, MINES)
        
    def test_3x3x10(self):
        """Próba rozpoczęcia gry z planszą 3x3 i z 10 minami"""
        WIDTH = 3
        HEIGHT = 3
        MINES = 10
        
        self.assertRaises(TooManyMinesException, Game, WIDTH, HEIGHT, MINES)
        
    def test_1x10x5(self):
        """Próba rozpoczęcia gry z planszą 1x10 i z 5 minami"""
        WIDTH = 1
        HEIGHT = 10
        MINES = 5
        
        self.assertRaises(BoardTooSmallException, Game, WIDTH, HEIGHT, MINES)
        
class TestLeftClick(unittest.TestCase):
    WIDTH = 8
    HEIGHT = 8
    MINES = 12
    
    def test_mines_count_on_field(self):
        """Test, czy cyfra wyświetlana na polu rzeczywiście odpowiada prawdziwej liczbie min w okolicy pola"""
        game = Game(TestLeftClick.WIDTH, TestLeftClick.HEIGHT, TestLeftClick.MINES)
        
        CLICK_X = 4
        CLICK_Y = 4
        DIRECTIONS = [(-1, -1,), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        
        game.leftClick(CLICK_X, CLICK_Y)
        minesNearby = game.getField(CLICK_X, CLICK_Y).getMinesNearby()
        
        realMinesNearby = 0
        for x_shift, y_shift in DIRECTIONS:
            newX = CLICK_X + x_shift
            newY = CLICK_Y + y_shift                
        
            if game.getField(newX, newY).isMine():
                realMinesNearby += 1
                
        self.assertEqual(realMinesNearby, minesNearby)
        
    def test_click_on_mine(self):
        """Test, czy gra kończy się przegraną w momencie kliknięcia na minę"""
        game = Game(TestLeftClick.WIDTH, TestLeftClick.HEIGHT, TestLeftClick.MINES)
        
        CLICK_X = 4
        CLICK_Y = 4
        game.leftClick(CLICK_X, CLICK_Y)
        
        self.assertFalse(game.isEnd())
        
        iterate = True
        for y in range(TestLeftClick.HEIGHT):
            if not iterate:
                break
                
            for x in range(TestLeftClick.WIDTH):
                if game.getField(x, y).isMine():
                    game.leftClick(x, y)
                    iterate = False
                    break
                    
        self.assertTrue(game.isLost())
        
    def test_click_on_field_without_mines_nearby(self):
        """Test, czy w momencie kliknięcie na pole z minami w okolicy otworzy się tylko to pole, a w przypadku gdy otworzymy pole bez min w okolicy, to otworzą się wszystkie pola w pobliżu (i możliwe że jeszcze więcej pól)"""
        game = Game(TestLeftClick.WIDTH, TestLeftClick.HEIGHT, TestLeftClick.MINES)
        
        CLICK_X = 4
        CLICK_Y = 4
        game.leftClick(CLICK_X, CLICK_Y)
        minesNearby = game.getField(CLICK_X, CLICK_Y).getMinesNearby()
        
        if minesNearby == 0:
            self.assertGreaterEqual(game.getOpenedFieldsCount(), 9)
            
        else:
            self.assertEqual(game.getOpenedFieldsCount(), 1)
            
class TestRightClick(unittest.TestCase):
    WIDTH = 8
    HEIGHT = 8
    MINES = 12
    
    def test_flagged_field_counter(self):
        """Test czy po jednokrotnym kliknięciu prawym przyciskiem myszy zwiększa się liczba pól oznaczonych flagą"""
        game = Game(TestLeftClick.WIDTH, TestLeftClick.HEIGHT, TestLeftClick.MINES)
        
        CLICK_X = 4
        CLICK_Y = 4
        
        self.assertEqual(game.getFlaggedFieldsCount(), 0)
        game.rightClick(CLICK_X, CLICK_Y)
        self.assertEqual(game.getFlaggedFieldsCount(), 1)
        
    def test_might_be_mine_(self):
        """Test czy po dwukrotnym kliknięciu prawym przyciskiem myszy pole otrzymuje status "może być miną" """
        game = Game(TestLeftClick.WIDTH, TestLeftClick.HEIGHT, TestLeftClick.MINES)
        
        CLICK_X = 4
        CLICK_Y = 4
        
        game.rightClick(CLICK_X, CLICK_Y)
        self.assertFalse(game.getField(CLICK_X, CLICK_Y).isMaybeMine())
        game.rightClick(CLICK_X, CLICK_Y)
        self.assertTrue(game.getField(CLICK_X, CLICK_Y).isMaybeMine())
        
    def test_field_flagging(self):
        """Test czy po wielokrotnym kliknięciu prawym przyciskiem myszy na pole, cały czas jest aktualizowany licznik oznaczonych pól"""
        game = Game(TestLeftClick.WIDTH, TestLeftClick.HEIGHT, TestLeftClick.MINES)
        
        CLICK_X = 4
        CLICK_Y = 4
        
        self.assertEqual(game.getFlaggedFieldsCount(), 0) #brak kliknięć - pole puste
        game.rightClick(CLICK_X, CLICK_Y)
        self.assertEqual(game.getFlaggedFieldsCount(), 1) #pierwsze kliknięcie - flaga
        game.rightClick(CLICK_X, CLICK_Y)
        self.assertEqual(game.getFlaggedFieldsCount(), 0) #drugie kliknięcie - może mina, 0 flag
        game.rightClick(CLICK_X, CLICK_Y)
        self.assertEqual(game.getFlaggedFieldsCount(), 0) #trzecie kliknięcie - pole puste
        game.rightClick(CLICK_X, CLICK_Y)
        self.assertEqual(game.getFlaggedFieldsCount(), 1) #czwarte - flaga
        game.rightClick(CLICK_X, CLICK_Y)
        self.assertEqual(game.getFlaggedFieldsCount(), 0) #piąte - może mina
        game.rightClick(CLICK_X, CLICK_Y)
        self.assertEqual(game.getFlaggedFieldsCount(), 0) # szóste - puste
        
class TestWinning(unittest.TestCase):
    WIDTH = 8
    HEIGHT = 8
    MINES = 12
    
    def test_open_all_without_mines(self):
        """Test, czy następuje wygrana po otworzeniu wszystkich pól bez min"""
        game = Game(TestWinning.WIDTH, TestWinning.HEIGHT, TestWinning.MINES)
        
        CLICK_X = 4
        CLICK_Y = 4
        
        game.leftClick(CLICK_X, CLICK_Y)
        
        self.assertFalse(game.isWon())
        
        for y in range(TestWinning.HEIGHT):
            for x in range(TestWinning.WIDTH):
                field = game.getField(x, y)
                if not field.isMine() and not field.isOpened():
                    game.leftClick(x, y)
                    
        self.assertTrue(game.isWon())
        
    def test_mark_only_field_with_mines(self):
        """Test, czy następuje wygrana po oznaczeniu wszystkich pól z minami (i tylko tych) za pomocą flagi."""
        game = Game(TestWinning.WIDTH, TestWinning.HEIGHT, TestWinning.MINES)
        
        CLICK_X = 4
        CLICK_Y = 4
        
        game.leftClick(CLICK_X, CLICK_Y)
        
        self.assertFalse(game.isWon())
        
        for y in range(TestWinning.HEIGHT):
            for x in range(TestWinning.WIDTH):
                field = game.getField(x, y)
                if field.isMine():
                    game.rightClick(x, y)
                    
        self.assertTrue(game.isWon())
        
class MiscTests(unittest.TestCase):
    WIDTH = 8
    HEIGHT = 8
    MINES = 12
        
    def test_clicking_on_opened_field(self):
        """Test, czy po kliknięciu lewym przyciskiem na już otworzone pole nic się nie dzieje"""
        game = Game(MiscTests.WIDTH, MiscTests.HEIGHT, MiscTests.MINES)
        
        CLICK_X = 4
        CLICK_Y = 4
        game.leftClick(CLICK_X, CLICK_Y)
        openedFieldsBefore = game.getOpenedFieldsCount()
        game.leftClick(CLICK_X, CLICK_Y)
        openedFieldsAfter = game.getOpenedFieldsCount()
        
        self.assertEqual(openedFieldsBefore, openedFieldsAfter) #nic się nie zmienia
        
    def test_opening_and_marking_multiple_fields(self):
        """Test, otworzenie trzech pól bez min, oznaczenia flagą trzech pól, zrestartowanie gry, sprawdzenie czy za każdym razem licznik otwartych pól i oznakowych pól działa poprawnie"""
        game = Game(MiscTests.WIDTH, MiscTests.HEIGHT, MiscTests.MINES)
        
        CLICK_X = 4
        CLICK_Y = 4
        TO_CLICK = 3
        TO_MARK = 3
        
        game.leftClick(CLICK_X, CLICK_Y)
        clickedFields = 1
        markedFields = 0
        
        iterate = True
        for y in range(TestWinning.HEIGHT):
            if not iterate:
                return False
                
            for x in range(TestWinning.WIDTH):
                field = game.getField(x, y)
                if clickedFields < TO_CLICK:
                    if field.isOpened() or field.isMine():
                        continue
                        
                    game.leftClick(x, y)
                    clickedFields += 1
                
                elif markedFields < TO_MARK:
                    if field.isOpened():
                        continue
                        
                    game.rightClick(x, y)
                    markedFields += 1
                    
                else:
                    iterate = False
                    break
                    
        self.assertGreaterEqual(game.getOpenedFieldsCount(), clickedFields)
        self.assertEqual(game.getFlaggedFieldsCount(), markedFields)
        game = Game(MiscTests.WIDTH, MiscTests.HEIGHT, MiscTests.MINES)
        self.assertEqual(game.getOpenedFieldsCount(), 0)
        self.assertEqual(game.getFlaggedFieldsCount(), 0)
        
        
    def test_secret_code(self):
        """Test sprawdzający, czy po wciśnięciu sekwencji klawiszy 'xyzzy' kolor pól, pod którymi są miny zmienia kolor"""
        X_KEYCODE = 120
        Y_KEYCODE = 121
        Z_KEYCODE = 122
        game = Game(MiscTests.WIDTH, MiscTests.HEIGHT, MiscTests.MINES)
        
        self.assertFalse(game.isSecretCodeActivated())
        game.addKeypress(60)
        self.assertFalse(game.isSecretCodeActivated())
        game.addKeypress(65)
        self.assertFalse(game.isSecretCodeActivated())
        game.addKeypress(70)
        self.assertFalse(game.isSecretCodeActivated())
        game.addKeypress(X_KEYCODE)
        self.assertFalse(game.isSecretCodeActivated())
        game.addKeypress(Y_KEYCODE)
        self.assertFalse(game.isSecretCodeActivated())
        game.addKeypress(Z_KEYCODE)
        self.assertFalse(game.isSecretCodeActivated())
        game.addKeypress(Z_KEYCODE)
        self.assertFalse(game.isSecretCodeActivated())
        game.addKeypress(Y_KEYCODE)
        
        self.assertTrue(game.isSecretCodeActivated())
        
        game = Game(MiscTests.WIDTH, MiscTests.HEIGHT, MiscTests.MINES)
        
        self.assertFalse(game.isSecretCodeActivated())
        

if __name__ == '__main__':
    unittest.main()