from requests import get, post


#print(get('http://localhost:5000/api/jobs').json())
# {'jobs': [{'collaborators': '2, 3', 'end_date': None, 'is_finished': False, 'job': 'jobbbbbs', 'start_date': None, 'team_leader': 1, 'work_size': 12}, {'collaborators': '1, 2', 'end_date': None, 'is_finished': False, 'job': 'gfdgdfg', 'start_date': None, 'team_leader': 1, 'work_size': 123}, {'collaborators': '2, 3', 'end_date': None, 'is_finished': True, 'job': 'dfgdfgdg', 'start_date': None, 'team_leader': 1, 'work_size': 156}, {'collaborators': '2, 3', 'end_date': None, 'is_finished': False, 'job': 'фыывпывпа', 'start_date': None, 'team_leader': 1, 'work_size': 12}, {'collaborators': '2, 3', 'end_date': None, 'is_finished': False, 'job': 'fsdfsdfsdf', 'start_date': None, 'team_leader': 1, 'work_size': 162}]}
#print(get('http://localhost:5000/api/jobs/1').json())
# {'jobs': [{'collaborators': '2, 3', 'end_date': None, 'is_finished': False, 'job': 'jobbbbbs', 'start_date': None, 'team_leader': 1, 'work_size': 12}]}
#print(get('http://localhost:5000/api/jobs/100').json())
# {'error': 'Not found'}
#print(get('http://localhost:5000/api/jobs/asgdfgd').json())
# {'error': 'Not found'}


from requests import get, post


print(get('http://localhost:5000/api/jobs').json())

# нет ни одного необходимого ключа в json
data = {'asd': 4}
print(post('http://localhost:5000/api/jobs/edit/1', json=data).json())

# не передали json
print(post('http://localhost:5000/api/jobs/edit/1').json())

# не можем занять занятый id 2
data = {'id': 2}
print(post('http://localhost:5000/api/jobs/edit/1', json=data).json())

data = {'is_finished': False}
print(post('http://localhost:5000/api/jobs/edit/999', json=data).json())
# {'error': 'Not found'}

print(post('http://localhost:5000/api/jobs/edit/g', json=data).json())
# {'error': 'Not found'}

print(post('http://localhost:5000/api/jobs/edit/1', json=data).json())
# {'success': 'OK'}
print(get('http://localhost:5000/api/jobs').json())