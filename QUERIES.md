# Example Queries

The API can be queried either via POST or GET request. The same parameters are required in either case.

All queries are written assuming the Docker container is running as described in the README.
## Example 1
### Query
```sh
curl -H "Content-Type: application/json" -X POST \
-d '{  "age": "35",   "gender": "F",   "nationality": "NZ",   "seniority": "46",   "rel_type": "ACTIVE",   "activity_type": "ACTIVE",   "segment": "INDIVIDUAL",   "income": "312000"}' \
http://localhost/api/recommender/v1/get_recc
```
### Response
```
{"products":["Current Accounts","Long-term deposits","Pensions","Direct Debit","Credit Card","Payroll Account","Más Particular Account"]}
```

## Example 2
### Query
```sh
curl -H "Content-Type: application/json" -X POST \
-d '{ "age": "19",   "gender": "M",   "nationality": "AU",   "seniority": "5",   "rel_type": "ACTIVE",   "activity_type": "INACTIVE",   "segment": "STUDENT",   "income": "46000"}' \
http://localhost/api/recommender/v1/get_recc
```
### Response
```
{"products":["Current Accounts","E-Account","Direct Debit","Payroll Account","Pensions","Long-term deposits","Taxes"]}
```

## Example 3
Note that the `income` field is not provided
### Query
```sh
curl -H "Content-Type: application/json" -X POST \
-d '{ "age": "19",   "gender": "M",   "nationality": "AU",   "seniority": "5",   "rel_type": "ACTIVE",   "activity_type": "INACTIVE",   "segment": "STUDENT"}' \
http://localhost/api/recommender/v1/get_recc
```
### Response
```
{"err":"Required parameters not provided"}
```