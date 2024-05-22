#include <iostream>
#include <vector>

const int BOARD_SIZE = 19;

enum Stone { EMPTY, BLACK, WHITE };

class GoBoard {
public:
    GoBoard() {
        board.resize(BOARD_SIZE, std::vector<Stone>(BOARD_SIZE, EMPTY));
    }

    void displayBoard() const {
        for (int i = 0; i < BOARD_SIZE; ++i) {
            for (int j = 0; j < BOARD_SIZE; ++j) {
                char stone;
                switch (board[i][j]) {
                case EMPTY:
                    stone = '.';
                    break;
                case BLACK:
                    stone = 'B';
                    break;
                case WHITE:
                    stone = 'W';
                    break;
                }
                std::cout << stone << " ";
            }
            std::cout << std::endl;
        }
    }

    bool placeStone(int x, int y, Stone stone) {
        if (x < 0 || x >= BOARD_SIZE || y < 0 || y >= BOARD_SIZE) {
            std::cerr << "Position out of bounds!" << std::endl;
            return false;
        }
        if (board[x][y] != EMPTY) {
            std::cerr << "Position already occupied!" << std::endl;
            return false;
        }
        board[x][y] = stone;
        return true;
    }

private:
    std::vector<std::vector<Stone>> board;
};

int main() {
    GoBoard board;
    board.displayBoard();

    int x, y;
    char color;

    while (true) {
        std::cout << "Enter position and color (x y B/W): ";
        std::cin >> x >> y >> color;

        Stone stone;
        if (color == 'B') {
            stone = BLACK;
        }
        else if (color == 'W') {
            stone = WHITE;
        }
        else {
            std::cerr << "Invalid color!" << std::endl;
            continue;
        }

        if (board.placeStone(x, y, stone)) {
            board.displayBoard();
        }
    }

    return 0;
}
