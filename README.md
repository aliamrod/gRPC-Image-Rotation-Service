# gRPC-Image-Rotation

## A. Overview.
gRPC is a framework for Google. It provides an efficient and language-independent way to make Remote Procedure Calls. gRPC builds on HTTP/2 and the Protobuf message-encoding protocol to provide high performance, low-bandwidth communication between applications and services. It supports server and client code generation across most popular programming languages and platforms, including .NET, Java, Python, Node.js, Go and C++. The major usecase for gRPC is the making of remote procedure calls performant while ensuring language independence. Remote procedure calls play an important role in data microservices/distributed environment where is transferred across services. Notably, in comparison to REST, gRPC operates faster. The only limited support on browser side, gRPC requires gRPC-Web as a proxy layer to convert between HTTP/2 to HTTP/1.1.

![1_2Ku04PlBecXfkXZKmWm6Qg](https://user-images.githubusercontent.com/62684338/169071946-c89fe98e-d3dd-4d3e-80c9-aff10daef717.png)

The following module contains a series of gRPC-based image processing and storage microservices. ImageAdapt takes a raw, original image and proceeds to perform a set of operations to process. 
 
 The following gRPC Python3 client-server model runs two microservices:
- [x] Rotation: An arbitrary input image is rotated at a certain angle counter-clockwise and the final image will be saved as an output file. The called argument will specify the path of the output image. 
- [x] Image filtering: Median filter, a non-linear digital filtering technique utilized in image processing, will reduce noice in order to  improve results of             downstream processing (e.g. edge detection on an image). 

In summation, the structure of the gRPC architecture contains the following:
- [x] Parallel Image Processing and Storage
- [x] NLI Server 
- [x] NLI Client
- [x] Test Client-Server Model


**********************

## B. Setup and Installation. 
This setup guide assumes the user is using <ins>Ubuntu 18.04</ins>. 
 1. Save this directory, and all affiliated files to a desired location.
 2. The Google protobuf compiler (which is a standalone binary named ```protoc```) needs to be installed somewhere on your ```$PATH```. This may be achieved  performing the following Windows-specific operations for installing the binary. * These instructions also install basic ```.proto``` files (i.e. ```wrappers.proto```, ```any.proto```, and ```descriptor.proto```. 
 ```
PROTOC_INSTALL=protoc-3.20.1-win64.zip
curl -OL https://github.com/protocolbuffers/protobuf/releases/download/v3.20.1/$PROTOC_INSTALL
unzip protoc-3.20.1-win64.zip -d protoc3
 ```
 4. Clean install of Python 3.9 or above; ```pip``` version 9.0.1 or higher. If necessary, upgrade your version by entering 
```$ python3 -m pip install --upgrade pip```. If you cannot upgrade ```pip``` due to a system-owned installation, you can run the example in a virtualenv:
```$ python3 -m pip install virtualenv
   $ virtualenv venv
   $ source venv/bin/activate
   $ python3 -m pip install --upgrade pip
```
 3. Install gRPC and Python's gRPC tools which include the protocol buffer compiler ```protoc``` and the special plugin for generating server and client code from ```.proto``` service definitions.
```
$ python3 -m pip install grpcio
$ python3 -m pip install grpcio-tools
```
 4. In order to execute the gRPC streaming, verify the following pre-requisite pip libraries have been installed (requirements.txt). NOTE: You may possibly want to add a virtual environment (optional). 
 5. Verify that the setup/build files are executable using: ```chmod +x ./setup``` and ```chmod +x ./build```.
 6. Use the protoc compiler to compile the image.proto file to code artifacts. Unlike NodeJS, Python classes will not be able to read the .proto files directly, thus implying the required conversion of .proto files to native Python classes. Running `build` invokes the Protocol Compiler and consequently generates two Python class files *sample_pb2_grpc.py* and *sample_pb2.py*. * Note: Upon inspection, image_pb2_grpc.py will include three generated classes, two of which are GEchangeServicer and GExchangeStub. You will use them to implement server-side code and client code, respectively
 7. Run the setup file, ```./setup```. 
```
$ python3 server.py
$ python3 client.py
```
If there are changes made to the ./proto/image.proto or changes to the services or message classes in ./src/server.py or ./src/client.py, navigate to ./src/ and run the following to update ./src/image_pb2.py and ./src/image_pb2_grpc.py:
```
$ python -m grpc_tools.protoc -I../../protos --python_out=. --grpc_python_out=. ../../protos/image.proto
```

Note: The provided code places the server at an unsecure local port. This is for the convenience of deploying and testing the server locally. It is recommendable to change to a secure port (using ```server.add_secure_port```) with credentials when deploying this externally.

**********************

 ## D. Running and Deploying Server-Client Scripts. 
 To start the server, navigate to the root source directory commanding ```cd ./grpc-image-service-prompt/``` and run the server using ```python3 server.py```. Once the server is running, navigate to the source directory (see above), open a new terminal and run the client script by entering ```python3 client.py```.
 
 
  
 ## E. Discussion.
 
 * Design Overview. 
   
   
   mean_filter => function that is implicated to blur an image in order to remove noise. It involves determinign the mean of th pixel values within a n x n kernel. The pixel intensity of the center element is then replaced the mean value. This eliminates some of he noise in the image and smooths the edges of the image. The blur function from the OpenCV library has been included in otder to apply the mean filter to the image. 
   


When dealing with color images it is first necessary to convert from RGB to HSV since the dimensions of RGB are dependent on one another where as the three dimensions in HSV are independent of one another (this allows us to apply filters to each of the three dimensions separately.)

The following is a python implementation of a mean filter:

**********************   
 
 ## E. Conclusion and Future Scope for Improvement.
 
Due to time constraints, a more elaborate structure to the gRPC-framework was not implemented. I recommend the following implementations in the future:
Streaming RPC:

 
 Other frameworks are recommended over the gRPC modality 



Future Scope for Improvement.




Due to time constraints, the following were not implemented. I recommend such improvements:

* Streaming RPC
  
 It is a common misconception that streaming RPCs, 
  
  
  In Python however, Streaming RPCs create additional threads for receiving and possibly sending the messages, which makes streaming RPCs much slower than unary RPCs in gRPC Python, unlike the other languages supported by gRPC (e.g., GoLang, C++, Java).
  
  
  ![1_RDb-hNTukaL0maxTctocXw](https://user-images.githubusercontent.com/62684338/169076270-760cede7-af5e-412c-9e35-64dd91005076.png) Figure 05. Unary Service. 

  
  An alternative to the unary RPC would be a streaming RPC which would allow multiple chunks of messages to be sent as requests and responses. One of the limitations of the image rotation service is the inability to send over large images in a single message request. A bidirectional streaming RPC would allow the client to break down the image into several messages and send a stream of these messages to the server. The server may then send back the rotated image in a stream of messages as well. This will allow the transfer of large images for the rotation service.

A streaming RPC is unnecessary for the current implementation of the facial recognition service. Because the facial recognition model operates with 30 pixels by 57 pixels greyscale images, all images, regardless of size, is downsampled prior to sending to the server. Therefore, an unary RPC would be sufficient for sending the entire image.
  
  It is recommandable to utilize streaming RPCs, when handling a long-lived logical flow of data from the client-to-server, server-to-client, or in both directions. Streams can avoid contiguous RPC initiation, which includes connection load balancing at the client-side, generating a new HTTP/2 request at the transport layer, and invoking a user-defined method handler on the server side. The primary concern however, lies in the notion that streams cannot be load-balanced once they have started and can be hard to debug for stream failures. They also may increase performance at a small, negligible scale but can reduce scalability due to load balancing and complexity, so they should only be used when they provide substantial performance or simplicity benefit to application logic. In summation, streaming RPC is recommendable for the optimization of the Image Rotation Service, not gRPC itself. 
 
 
 
 * 
  
  

Using asyncio could improve performance.

Using the future API in the sync stack results in the creation of an extra thread. Avoid the future API if possible.

(Experimental) An experimental single-threaded unary-stream implementation is available via the SingleThreadedUnaryStream channel option, which can save up to 7% latency per message.
  
  
  
  

* 


Thread pooling
While the current implementation may be sufficient for a small team of engineers who are not running this service automated or concurrently, this server may be unable to handle high traffic from many requests sent at the same time. Using a large thread pool where a large number of threads is set and made available for concurrent requests would help mitigate this problem. Ideally, in the scenario where all the threads are occupied, additional requests would be queued. However, performance will then be dependent on the number of available processors because more processors would be necessary to handle higher number of threads and concurrent requests.

Because our implementation is in Python, the global interpreter lock (GIL) will limit the number of threads to the available processor cores, preventing a high number of threads from being executed at once. This is a major limitation to the deployment of such a server for high traffic applications.

Image type support
The following server has been tested with .jpg and .png images. Further testing and additional support for images of other file types (e.g., .webm) may be necessary.







Scope for improvement:

One of the bottlenecks in the current implementation is that the byte-buffer should have the information encoded in uint8, else there could be improper parsing of the encoded information. The intuition behind this is to ensure that Pillow (Image-processing library from Python) reads the images, and doesn't through an error especially when reading RGB images as it doesn't accept floats. Applying the mean filter is bound to introduce some floats into the arrays, hence the typecasting needed. One possible further implementation could be to be able to extend the datatypes to float.
One possible case that the scripts omit is the output NLImage sent from the server back to the client, it has to be parsed exactly as shown in the client code which is converting the whole 3D matrix to bytes rather than arranging it as triplets as specified earlier. This has been left as it is due to time constraints.
Another potential future implementation would be avoiding the use of pre-existing packages and write code from scratch for both the in-place rotation and mean-filter operations.
With more resources and time, I would have loved tp deploy the scripts on the cloud (Google Compute Engine, or an AWS Instance), and increase the number of workers in the GRPC server so that the number of clients can access the server simultaneously doesn't saturate. I would do an intermittent test to evaluate the client-server tests, latency.
Lastly, the edge cases. The server script is able to throw an error when an invalid format of data (datatype or dimensions) is sent through the bytes in the NLImage, or if NaN cases exist in the data. In such cases, the server throws an error, and exits the execution although that doesn't terminate the execution of the server, i.e., it can still handle requests from other servers.
If given more invalid images passed through the NLImage, I can make the whole implementation error-free and crash proof.
