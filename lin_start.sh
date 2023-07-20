docker pull ioannagkika/localization_simulator
xhost +
docker run -it --name simulator --net=host --env="DISPLAY" -v /home:/localization_simulator/C ioannagkika/localization_simulator
docker rm --volumes simulator
xhost -