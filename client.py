"""
Author :    Alia Mahama-Rodriguez
To interact with provided 'server.py', client.py will first create a channel to the server and create a stub object to
interact with the users service via this channel.
"""
#!/usr/bin/python3 
import io 
from PIL import image
import argparse


# Import the generated classes.
import grpc
import image_pb2
import image_pb2_grpc
from image_pb2 import (NLImage, NLImageRotateRequest)

# Import image_processing.py

# Data encoding.
import numpy as np
import logging


logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


"""
Client Arguments:
'--input'   : allocates location of input .jpg or .png image file.
'--output'  : specifies path of output image file. 
'--rotate'  : takes string argument form of the rotation in multiples of 90 (e.g., NINETY_DEG).
'--mean'    : invokes mean filter on NLImage.
"""
class NLImageClient():
    def __init__(self, host: str, port: int):
        # open connection to server
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        logger.info(f"Connected to {host}:{port}")
        # bind the client and the server
        self.stub = image_pb2_grpc.NLImageServiceStub(self.channel)

    def rotate_image(self, image_filepath: str, rotation_string: str):
        rotation_map = {
            "NONE" : NLImageRotateRequest.Rotation.NONE,
            "NINETY_DEG" : NLImageRotateRequest.Rotation.NINETY_DEG,
            "ONE_EIGHTY_DEG" : NLImageRotateRequest.Rotation.ONE_EIGHTY_DEG,
            "TWO_SEVENTY_DEG" : NLImageRotateRequest.Rotation.TWO_SEVENTY_DEG
        }

        image = Image.open(image_filepath)
        # retrieve binary content (bytes) of image
        image_bytes = io.BytesIO()
        image.save(image_bytes, format=image.format)

        request = NLImageRotateRequest(
            image = NLImage(
                color = image.mode == "RGB",
                data = image_bytes.getvalue(),
                width = image.width,
                height = image.height
            ),
            rotation = rotation_map[rotation_string]
        )
        try:
            return self.stub.RotateImage(request)
        except grpc.RpcError as e:
            logger.error(f"{e.code()}: {e.name}={e.value}. {e.details()}")
    
    def mean_image(self, image_filepath: str):
        image = Image.open(image_filepath)
        image_bytes = io.BytesIO()
        image.save(image_bytes, format=image.format)
        
        nl_image = NLImage(
            color = image.mode == "RGB",
            data = image_bytes.getvalue(),
            width = image.width,
            height = image.height
        )
        try:
            return self.stub.MeanFilter(nl_image)
        except grpc.RpcError as e:
            logger.error(f"{e.code()}: {e.name}={e.value}. {e.details()}")

    def save_image(self, image: NLImage, output_filepath: str):
        image = Image.open(io.BytesIO(image.data))
        image.save(output_filepath)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Configure host and port for server")
    parser.add_argument("--input",type=str,required=True)
    parser.add_argument("--output",type=str,required=True)
    parser.add_argument("--host",type=str,required=True)
    parser.add_argument("--port",type=int,required=True)

    parser.add_argument("--rotate",type=str)
    parser.add_argument("--mean", action="store_true")

    args = parser.parse_args()
    if args.rotate is None and not args.mean:
        parser.error("Must specify rotate,mean or both")
    else:
        client = NLImageClient(args.host,args.port)
        if args.rotate:
            image = client.rotate_image(args.input,args.rotate)
            client.save_image(image,args.output)
        if args.mean:
            if args.rotate:
                image_filepath = args.output
            else:
                image_filepath = args.input
            image = client.mean_image(image_filepath)
            client.save_image(image,args.output)
        logger.info(f"Saving image to {args.output}")
