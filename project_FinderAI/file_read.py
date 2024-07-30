import os

class FileRead():
    def __init__(self, folder_path):
        self.image_path_names = self._extracting_images(folder_path)
        self.image_names = self._extracting_names(self.image_path_names)

    def _extracting_images(self, folder_path):
        return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    
    def _extracting_names(self, image_path_names):
        return [os.path.splitext(os.path.basename(f))[0] for f in image_path_names]
