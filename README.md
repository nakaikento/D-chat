# D-chat

## sample
```
(D-chat) bash-3.2$ python main.py 
2023-07-06 23:40:05,275 - Loading data...
2023-07-06 23:40:05,310 - Data Format: (2823, 17)
2023-07-06 23:40:05,311 - Converting to database...
2023-07-06 23:40:05,443 - Fixed SQL Prompt: ### sqlite table, with its properties:
#
# Sales(ORDERNUMBER,QUANTITYORDERED,PRICEEACH,SALES,ORDERDATE,QTR_ID,MONTH_ID,YEAR_ID,PRODUCTLINE,PHONE,ADDRESSLINE1,CITY,STATE,POSTALCODE,COUNTRY,CONTACTLASTNAME,CONTACTFIRSTNAME)
#

2023-07-06 23:40:05,443 - Waiting for user input...
Tell OpenAi what you want to know about the data: 2003年の最高売上額を教えて
2023-07-06 23:40:19,475 - Final Prompt: ### sqlite table, with its properties:
#
# Sales(ORDERNUMBER,QUANTITYORDERED,PRICEEACH,SALES,ORDERDATE,QTR_ID,MONTH_ID,YEAR_ID,PRODUCTLINE,PHONE,ADDRESSLINE1,CITY,STATE,POSTALCODE,COUNTRY,CONTACTLASTNAME,CONTACTFIRSTNAME)
#
### A query to answer: 2003年の最高売上額を教えて
SELECT
2023-07-06 23:40:19,475 - Sending to OpenAI...
2023-07-06 23:40:21,793 - Response obtained. Proposed sql query: Select MAX(SALES) FROM Sales WHERE YEAR_ID = 2003
2023-07-06 23:40:21,796 - Result: [(11279.2,)]
[(11279.2,)]
```
## SetUp
1. install pyenv
```
brew install pyenv
```
2. install pipenv
```
pip install pipenv
```
3. designate python version 3.11
```
pipenv --python 3.11
```
4. activate pipenv
```
pipenv shell
```
5. install python package list
```
pipenv install -r requirements.txt
```
6. write down your OPENAI_API_KEY to `.env` file in the root dir
```
OPENAI_API_KEY=<YOUR_OPENAI_API_KEY>
```
7. run `main.py `
```
python main.py
```
