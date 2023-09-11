docker pull ioannagkika/localization_simulator
docker run -it --name simulator -v C:/:/localization_simulator/C ioannagkika/localization_simulator
docker rm --volumes simulator
pause