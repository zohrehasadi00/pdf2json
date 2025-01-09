FROM ubuntu:latest
LABEL authors="zohre"

ENTRYPOINT ["top", "-b"]