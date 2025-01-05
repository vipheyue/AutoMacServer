from flask import Flask, request
import subprocess

app = Flask(__name__)


@app.route('/event', methods=['GET'])
def handle_event():
    event = request.args.get('event')
    if event:
        result = execute_applescript(event)
        return f"接受到的事件ID: {event} 执行结果:{result}", 200
    else:
        return "没有传递event或者不是有效值 检查是不是多了空格", 400


def execute_applescript(trigger_id):
    script = f'''
    tell application "BetterTouchTool"
        execute_assigned_actions_for_trigger "{trigger_id}"
    end tell
    '''

    try:
        # 使用 osascript 命令执行 AppleScript
        subprocess.run(['osascript', '-e', script], check=True, text=True, capture_output=True)
        print(f"\n\n\n\nAppleScript 执行成功 BetterTouchToolID:{trigger_id}")
        return True

        # print(result.stdout)  # 打印 AppleScript 输出结果
    except subprocess.CalledProcessError as e:
        print(f"执行 AppleScript 时出错:{e.stderr}")
        return False


# 示例：调用函数并传入动态的 trigger_id
# trigger_id = "B483B59C-C8CC-4846-8953-43B6F045D07B"  # 动态传入触发器 ID
# execute_applescript(trigger_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
