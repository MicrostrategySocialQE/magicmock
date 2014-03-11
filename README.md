# magicmock
A mock server implemented in python
##Installation
```
>>pip install magicmock
```
##Create a project
```
>>magicmocksetup mockproject 
```
##Launch 
```
>>cd mockproject
>>magicmock -c mockserver.cfg -o .
```
##Usage
###magicmock api:
```
from magicmock import server, Mode
from APITemplate import SampleAPI
s = server("localhost", 8081, ssl = False)
# set response
s.SetResponse(SampleAPI, SampleAPI.response)
# set mode
s.SetMode(Mode.Mock)
# set delay
s.SetDelay(5, is_global = False)
```
###restful api:
1. Set response:
POST /set/response
{"response":{"headers":{"k":"v"}, "status": "200 OK", "body":{"k":"v"}}, "url":"/key/value", "method":"get"}
2. Set mode:
POST /set/mode
{"mode":"Proxy", "is_global":false}
3. Set delay
POST /set/delay
{"delay":5, "is_global":false}

