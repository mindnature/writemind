---
name: writemind
description: "Universal writing-judgment distiller. Distill a writer's evidence-grounded writing decisions into a callable Writer Advisor. Reconstruct Writing Episodes, synthesize writer-specific heuristics, test task fit and provenance, and abstain when the writer adds no reliable value. Never impersonate the writer or confuse surface style imitation with writing judgment."
---

# WriteMind · 通用型写作思维蒸馏器

WriteMind 不做“作家 cosplay”。它蒸馏的是可验证的写作判断。

## 核心问题

1. 这位作者相比 Generic Writing Baseline 多提供了什么？
2. 这些增量是否有作品、书信、改稿、创作谈等证据支持？
3. 面对当前文章，它是否适用？
4. 如果不适用，系统是否愿意让这位 Writer Advisor 保持沉默？

## Distillation pipeline

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

## Advisor pipeline

```text
user text + task
→ writing baseline
→ Writer–Task Fit
→ lens activation / experimental / abstain
→ provenance packet
→ transfer validation
→ diagnose / advise / revise / challenge / compare
```

## Lens Families

- `thesis_judgment`：立意、中心命题、问题聚焦。
- `structural_judgment`：开篇、推进、转折、论证、收束、删减。
- `rhetorical_judgment`：句法节奏、修辞选择、语气强弱；必须说明其功能，禁止只做表面模仿。
- `narrative_judgment`：人物、场景、细节、叙事顺序、信息释放。
- `revision_judgment`：删、改、移、补的优先级与修改决策。
- `audience_judgment`：读者预期、传播对象、解释密度与表达边界。

## Evidence model

A：同期一手写作过程证据，如手稿、改稿、书信、作者自述写作决策。
B：作者正式作品，可直接观察结构与表达选择。
C：作者后来的创作回顾、演讲、访谈。
D：可靠第三方研究、传记、评论。

强 Writer Lens 优先要求 A/B 支撑。只有 D 级概括时，不得包装成“作者亲自使用的写作算法”。

## Static heuristic dimensions

`status`: candidate / provisional / validated / rejected

`routing.lens_eligibility`:
- active_lens
- experimental_lens
- generic_absorbed
- excluded

普通写作常识即使正确，也应进入 `generic_absorbed`，不能因为挂了作家名字就变成“独门方法”。

## Writer–Task Fit

每次使用 Writer Advisor 前评估：
- genre_fit
- decision_structure_fit
- evidence_fit
- added_value_fit

结果：active / experimental / abstain。

用户点名“请用韩愈”不是 Fit 证据。

## Advisor modes

- `diagnose`：只诊断，不代写。
- `advise`：提出有优先级的修改建议。
- `revise`：在允许的 lens 范围内改稿。
- `challenge`：用该作者的证据化判断挑战文章立意或结构。
- `compare`：同一篇文章进行多 Writer / Generic 对照。

## Anti-cosplay rules

- 不把现代文章强行改成作者时代语言。
- 不因作者常用某修辞，就机械增加该修辞。
- 不写“韩愈一定会……”等伪代言。
- 不把单篇作品的局部特点直接升级为稳定 heuristic。
- 不把多个真实特征拼成一个从未被证据支持的“作者公式”。

## CLI

```bash
python scripts/writemind.py init-writer "韩愈" --slug han-yu
python scripts/writemind.py validate --writer han-yu
python scripts/writemind.py task-fit --input examples/task-fit.han-yu.wechat.json
python scripts/writemind.py transfer-action high
python scripts/writemind.py build-skill --writer han-yu
python scripts/writemind.py list-writers
```

WriteMind 的成功标准不是“每次都像某位大师”，而是能够区分：哪里是普通写作常识，哪里确实来自这位作者的可验证判断，以及什么时候根本不该调用这位作者。
