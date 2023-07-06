# D-chat

## sample
```
(D-chat) bash-3.2$ python main.py 
2023-07-06 23:29:02,129 - Loading data...
2023-07-06 23:29:02,150 - Data Format: (2823, 17)
2023-07-06 23:29:02,150 - Converting to database...
2023-07-06 23:29:02,300 - Fixed SQL Prompt: ### sqlite table, with its properties:
#
# Sales(ORDERNUMBER,QUANTITYORDERED,PRICEEACH,SALES,ORDERDATE,QTR_ID,MONTH_ID,YEAR_ID,PRODUCTLINE,PHONE,ADDRESSLINE1,CITY,STATE,POSTALCODE,COUNTRY,CONTACTLASTNAME,CONTACTFIRSTNAME)
#

2023-07-06 23:29:02,300 - Waiting for user input...
Tell OpenAi what you want to know about the data: Tell me the max sales amount in 2003
2023-07-06 23:29:25,681 - Final Prompt: ### sqlite table, with its properties:
#
# Sales(ORDERNUMBER,QUANTITYORDERED,PRICEEACH,SALES,ORDERDATE,QTR_ID,MONTH_ID,YEAR_ID,PRODUCTLINE,PHONE,ADDRESSLINE1,CITY,STATE,POSTALCODE,COUNTRY,CONTACTLASTNAME,CONTACTFIRSTNAME)
#
### A query to answer: Tell me the max sales amount in 2003
SELECT
2023-07-06 23:29:25,682 - Sending to OpenAI...
2023-07-06 23:29:28,158 - Response obtained. Proposed sql query: Select MAX(SALES)
FROM Sales
WHERE YEAR_ID = 2003
2023-07-06 23:29:28,162 - Result: [(11279.2,)]
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
6. run `main.py `
```
python main.py
```
