# APRS_description
Loads the robots from the APRS lab in Gazebo Harmonic Running Iron

## Packages
* `aprs_description` - Includes all descriptions for the four robots.

## Installation Instructions
* Pull the docker image

    `docker image pull jaybrecht/aprs-description`

* Create a container using the docker image

    `docker run -t -d --name aprs-description -e DISPLAY=$DISPLAY -e LOCAL_USER_ID=1001  --gpus=all --runtime=nvidia -e "NVIDIA_DRIVER_CAPABILITIES=all" --network=host --pid=host --privileged -v /tmp/.X11-unix:/tmp/.X11-unix:rw jaybrecht/aprs-description:latest`

* Enable local connections to docker

    `xhost +local:docker`

* Access the docker container through the terminal

    `docker exec -it aprs-description bash`

* Clone the package

    `git clone https://github.com/jaybrecht/aprs_description.git src/aprs_description`

* Set the resource path

    `export GZ_SIM_RESOURCE_PATH=/home/ubuntu/aprs_ws/install/ur_description/share/:/home/ubuntu/aprs_ws/install/aprs_description/share/aprs_description/gz_models/:/home/ubuntu/aprs_ws/install/aprs_description/share`

* Build the workspace

  `colcon build`

* Source the workspace

    `. install/setup.bash`

* Launch the environment with the robots

    `ros2 launch aprs_description load_aprs_robots.launch.py `
