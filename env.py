import pygame
from track import FullTrack


def main():
    pygame.init()

    screen: pygame.Surface = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("CarRacing-env")

    track: FullTrack = FullTrack()
    track.create_track_from_file("./track_points.txt")

    # TODO : add a car class
    # TODO : create a zoom following the car : the car isn't moving relatively to the window.
    #  It's the track which moves around.

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 255, 0))

        track.display(screen)

        pygame.display.flip()


if __name__ == "__main__":
    main()
