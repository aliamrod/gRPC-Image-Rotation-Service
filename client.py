"""
Author :    Alia Mahama-Rodriguez
To interact with provided 'server.py', client.py will first create a channel to the server and create a stub object to
interact with the users service via this channel.
"""
#!/usr/bin/python3 
from __future__ import print_function
from flask import Flask, flash, request, redirect, url_for, render_template_string
from pathlib import Path 
import time 
import argparse

# Import the generated classes.
import grpc
import image_pb2
import image_pb2_grpc
from image_pb2 import (NLImage, NLImageRotateRequest)

# Import image_processing.py
from image_processing import convert_imagefile_to_NLImage, save_image, convert_image_to_NLImage, convert_bytes_to_image

# Data encoding.
import numpy as np
import logging

from PIL import Image
import imghdr

from pathlib import Path
import sys, os, getopt

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
    def client():
        parser = argparse.ArgumentParser()
        parser.add_argument("-i", "--input",help ="Allocate location of the input image (e.g., .jpeg, .png", type=str,required=True)
        parser.add_argument("-o", "--output",type=str, help = "Allocate output image's file path.", required=True)
        parser.add_argument("-r", "--rotate",help = "Specify whether angle of rotation applied to raw input image (e.g., NONE, NINETY_DEG, ONE_EIGHTY_DEG, TWO_SEVENTY_DEG)." , type=str)
        parser.add_argument("-m", "--mean", help = "Specify whether mean filter will be applied to raw input image.", action="store_true")
        parser.add_argument("-h", "--host",type=str, help = "Specify host of the server.", required=True)
        parser.add_argument("-p", "--port",type=int,help = "Specify the port of the server.", required=True)
        # Parse command-line arguments.
        args = parser.parse_args()
    # Validate input file.
        try:
            image = Image.open(args.input)
            type_input = image.format
            if type_input == "JPEG" or "PNG":
                valid_image = True
            if valid_image:
                logging.info("The system has verified validity of input image file.")
        except:
            logging.error("INVALID. The system has denied the input image file. Please verify that the file is either .JPEG or .PNG.")
            sys.exit(1)
        # Validate output file path.
        try:
            if args.output.exists():
                valid_output = True
            if valid_output:
                logging.info("The system has verified validity of output file path. Please proceed for further image processing.")
        except:
            logging.error("INVALID. The system has denied the entered output file path. Please verify that the entered string is correct.")
            sys.exit(1)
    
        # Validate Image Processing Pipeline(s).
        try:
            if args.mean_filter or args.rotate:
                image_processing_pipeline = True
            if image_processing_pipeline:
                logging.info("The system has confirmed the implication of one or more image processing modalities. System will proceed to pass these argument(s).")
        except:
            logging.error("No image processing pipeline/operation has been implicated. Please proceed to pass at least one image processing operation to move forward.")
        
def __init__(self, host: str, port: int):
# Open connection to server
    self.channel = grpc.insecure_channel(f"{host}:{port}")
    # Bind host:client components.
    logger.info(f"System is connected to {host}:{port}")
    self.stub = image_pb2_grpc.NLImageServiceStub(self.channel)

def rotate_image(self, image_filepath: str, rotation_string: str):
    # System retrieving byte data content of input file.
    rotation_map = {
        "NONE": NLImageRotateRequest.Rotation.NONE,
        "NINETY_DEG": NLImageRotateRequest.Rotation.NINETY_DEG,
        "ONE_EIGHTY_DEG": NLImageRotateRequest.Rotation.ONE_EIGHTY_DEG,
        "TWO_SEVENTY_DEG": NLImageRotateRequest.Rotation.TWO_SEVENTY_DEG
    }
    image = Image.open(image_filepath)
    image_bytes = io.BytesIO()
    image.save(image_bytes, format=image.format)

    request = NLImageRotateRequest(
        image = NLImage(color = image.mode == "RGB", data = image_bytes.getValue(), width = image.width, height = image.height),
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
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input",help ="Allocate location of the input image (e.g., .jpeg, .png", type=str,required=True)
    parser.add_argument("-o", "--output",type=str, help = "Allocate output image's file path.", required=True)
    parser.add_argument("-r", "--rotate",help = "Specify whether angle of rotation applied to raw input image (e.g., NONE, NINETY_DEG, ONE_EIGHTY_DEG, TWO_SEVENTY_DEG)." , type=str)
    parser.add_argument("-m", "--mean", help = "Specify whether mean filter will be applied to raw input image.", action="store_true")
    parser.add_argument("-h", "--host",type=str, help = "Specify host of the server.", required=True)
    parser.add_argument("-p", "--port",type=int,help = "Specify the port of the server.", required=True)
    
    # Parse command-line arguments.
    args = parser.parse_args()
    
    # Parse command-line arguments.
    #args = parser.parse_args()
    if args.rotate is None and not args.mean:
        parser.error("Must specify rotate, mean or both")
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
