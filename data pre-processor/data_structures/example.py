from typing import Any, List

class ImageData:
    def __init__(self, img: str, height: int, width: int, shapes: List[Any] = None):
        self.img = img
        self.height = height
        self.width = width
        self.shapes = shapes if shapes is not None else []

    def __str__(self):
        return (f"Image: {self.img}\n"
                f"Height: {self.height}\n"
                f"Width: {self.width}\n"
                f"Shapes: {self.shapes}")


if __name__ == "__main__":
     image_data = ImageData("/path/", 100, 200, ["shape1", "shape2"])
     print(image_data)