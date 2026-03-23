# encoding:utf-8
import os
import sys
import json
import requests
from datetime import datetime, timezone, time, timedelta
from bs4 import BeautifulSoup

PUSHPLUS_API = "http://www.pushplus.plus/send"
BEIJING_TZ = timezone(timedelta(hours=8))

def fetch_web_text(url):
    """获取网页的纯文本内容，失败返回None"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text(separator='\n', strip=True)
        return text
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

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
    url = os.environ.get("URL")
    if not token:
        print("错误: 未设置 PUSHPLUS_TOKEN")
        sys.exit(1)
 # 获取网页文本
    url = "url"
    web_text = fetch_web_text(url)
    now = datetime.now(BEIJING_TZ)
    title = f"每日通知 - {now.strftime('%m月%d日')}"
    
    # 构建推送内容，将 web_text 嵌入
    if web_text is None:
        content = f"""## 定时任务报告

**时间**: {now.strftime('%Y-%m-%d %H:%M:%S')} (北京时间)

**状态**: ❌ 网页获取失败

---
> 未能获取到网页内容，请检查网络或目标网站。
"""
    else:
        # 将网页文本以代码块或引用形式嵌入，避免格式混乱
        # 这里使用 Markdown 引用块，每行前加 > 
        quoted_text = '\n'.join(f"> {line}" for line in web_text.split('\n'))
        content = f"""## 定时任务报告

**时间**: {now.strftime('%Y-%m-%d %H:%M:%S')} (北京时间)

**状态**: ✅ 正常运行

---
> {quoted_text}
> 此消息由 GitHub Actions 自动发送
"""

    send_notification(token, title, content)


if __name__ == "__main__":
    main()
