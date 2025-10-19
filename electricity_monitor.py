import os
from datetime import datetime

import requests

# ========== 配置 ==========
OPEN_ID_LIGHT = "2241221069"   # 照明
ROOM_ID_LIGHT = "4691"         # 理工大厦北415（照明）

OPEN_ID_AC = "2241221070"      # 空调
ROOM_ID_AC = "3500"            # 理工大厦北K415（空调）

THRESHOLD_LIGHT = 5100.0       # 照明预警线
THRESHOLD_AC = 1000.0          # 空调预警线

SCKEY = os.getenv("SCKEY", "").strip()

# ========== 推送 ==========
def send_wechat_alert(title, desp):
    if not SCKEY:
        print("⚠️  SCKEY 为空，跳过推送")
        return
    url = f"https://sctapi.ftqq.com/{SCKEY}.send"
    requests.post(url, params={"title": title, "desp": desp}, timeout=10)

# ========== 查电费 ==========
def get_balance(open_id, room_id):
    url = "https://ammeter.xaut.edu.cn/pwsyscas/adk2xaut/getAccountInfo"
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://ammeter.xaut.edu.cn",
        "Referer": "https://ammeter.xaut.edu.cn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    resp = requests.post(url, json={"openId": open_id}, headers=headers, timeout=10).json()
    for item in resp["result"]:
        if str(item["roomId"]) == str(room_id):
            return float(item["baseBalance"])
    return None

# ========== 每日日报 ==========
if __name__ == "__main__":
    light = get_balance(OPEN_ID_LIGHT, ROOM_ID_LIGHT)
    ac = get_balance(OPEN_ID_AC, ROOM_ID_AC)

    print(f"照明余额：{light} 元")
    print(f"空调余额：{ac} 元")

    desp = f"""💡 **西理工电费日报** | {datetime.now():%Y-%m-%d %H:%M:%S}
---

| 项目 | 当前余额 | 预警线 | 状态 |
|----|----|----|----|
| 🔌 照明 | `{light:.2f}` 元 | {THRESHOLD_LIGHT} 元 | {'⚠️ 余额不足' if light and light < THRESHOLD_LIGHT else '✅ 充足'} |
| ❄️ 空调 | `{ac:.2f}` 元 | {THRESHOLD_AC} 元 | {'⚠️ 余额不足' if ac and ac < THRESHOLD_AC else '✅ 充足'} |

---

> 🎯 **小贴士**  
> 1. 推荐在 **22:00 前** 充值，避开系统结算高峰  
> 2. 快充入口：[点击直达](https://ammeter.xaut.edu.cn/#/pages/index/login)

---
🕒 推送时间：{datetime.now():%Y-%m-%d %H:%M:%S}
"""
    send_wechat_alert("西理工电费日报", desp)