import os
import settings
import zipfile
from werkzeug.utils import secure_filename
from pyunpack import Archive

class File:
    def __init__(self, file):
        self.file = file

    def allowed_file(self, allow_extensions):
        return '.' in self.file.filename and self.file.filename.rsplit('.', 1)[1].lower() in allow_extensions

    def save(self, folder, name):
        filename = secure_filename(self.file.filename)
        print (filename)
        return self.file.save(os.path.join(folder, name))
    
    def unzip(self, folder_output):
        print (self.file)
        print (folder_output)
        print (self.file.filename)
        output_file = "filee." + self.file.filename.rsplit('.', 1)[1]
        self.save(folder_output, output_file)
        if (self.file.filename.rsplit('.', 1)[1].lower() in {"zip", "rar"}):
            Archive(self.file).extractall(folder_output)