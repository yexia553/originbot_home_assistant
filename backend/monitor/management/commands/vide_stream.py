# A simplified example.
import cv2
from django.core.management.base import BaseCommand
from django.conf import settings
from monitor.models import ImageModel


def frames_to_video():
    # Read all images from database.
    images = ImageModel.objects.all()

    # Define the codec and create VideoWriter object.
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(settings.BASE_DIR + '/output.mp4', fourcc, 20.0, (640, 480))

    for image in images:
        frame = ...  # recover the frame data from your model
        # Write the frame into the file 'output.mp4'.
        out.write(frame)

    # Release everything after writing.
    out.release()


class Command(BaseCommand):
    def handle(self, *args, **options):
        frames_to_video()
