# Writer–Task Fit

四维评分均为 0–100：

- genre_fit：原作者强证据覆盖的文体与当前目标文体接近程度。
- decision_structure_fit：来源中的写作问题与当前文章的问题是否具有相同决策结构。
- evidence_fit：拟激活 heuristic 的 Episode、source locator、specificity 是否充分。
- added_value_fit：相比 Generic Writing Baseline，作者 Lens 是否提供明确增量。

默认权重见 config/policy.json。

active：可进入 provenance / transfer 检查。
experimental：只能诊断、提问题、提供备选视角；默认不能大规模重写。
abstain：不用该 Writer Lens，继续提供 Generic Writing Baseline。

跨文体时，genre_fit 很低不能靠“作者名气”补分。
