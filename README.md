# Flask, Kafka & ElasticSearch Playground

## Description
Build a webapi that will POST requests to kafka, consume the requests from kafka and will send the consumned requests to elasticsearch.
The api will also support get requests from elasicsearch that will return a list of objects that matched a message that was previously sent to elastic.
Note: if the message string done not exist in elastic, return empty list. 

## How to run
1. `git clone` this repo
1. `cd` to this repo
1. Run: `docker-compose up --build`
1. Wait for the container to finish loading
1. Run the http requests

## Using
1. Flask - python HTTP server:

   * `GET localhost:5000/health` - Health check for the web-server.
   * `POST localhost:5000/message` - Send message with string as raw data to Kafka, then consume kafka and send the data to ElasticSearch.
   * `GET localhost:5000/message/<msg>` - Get all msg from ElasticSearch.

### API tests via CURL
1. `curl -X POST http://localhost:5000/message  -H 'content-type: text/plain' -d hello`
1. `curl -X GET http://localhost:5000/message/hello`

### POST 5 messages with string "hello" and invoke GET from elastic
```
[
    {
        "message": "hello",
        "timestamp": 1553376078.751528
    },
    {
        "message": "hello",
        "timestamp": 1553370386.6626382
    },
    {
        "message": "hello",
        "timestamp": 1553382277.687757
    },
    {
        "message": "hello",
        "timestamp": 1553382381.1357608
    },
    {
        "message": "hello",
        "timestamp": 1553382391.81499
    }
]
```
### GET string "missing" from elastic without invoking the string via POST
```
[]
```

### Future Improvements
Use `confluentinc/kafka-connect-elasticsearch` to send data directly from kafka to ElasticSearch.
