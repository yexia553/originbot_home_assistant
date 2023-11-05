""""
从数据中获取最近的一张图片然后生产一个图片文件保存到本地
"""
from django.core.management.base import BaseCommand
import cv2
import numpy as np
from datetime import datetime
import base64

from monitor.models import ImageModel  # Replace 'myapp' with your actual app name


class Command(BaseCommand):
    help = 'Retrieve the latest image from database and save it to local system'

    def handle(self, *args, **kwargs):
        try:
            # Fetch the most recent image data from database
            img_obj = ImageModel.objects.latest('timestamp')

            decoded_img = base64.b64decode(img_obj.data)

            # Create a numpy array and reshape it into an OpenCV image matrix
            npimg = np.fromstring(decoded_img, dtype=np.uint8)
            img = cv2.imdecode(npimg, 1)

            # Save the file locally with timestamp in filename to differentiate multiple files
            now = datetime.now()
            time_string = str(now.strftime("%Y_%m_%d-%H_%M_%S"))
            filename = "image_" + time_string + ".jpg"

            cv_state = cv2.imwrite(filename, img)
            if cv_state:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully saved image as {filename}')
                )
            else:
                self.stdout.write(self.style.ERROR('Failed to write image.'))

        except ImageModel.DoesNotExist:
            self.stdout.write(self.style.WARNING('No images found in the database.'))
