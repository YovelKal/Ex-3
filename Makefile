# Define variables for the image name and container port
IMAGE_NAME = dish_api
CONTAINER_PORT = 8000

# Define default target to build and run the Docker container
all: build run

# Define target to build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Define target to run the Docker container
run:
	docker run -p $(CONTAINER_PORT):8000 $(IMAGE_NAME)
