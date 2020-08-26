import requests

data = {"data":'''{"cmd": "post_data", "data": [{"name": "field1", "val": 1}, {"name": "field2", "val": "+7(999)-999-99-99"}, {"name": "field3", "val": "sjhdfhskdfhksj"} ]}'''}
r = requests.post(url="http://0.0.0.0:4000/", data=data)
print('r', r.text)