import pygame
from point import Point


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

    def display(self, screen: pygame.Surface) -> None:
        pass
