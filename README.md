# D-chat

## Demo
![D-chat_demo_img](https://github.com/nakaikento/D-chat/assets/27417352/14f4d60a-381c-454c-b622-9d9ae759464a)

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
streamlit run main.py
```
