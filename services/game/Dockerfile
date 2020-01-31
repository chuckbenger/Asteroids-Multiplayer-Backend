FROM python:3.7.6-alpine3.10
RUN echo Copying game service files to container
RUN apk add gcc linux-headers g++
WORKDIR /game
COPY ./game/requirements.txt ./
RUN pip install -r ./requirements.txt
COPY ./common ./common
COPY ./game/*.py ./
COPY ./game/templates ./templates
RUN echo Starting Game Service
ENTRYPOINT ["python"]
CMD ["./game.py"]