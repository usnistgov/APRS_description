FROM osrf/ros:iron-desktop

SHELL ["/bin/bash", "-c"]

RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1001 ubuntu 

RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER ubuntu

WORKDIR /home/ubuntu

RUN mkdir -p /home/ubuntu/aprs_ws/src

WORKDIR /home/ubuntu/aprs_ws

ENV GZ_SIM_RESOURCE_PATH=/home/ubuntu/aprs_ws/install/ur_description/share/
ENV GZ_SIM_SYSTEM_PLUGIN_PATH=/home/ubuntu/aprs_ws/install/gz_ros2_control/lib/
ENV GZ_VERSION=harmonic

RUN source /opt/ros/iron/setup.bash && \
    sudo apt-get update -qq && \
    sudo apt-get install lsb-release gnupg python3-pip wget -y && \
    pip install setuptools==58.2.0 && \
    sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null && \
    sudo apt-get update -qq && \
    sudo apt-get -y install gz-harmonic && \
    git clone https://github.com/ros-controls/gz_ros2_control.git src/gz_ros2_control -b iron && \
    git clone https://github.com/gazebosim/ros_gz.git src/ros_gz -b humble && \
    git clone https://github.com/UniversalRobots/Universal_Robots_ROS2_Description.git src/ur_description -b rolling && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -y -r && \
    colcon build

RUN echo 'source /home/ubuntu/aprs_ws/install/setup.bash' >> /home/ubuntu/.bashrc