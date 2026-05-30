# Candy Daily Pulse（每日业务脉搏）

一个用纯 Python 标准库写的命令行小工具,给我自己每天用。

## 一、这个工具是什么

Candy Daily Pulse 是一个**双语(中文 / English)命令行记账工具**,服务于我家公司
**CANDY & FRANK LTD**。它让我每天快速记下每块业务的「收入」和「支出」,并自动算出
公司离 **2026 年 AU$200,000 税后净收入目标**还差多少。

启动时先选语言(`1 = 中文`,`2 = English`),之后所有菜单和提示都按所选语言显示。

## 二、它解决我的什么真实问题

我家公司有 **4 块真实业务**,每天都有零散的收支,但我心里没数,也不知道全年到底
能不能完成 AU$200,000 的税后目标。这个工具把每天的流水记下来,随时一键看到:

- 每块业务各自的总收入、总支出、净利
- 整个公司离 AU$200,000 目标还差多少、剩多少天、每天还得净赚多少

4 块业务:

| 代号 | 中文名 | English |
|------|--------|---------|
| `camp` | 青少年创业营 | Youth Entrepreneurship Camp |
| `clothing` | 童装店 | Kids Clothing Store |
| `youtube` | YouTube 频道 | YouTube Channel |
| `secondhand` | 二手书玩具店 | Secondhand Toy & Book Store |

## 三、怎么运行

```bash
python3 main.py
```

- 需要 **Python 3**(用到 f 风格的 `.format()` 和标准库,Python 3.6+ 即可),无需安装任何第三方包。
- 数据保存在 **`data/pulse_data.json`**。程序关掉再打开,记录还在,会自动读回。
- 第一次运行还没有数据文件,工具会自动新建 `data/` 文件夹和 JSON 文件。

主菜单功能:

1. 记一笔收入
2. 记一笔支出
3. 查看今天的收支
4. 查看全部汇总(按业务分类的总收入、总支出、净利)
5. 查看 AU$200,000 目标进度
6. 退出

## 四、目标进度怎么算

- 总收入 = 所有 `income` 记录金额之和
- 总支出 = 所有 `expense` 记录金额之和
- 税前净利 = 总收入 − 总支出
- 税后净利 = 税前净利 × (1 − 0.25)　← 税率 25%
- 距离目标 = 200000 − 税后净利
- 剩余天数 = 2026-12-31 − 今天(用 `datetime` 算)
- 还需日均税后净利 = 距离目标 ÷ 剩余天数(已达标则显示「已达成目标!」)
- 进度百分比 = 税后净利 ÷ 200000 × 100,并用文字进度条 `[#####-----]` 显示

## 五、6 个技术要素在代码哪里(现场讲解对照表)

> 行号以 `main.py` 为准,若微调请以函数名为准搜索。

| 技术要素 | 落在哪里 |
|----------|----------|
| **1. 至少 3 个自定义函数** | `load_data()`、`save_data(data)`、`add_record(data, lang, kind)`、`show_summary(data, lang)`、`show_goal_progress(data, lang)`,另有 `choose_language()`、`show_today()`、`make_bar()`、`main()` |
| **2. 循环 + 条件判断** | `main()` 里的 `while True` 主菜单循环 + `if / elif / else` 分发选项;`show_summary()` 和 `show_goal_progress()` 里用 `for` 循环遍历所有记录累加 |
| **3. 用字典存数据** | 每一笔记录是字典 `{"date":..., "type":..., "business":..., "amount":..., "note":...}`(见 `add_record()`);界面文案字典 `TEXT`;业务配置字典 `BUSINESSES` |
| **4. try / except 异常处理** | `add_record()` 里输入金额用 `try/except ValueError` 捕获非数字并重输;`load_data()` 里用 `try/except` 处理 `FileNotFoundError` 和 `json.JSONDecodeError` |
| **5. 数据存到本地 JSON 文件** | `save_data()` 用 `json.dump` 写入 `data/pulse_data.json`;`load_data()` 用 `json.load` 读回 |
| **6. Git 分支开发 + merge 回 main** | 在 `feature/cli-tracker` 分支开发,分多次 commit,最后 `git merge` 回 `main`(见 `git log --oneline` 和 `git branch`) |

## 六、记录的数据长什么样

`data/pulse_data.json` 里就是一个记录列表,每条是一个字典:

```json
[
  {"date": "2026-05-30", "type": "income", "business": "camp", "amount": 500.0, "note": "夏令营报名"}
]
```
