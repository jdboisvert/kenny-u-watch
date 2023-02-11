FROM golang:1.17.1-alpine3.14
RUN mkdir /alert-producer

WORKDIR /alert-producer

COPY . /alert-producer

RUN go mod download
RUN go get github.com/githubnemo/CompileDaemon

EXPOSE 8080

ENTRYPOINT CompileDaemon --build="go build main.go" --command=./main
