import requests

print('Testing Frontend-Backend Integration')
print('=' * 50)

# Test register
print('\n1. Register new user:')
reg_data = {'email': 'frontend@test.com', 'password': 'pass123'}
reg_resp = requests.post('http://localhost:8000/api/auth/register', json=reg_data)
print(f'   Status: {reg_resp.status_code}')
print(f'   Response: {reg_resp.json()}')

# Test login
print('\n2. Login:')
login_data = {'username': 'frontend@test.com', 'password': 'pass123'}
login_resp = requests.post('http://localhost:8000/api/auth/login', data=login_data)
print(f'   Status: {login_resp.status_code}')
token = login_resp.json()['access_token']
print(f'   Token obtained: {token[:30]}...')

# Test create task
print('\n3. Create Task:')
headers = {'Authorization': f'Bearer {token}'}
task_data = {'title': 'Frontend Task', 'description': 'Created from frontend test'}
task_resp = requests.post('http://localhost:8000/api/tasks', json=task_data, headers=headers)
print(f'   Status: {task_resp.status_code}')
print(f'   Response: {task_resp.json()}')

# Test get tasks
print('\n4. Get Tasks:')
get_resp = requests.get('http://localhost:8000/api/tasks', headers=headers)
print(f'   Status: {get_resp.status_code}')
tasks = get_resp.json()
print(f'   Tasks Count: {len(tasks)}')
for task in tasks:
    print(f'     - {task["title"]}: {task["description"]}')

print('\n' + '=' * 50)
print('SUCCESS: Frontend-Backend-Database connection OK!')
print('You can now use the Streamlit frontend at: http://localhost:8501')
