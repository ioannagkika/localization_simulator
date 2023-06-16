# sudo apt-get install x11-xserver-utils
sudo docker pull ioannagkika/localization_simulator
xhost +
sudo docker run --net=host --env="DISPLAY" --volume="$HOME/.Xauthority:/root/.Xauthority:rw" ioannagkika/localization_simulator
xhost -