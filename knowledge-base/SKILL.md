---
name: knowledge-base
description: "MANDATORY for ALL course/deep-learning/ML/knowledge questions. You MUST run the script via the exec tool BEFORE answering. Do NOT answer from your own training data."
when_to_use: "any question about deep learning, neural networks, machine learning, supervised/unsupervised learning, activation functions (tanh/sigmoid/relu), regularization, tensors, training process, ANN, CNN, RNN, loss functions, backpropagation, gradient descent, course concepts, exam review, study material, notes lookup, knowledge search, what is X, explain X, 定义, 是什么, 解释一下"
always: true
---
# IMPORTANT: You MUST use the exec tool to run the script below. Do NOT answer ANY course/knowledge question directly.

When the user asks anything that could be answered from course notes / knowledge base / study material, run the search script via the **exec** tool and base your answer on its output. This covers deep learning, neural networks, machine learning concepts, formulas, training process, activation functions, regularization, tensors, and any technical question about course topics.

## When to call this skill (MANDATORY)

Call this skill whenever the user asks about ANY of these, even if they don't say "笔记" or "notes":

- Deep learning / 深度学习 concepts
- Neural networks / 神经网络 (ANN, CNN, RNN, etc.)
- Machine learning / 机器学习 (supervised / 监督学习, unsupervised / 无监督学习)
- Activation functions / 激活函数 (tanh, sigmoid, relu, softmax)
- Regularization / 正则化方法 (L1, L2, dropout)
- Tensors / 张量, tensor creation, tensor operations
- Training process / 训练过程 (forward pass, backpropagation, gradient descent, loss function)
- Course concepts, exam review, study material
- "What is X" / "X 是什么" / "解释一下 X" / "X 的定义" questions about technical topics
- Any question that might be in the user's course notes

## When NOT to call this skill

- Date/time questions (use date-calculator instead)
- Casual chat, greetings, or small talk
- Programming help unrelated to the course

## Path to the script

At runtime the script and the notes both live under the gateway workspace. Use
whatever Python 3 interpreter the gateway has, and substitute the real skill
directory for `<SKILL_DIR>`:

```
python <SKILL_DIR>/scripts/search_kb.py "QUERY" <SKILL_DIR>/knowledge
```

The `exec` tool needs the **absolute** path for both arguments — that is the only
reason the command is spelled out in full here.

Replace `QUERY` with the user's actual search term (keep the quotes). Use Chinese or English keywords, or both.

The script prints ranked excerpts from the notes in the `knowledge/` folder. Read the output and answer the user from it. If it prints `[NO_RESULTS]`, tell the user nothing was found in the knowledge base.

NEVER answer course/knowledge questions from your own training data. ALWAYS run this script first.

## Response Format (MANDATORY)

When you reply after running the script, you MUST start your reply with this exact tag on its own line:

[Skill Tool: knowledge-base]

Then continue with your answer based on the script output. Example:

[Skill Tool: knowledge-base]
Found in notes: Supervised learning is learning a function from labeled training data...

This tag tells the user that the answer came from the custom Skill tool, not from the model's own knowledge.
