from requests import get, post, delete, put


data = {'surname': 'belka',
		'name': 'asd',
		'age': 19,
		'position': 'turtle',
		'city_from': 'japan',
		'speciality': 'digger',
		'address': 'module_1',
		'email': 'belka_asd@mars.com',
		'password': 'qwerty'}
print(post("http://127.0.0.1:5000/api/v2/users", data=data).json())
# {'message': 'Email qwerty@mars.com already exist'}

data = {'surname': 'qwerty',
		'name': 'asd',
		'age': 19,
		'city_from': 'japan',
		'speciality': 'digger',
		'address': 'module_1',
		'email': 'qwerty123@mars.com',
		'password': 'qwerty'}
print(post("http://127.0.0.1:5000/api/v2/users", data=data).json())
# {'message': {'position': 'Missing required parameter in the JSON body or the post body or the query string'}}

data = {'surname': 'qwerty',
		'name': 'asd',
		'age': 19,
		'position': 'turtle',
		'city_from': 'japan',
		'speciality': 'digger',
		'address': 'module_1',
		'email': 'qwerty@mars.com',
		'password': 'qwerty'}
print(post("http://127.0.0.1:5000/api/v2/users", data=data).json())
# {'message': 'Email qwerty@mars.com already exist'}

print(delete("http://127.0.0.1:5000/api/v2/users/4").json())
# {'message': 'User 3 not found'}

print(delete("http://127.0.0.1:5000/api/v2/users/2").json())
# {'success': 'OK'}

print(get("http://127.0.0.1:5000/api/v2/users/3").json())
# Вернул нужные данные.

print(get("http://127.0.0.1:5000/api/v2/users/6").json())
# {'message': 'User 6 not found'}

print(get("http://127.0.0.1:5000/api/v2/users").json())
# Вернул все данные.

data = {'surname': 'wasgsr'}
print(put("http://127.0.0.1:5000/api/v2/users/3", data=data).json())
{'success': 'OK'}

data = {'surname': 'wasgsr'}
print(put("http://127.0.0.1:5000/api/v2/users/17", data=data).json())
{'message': 'User 17 not found'}