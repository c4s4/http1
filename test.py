import http1

response = http1.request('http://www.google.com')
print(f'Status: {response.status} ({response.message})')
print(f'Headers: {response.headers}')
#print(f'Body: {response.body.strip()}')
