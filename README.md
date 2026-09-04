# WriteMind

> Universal writing-judgment distiller — 把作家的写作判断，蒸馏成可调用的 AI 写作顾问。

WriteMind 不是“模仿文风”工具，也不是角色扮演器。

v0.2 开始，WriteMind 同时维护两类模型：

- `Writer Lens`：从韩愈、苏轼、王小波等作家的公开材料中蒸馏可验证写作判断；
- `Personal Style`：从用户自己的成稿、改稿、接受/拒绝反馈中蒸馏个人写作判断。

最终目标不是让用户越来越像某位作家，而是让不同作家的方法经过练习，逐渐变成用户自己的写作能力。

## 核心结构

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

## Writer Distillation

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

## Personal Learning

```text
user draft
→ advisor suggestion
→ user accepts / rejects / rewrites
→ Revision Episode
→ candidate Personal Heuristic
→ repeated evidence
→ Personal Style update
```

默认同一个人规则需要多个独立 Revision Episodes 才能从 `candidate` 晋级为 `provisional` / `validated`。

## Coach mode

Coach 不默认直接代写全文，而是一次训练一个高杠杆问题：

```text
诊断 → 解释 → 局部示范 → 用户重写/选择 → 对照反馈 → Revision Episode → Personal Heuristic
```

用户明确要求直接成稿时，先完成任务；只有真实反馈发生后，才进入个人学习链。

## 隐私

个人文章、改稿史和文风画像默认保存在本地 `personal/`，该目录已加入 `.gitignore`，不会因为使用公开仓库而自动提交到 GitHub。

## 当前 Golden Set

首个 Writer Golden Set：`韩愈 / han-yu`。

WriteMind 关注的是可迁移的写作决策，不是“韩愈腔”。例如当前 active lens `HY-H01` 关注：学习强文本时提取其写作动作与原则，再主动清除不属于当前文章的模板化或借来措辞。

## CLI

```bash
python scripts/writemind.py validate --writer han-yu
python scripts/writemind.py build-skill --writer han-yu

python scripts/writemind.py init-personal "My Writing" --slug my-style
python scripts/writemind.py record-revision --profile my-style --input examples/revision-episode.example.json
python scripts/writemind.py build-personal-skill --profile my-style
```

更多设计见：

- `SKILL.md`
- `prompts/coach.md`
- `prompts/personal-distiller.md`
- `references/personal-writing-coach.md`
- `references/build-quality-contract.md`

## 与 ResearchMind 的关系

WriteMind 借鉴 ResearchMind 的 Episode → Heuristic → Specificity → Task Fit → Provenance → Transfer 方法，但两者是完全独立的仓库和运行时。WriteMind 的开发不会修改 ResearchMind。
