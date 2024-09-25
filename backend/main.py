# Import necessary libraries
from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import diskcache as dc

# Initialize Flask app
app = Flask(__name__)

CORS(app)

# Initialize DiskCache
cache = dc.Cache('disk_cache')


# 捕获所有其他异常
@app.errorhandler(Exception)
def handle_exception(e):
    return 'error'


# Define route to handle POST requests for saving code data
@app.route('/code/save', methods=['POST'])
def save_code():
    # Get JSON data from request
    data = request.json

    # Generate a unique UUID key
    unique_key = str(uuid.uuid4().hex)

    # Save data to disk cache with the UUID key
    cache.set(unique_key, data, expire=24 * 60 * 60)
    # Return the url as the response
    return jsonify({"url": '/code/' + unique_key})


@app.route('/code/info', methods=['POST'])
def get_code_info():
    # 从请求体中获取key
    data = request.get_json()
    key = data.get('key', None)

    if not key:
        return jsonify({"code": "无效的key", "code_lang": "text"})

    # 从diskcache中查询对应的value
    value = cache.get(key)

    if value is None:
        return jsonify({"code": "无效的key", "code_lang": "text"})

    # 返回查询到的value
    return jsonify(value)


# To run the Flask app (debug mode for development purposes)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
