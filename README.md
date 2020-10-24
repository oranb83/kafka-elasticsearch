# Words Counter

## Description
Word counter REST API support 2 endpoints.
1. HTTP POST requests of a stream of text (filepath / url / string) and calcualtes the amount of appearence per word.
1. The API also supports HTTP GET requests with a word and returns the amount of appearences it has previously calculated from the POST requests. It does that in O(1) efficency from the DB.

### Note
1. For persistency I use a single small redis cluster that is not optimized for performance. The DB saved the calculated results and increments existing keys based on new data. I use redis pipelines for batch updates (to reduce network round trips) and atomic operations to avoid race conditions (that's why I picked redis).
1. If the word not exist in the DB, I return zero.

### Assumptions on the input
1. The input will NOT be sanitied, I will do that by removing digits and panctuations besides: `-` or `,` or `'` - they will be part of the word, meaning: `it's,` in this context will not be a match for `it's` nor will be matched to `its,`. See additional examples in the code.
1. The data uniqness is limited, there's a limited amount of words in the english langauge and only ~140k are used so on that I based my assumption. The more uniqness we will have the more we will need to do round trips to the DB which slows the operation.
1. All the input lines have roughly the same amount of characters, let's assume up to 1k (I tested for 2k). This assumption is based on english text that is rarely this big per line. I can support that as well, but it takes more development time and I prefered not to waste too much time on splitting files into valid chunks of words.
1. A string (not filepaths or URLs) will always be short, few k's at most, otherwise it doesn't make sense not to pass a file. It will be a decoded string.
1. The file / urls will contain text and not binary files nor any other format like HTML, meaning I will not have to deal with decoding.
1. Additional points: assumptions, notes, todo's are documented in the code.

### Note
I tested the URL only with small files, but tested the filepaths with files of 400MB, 1GB and 3GB with ~100 unique words. If a test case fails it's easy to change the relevant constants (currently not in config although it should be) to support the new data, all under controler.py, start by reducing the `MAX_UNIQUE_KEYS`, but make sure you solved the redis bottleneck (it should be in the redis config - need time to find out what parameters to change):
* `LINES_TO_READ = 10000`
* `MAX_UNIQUE_KEYS = 10000`

## How to run
1. `git clone` this repo
1. `cd` to this repo
1. Move all test files into the repo:
    * big files will effect the build time, if the build fails on very big files then I will need to fix the `docker-compose.yaml` to accept the filepath from a volume.
    * You can always run `python app.py` for the API, download redis locally, start it and change the redis client in the code to accept localhost, but my way saves you the throuble.
1. Run: `docker-compose up --build`
1. Wait for the container to finish loading
1. Run the http requests

## Using
1. Flask - python HTTP server:
   * `GET localhost:5000/health/` - Health check for the web-server.
   * `POST localhost:5000/v1/words/count/` - Send string / valid url / filepath on the local server, once the operation is completed successfully send HTTP 201 back to the client - I assume the client needs to get the OK confirmation that the operation completed, otherwise I would prefer to send HTTP 202 and process the payload in the background.
   * `GET localhost:5000/v1/words/<word>/stats/` - Get the word count from redis.

### API tests via CURL
1. `curl -X POST 'http://127.0.0.1:5000/v1/words/count/' --header 'Content-Type: text/plain' --data-raw 'test_big.txt'` => response(created, 201) - speed depands on the file size, line size, words uniqness and instance on which it will run (downloading an optimized redis cluster will dramatically bost performance).
1. `curl -X GET 'http://127.0.0.1:5000/v1/words/hello/stats/' --header 'Content-Type: text/plain'` => response(3425252, 200) - O(1) operation done extremly fast.

### Future Improvements and considerations
Use several redis containers linked with a bridge, fix the IO preformance issues of the container (well known network issue that can be deactivates - needs to read about it, it's due to some redis improvments that have negetive effect when running locally on a single cluster).
If the redis performance does increase dramatically (as I expect) and we are no longer IO bound, consider changing the code to not do in memory words count calculations and dump it to redis once in a while when the memory consumption is too big, instead use redis pipeline while incrementing each seen word by 1 and using multi-thread. This needs to be tested, since in python sometimes the overhead of creating threads is more costly then using a single thread (see GIL).
