"""
Author :    Alia Mahama-Rodriguez
Server for receiving requests and sending responses to clients.
"""

# concurrent.futures module provides a high-level interface for asynchronously executing callables.
from concurrent import futures
from dataclasses import dataclass

import logging

# Import generated files from ./build proto-compiler
import grpc
from google.rpc import error_details_pb2
from grpc_status import rpc_status
import image_pb2, image_pb2_grpc
from image_pb2 import(NLImage, NLImageRotateRequest)



# Import image_processing.py script.
from image_processing import rotate_image, convert_image_to_NLImage

# Import Threading --> threading will be used to run multiple threads (tasks, function calls) concomitantly.
import threading
import numpy as np
from PIL import Image
from argparse import ArgumentParser

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


#Options for gRPC server.
options = [('grpc.max_send_message_length', 512 * 1024 * 1024), ('grpc.max_receive_message_length', 512 * 1024 * 1024)]
logging.info("Session Start")

class NLImageService(image_pb2_grpc.NLImageServiceServicer):
    def RotateImage(self, request, context):
        if request.rotation == NLImageRotateRequest.Rotation.NONE:
            return request.image

        ROTATIONS = {
            NLImageRotateRequest.Rotation.NINETY_DEG : cv2.ROTATE_90_COUNTERCLOCKWISE,
            NLImageRotateRequest.Rotation.ONE_EIGHTY_DEG : cv2.ROTATE_180,
            NLImageRotateRequest.Rotation.TWO_SEVENTY_DEG : cv2.ROTATE_90_CLOCKWISE,
        }

        image_bytes_nparr = np.frombuffer(request.image.data, np.uint8)
        image_cv2 = cv2.imdecode(image_bytes_nparr, cv2.IMREAD_COLOR if 
            request.image.color else cv2.IMREAD_GRAYSCALE)

        if image_cv2.size == 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                "Image data buffer is too short or contains invalid data")
        rotated_image = cv2.rotate(image_cv2, ROTATIONS[request.rotation])

        if request.rotation == NLImageRotateRequest.Rotation.ONE_EIGHTY_DEG:
            rotated_image_width = request.image.width
            rotated_image_height = request.image.height
        else:
            rotated_image_width = request.image.height
            rotated_image_height = request.image.width

        return NLImage(
            color = request.image.color,
            width = rotated_image_width,
            height = rotated_image_height,
            data = cv2.imencode(".PNG", rotated_image)[1].tobytes()
        )
    
    def MeanFilter(self, nl_image, context):
        # IDEA: make this a parameter in request proto to customize blur level
        # recommend changing to (15,15) to get noticeable blurring;
        KERNEL_SIZE = (3,3)

        image_bytes_nparr = np.frombuffer(nl_image.data, np.uint8)
        image_cv2 = cv2.imdecode(image_bytes_nparr, cv2.IMREAD_COLOR if 
            nl_image.color else cv2.IMREAD_GRAYSCALE)
        if image_cv2.size == 0:
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                "Image data buffer is too short or contains invalid data")
        mean_image = cv2.blur(image_cv2,KERNEL_SIZE)

        return NLImage(
            color = nl_image.color,
            width = nl_image.width,
            height = nl_image.height,
            data = cv2.imencode(".PNG", mean_image)[1].tobytes(),
        )

# '--host' and '--port' arguments that will allocate host and port of sev
def serve(host, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    image_pb2_grpc.add_NLImageServiceServicer_to_server(NLImageService(), server)
    server.add_insecure_port(f"{host}:{port}")
    server.start()
    logger.info(f"Serving at {host}:{port}")
    server.wait_for_termination()

# `--port` and `--host` arguments that specify the host and port of the server.
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Configure host and port for server")
    parser.add_argument("--host",type=str,required=True)
    parser.add_argument("--port",type=int,required=True)

    args = parser.parse_args()
    serve(args.host, args.port)
