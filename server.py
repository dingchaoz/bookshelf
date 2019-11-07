# Import libraries

import subprocess
from signal import SIG_DFL, SIGPIPE, signal

from flask import Flask, jsonify, request

app = Flask(__name__)

# curl -X POST -H 'content-type: application/json' --data '{"exp":1800,"userid":"adfsa"}' http://127.0.0.1:5000/api
signal(SIGPIPE, SIG_DFL)


@app.route('/api', methods=['POST'])
def predict():
    # Get the data from the POST request.
    data = request.get_json(force=True)
    print('received data')

    # Make prediction using model loaded from disk as per the data.
    # book_info = subprocess.call(['python', 'zhengli/core/main.py',
    #                              "-f", data['file']])

    process = subprocess.Popen(['python', 'zhengli/core/main.py',
                                "-f", data['file']], stdout=subprocess.PIPE)

    # Take the first value of prediction
    output, err = process.communicate()

    print('prediction made', output)

    return output


if __name__ == '__main__':
    app.run(port=8080, debug=True, host='0.0.0.0', threaded=True)
