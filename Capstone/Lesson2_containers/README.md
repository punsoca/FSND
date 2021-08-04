# Exercise 1: Hello World #

## Create an empty Dockerfile ##

In a new directory for this exercise, create a file named `Dockerfile`. Note that a `Dockerfile` does not have any file extensions.

Mac/Linux/Windows users using WSL/GitBash can use the following commands:
`# create a new directory`
    
    > mkdir Example1
    > cd Example1


`# create a file in the present working directory`
    
    > touch Dockerfile

`# open the file in any text editor, such as VS Code`

    > code .`
    

Windows users using CMD: First, you will have to manually (right-clicking way) create a new folder using the Windows explorer, and create the Dockerfile (without extension). 

## Write Dockerfile content ##

In the Dockerfile, add the lines

    > FROM  debian:jessie-slim
    > ENTRYPOINT ["echo", "hello world"]


## Build an image ## 
`Build the image from the same directory using the command`

    docker build --tag test .


Here, the image name is "test". Note that the full stop (.) tells the docker build command to use the Dockerfile found in the current directory.

## Create and run a container ## 
`Once the image is built, you can run the container with the command:`

    docker run --name myContainer  test --rm
where, --rm option ensures that the container is removed when it exits.

### Clean up ##
`Stop and remove the container:`

    docker ps --a
    docker container stop <container_ID or container_NAME>
    docker container rm <container_ID or container_NAME>


# Exercise 2: Flask#
In this example, you will containerize a flask app by following the steps below:

Fork and clone the repo
Fork this repository to your GitHub account. After forking, you can clone it locally by running the following commands in your terminal/WSL/GitBash:

## Clone the repository to your local system
    git clone https://github.com/USERNAME/FSND-Deploy-Flask-App-to-Kubernetes-Using-EKS
    cd FSND-Deploy-Flask-App-to-Kubernetes-Using-EKS

## See the content in the current directory. 
    ls

Now you have the repository content locally. Navigate to this relative folder in your locally downloaded repository. It has a Dockerfile and a sample flask app ready for you.

## Navigate to the "examples/flask" folder
    cd examples/flask
## Open the VS code editor to display the file content
    code .

## Build an image ##

Run the following commands in your terminal while you are in the FSND-Deploy-Flask-App-to-Kubernetes-Using-EKS/examples/flask/ folder.

Build the image and give it the name "test":

    docker build -t test .
Here, the `-t` flag is an alternate way of writing --tag. Don't forget to put a period (.) at the end of the command. It tells the build command to look out for the Dockerfile in the current directory. Check the list of images:

    docker image ls

## Create and run a container
Use the `test` image to create and run the container `myContainer`:
    docker run --name myContainer  -p 80:8080 test
In this command, you are mapping port 80 of your local machine to the port 8080 of the container running the flask application. If your port 80 is already in use by other application, feel free to use any other port number, such as 9090.

Access the application
Open a new terminal, and Curl the endpoint
`Mac/Linux users only`

    curl http://0.0.0.0/
`Windows users using WSL/GitBash`

    curl http://127.0.0.1:80/
Alternatively, you can check your browser with `http://localhost:80/` or `http://127.0.0.1:80/`
(Use the host port number as you've mapped in the docker run command).
## Clean up
When you are finished, stop and remove the container:
Get the id of the running container

    docker ps
## Stop the container
    docker stop <Container Id>
Further, you can remove the container and image from your local machine as:

    docker container rm <container_Id or container_Name>
    docker image ls
    docker image rm <image_Id>


Note - watch the https://www.youtube.com/watch?v=mSb137H1IH8&t=10s video and compare the results of your exercises 
