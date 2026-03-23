# encoding:utf-8
import os
import sys
import json
import requests
from datetime import datetime, timezone, time, timedelta
from bs4 import BeautifulSoup

PUSHPLUS_API = "http://www.pushplus.plus/send"
BEIJING_TZ = timezone(timedelta(hours=8))

url = "https://tunnel.cloudsnow.top/download/sub"  # 替换为你想要获取的网址

try:
    # 发送 GET 请求，设置超时和常见的 User-Agent 头，避免被一些网站拒绝
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()  # 如果请求失败则抛出异常
    response.encoding = response.apparent_encoding  # 自动处理编码

    # 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 获取所有可见文本（去除 script, style 等标签）
    for script in soup(["script", "style"]):
        script.decompose()

    text = soup.get_text(separator='\n', strip=True)
    print(text)

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")

def send_notification(token, title, content, template="markdown"):
    data = {
        "token": token,
        "title": title,
        "content": content,
        "template": template,
    }
    headers = {"Content-Type": "application/json"}
    body = json.dumps(data).encode("utf-8")
    response = requests.post(PUSHPLUS_API, data=body, headers=headers, timeout=30)
    result = response.json()
    if result.get("code") == 200:
        print(f"推送成功: {title}")
    else:
        print(f"推送失败: {result.get('msg')}")
    return result


def main():
    token = os.environ.get("PUSHPLUS_TOKEN")
    if not token:
        print("错误: 未设置 PUSHPLUS_TOKEN")
        sys.exit(1)

    now = datetime.now(BEIJING_TZ)
    title = f"每日通知 - {now.strftime('%m月%d日')}"

    # ===== 在这里修改你的推送内容 =====
    
    text = text
    
    content = f"""## 定时任务报告

**时间**: {now.strftime('%Y-%m-%d %H:%M:%S')} (北京时间)

**状态**: ✅ 正常运行

---

> 此消息由 GitHub Actions 自动发送
"""

    send_notification(token, title, content)


if __name__ == "__main__":
    main()
