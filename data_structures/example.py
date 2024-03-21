from typing import Any, List

class ImageData:
    """_summary_
    object to store image data of each example in dataset.
    """
    def __init__(self, image_dir: str, height: int, width: int, jaw: str, shapes: List[Any] = None):
        self.image_dir = image_dir
        self.height = height
        self.width = width
        self.shapes = shapes if shapes is not None else []
        
        if jaw.lower() not in ["upper", "lower"]:
            raise Exception("Jaw must be either 'upper' or 'lower'")
        
        self.jaw = jaw.lower()

    def __str__(self):
        return (f"Image Directory: {self.image_dir}\n"
                f"Height: {self.height}\n"
                f"Width: {self.width}\n"
                f"Jaw: {self.jaw}\n"
                f"Shapes: {self.shapes}")


if __name__ == "__main__":
     image_data = ImageData("/path/", 100, 200, "upper", ["shape1", "shape2"])
     print(image_data)