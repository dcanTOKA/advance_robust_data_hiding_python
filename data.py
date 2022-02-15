from PIL import Image
import os


class Images:
    @staticmethod
    def get_cover(image_name):
        return Image.open(f"data/cover/{image_name}")

    @staticmethod
    def get_secret(image_name):
        return Image.open(f"data/secret/{image_name}")

    @staticmethod
    def get_envelopes():
        file_dir = "data/envelopes/"
        file_ext = ".jpeg"
        list_envelopes_names = [_ for _ in os.listdir(file_dir) if _.endswith(file_ext)]
        list_envelopes_images = []
        for env in list_envelopes_names:
            print(f"Reading the file : {env}")
            list_envelopes_images.append(Image.open(f"{file_dir}/{env}"))
        return list_envelopes_images

