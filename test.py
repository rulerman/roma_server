import requests

url = "http://127.0.0.1:5000/upload"
file1_path = "input/27_1_1712701850_268.JPG"
file2_path = "input/27_1_1712701877_269.JPG"

files = {
    'file1': open(file1_path, 'rb'),
    'file2': open(file2_path, 'rb')
}

# 请求的其他数据
data = {
    'max_keypoints': 5000,       # 设置 max_keypoints 的值
    'match_threshold': 0.5       # 设置 match_threshold 的值
}

response = requests.post(url, files=files, data=data)

print(response.json())
