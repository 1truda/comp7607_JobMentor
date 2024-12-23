import json
import os
import subprocess

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from model import JobMentor, InterviewSession

app = Flask(__name__)
CORS(app)
# Initialize the JobMentor model
mentor = JobMentor()
sessions = {}  # 存储会话

@app.route('/select_theme', methods=['POST'])
def select_theme():
    """用户选择面试主题"""
    data = request.json
    theme = data.get("theme")
    if theme not in ["JAVA", "Python", "SQL"]:
        return jsonify({"error": "无效的主题，请选择 JAVA, Python 或 SQL"}), 400

    # 创建新的会话
    session_id = len(sessions) + 1
    sessions[session_id] = InterviewSession(theme=theme)

    return jsonify({"message": "主题已选择", "session_id": session_id})


@app.route('/start_interview', methods=['POST'])
def start_interview():
    """启动面试并获取第一个问题"""
    data = request.json
    session_id = data.get("session_id")

    # 验证会话 ID
    if session_id not in sessions:
        return jsonify({"error": "无效的会话 ID"}), 400

    session = sessions[session_id]

    # 获取第一个问题
    question = session.get_next_question(mentor)

    return jsonify({"question": question, "session_id": session_id})


@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    """提交用户回答并获取下一个问题"""
    data = request.json
    session_id = data.get("session_id")
    user_answer = data.get("answer")

    # 验证会话 ID
    if session_id not in sessions:
        return jsonify({"error": "无效的会话 ID"}), 400

    session = sessions[session_id]

    try:
        session.add_user_answer(user_answer)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    # 判断是否达到问题上限
    if session.completed_questions >= session.max_questions:
        return jsonify({
            "message": "所有问题已回答完毕，请调用总结接口获取面试表现。",
            "session_id": session_id
        })

    # 获取下一个问题
    question = session.get_next_question(mentor)

    return jsonify({"question": question, "session_id": session_id})


@app.route('/summarize_interview', methods=['POST'])
def summarize_interview():
    """总结面试表现"""
    data = request.json
    session_id = data.get("session_id")

    # 验证会话 ID
    if session_id not in sessions:
        return jsonify({"error": "无效的会话 ID"}), 400

    session = sessions[session_id]

    # 生成总结
    summary = session.summarize_interview(mentor)

    return jsonify({"message": "面试结束", "summary": summary})


# 文件路径和脚本配置
READABILITY_SCRIPT = "readability.py"  # readability.py 脚本路径
FINAL_CODE_FILE = "final_code.json"  # 最终生成的 JSON 文件路径


def execute_readability_script(problem_description):
    """
    调用 readability.py，将问题描述传递进去，并读取生成的 final_code.py 内容。
    """
    try:
        # 构造命令，传递问题描述给 readability.py
        command = [
            "python", READABILITY_SCRIPT,  # readability.py 脚本
        ]
        # 使用环境变量传递问题描述
        env = os.environ.copy()
        env["PROBLEM_DESCRIPTION"] = problem_description

        # 执行脚本
        subprocess.run(command, env=env, check=True)

        # 检查是否生成了 final_code.json
        if not os.path.exists(FINAL_CODE_FILE):
            raise FileNotFoundError(f"File {FINAL_CODE_FILE} not found after script execution.")

        # 读取 final_code.json 内容
        with open(FINAL_CODE_FILE, "r") as file:
            final_code_data = json.load(file)  # 读取并解析 JSON 文件内容

        return final_code_data
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Error during readability.py execution: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Error: {str(e)}")


@app.route("/api/code/generate", methods=["POST"])
def generate_code_api():
    """
    处理生成代码的 API 请求
    """
    data = request.json
    description = data.get("description", "")
    if not description:
        return jsonify({"error": "Description is required"}), 400

    try:
        # 调用 execute_readability_script，生成代码
        final_code = execute_readability_script(description)
        return jsonify({"code": final_code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



# # Route for running the email pipeline
# @app.route('/api/run-email-pipeline', methods=['POST'])
# def run_email_pipeline():
#     def generate_output():
#         try:
#             # Run the email_pipeline.py script
#             process = subprocess.Popen(
#                 ["python3", "email_pipeline.py"],
#                 stdout=subprocess.PIPE,
#                 stderr=subprocess.PIPE,
#                 text=True,
#                 bufsize=1
#             )
#             # Print each line from stdout to the backend console
#             for line in process.stdout:
#                 print(line, flush=True)  # Print to backend console
#             process.stdout.close()
#             process.wait()
#
#             # If the process encountered errors, print stderr
#             if process.returncode != 0:
#                 error_message = process.stderr.read()
#                 print(f"Error: {error_message}", flush=True)
#         except Exception as e:
#             print(f"An error occurred: {str(e)}", flush=True)
#
#     # Call the function to execute and print, return a basic response
#     generate_output()
#     return {"message": "Pipeline executed. Check backend logs for details."}, 200
@app.route('/api/run-email-pipeline', methods=['POST'])
def run_email_pipeline():
    try:
        # 获取前端传递的 command 参数
        data = request.get_json()
        command = data.get('command', '')

        if not command:
            return jsonify({"error": "Command is required"}), 400

        def generate_output():
            try:
                # 将 command 作为参数传递给 email_pipeline.py
                process = subprocess.Popen(
                    ["python3", "email_pipeline.py", command],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1
                )

                # 实时打印脚本的 stdout 输出
                for line in process.stdout:
                    print(line, flush=True)
                process.stdout.close()
                process.wait()

                # 如果脚本有错误，打印 stderr
                if process.returncode != 0:
                    error_message = process.stderr.read()
                    print(f"Error: {error_message}", flush=True)
            except Exception as e:
                print(f"An error occurred: {str(e)}", flush=True)

        # 执行脚本
        generate_output()
        return jsonify({"message": "Pipeline executed. Check backend logs for details."}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)