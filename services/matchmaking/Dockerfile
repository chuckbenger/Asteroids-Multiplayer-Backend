FROM python:3.7.6-alpine3.10
RUN echo Copying matchmaking service files to container
WORKDIR /matchmaking
COPY ./matchmaking/requirements.txt ./
RUN pip install -r ./requirements.txt
COPY ./matchmaking/*.py ./
COPY ./common ./common
RUN echo Starting Matchmaking Service
ENTRYPOINT ["python"]
CMD ["./matchmaking.py"]