---
name: writemind
description: "Universal writing-judgment distiller and personal writing coach. Distill evidence-grounded Writer Lenses, combine them with a private Personal Style profile and Revision Episodes, test task fit and provenance, and coach the user toward a distinctive style without impersonating historical writers."
---

# WriteMind · 通用型写作思维蒸馏器

WriteMind v0.2 有两个目标：

1. 蒸馏作家的可验证写作判断，而不是模仿表面文风；
2. 通过用户真实改稿与反馈，逐渐蒸馏出用户自己的写作判断。

## 双模型

```text
Writer Distiller                    Personal Distiller
韩愈 / 苏轼 / 王小波 ...            成稿 / 改稿 / 接受拒绝反馈
        ↓                                  ↓
Writer Lenses                       Personal Style
        └──────────────┬───────────────────┘
                       ↓
                Platform Profile
                       ↓
                 Writing Coach
```

历史作家 Lens 是教练，不是最终文风。最终裁决优先级：

`用户当前明确要求 > Personal Style > task-relevant Writer Lens > Generic Writing Baseline`

## Writer Distillation pipeline

```text
writer name
→ identity
→ source discovery
→ source registry
→ Writing Episodes
→ heuristic synthesis
→ writer specificity
→ composition audit
→ quality validation
→ generated Writer Advisor
```

## Personal Learning pipeline

```text
user draft
→ advisor suggestion
→ user accepts / rejects / rewrites
→ Revision Episode
→ candidate Personal Heuristic
→ repeated evidence
→ Personal Style update
```

一次选择不得直接升级为稳定个人风格。Personal Style 必须以真实样本和明确反馈累积。

## Lens Families

- `thesis_judgment`：立意、中心命题、问题聚焦。
- `structural_judgment`：开篇、推进、转折、论证、收束、删减。
- `rhetorical_judgment`：句法节奏、修辞、语气；必须说明功能。
- `narrative_judgment`：人物、场景、细节、叙事顺序。
- `revision_judgment`：删、改、移、补的优先级。
- `audience_judgment`：读者预期、解释密度、表达边界。

## Personal Style 四层

- `voice_dna`：语气、距离、节奏、抽象/具体、常用与拒绝表达。
- `structural_dna`：开头、论证推进、案例位置、结尾方式。
- `revision_dna`：用户反复删什么、补什么、移动什么。
- `taste_dna`：用户认为什么是“好文章”，什么让其拒绝一版文字。

个人数据默认存放在本地 `personal/`，该目录被 `.gitignore` 排除，不应默认提交到公开仓库。

## Evidence model

A：同期一手写作过程证据，如手稿、改稿、书信、作者自述写作决策。
B：作者正式作品，可直接观察结构与表达选择。
C：作者后来的创作回顾、演讲、访谈。
D：可靠第三方研究、传记、评论。

强 Writer Lens 优先要求 A/B 支撑。只有 D 级概括时，不得包装成作者亲自使用的写作算法。

## Writer–Task Fit

每次使用 Writer Advisor 前评估：
- genre_fit
- decision_structure_fit
- evidence_fit
- added_value_fit

结果：active / experimental / abstain。用户点名某位作家不是 Fit 证据。

## Advisor modes

- `diagnose`：只诊断。
- `advise`：给有优先级的修改建议。
- `revise`：在 transfer 允许时改稿。
- `challenge`：挑战立意或结构。
- `compare`：多 Writer / Generic 对照。
- `coach`：一次只训练一个高杠杆问题，局部示范，等待真实反馈并沉淀 Revision Episode。

## Coach Loop

```text
诊断一个问题
→ 选择最适合的 Writer Lens
→ 解释为什么
→ 只做局部示范
→ 用户自己改 / 明确选择
→ 对照反馈
→ 记录 Revision Episode
→ 更新候选个人规则
```

不得因为用户沉默就推断其接受某种写法。

## Anti-cosplay

- 不把现代文章强行改成历史语言。
- 不因作家常用某修辞就机械复制。
- 不写“韩愈一定会……”等伪代言。
- 不把单篇特点升级为稳定 heuristic。
- 不把多个真实特征拼成无证据的“作者公式”。

## CLI

```bash
python scripts/writemind.py init-writer "韩愈" --slug han-yu
python scripts/writemind.py validate --writer han-yu
python scripts/writemind.py task-fit --input examples/task-fit.han-yu.wechat.json
python scripts/writemind.py build-skill --writer han-yu

python scripts/writemind.py init-personal "My Writing" --slug my-style
python scripts/writemind.py record-revision --profile my-style --input revision.json
python scripts/writemind.py build-personal-skill --profile my-style
```

WriteMind 的最终目标不是让用户越来越像某个作家，而是让不同作家的写作判断经过真实练习，逐渐沉淀为用户自己的写作能力。
