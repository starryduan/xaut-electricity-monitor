import os
from datetime import datetime

import requests

# ========== 配置 ==========
OPEN_ID_LIGHT = "2241221070"   # 照明
ORG_CODE_LIGHT = "A000009"
ROOM_ID_LIGHT = "4691"         # 理工大厦北415（照明）

OPEN_ID_AC = "2241221070"      # 空调
ORG_CODE_AC = "A000009"
ROOM_ID_AC = "3500"            # 理工大厦北K415（空调）

THRESHOLD_LIGHT = 5100.0         # 照明阈值
THRESHOLD_AC = 1000.0            # 空调阈值

SCKEY = os.getenv("SCKEY", "")            # Server酱密钥
print("SCKEY=", SCKEY)

# ========== 推送 ==========
def send_wechat_alert(title, desp):
    # 让 desp 变成 高颜值 Markdown
    desp = f"""💡 **电费余额快报** | 西安理工大学
---

| 项目 | 当前余额 | 预警线 | 状态 |
|----|----|----|----|
| 🔌 照明 | `{light:.2f} 元` | {THRESHOLD_LIGHT} 元 | {'⚠️ 余额不足' if light < THRESHOLD_LIGHT else '✅ 余额充足'} |
| ❄️ 空调 | `{ac:.2f} 元` | {THRESHOLD_AC} 元 | {'⚠️ 余额不足' if ac < THRESHOLD_AC else '✅ 余额充足'} |

---

> 🎯 **小贴士**  
> 1. 推荐在 ** 22:00 前 ** 充值，避开系统结算高峰。  
> 2. 充电网址：https://ammeter.xaut.edu.cn/#/pages/index/login

---

🕒 推送时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    url = f"https://sctapi.ftqq.com/{SCKEY}.send"
    requests.post(url, params={"title": title, "desp": desp})

# ========== 查电费 ==========
def get_balance(open_id, room_id):
    url = "https://ammeter.xaut.edu.cn/pwsyscas/adk2xaut/getAccountInfo"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://ammeter.xaut.edu.cn",
        "Referer": "https://ammeter.xaut.edu.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    payload = {"openId": open_id}
    resp = requests.post(url, json=payload, headers=headers).json()
    for item in resp["result"]:
        if item["roomId"] == room_id:
            return float(item["baseBalance"])
    return None

# ========== 主逻辑 ==========
if __name__ == "__main__":
    light = get_balance("2241221069", "4691")  # 照明
    ac = get_balance("2241221070", "3500")  # 空调

    print(f"照明余额：{light} 元")
    print(f"空调余额：{ac} 元")

    msgs = []
    if light is not None and light < THRESHOLD_LIGHT:
        msgs.append(f"照明电费仅剩 {light} 元（阈值 {THRESHOLD_LIGHT} 元）")
    if ac is not None and ac < THRESHOLD_AC:
        msgs.append(f"空调电费仅剩 {ac} 元（阈值 {THRESHOLD_AC} 元）")

    if msgs:
        send_wechat_alert("西安理工电费充值提醒", "\n".join(msgs))