# app.py
import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from test_app_cli import test_one

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['POST'])
def upload_file():
    # 检查请求是否有文件部分
    if 'file1' not in request.files or 'file2' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file1 = request.files['file1']
    file2 = request.files['file2']

    # 如果用户没有选择文件，浏览器提交一个没有文件名的部分
    if file1.filename == '' or file2.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        max_keypoints = int(request.form.get('max_keypoints', 1000))
        match_threshold = float(request.form.get('match_threshold', 0.2))

        if not (1000 <= max_keypoints <= 10000):
            return jsonify({"error": "max_keypoints must be between 1000 and 10000"}), 400
        if not (0 <= match_threshold <= 1):
            return jsonify({"error": "match_threshold must be between 0 and 1"}), 400
    except ValueError:
        return jsonify({"error": "Invalid parameter value"}), 400

    print("server: max_keypoints ", max_keypoints)
    print("server: match_threshold ", match_threshold)

    if file1 and allowed_file(file1.filename) and file2 and allowed_file(file2.filename):
        filename1 = secure_filename(file1.filename)
        filename2 = secure_filename(file2.filename)

        # 创建上传文件夹，如果不存在
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)

        file1.save(filepath1)
        file2.save(filepath2)

        # 调用 testone 函数
        result = test_one(filepath1, filepath2, max_keypoints=max_keypoints, match_threshold=match_threshold)

        return jsonify({"result": result})

    return jsonify({"error": "Invalid file format"}), 400


if __name__ == '__main__':
    app.run(debug=True)

