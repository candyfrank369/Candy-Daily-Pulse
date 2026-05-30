# Candy Daily Pulse（每日业务脉搏）

一个用纯 Python 标准库写的命令行小工具，给我自己每天记录业务收支和年度目标进度。

## 一、这个工具是什么

Candy Daily Pulse 是一个 **中英双语命令行记账工具**，服务于我家公司 **CANDY & FRANK LTD**。
它可以每天记录 4 块业务的收入和支出，并自动计算公司离 **2026 年 AU$200,000 税后净收入目标**还差多少。

程序启动后会先选择语言：

- `1 = 中文`
- `2 = English`

选择后，菜单和提示会按所选语言显示。

## 二、它解决我的什么真实问题

我有 4 块真实业务，每天都有零散收入和支出。如果只靠脑子记，很难知道每块业务是否赚钱，也不知道全年 AU$200,000 税后净收入目标是否能完成。

这个工具解决的问题是：

- 每天快速记录每块业务的收入和支出
- 随时查看今天的收支
- 按业务查看总收入、总支出、净利
- 查看公司整体离 AU$200,000 目标还差多少
- 看到剩余天数和还需要的日均税后净利

4 块业务如下：

| 代号 | 中文名 | English |
|------|--------|---------|
| `camp` | 青少年创业营 | Youth Entrepreneurship Camp |
| `clothing` | 童装店 | Kids Clothing Store |
| `youtube` | YouTube 频道 | YouTube Channel |
| `secondhand` | 二手书玩具店 | Secondhand Toy & Book Store |

## 三、怎么运行

在项目文件夹中运行：

```bash
python3 main.py
```

要求：

- 需要 Python 3
- 不需要安装任何第三方库
- 只使用 Python 标准库：`json`、`os`、`datetime`
- 数据保存在 `data/pulse_data.json`
- 程序关闭后再打开，历史记录会自动读回来

主菜单功能：

1. 记一笔收入
2. 记一笔支出
3. 查看今天的收支
4. 查看全部汇总
5. 查看 AU$200,000 目标进度
6. 退出

## 四、目标进度怎么算

计算规则：

- 总收入 = 所有 `income` 记录金额之和
- 总支出 = 所有 `expense` 记录金额之和
- 税前净利 = 总收入 - 总支出
- 税后净利 = 税前净利 x (1 - 0.25)
- 距离目标 = 200000 - 税后净利
- 剩余天数 = 2026-12-31 - 今天
- 还需日均税后净利 = 距离目标 / 剩余天数
- 进度百分比 = 税后净利 / 200000 x 100

进度会用简单文字条显示，例如：

```text
[#####-----] 50.0%
```

## 五、6 个技术要素在代码哪里

现场讲解时可以按这个表说明：

| 技术要素 | 代码位置 |
|----------|----------|
| 1. 至少 3 个自定义函数 | `load_data()`、`save_data(data)`、`add_record(data, lang, kind=None)`、`show_summary(data, lang)`、`show_goal_progress(data, lang)`，另外还有 `choose_language()`、`show_today()`、`make_bar()`、`main()` |
| 2. 循环 + 条件判断 | `main()` 里的 `while True` 主菜单循环，以及 `if / elif / else` 处理用户选择；`show_summary()` 和 `show_goal_progress()` 里用 `for` 循环遍历记录 |
| 3. 字典 | 每一笔记录都是字典；`BUSINESSES` 保存 4 块业务；`TEXT` 保存中英文界面文字 |
| 4. try / except | `load_data()` 处理文件不存在和 JSON 损坏；`add_record()` 处理金额输入不是数字的情况 |
| 5. JSON 文件读写 | `load_data()` 用 `json.load` 读取 `data/pulse_data.json`；`save_data(data)` 用 `json.dump` 保存 |
| 6. Git 分支开发 + merge | 在 `feature/cli-tracker` 分支开发并提交，再 merge 回 `main` |

## 六、记录的数据长什么样

`data/pulse_data.json` 里保存的是一个列表，每一笔记录是一个字典：

```json
[
  {
    "date": "2026-05-30",
    "type": "income",
    "business": "camp",
    "amount": 500.0,
    "note": "夏令营报名"
  }
]
```
