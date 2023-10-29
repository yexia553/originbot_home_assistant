# A simplified example.
import cv2
from django.core.management.base import BaseCommand
from django.conf import settings
import numpy as np
import base64
from monitor.models import ImageModel


def frames_to_video():
    # Read all images from database.
    images = ImageModel.objects.all()

    # Define the codec and create VideoWriter object.
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(
        str(settings.BASE_DIR) + '/output.mp4', fourcc, 20.0, (640, 480)
    )

    for image in images:
        decoded_data = base64.b64decode(image.data)
        nparr = np.fromstring(decoded_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if frame is None:
            print('Failed to decode image with timestamp:', image.timestamp)
            continue

        # Resize the frame to required dimensions if necessary
        frame = cv2.resize(frame, (640, 480))
        out.write(frame)

    # Release everything after writing.
    out.release()


class Command(BaseCommand):
    def handle(self, *args, **options):
        frames_to_video()
