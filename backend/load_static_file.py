from flask import Flask, send_from_directory

app = Flask(__name__, static_folder='static', static_url_path='')


# 提供入口 HTML 页面
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')


# 通用路由，提供所有静态资源
@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(app.static_folder, filename)


# 捕获所有其它请求，返回给 Vue 处理
@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
