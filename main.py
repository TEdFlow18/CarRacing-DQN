import pygame
import math
pygame.init()

def dist(x1, y1, x2, y2):
    return math.sqrt((x1-x2)**2+(y1-y2)**2)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.radius = 10

    def display(self, screen):
        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (self.x, self.y),
            self.radius
        )
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (self.x, self.y),
            self.radius - 4
        )

    def collide(self, x, y):
        if dist(x, y, self.x, self.y) < self.radius:
            return True
        return False


def main():
    screen = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("CarRacing-DQN")

    points = []
    moving_point = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    is_colliding = False
                    colliding_index = None
                    for i in range(len(points)):
                        if points[i].collide(*event.pos):
                            is_colliding = True
                            colliding_index = i
                            break

                    distance = dist(screen.get_width()-30, screen.get_height()-30, event.pos[0], event.pos[1])

                    if not is_colliding and distance > 20:
                        points.append(Point(*event.pos))
                    elif colliding_index is not None:
                        moving_point = colliding_index

                    elif distance < 20:
                        print("Create a spline")

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    moving_point = None

            elif event.type == pygame.MOUSEMOTION:
                if moving_point is not None:
                    points[moving_point].x = event.pos[0]
                    points[moving_point].y = event.pos[1]

        screen.fill((255, 255, 255))

        for point in points:
            point.display(screen)
        if moving_point is not None: points[moving_point].display(screen)

        #Draw the + button
        pygame.draw.circle(
            screen,
            (0, 200, 50),
            (screen.get_width() - 30, screen.get_height() - 30),
            20
        )
        pygame.draw.line(screen, (255, 255, 255),
            (screen.get_width()-30, screen.get_height()-15),
            (screen.get_width()-30, screen.get_height()-45), 5)
        pygame.draw.line(screen, (255, 255, 255),
            (screen.get_width()-45, screen.get_height()-30),
            (screen.get_width()-15, screen.get_height()-30), 5)

        pygame.display.flip()
            
if __name__ == "__main__":
    main()