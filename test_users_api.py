from requests import get, post, delete, put
import datetime


print(get('http://localhost:5000/api/users').json())