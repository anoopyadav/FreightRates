# FreightRates API v0.1

## Description
Provides price information between two regions

## Service Endpoints
Exposes four endpoints:
- rates - Provides average price information
- rates_null - Same as rates, but only for those ports which have 3 or more data points available
- submit_rate - Add the supplied price data to the DB (price in USD)
- submit_rate_currency - Same as submit_rate, with added currency (other than USD)

## Startup
- Navigate to the project root (FreightRates)
- docker-compose build
- docker-compose up

## Usage
- `curl "http://127.0.0.1:5000/rates?date_from=<YYYY-MM-DD>&date_to=<YYYY-MM-DD>&origin=<code_or_region>&destination_code=<code_or_region>"`
- `curl "http://127.0.0.1:5000/rates_null?date_from=<YYYY-MM-DD>&date_to=<YYYY-MM-DD>&origin=<code_or_region>&destination_code=<code_or_region>"`
- `curl --data "date_from=<YYYY-MM-DD>&date_to=2<YYYY-MM-DD>&origin_code=<code_or_region>&destination_code=<code_or_region>&price=<number>” http://127.0.0.1:5000/submit_rate`
- `curl --data "date_from=<YYYY-MM-DD>&date_to=2<YYYY-MM-DD>&origin_code=<code_or_region>&destination_code=<code_or_region>&currency_code=<XXX>” http://127.0.0.1:5000/submit_rate_currency`

## Notes
- Average Price is rounded up to two decimal places
 
