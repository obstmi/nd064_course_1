FROM golang:alpine

WORKDIR /go/src/app

ADD . /go/src/app/
# oder: ADD . .

RUN go mod init && go build -o helloworld

EXPOSE 6111

CMD [ "./helloworld" ]