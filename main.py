from flask import Flask, request
import subprocess
import json
from datetime import datetime
import math

app = Flask(__name__)

# 存储统计信息的文件路径
STATS_FILE = 'request_stats.json'


# 加载统计信息
def load_stats():
    try:
        with open(STATS_FILE, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # 如果文件不存在或格式不正确，返回一个初始的统计数据
        return {
            "total_requests": 0,
            "daily_requests": {},
            "monthly_requests": {},
            "weekly_requests": {}
        }


# 保存统计信息
def save_stats(stats):
    with open(STATS_FILE, 'w') as file:
        json.dump(stats, file, indent=4)


# 获取今天的日期字符串
def get_today_date():
    return datetime.now().strftime('%Y-%m-%d')


# 获取本月的字符串格式（YYYY-MM）
def get_this_month():
    return datetime.now().strftime('%Y-%m')


# 获取本周的字符串格式（YYYY-WW）
def get_this_week():
    year, week, _ = datetime.now().isocalendar()
    return f"{year}-W{week:02d}"


@app.route('/event', methods=['GET'])
def handle_event():
    event = request.args.get('event')

    # 加载当前的统计信息
    stats = load_stats()

    # 更新总请求次数
    stats['total_requests'] += 1

    # 获取今天、这个月、这个周的日期信息
    today_date = get_today_date()
    this_month = get_this_month()
    this_week = get_this_week()

    # 更新每天的请求次数
    if today_date not in stats['daily_requests']:
        stats['daily_requests'][today_date] = 0
    stats['daily_requests'][today_date] += 1

    # 更新本月的请求次数
    if this_month not in stats['monthly_requests']:
        stats['monthly_requests'][this_month] = 0
    stats['monthly_requests'][this_month] += 1

    # 更新本周的请求次数
    if this_week not in stats['weekly_requests']:
        stats['weekly_requests'][this_week] = 0
    stats['weekly_requests'][this_week] += 1

    # 保存更新后的统计信息
    save_stats(stats)

    # 执行 AppleScript
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
    except subprocess.CalledProcessError as e:
        print(f"执行 AppleScript 时出错:{e.stderr}")
        return False


# 示例：调用函数并传入动态的 trigger_id
# trigger_id = "B483B59C-C8CC-4846-8953-43B6F045D07B"  # 动态传入触发器 ID
# execute_applescript(trigger_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)