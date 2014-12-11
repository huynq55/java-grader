import BaseHTTPServer
import json
import os
import subprocess
import re

class HTTPHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_POST(self):
        body_len = int(self.headers.getheader('content-length', 0))
        body_content = self.rfile.read(body_len)
        problem_name, student_response = get_info(body_content)
        result = grade(problem_name, student_response)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(result)

def grade(problem_name, student_response):

    source_file = open("/edx/java-grader/Program.java", 'w')
    source_file.write(student_response)
    source_file.close()
    result = {}
    p = subprocess.Popen(["javac", "/edx/java-grader/Program.java"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    if (err != ""):
        result.update({"compile_error": err})
        result = process_result(result)
        return result
    else:
        result.update({"compile_error": 0})

    test_runner = problem_name["problem_name"] + "TestRunner"
    test_runner_java = "/edx/java-grader/" + test_runner + ".java"
    p = subprocess.Popen(["javac", "-classpath", "/edx/java-grader:/edx/java-grader/junit-4.11.jar:/edx/java-grader/hamcrest-core-1.3.jar", test_runner_java], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    p = subprocess.Popen(["java", "-classpath", "/edx/java-grader:/edx/java-grader/junit-4.11.jar:/edx/java-grader/hamcrest-core-1.3.jar", test_runner], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = re.split('\n', out)
    correct = out[len(out) - 2]

    if (correct == "true"):
        correct = True
    else:
        correct = False

    if (len(out) > 2):
        message = out[0]
    else:
        message = "Good job!"

    result.update({"correct": correct, "msg": message,})
    result = process_result(result)
    return result

def process_result(result):

    if (result["compile_error"] != 0):
        correct = False
        score = 0
        message = result["compile_error"]
    else:
        correct = result["correct"]
        message = result["msg"]

    if (correct == True):
        score = 1
    else:
        score = 0

    result = {}
    result.update({"correct": correct, "score": score, "msg": message })
    result = json.dumps(result)
    return result

def get_info(body_content):
    json_object = json.loads(body_content)
    json_object = json.loads(json_object["xqueue_body"])
    problem_name = json.loads(json_object["grader_payload"])
    student_response = json_object["student_response"]
    return problem_name, student_response

if __name__ == "__main__":

    server = BaseHTTPServer.HTTPServer(("localhost", 1710), HTTPHandler)
    server.serve_forever()
