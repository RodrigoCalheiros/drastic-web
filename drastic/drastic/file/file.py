import os
import settings
from werkzeug.utils import secure_filename

class File:

    def allowed_file(self, filename, allow_extensions):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allow_extensions

    def save(self, file, folder):
        filename = secure_filename(file.filename)
        return file.save(os.path.join(folder, filename))