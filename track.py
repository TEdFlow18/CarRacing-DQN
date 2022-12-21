import pygame
import math
import numpy as np
from point import Point


def lerp(x1: float, y1: float, x2: float, y2: float, t: float) -> (float, float):
    """
    Uses the following formula to compute an intermediate point between (x1; y1) and (x2; y2):
        (1-t)p1+tp2
    :param x1: x coordinate of the first point
    :param y1: y coordinate of the first point
    :param x2: x coordinate of the second point
    :param y2: y coordinate of the second point
    :param t: float between 0 and 1 indicating how far the intermediate point is from the first one.
    :return: (x, y) coordinates of the intermediate point
    """
    return (1 - t) * x1 + t * x2, (1 - t) * y1 + t * y2


class FullTrack:
    """
    Represents a track on which cars will race.
    The track is mainly composed of track_parts which added together make the whole track
    """

    def __init__(self):
        self.track_parts: list[TrackPart] = []

    def create_track_from_file(self, filepath: str) -> None:
        """
        Creates the track from an existing file
        The file must have a blank line at the end of it.
        The lines in the file must be ordered. If not track won't load correctly
        :param filepath: a string representing the path to the file containing the data
        :return: None
        """
        with open(filepath, "r") as file:
            for line in file.readlines():
                points_str: list[list[str]] = [["", ""]]
                xs: bool = True
                for character in line[:-1]:
                    if character == ",":
                        points_str.append(["", ""])
                        xs = True
                    elif character == ";":
                        xs = False
                    else:
                        points_str[-1][0 if xs else 1] += character

                points: list[Point] = []
                for point in points_str:
                    points.append(Point(float(point[0]), float(point[1])))
                self.track_parts.append(TrackPart(*points))

    def display(self, screen: pygame.Surface) -> None:
        left_points: list[Point] = []
        right_points: list[Point] = []
        for track_part in self.track_parts:
            (start_left_point, start_right_point), (end_left_point, end_right_point) = track_part.display(screen)
            left_points.append(start_left_point)
            left_points.append(end_left_point)
            right_points.append(start_right_point)
            right_points.append(end_right_point)

        for i in range(-1, len(left_points)-1, 2):
            pygame.draw.line(
                screen,
                color=(0, 0, 0),
                start_pos=(left_points[i].x, left_points[i].y),
                end_pos=(left_points[i+1].x, left_points[i+1].y)
            )
            pygame.draw.line(
                screen,
                color=(0, 0, 0),
                start_pos=(right_points[i].x, right_points[i].y),
                end_pos=(right_points[i+1].x, right_points[i+1].y)
            )


class TrackPart:
    """
    Represents a part of a track.
    Consists of a bezier cubic curve with the point p1, p2, p3 and p4.
    """

    def __init__(self, p1: Point, p2: Point, p3: Point, p4: Point):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

        self.points: list[Point] = [self.p1, self.p2, self.p3, self.p4]

        # Computes the track useful for the display function
        path_points: list[Point] = []

        ts = np.linspace(0, 1, 20)
        for t in ts:
            points_to_lerp_on: list[Point] = self.points[::]
            for _ in range(len(points_to_lerp_on) - 1):
                new_points: list[Point] = []
                for i in range(len(points_to_lerp_on) - 1):
                    new_points.append(Point(
                        *lerp(points_to_lerp_on[i].x, points_to_lerp_on[i].y,
                              points_to_lerp_on[i + 1].x, points_to_lerp_on[i + 1].y, t)
                    ))
                points_to_lerp_on = new_points

            assert len(points_to_lerp_on) == 1
            last_point = points_to_lerp_on[0]
            path_points.append(last_point)  # Points in the middle of the track

        self.left_points: list[Point] = []
        self.right_points: list[Point] = []
        for i in range(len(path_points) - 1):
            first: Point = path_points[i]
            second: Point = path_points[i + 1]
            middle: Point = Point((first.x + second.x) / 2, (first.y + second.y) / 2)

            # Computes the angle of the slope between pairs of middle points
            u: tuple[float, float] = (1., 0.)
            u_mag: float = 1.
            v: tuple[float, float] = (second.x - middle.x, second.y - middle.y)
            v_mag: float = math.sqrt(v[0] ** 2 + v[1] ** 2)
            angle: float = math.acos((u[0] * v[0] + u[1] * v[1]) / (u_mag * v_mag))
            if v[1] < 0:
                angle *= -1

            # Changes the angle to get left and right points of the track
            rotated_angle_inside: float = (angle + math.pi / 2) % (2 * math.pi)
            rotated_angle_outside: float = (angle - math.pi / 2) % (2 * math.pi)

            # left coordinates of the track
            x1 = middle.x + 30 * math.cos(rotated_angle_inside)
            y1 = middle.y + 30 * math.sin(rotated_angle_inside)

            # right coordinates of the track
            x2 = middle.x + 30 * math.cos(rotated_angle_outside)
            y2 = middle.y + 20 * math.sin(rotated_angle_outside)

            self.left_points.append(Point(x1, y1))
            self.right_points.append(Point(x2, y2))

    def __repr__(self):
        representation = ""
        for i in range(len(self.points)):
            representation += str(self.points[i])
            if i != len(self.points) - 1:
                representation += ", "
        return representation

    def display(self, screen: pygame.Surface) -> tuple[tuple[Point, Point], tuple[Point, Point]]:
        for i in range(len(self.left_points)-1):
            pygame.draw.line(
                screen,
                color=(0, 0, 0),
                start_pos=(self.left_points[i].x, self.left_points[i].y),
                end_pos=(self.left_points[i+1].x, self.left_points[i+1].y)
            )
            pygame.draw.line(
                screen,
                color=(0, 0, 0),
                start_pos=(self.right_points[i].x, self.right_points[i].y),
                end_pos=(self.right_points[i+1].x, self.right_points[i+1].y)
            )
        return (self.left_points[0], self.right_points[0]), (self.left_points[-1], self.right_points[-1])
