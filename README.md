# Flask, Kafka & ElasticSearch Playground

## Using
1. Flask - python HTTP server:

   * `GET localhost:5000/health` - Health check for the web-server.
   * `POST localhost:5000/message` - Send message with string as raw data to Kafka, then consume kafka and send the data to ElasticSearch.
   * `GET localhost:5000/message/<msg>` - Get all msg from ElasticSearch.

### API tests via CURL
1. `curl -X POST http://localhost:5000/message  -H 'content-type: text/plain' -d hello`
1. `curl -X GET http://localhost:5000/message/hello`

### Test Output for 5 POSTS
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
### Test Output for 0 POSTS
```
[]
```

### Future Improvements
Use `confluenting/kafka-connect-elasticsearch` to send data directly from kafka to ElasticSearch.
