# encoding=utf-8
import uuid
from flask import Flask, request, jsonify, current_app
from flask_script import Manager
import os
from pyengine import FuncClass
import queue
import sys

sys.path.append('.')

app = Flask('python_engine')
queue.Queue().empty()


def get_q(n):
    q = queue.Queue()
    for i in range(n):
        q.put(str(uuid.uuid4()))
    return q


def get_class(filename):
    all = list([i.__module__ for i in FuncClass.__subclasses__()])
    print(all)
    j = 0
    all_c = {}
    for i in all:
        all_c[i] = j
        j += 1
    return FuncClass.__subclasses__()[all_c[filename]]


def get_res(data, q):
    if q.empty():
        return jsonify({'msg': 'I am busy'})
    filename = q.get()
    filepath = filename + '.py'
    with open(filepath, 'wb') as f:
        f.write(data)
    a = __import__(filename.replace('.py', ''))
    os.remove(filepath)
    try:
        print(len(FuncClass.__subclasses__()))
        res = get_class(filename)().predict()
        res = jsonify({'msg': str(res)}), 200
    except Exception as e:
        res = jsonify({'msg': str(e)}), 500
    finally:
        q.put(filename)

    return res


@app.route('/register/', methods=['POST'])
def register():
    data = request.data

    return get_res(data, current_app.q)


@app.route('/reduce/')
def reduce():
    return jsonify({'msg': current_app.q.get()})

@app.route('/add/')
def add():
    filename = str(uuid.uuid4())
    current_app.q.put(filename)
    return jsonify({'msg': filename})

manager = Manager(app)


@manager.option('-p', '--port', dest='port', help='端口号')
@manager.option('-n', '--num', dest='num', help='一个工程中最多可以存在的子类数量，也是同时可以被调用的次数')
def run(port, num):
    app.q = get_q(int(num))
    app.run(host='0.0.0.0', port=port, threaded=True)


def main():
    manager.run()


if __name__ == '__main__':
    main()
