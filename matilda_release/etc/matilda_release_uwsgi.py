from matilda_release.api.v2 import app
from matilda_release.api.v2.app import app as votr
from flask_cors import CORS
from flask import Flask

if __name__ == "__main__":
    votr.run(host='0.0.0.0', port=5000, debug=True)

