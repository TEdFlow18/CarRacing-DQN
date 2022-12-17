import pygame
import math
pygame.init()

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
        if math.sqrt((self.x-x)**2+(self.y-y)**2) < self.radius:
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
                    if not is_colliding:
                        points.append(Point(*event.pos))
                    else:
                        moving_point = colliding_index

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

        pygame.display.flip()
            
if __name__ == "__main__":
    main()