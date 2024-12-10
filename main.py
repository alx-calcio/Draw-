import tkinter as tk
from collections import namedtuple
from typing import List
from statistics import mean

Point = namedtuple(typename="Point", field_names=["x", "y"])
canvas = 0
shapes = []
points = []


def create_window() -> None:
    global canvas
    window = tk.Tk()
    window.title("Draw")
    canvas = tk.Canvas(window, width=800, height=800)
    canvas.pack(fill="both", expand=True)
    canvas.bind("<Button-1>", on_click)
    canvas.bind("<B1-Motion>", on_move)
    canvas.bind("<ButtonRelease-1>", on_release)
    window.mainloop()


def on_click(event) -> None:
    global points
    points = [Point(event.x, event.y)]


def on_move(event):
    global points
    global canvas
    canvas.create_line(points[-1].x, points[-1].y, event.x, event.y)
    points.append(Point(event.x, event.y))


def on_release(event):
    global canvas
    global shapes
    canvas.delete("all")
    if detect_strokes():
        for stroke in detect_strokes():
            shapes.append((stroke[0].x, stroke[0].y, stroke[-1].x, stroke[-1].y))
    for shape in shapes:
        canvas.create_line(*shape)


def detect_strokes():
    global points
    derivatives_list = []
    for result in get_derivative(get_derivative(points)):
        derivatives_list.append(abs(result.y))
    if mean(derivatives_list) < 0.5:
        is_on_inflexion = True
        strokes_list = []
        print(derivatives_list)
        for index, derivative in enumerate(derivatives_list):
            if derivative < 0.5 and is_on_inflexion:
                first_point = Point(mean([points[index].x, points[index+2].x]), mean([points[index].y, points[index+2].y]))
                strokes_list.append([first_point])
                is_on_inflexion = False
            elif derivative > 0.5 and not is_on_inflexion:
                last_point = Point(mean([points[index].x, points[index+2].x]), mean([points[index].y, points[index+2].y]))
                strokes_list[-1].append(last_point)
                is_on_inflexion = True
            print(strokes_list)
        if len(strokes_list[-1]) == 1:
            strokes_list[-1].append(Point(points[-1].x, points[-1].y))
        return strokes_list


def get_derivative(points: List[Point]) -> List[Point]:
    derivatives_list = []
    for index in range(len(points) - 1):
        if points[index].x != points[index + 1].x:
            derivative = (points[index].y - points[index + 1].y) / (
                points[index].x - points[index + 1].x
            )
            derivatives_list.append(
                Point(mean([points[index].x, points[index + 1].x]), derivative)
            )

        else:
            derivatives_list.append(
                Point(mean([points[index].x, points[index + 1].x]), 0)
            )
    return derivatives_list


if __name__ == "__main__":
    create_window()
