# WriteMind v0.2 — Personal Writing Coach

## 目标

WriteMind 不把“大师文风”覆盖到用户身上，而是把 Writer Lens 当作教练，把用户真实的改稿选择沉淀成自己的 Personal Style。

```text
Writer Lens + Personal Style + Platform Profile → Writing Coach
```

## 为什么需要 Revision Episode

只保存最终成稿无法知道用户为什么这样写。Revision Episode 记录：

- 原稿；
- 顾问建议；
- 用户最终版本；
- 接受了什么；
- 拒绝了什么；
- 用户为什么这么选；
- 这次可能形成什么个人写作规则。

默认同一规则需要至少 3 个独立 Revision Episodes 才升级为 `validated`。

## 私有数据

`personal/` 默认被 `.gitignore` 排除。个人文章、改稿和偏好不应因为使用公开的 WriteMind 仓库而自动公开。

## 本地初始化

```bash
python scripts/writemind.py init-personal "My Writing" --slug my-style
python scripts/writemind.py record-revision --profile my-style --input examples/revision-episode.example.json
python scripts/writemind.py build-personal-skill --profile my-style
```

## Coach 模式

一次只训练一个高杠杆问题：

```text
诊断 → 解释 → 局部示范 → 用户重写/选择 → 对照反馈 → Revision Episode → Personal Heuristic
```

用户如果明确要求直接成稿，Coach 不应强迫练习；先完成任务，再根据真实反馈学习。
