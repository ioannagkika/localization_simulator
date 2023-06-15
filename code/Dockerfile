#FROM python:3.8.3
FROM python:3.10.5-slim

RUN apt-get update && apt-get install -y \
    python3-tk 
RUN apt-get install -y --no-install-recommends libboost-all-dev
RUN apt-get install sudo

RUN pip install --upgrade pip

ENV DISPLAY=host.docker.internal:0
WORKDIR /localization_simulator
COPY requirements.txt ./requirements.txt
COPY additional_functions.py ./additional_functions.py
COPY print_path.py ./print_path.py
COPY set_path.py ./set_path.py
COPY to_broker.py ./to_broker.py

RUN pip install -r requirements.txt

# PORT-FORWARDING
EXPOSE 1883

#ENTRYPOINT sh docker_entrypoint.sh
CMD ["python", "./print_path.py"]
