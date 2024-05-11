import socket
import threading


class TicTacToe:

    def __init__(self):
        self.board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        self.turn = "X"
        self.you = "X"
        self.opponent = "O"
        self.winner = None
        self.game_over = False

        self.counter = 0

    def host_game(self, host, port):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((host, port))
        server.listen(1)

        client_socket, addr = server.accept()

        self.you = "X"
        self.opponent = "O"

        threading.Thread(target=self.handle_connection, args=(client_socket,)).start()
        server.close()

    def connect_to_game(self, host, port):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        self.you = "O"
        self.opponent = "X"

        threading.Thread(target=self.handle_connection, args=(client_socket,)).start()

    def handle_connection(self, client_socket):
        while not self.game_over:
            if self.turn == self.you:
                move = input("Enter your move (row, column) : ")
                if self.check_valid_move(move.split(',')):
                    client_socket.send(move.encode('utf-8'))
                    self.apply_move(move.split(','), self.you)
                    self.turn = self.opponent

                else:
                    print("Invalid move!")
            else:
                data = client_socket.recv(1024)
                if not data:
                    break
                else:
                    self.apply_move(data.decode('utf-8').split(','), self.opponent)
                    self.turn = self.you
        client_socket.close()

    def apply_move(self, move, player):
        if self.game_over == True:
            return
        self.counter += 1

        row = int(move[0])
        col = int(move[1])
        self.board[row][col] = player
        self.print_board()
        if self.check_if_won():
            if self.winner == self.you:
                print("You've won")
                exit()
            elif self.winner == self.opponent:
                print("You lost")
                exit()
            else:
                if self.counter == 9:
                    print("It's a draw")
                    exit()

    def check_valid_move(self, move):
        return self.board[int(move[0])][int(move[1])] == " "

    def check_if_won(self):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] != " ":
                self.winner = self.board[row][0]
                self.game_over = True
                return True
        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] != " ":
                self.winner = self.board[0][col]
                self.game_over = True
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != " ":
            self.winner = self.board[0][0]
            self.game_over = True
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != " ":
            self.winner = self.board[0][2]
            self.game_over = True
            return True

    def print_board(self):
        for row in range(3):
            print(" | ".join(self.board[row]))
            if row != 2:
                print("----------")


game = TicTacToe()
game.connect_to_game("localhost", 9999)
