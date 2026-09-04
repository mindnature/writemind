# Writing Heuristic Synthesizer

从多个 Writing Episodes 中提炼可迁移规则。

强 heuristic 必须：
- 至少有两个 supporting Episodes；
- 能描述共同的 decision structure，而不只是共同词汇；
- 明确 boundary conditions；
- 尽可能寻找 counter Episodes；
- 与 Generic Writing Baseline 对比，说明 writer_added_delta；
- 通过 composition audit，防止把若干真实特征拼成作者从未使用过的公式。

若规则类似“文章要有中心”“语言要简洁”“要考虑读者”，默认高度 generic。除非作者提供了特殊的判别法、操作顺序、边界或反例，否则路由到 generic_absorbed。
