import sys
from flask import Flask, request
from typing import TypedDict

app = Flask(__name__)

class JobReport(TypedDict):
    endpoint: str
    success: bool

class ReportReq(TypedDict):
    jobs: list[JobReport]
    

@app.route('/report', methods=['POST'])
def report():
    data: ReportReq = request.json
    print('----REPORT----')
    for i in data["jobs"]:
        print("{}: {}".format(("SUCCESS" if i["success"]  else "FAIL"), i["endpoint"]))
    print('-----END-----')
    sys.stdout.flush()
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)