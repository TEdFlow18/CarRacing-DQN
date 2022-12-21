import pygame
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
    return (1-t)*x1+t*x2, (1-t)*y1+t*y2


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

        for track_part in self.track_parts:
            print(track_part)

    def display(self, screen: pygame.Surface) -> None:
        for track_part in self.track_parts:
            track_part.display(screen)


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

    def __repr__(self):
        representation = ""
        for i in range(len(self.points)):
            representation += str(self.points[i])
            if i != len(self.points)-1:
                representation += ", "
        return representation

    def display(self, screen: pygame.Surface) -> None:
        ts = np.linspace(0, 1, 20)
        for t in ts:
            points_to_lerp_on: list[Point] = self.points[::]
            for _ in range(len(points_to_lerp_on)-1):
                new_points: list[Point] = []
                for i in range(len(points_to_lerp_on)-1):
                    new_points.append(Point(
                        *lerp(points_to_lerp_on[i].x, points_to_lerp_on[i].y,
                              points_to_lerp_on[i+1].x, points_to_lerp_on[i+1].y, t)
                    ))
                points_to_lerp_on = new_points

            assert len(points_to_lerp_on) == 1
            last_point = points_to_lerp_on[0]
            pygame.draw.circle(
                screen,
                color=(255, 0, 0),
                center=(last_point.x, last_point.y),
                radius=5
            )
