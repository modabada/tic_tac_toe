import pygame
from tic.algorithm import find_best_move, is_draw, is_won, command

Button = {
    "X": pygame.image.load("tic/Resources/X.png"),
    "O": pygame.image.load("tic/Resources/O.png"),
    "Reset": pygame.image.load("tic/Resources/Reset.png"),
    "Exit": pygame.image.load("tic/Resources/Exit.png")
}


class GUI:
    board, isPlayerTurn = [-1] * 9, True
    size = None
    board_pos = None
    screen = None

    def __init__(self):
        self.setting()

    def setting(self):
        pygame.init()  # 초기화
        self.size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.board_pos = (self.size[0] / 2 - 380, self.size[1] / 2 - 380 - 100)
        self.screen = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        pygame.display.set_caption("Game Title")  # 타이틀
        self.screen.fill((0, 255, 255))  # BG color
        self.drawGrid()
        self.Update()

    def Update(self):
        mousePressed = [None, None, None]  # o_클릭 n_클릭 클릭좌표
        isExited = False
        while not isExited:
            pygame.time.Clock().tick(30)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    isExited = True
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_r:
                    self.reset()

            if is_draw(self.board):
                text = pygame.font.SysFont("None", 72).render("Draw... Try again?", True, (0, 0, 0))
                locate_y = (self.size[1] - (760 + self.board_pos[1])) / 2 - text.get_size()[1] / 2 + \
                           (760 + self.board_pos[1])
                self.screen.blit(text, (self.size[0] / 2 - text.get_size()[0] / 2, locate_y))
            elif is_won(self.board):
                text = pygame.font.SysFont(
                    "None", 72
                ).render(
                    "You {}".format(
                        "lose... Try again?" if self.isPlayerTurn else "win!"
                    ), True, (0, 0, 0)
                )
                locate_y = (self.size[1] - (760 + self.board_pos[1])) / 2 - text.get_size()[1] / 2 + \
                           (760 + self.board_pos[1])
                self.screen.blit(text, (self.size[0] / 2 - text.get_size()[0] / 2, locate_y))
            elif not self.isPlayerTurn:
                self.AIControlled()

            mousePressed[1] = pygame.mouse.get_pressed(3)[0]  # n 클릭값 초기화
            if not mousePressed[0] and mousePressed[1]:  # 이전에 누르지 않고있다가 지금 눌렀을 때
                mousePressed[2] = pygame.mouse.get_pos()  # 클릭 당시의 좌표저장
            elif mousePressed[0] and not mousePressed[1]:  # 이전에 누르고 있다가 지금 해제했을 때
                pos = pygame.mouse.get_pos()
                if mousePressed[2] == pos:  # 지금 좌표와 저장된 좌표가 같다면(마우스의 이동이 없었다면)
                    if not self.PlayerControlled(pos):
                        isExited = True
            mousePressed[0] = mousePressed[1]  # 업데이트

            # pygame.display.update()   # 디스플레이 업데이트
            pygame.display.flip()  # 위와 차이점은 refresh 범위, flip 전체, update 는 전달받은 인자만 업데이트 가능

    def drawGrid(self):
        x = int(self.board_pos[0])
        y = int(self.board_pos[1])
        self.screen.blit(Button["Reset"], (10, 10))
        self.screen.blit(Button["Exit"], (self.size[0] - 110, 10))
        pygame.draw.rect(self.screen, (0, 0, 0), (250 + x, y, 5, 760))
        pygame.draw.rect(self.screen, (0, 0, 0), (505 + x, y, 5, 760))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 250 + y, 760, 5))
        pygame.draw.rect(self.screen, (0, 0, 0), (x, 505 + y, 760, 5))

    def reset(self):
        self.board, self.isPlayerTurn = [-1] * 9, True
        self.screen.fill((0, 255, 255))  # BG color
        self.drawGrid()
        pass

    def PlayerControlled(self, pos):
        board_x = self.board_pos[0]
        board_y = self.board_pos[1]
        x = pos[0]
        y = pos[1]

        if 10 <= x <= 147 and 10 <= y <= 110:  # 리셋버튼
            self.reset()
            return True
        elif self.size[0] - 110 <= x <= self.size[0] - 10 and 10 <= y <= 110:  # 게임종료
            return False
        elif self.isPlayerTurn:
            if board_x <= x <= board_x + 250 and board_y <= y <= board_y + 250 and self.board[0] == -1:
                index = 0
            elif board_x + 255 <= x <= board_x + 505 and board_y <= y <= board_y + 250 and self.board[1] == -1:
                index = 1
            elif board_x + 510 <= x <= board_x + 760 and board_y <= y <= board_y + 250 and self.board[2] == -1:
                index = 2
            elif board_x <= x <= board_x + 250 and board_y + 255 <= y <= board_y + 505 and self.board[3] == -1:
                index = 3
            elif board_x + 255 <= x <= board_x + 505 and board_y + 255 <= y <= board_y + 505 and self.board[4] == -1:
                index = 4
            elif board_x + 510 <= x <= board_x + 760 and board_y + 255 <= y <= board_y + 505 and self.board[5] == -1:
                index = 5
            elif board_x <= x <= board_x + 250 and board_y + 510 <= y <= board_y + 760 and self.board[6] == -1:
                index = 6
            elif board_x + 255 <= x <= board_x + 505 and board_y + 510 <= y <= board_y + 760 and self.board[7] == -1:
                index = 7
            elif board_x + 510 <= x <= board_x + 760 and board_y + 510 <= y <= board_y + 760 and self.board[8] == -1:
                index = 8
            else:
                return True
            self.board[index] = "X"
            self.DrawXO(index, "X")
            self.isPlayerTurn = False

        return True

    def AIControlled(self):
        v, _ = find_best_move(self.board, True, self.isPlayerTurn)
        for i, e in enumerate(self.board):
            if v[i] != e:
                v = i
                break
        command(v)
        while True:
            isInput = False
            for event in pygame.event.get():
                if event.type == pygame.FINGERDOWN:
                    isInput = True
            if isInput:
                break

        self.DrawXO(v, "O")
        self.board[v] = "O"
        self.isPlayerTurn = True

    def DrawXO(self, index, mark):
        board_x = self.board_pos[0]
        board_y = self.board_pos[1]
        margin = 10

        if index == 0:
            self.screen.blit(Button[mark], (board_x + margin, board_y + margin))
            pass
        elif index == 1:
            self.screen.blit(Button[mark], (board_x + 255 + margin, board_y + margin))
            pass
        elif index == 2:
            self.screen.blit(Button[mark], (board_x + 510 + margin, board_y + margin))
            pass
        elif index == 3:
            self.screen.blit(Button[mark], (board_x + margin, board_y + 255 + margin))
            pass
        elif index == 4:
            self.screen.blit(Button[mark], (board_x + 255 + margin, board_y + 255 + margin))
            pass
        elif index == 5:
            self.screen.blit(Button[mark], (board_x + 510 + margin, board_y + 255 + margin))
            pass
        elif index == 6:
            self.screen.blit(Button[mark], (board_x + margin, board_y + 510 + margin))
            pass
        elif index == 7:
            self.screen.blit(Button[mark], (board_x + 255 + margin, board_y + 510 + margin))
            pass
        elif index == 8:
            self.screen.blit(Button[mark], (board_x + 510 + margin, board_y + 510 + margin))
            pass
        else:
            return BaseException


def DrawGui():
    GUI()


if __name__ == "__main__":
    DrawGui()
