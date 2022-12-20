import pygame
import math
import numpy as np

pygame.init()


def dist(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Computes the distance between (x1; y1) and (x2; y2)
    """
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def lerp(x1: float, y1: float, x2: float, y2: float, t: float) -> (float, float):
    """
    Computes a simple lerp function from the formula : (1-t)p0+tp1
    :param x1: x coordinate of the first point
    :param y1: y coordinate of the first point
    :param x2: x coordinate of the second point
    :param y2: y coordinate of the second point
    :param t: float between 0 and one representing how far on the segment the point is
    :return: Coordinates (x, y) of lerped point
    """
    return (1-t)*x1+t*x2, (1-t)*y1+t*y2


class Point:
    def __init__(self, x: float, y: float):
        """
        Creates a new point instance with position (x; y) and a radius
        """
        self.x = x
        self.y = y

        self.radius = 10

    def display(self, screen: pygame.Surface, color: tuple[int, int, int] = (0, 0, 0)) -> None:
        """
        Displays the point on screen
        :param screen: The screen window on which to draw the point
        :param color: The color to use to draw the point
        :return: None
        """
        pygame.draw.circle(
            screen,
            color,
            (self.x, self.y),
            self.radius
        )
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (self.x, self.y),
            self.radius - 4
        )

    def __repr__(self):
        return f"({self.x}; {self.y})"

    def collide(self, x: float, y: float):
        """
        Check if the point collides with (x; y)
        :param x: The x coordinate,
        :param y: The y coordinate,
        :return: bool if the point collides with (x; y)
        """
        if dist(x, y, self.x, self.y) < self.radius:
            return True
        return False


class Spline:
    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def display(self, screen):
        pygame.draw.line(screen, (0, 0, 0), (self.p1.x, self.p1.y), (self.p2.x, self.p2.y))
        pygame.draw.line(screen, (0, 0, 0), (self.p3.x, self.p3.y), (self.p4.x, self.p4.y))

        # For each value of t, calculating the bezier spline
        ts = np.linspace(0, 1, 200)
        for t in ts:
            to_lerp: list[Point] = [self.p1, self.p2, self.p3, self.p4]
            for _ in range(len(to_lerp)-1):
                new_points: list[Point] = []
                for i in range(len(to_lerp)-1):
                    new_points.append(Point(*lerp(
                        to_lerp[i].x, to_lerp[i].y,
                        to_lerp[i+1].x, to_lerp[i+1].y, t
                    )))
                to_lerp = new_points

            point = new_points[0]
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (point.x, point.y),
                2
            )


def main():
    screen: pygame.Surface = pygame.display.set_mode((1000, 800))
    pygame.display.set_caption("CarRacing-DQN")

    points: list[Point] = []
    moving_point = None  # index of the moving point in the point list
    last_moving_point = None

    splines: list[Spline] = []
    new_spline: list[Point] = []
    creating_new_spline: bool = False

    font = pygame.font.SysFont(name="Arial", size=25, bold=False, italic=False)
    print_text = font.render("PRINT", False, (255, 255, 255))

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    if last_moving_point is not None:
                        points.remove(last_moving_point)
                        spline_to_remove = None
                        for spline in splines:
                            if last_moving_point in (spline.p1, spline.p2, spline.p3, spline.p4):
                                spline_to_remove = spline
                                break
                        if spline_to_remove is not None:
                            splines.remove(spline_to_remove)
                        last_moving_point = None

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Find if mouse collides with an existing point
                    is_colliding = False
                    colliding_index = None
                    for i in range(len(points)):
                        if points[i].collide(*event.pos):
                            is_colliding = True
                            colliding_index = i
                            break

                    circle_distance = dist(screen.get_width() - 30,
                                           screen.get_height() - 30,
                                           event.pos[0], event.pos[1])

                    # Check if the mouse collides with the print button
                    collides_with_print = False
                    if screen.get_width()-145 < event.pos[0] < screen.get_width()-145+75:
                        if screen.get_height()-50 < event.pos[1] < screen.get_height()-10:
                            collides_with_print = True

                    if not is_colliding and circle_distance > 20 and not collides_with_print:
                        # If not any point is colliding with the mouse and that the user is not pressing the + button
                        if creating_new_spline:
                            # If already in the process of creating a spline,
                            # Then add a new point to the creating spline
                            point = Point(*event.pos)
                            new_spline.append(point)
                            points.append(point)
                            if len(new_spline) == 4:
                                # If 4 points in the creating spline, then the spline is ready
                                splines.append(Spline(*new_spline))
                                creating_new_spline = False
                                new_spline = []
                        else:
                            # If not in the process of creating a spline,
                            # Then simply add a new point to points.
                            points.append(Point(*event.pos))

                    elif colliding_index is not None:
                        # If we collide an existing point
                        if creating_new_spline:
                            # If in the process of creating a new spline,
                            # Then add that point to the points of the creating spline.
                            new_spline.append(points[colliding_index])
                            if len(new_spline) == 4:
                                splines.append(Spline(*new_spline))
                                creating_new_spline = False
                                new_spline = []
                        else:
                            # Else mark the point as the point moving to allow it to follow the mouse.
                            moving_point = colliding_index
                            last_moving_point = points[colliding_index]  # Is used then to delete points

                    elif circle_distance < 20:
                        # The + button is pressed
                        creating_new_spline = True

                    elif collides_with_print:
                        if len(splines) == 0:
                            print("No path created yet !")
                        else:
                            for spline in splines:
                                print("Spline : ", [spline.p1, spline.p2, spline.p3, spline.p4])

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    moving_point = None

            elif event.type == pygame.MOUSEMOTION:
                if moving_point is not None:
                    # Moving the point according to mouse movements
                    points[moving_point].x = event.pos[0]
                    points[moving_point].y = event.pos[1]

        screen.fill((255, 255, 255))

        for point in points:  # Draw the points
            point.display(screen)
        for point in new_spline:  # Drawing the points of a constructing spline in blue
            point.display(screen, (0, 0, 255))
        for spline in splines:  # Drawing the last moved point in red
            spline.display(screen)

        if last_moving_point is not None:
            last_moving_point.display(screen, color=(255, 0, 0))

        # Draw the + button
        pygame.draw.circle(
            screen,
            (0, 200, 50),
            (screen.get_width() - 30, screen.get_height() - 30),
            20
        )
        pygame.draw.line(screen, (255, 255, 255),
                         (screen.get_width() - 30, screen.get_height() - 15),
                         (screen.get_width() - 30, screen.get_height() - 45), 5)
        pygame.draw.line(screen, (255, 255, 255),
                         (screen.get_width() - 45, screen.get_height() - 30),
                         (screen.get_width() - 15, screen.get_height() - 30), 5)

        # Drawing the print track
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            (screen.get_width() - 145, screen.get_height() - 50, 75, 40)
        )
        screen.blit(print_text, (screen.get_width()-142, screen.get_height()-40))

        pygame.display.flip()


if __name__ == "__main__":
    main()
