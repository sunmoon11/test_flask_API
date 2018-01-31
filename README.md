# Flask: Account Management

##1. get_balance  (_method = POST, "/getbalance"_)

**Parameters:**

```json
{
	"user_id" : "string",
	"currency": "string"
}
```

_e.g_
```json
{
	"user_id":"1",
	"currency": "string"
}
```

**Response:**
```json
{
	"StatusCode": 200,
	"result": {
		"RUB": "float",
		"RMB": "float"
	}
}
```
```json
{
	"StatusCode": 401,
	"error"     : "string"
}
```


##2. credit (method = POST,  "/credit")
**Parameters:**
```json
    {
        "user_id" : "string",
        "currency": "string",
        "amount"  : "float",
        "tx_id"   : "string"
    }
```

_e.g_
```json
{
  	"user_id" : "2",
	"currency": "RUB",
	"amount"  : 10,
	"tx_id"   : "okd2"
}
```
**Response:**
```json
{
    "StatusCode": 200,
    "result"    : "Amount of RUB is 10.0"
}
```
```json
{
    "StatusCode": 401,
    "error"     : "string"
}
```


##3. debit (method = POST, "/debit")
**Parameters:**
```json
{
	"user_id" : "string",
	"currency": "string",
	"amount"  : "float",
	"tx_id"   : "string"
}
```

_e.g_
```json
{
	"user_id" : "21",
	"currency": "RUB",
	"amount"  :	10,
	"tx_id"   : "adf"
}
```
**Response:**
```json
{
	"StatusCode": 200,
	"result"    : "string"
}
```
```json
{
	"StatusCode": 401,
	"error"     : "string"
}

```
##4. Add user (method = POST, "/adduser")
**Parameters:**
```json
{
	"user_id":"string"
}
```

**Response:**
```json
{
	"StatusCode": 200,
	"result"    : "string"
}
```
```json
{
	"StatusCode": 401,
	"error"     : "string"
}
```
