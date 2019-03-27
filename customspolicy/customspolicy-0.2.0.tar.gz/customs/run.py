from flask import Flask, request, jsonify
import customs.orchestrator as orch
import customs.validator as valid

app = Flask(__name__)


@app.route('/customs', methods=['POST'])
def customs():
    content = request.get_json(silent=True)  # exception?
    check = valid.is_json_correct(content)
    if check is True:
        response = orch.process(content)
    else:
        response = check
    return response


if __name__ == '__main__':
    app.run(debug=True)
