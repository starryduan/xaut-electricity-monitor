# 🏫 西安理工电费监控 · 自动日报  
[![GitHub Workflow](https://github.com/starryduan/xaut-electricity-monitor/actions/workflows/elec.yml/badge.svg)](https://github.com/starryduan/xaut-electricity-monitor/actions)

每天 10:00（北京时间）自动抓取 **照明 + 空调** 电费余额，微信推送日报；低于预警线自动高亮提醒，不怕断电！

---

## ✨ 功能一览
| 功能 | 状态 |
|---|---|
| 每日定时推送 | ✅ 已开启（10:00） |
| 微信模板消息 | ✅ Server 酱 |
| 多房间监控 | ✅ 照明 4691 + 空调 3500 |
| 手动触发测试 | ✅ `Run workflow` 按钮 |

---

## 🚀 3 步跑通
1. **Fork** 本仓库 → Settings → Secrets → New repository secret  
   Name 填 `SCKEY`，Value 填你的 [Server 酱 SCKEY](https://sct.ftqq.com)  
2. 修改 `electricity_monitor.py` 顶部配置（openId / roomId / 阈值）后 `git push`  
3. 进入 Actions → Run workflow → 手机微信收到「日报」即成功！

---

## 📷 推送效果
| 项目 | 当前余额 | 预警线 | 状态 |
|---|---|---|---|
| 🔌 照明 | `29.60` 元 | 20.00 元 | ✅ 充足 |
| ❄️ 空调 | `35.80` 元 | 30.00 元 | ⚠️ 余额不足 |

> 快充入口：[点我直达](https://ammeter.xaut.edu.cn/#/pages/index/login)

---

## 🔧 自定义
- **改时间**：`.github/workflows/elec.yml` 里 `cron: '0 2 * * *'`（UTC 02:00 = 北京 10:00）  
- **改阈值**：`THRESHOLD_LIGHT / THRESHOLD_AC` 任意调整  
- **加房间**：再写一行 `get_balance(openId, roomId)` 即可

---

## 📝 依赖
- Python 3.11+（GitHub Actions 自带）  
- requests（自动安装）

---

## 🙋‍♂️ 常见问题
| 问题 | 快速排查 |
|---|---|
| 收不到微信 | 检查 SCKEY 是否正确、余额是否低于阈值 |
| Actions 红 ❌ | 看日志是否文件名拼错 / 缩进 tab |
| 想立即测试 | Actions → Run workflow 手动触发 |

---

⭐ 觉得好用点个 **Star** ~  
🐛 有问题直接发 [Issue](https://github.com/starryduan/xaut-electricity-monitor/issues) ，看到就回！