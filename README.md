>   1. get_balance    method = POST /getbalance
Parameters:
{
	"user_id":"string",
	"currency": "string"
}
e.g
{
	"user_id":"1",
	"currency": "string"
}

Response:
{
	"StatusCode": 200,
	"result": {
		"RUB": 10.0,
		"RMB": 0.0
	}
}
{
	"StatusCode": 401,
	"error": "string"
}


>   2. credit    method = POST  /credit
Parameters:
{
	"user_id":"string",
	"currency": "string",
	"amount":"float",
	"tx_id":"string"
}

e.g
{
	
  	"user_id": 2,
	"currency": "RUB",
	"amount": 10,
	"tx_id": "okd2"
}
Response:
{
	"StatusCode": 200,
	"result": "Amount of RUB is 10.0"
}
{
	"StatusCode": 401,
	"error": "string"
}


>    3. debit     method = POST  /debit
Parameters:
{
	"user_id":"string",
	"currency": "string",
	"amount":"float",
	"tx_id":"string"
}

e.g
{
	"user_id":"21",
	"currency": "RUB",
	"amount":	10,
	"tx_id":"adf"
}
Response:
{
	"StatusCode": 200,
	"result": "Amount of RUB is 10.0"
}

{
	"StatusCode": 401,
	"error": "string"
}

>    4. Add user method = POST   /adduser
Parameters:
{
	"user_id":"string"
}

Response:
{
	"result": "string",
	"StatusCode": 200
}

{
	"error": "string",
	"StatusCode": 401
}