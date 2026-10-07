# Feishu AI Agent — 自定义 Skill

给飞书智能对话机器人写的两个 **OpenClaw 自定义 Skill**：日期计算与知识库检索。

> **合作与归属**
>
> 本项目是《跨学科跨文化大数据挖掘理论及应用研究》暑期课程作业的一部分，
> **由我与 [@chenqkkun](https://github.com/chenqkkun) 合作完成**。
> 机器人本体（OpenClaw 网关接入、飞书自建机器人、DeepSeek 模型配置）在
> [chenqkkun/feishu-ai-agent](https://github.com/chenqkkun/feishu-ai-agent)。
> **本仓库只包含我负责的那部分**：两个自定义 Skill 的指令文件、脚本实现，
> 以及给它们当语料的笔记。仓库结构做了调整，不是对方的目录原样。

---

## 这两个 Skill 解决什么

机器人本身能聊天，但它有两个短板：**日期算不对**、**答课程问题会一本正经地编**。
两个 Skill 分别把这两类问题从模型手里拿走，交给确定性的本地脚本：

```
飞书群聊 @机器人
      ↓
DeepSeek（deepseek-chat）决定：直接答 / 调 Skill
      ├── 日期时间类 → date-calculator   → Python 脚本算，模型只负责转述
      ├── 课程知识类 → knowledge-base    → 本地检索笔记，模型只负责转述
      └── 其它       → 模型直接答
      ↓
回复带着 [Skill Tool: xxx] 标记
```

---

## 目录结构

```
feishu-ai-agent-skills/
├── date-calculator/
│   ├── SKILL.md                  # 触发条件 + 命令表 + 回复格式
│   └── scripts/date_calc.py      # today / weekday / countdown / daysbetween / add / schedule
└── knowledge-base/
    ├── SKILL.md                  # 同上
    ├── scripts/search_kb.py      # 加权检索 + 按段落取摘要
    └── knowledge/                # 语料：自用复习笔记（见下）
```

部署时把两个目录放进网关工作区的 `skills/` 下，即
`<openclaw-workspace>/skills/date-calculator/`、`<openclaw-workspace>/skills/knowledge-base/`。

---

## 设计要点

### 1. 难的不是给模型能力，是让模型**放弃**它已有的答案

模型对"今天是几号"和"什么是卷积神经网络"都有很强的先验，写得再好的 Skill 也可能
根本不被调用 —— 它自己就答了，而日期算错、定义编歪。所以两个 `SKILL.md` 开头是：

```yaml
always: true
description: "MANDATORY for ALL ... You MUST run the script via the exec tool BEFORE
  answering. Do NOT answer from your own knowledge."
```

正文里再重复一遍 `NEVER answer ... directly`。**它不是提示，是纪律**：
这个项目里绝大部分文案都在做同一件事 —— 把模型的默认行为堵死。

### 2. 回答里带 `[Skill Tool: xxx]` 标记

两个 Skill 都要求模型在回复的第一行输出这个标记。它没有任何功能作用，
唯一的用处是**让人一眼看出这条回答来自本地脚本，还是来自模型的自由发挥**。
没有它，"模型没调工具、自己编了一个"和"调了工具"在聊天窗口里长得一模一样。

### 3. 检索没用向量库

语料只有几十 KB、查询是课堂问答，上向量库是过度设计。`search_kb.py` 用了一个
两段加权分：

```python
score = exact_score * 0.6 + term_score * 0.4
```

整句命中权重高、分词覆盖率权重低 —— 对"解释一下 tanh 激活函数"这类查询，
"tanh"这个词的精确出现比一堆词各沾一点更有指示性。

摘取也不是固定窗口，而是**按段落边界对齐**：找到命中位置后向前找 `\n\n`、向后找 `\n\n`，
避免返回半句话。

### 4. 两个具体的坑

| 坑 | 处理 |
|---|---|
| 网关捕获子进程 stdout 时中文乱码 | `sys.stdout.reconfigure(encoding='utf-8')` |
| 模型猜命令名不准（`dayofweek`? `dow`? `week`?） | `date_calc.py` 收一组别名，猜错也不报错 |

第二条是取舍：与其指望模型每次都说对 `weekday`，不如让它说错也能跑。
所有别名最终归一到同一个实现，不会出现两套行为。

---

## 相对合作版本的改动

拆出来时动过三处，都记在这里，方便与上游对照：

| 改动 | 为什么 |
|---|---|
| `SKILL.md` 里的绝对路径 → `<SKILL_DIR>` 占位 | 原文写的是网关所在那台机器的完整路径（含用户名），换机器就不通，也不该带着别人的用户名 |
| `date_calc.py` 补 `sys.stdout.reconfigure(encoding='utf-8')` | 它要输出中文星期名，而网关是经管道捕获 stdout 的，不设编码会乱码。兄弟脚本 `search_kb.py` 本来就有这一行，只它漏了 |
| 目录层级：`workspace/skills/<name>/` → `<name>/` | 这是 Skill 自己的仓库，不是网关工作区，少一层更直白 |

---

## 关于 `knowledge/` 里的语料

它是给 skill 当测试语料用的**自用复习笔记**，不是本项目的研究产出：

- `deeplearn_introduction.md`、`train_base_processAndsoon.md`、`create_tensorAndsoon.md`、
  `ANN_example.md` —— 跟着 PyTorch 教程一边敲一边记的课堂笔记
- `course_notes.md`、`exam_prep.txt` —— 通用知识点摘要，人工整理的示例数据

拿掉 `knowledge/`，`search_kb.py` 一样能跑，只是没东西可搜。

---

## 许可证

本仓库的代码与文档由我撰写，采用 **Mulan PSL v2**，全文见 [`LICENSE`](LICENSE)。

机器人本体及上游项目不在本仓库范围内，其授权状态见
[chenqkkun/feishu-ai-agent](https://github.com/chenqkkun/feishu-ai-agent)。
