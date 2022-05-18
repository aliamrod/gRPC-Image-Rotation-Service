# gRPC-Image-Rotation

## A. Overview.
gRPC is a framework for Google. It provides an efficient and language-independent way to make Remote Procedure Calls. gRPC builds on HTTP/2 and the Protobuf message-encoding protocol to provide high performance, low-bandwidth communication between applications and services. It supports server and client code generation across most popular programming languages and platforms, including .NET, Java, Python, Node.js, Go and C++. The major usecase for gRPC is the making of remote procedure calls performant while ensuring language independence. Remote procedure calls play an important role in data microservices/distributed environment where is transferred across services. That is why , a lot of it becomes a very useful framework in developing applications performance.

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
This setup guide assumes the user is using Ubuntu 18.04. 
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
 
 
 

The Image Rotation Service followed the demonstrated directory/file structure:

```plantuml
!define ICONURL https://raw.githubusercontent.com/tupadr3/plantuml-icon-font-sprites/v2.1.0
skinparam defaultTextAlignment center
!include ICONURL/common.puml
!include ICONURL/font-awesome-5/gitlab.puml
!include ICONURL/font-awesome-5/java.puml
!include ICONURL/font-awesome-5/rocket.puml
!include ICONURL/font-awesome/newspaper_o.puml
FA_NEWSPAPER_O(news,good news!,node) #White {
FA5_GITLAB(gitlab,GitLab.com,node) #White
FA5_JAVA(java,PlantUML,node) #White
FA5_ROCKET(rocket,Integrated,node) #White
}
gitlab ..> java
java ..> rocket
```
 
 ## E. Discussion.
 
 * Design Overview. 
   
   
   mean_filter => function that is implicated to blur an image in order to remove noise. It involves determinign the mean of th pixel values within a n x n kernel. The pixel intensity of the center element is then replaced the mean value. This eliminates some of he noise in the image and smooths the edges of the image. The blur function from the OpenCV library has been included in otder to apply the mean filter to the image. 
   


When dealing with color images it is first necessary to convert from RGB to HSV since the dimensions of RGB are dependent on one another where as the three dimensions in HSV are independent of one another (this allows us to apply filters to each of the three dimensions separately.)

The following is a python implementation of a mean filter:

**********************   
 
 ## E. Conclusion and Future Scope.
 
 Alternative framework scenarios.
 Other frameworks are recommended over the gRPC modality 
