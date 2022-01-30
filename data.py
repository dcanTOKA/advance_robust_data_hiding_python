from PIL import Image


class Images:
    @staticmethod
    def get_cover(image_name):
        return Image.open(f"data/cover/{image_name}")

    @staticmethod
    def get_secret(image_name):
        return Image.open(f"data/secret/{image_name}")
