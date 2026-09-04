# WriteMind

> Universal writing-judgment distiller — 把作家的写作判断，蒸馏成可调用的 AI 写作顾问。

WriteMind 不是“模仿文风”工具，也不是角色扮演器。

它试图回答两个更严格的问题：

1. 相比一个普通高水平写作 Agent，这位作者的公开作品、书信、序跋、评论、改稿记录与创作谈，究竟额外提供了什么可证据化、可区分的写作判断？
2. 面对当前这篇文章，这些判断真的应该被激活吗？

首个 Golden Set：**韩愈（Han Yu）**。

## 核心流程

```text
writer name
→ identity resolution
→ source discovery
→ source registry
→ Writing Episodes
→ contrastive heuristic synthesis
→ writer specificity assessment
→ composition audit
→ Writer–Task Fit
→ provenance check
→ transfer validation
→ Writer Advisor
```

## 不是“韩愈腔”

失败示例：把现代公众号改成半文言文、堆排比和古典词汇，然后声称“这是韩愈式写作”。

WriteMind 关注的是可迁移的写作决策，例如：

- 如何确定一篇文章唯一值得打穿的中心命题；
- 在什么情况下删掉枝蔓；
- 什么时候先叙事、什么时候直接立论；
- 如何安排反驳、转折、证据与收束；
- 什么样的句法节奏服务于当前功能，而不是单纯模仿表面风格。

只有这些判断能被来源与 Writing Episodes 支撑，并且与当前任务结构匹配时，才允许成为强 Writer Lens。

## 计划中的调用方式

```bash
python scripts/writemind.py init-writer "韩愈" --slug han-yu
python scripts/writemind.py validate --writer han-yu
python scripts/writemind.py task-fit --input task-fit.json
python scripts/writemind.py build-skill --writer han-yu
```

Agent Skill 使用层计划支持：

```text
$writemind 蒸馏 韩愈
$writemind 用韩愈顾问诊断这篇公众号文章
$writemind 让韩愈、王小波、汪曾祺分别评审这篇文章
```

## v0.1 设计原则

- **Evidence before persona**：证据优先于人物形象。
- **Decision before style**：先蒸馏写作判断，再考虑表达 DNA。
- **Specificity before branding**：普通写作常识不能包装成“某作家独门方法”。
- **Fit before activation**：用户点名某位作家，不等于该作家适合当前任务。
- **Abstention is valid**：没有可靠增量时，Writer Advisor 可以保持沉默。
- **No impersonation**：不得把模型推断写成“韩愈会说”“韩愈认为”。

## 目录

```text
config/                 # 单一机器 Policy Source
schemas/                # Episode / Heuristic / Profile schemas
prompts/                # 蒸馏与顾问提示规范
references/             # 方法论与证据规则
data/<writer>/          # 每位作者的来源、Episode、Heuristic
runtime/                # 路由、task-fit、验证逻辑
scripts/writemind.py    # CLI
tests/                  # 回归测试
examples/               # 顾问与对照实验
```

## 与 ResearchMind 的关系

WriteMind 借鉴 ResearchMind 已验证的 Episode → Heuristic → Specificity → Task Fit → Provenance → Transfer 方法，但两者是**完全独立的仓库和运行时**。

- ResearchMind：蒸馏科研判断。
- WriteMind：蒸馏写作判断。

ResearchMind 不会被 WriteMind 的开发修改。

## License

项目处于早期开发阶段。License 将在正式开源发布前确认。
