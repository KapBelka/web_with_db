from requests import get, post, delete, put


# id 8 нет в БД
data = {'id': 8,
        'team_leader': 1,
        'job': 'api test job',
        'work_size': 16,
        'collaborators': '2, 4',
        'is_finished': False}
print(post('http://localhost:5000/api/v2/jobs', json=data).json())
# {'success': 'OK'}
print(get('http://localhost:5000/api/v2/jobs').json())

# id 1 есть в БД
data = {'id': 1,
        'team_leader': 1,
        'job': 'api test job',
        'work_size': 16,
        'collaborators': '2, 4',
        'is_finished': False}
print(post('http://localhost:5000/api/v2/jobs', json=data).json())
# {'error': 'Id already exists'}

# отсутствует параметр job
data = {'id': 8,
        'team_leader': 1,
        'work_size': 16,
        'collaborators': '2, 4',
        'is_finished': False}
print(post('http://localhost:5000/api/v2/jobs', json=data).json())
# {'error': 'Bad request'}

# не передан json
print(post('http://localhost:5000/api/v2/jobs').json())
# {'error': 'Empty request'}


print(get('http://localhost:5000/api/v2/jobs').json())

print(delete('http://localhost:5000/api/v2/jobs/999').json())
# {'error': 'Not found'}

print(delete('http://localhost:5000/api/v2/jobs/g').json())
# {'error': 'Not found'}

print(delete('http://localhost:5000/api/v2/jobs/6').json())
# {'success': 'OK'}
print(get('http://localhost:5000/api/v2/jobs').json())


print(get('http://localhost:5000/api/v2/jobs').json())

# нет ни одного необходимого ключа в json
data = {'asd': 4}
print(put('http://localhost:5000/api/v2/jobs/1', json=data).json())

# не передали json
print(put('http://localhost:5000/api/v2/jobs/1').json())

# не можем занять занятый id 2
data = {'id': 2}
print(put('http://localhost:5000/api/v2/jobs/1', json=data).json())

data = {'is_finished': False}
print(put('http://localhost:5000/api/v2/jobs/999', json=data).json())
# {'error': 'Not found'}

print(put('http://localhost:5000/api/v2/jobs/g', json=data).json())
# {'error': 'Not found'}

print(put('http://localhost:5000/api/v2/jobs/1', json=data).json())
# {'success': 'OK'}
print(get('http://localhost:5000/api/jobs').json())