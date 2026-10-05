# HCIS v2.1 — Historical Facsimile OCR Integration

## Status

**P0 core capability for Histora v2.1**

本文件把中国古籍原版影印识别正式纳入 Histora，而不是继续把古籍 OCR 当成普通文档 OCR 的附属能力。

---

## 1. 核心原则

### Reuse Before Re-OCR

已有可靠电子文本时优先复用，只有在缺失、质量不足、需要版本校勘或需要回到原始版面证据时才重新 OCR。

### Text First · Image Anchored · OCR On Demand

- 电子文本：用于大规模分析、检索和抽取。
- 原版影像：作为最终证据锚点。
- OCR：用于没有可靠电子文本、缺页、低置信区域、夹注、异文和关键证据复核。

### Original Never Overwritten

OCR、校正、规范化、翻译都只能形成新的 TextLayer，不得覆盖原始影像或已有转录。

---

## 2. v2.1 正式 OCR 技术栈

### 2.1 PaddleOCR / PaddleOCR-VL — 默认生产引擎

角色：

- 页面与文本区域检测
- 普通古籍影印识别
- 坐标输出
- Layout 分析
- 一般竖排文本
- 印章、生僻字等新版本能力

适用：

- 清晰影印本
- 版面相对规则的刻本、排印本
- 大批量第一遍识别

许可：以官方仓库当前 Apache-2.0 许可为准，版本升级时必须重新核验。

Adapter：

```text
PaddleHistoricalOCRAdapter
```

---

### 2.2 Kraken — 古籍/历史文献专用识别引擎

角色：

- 历史文献 OCR / HTR
- 竖排文字
- 自定义 segmentation
- 自定义字符识别模型
- PAGE XML / ALTO 等学术文档格式
- 字符级 / 行级位置关联

适用：

- 木刻本
- 复杂竖排
- 特殊字体
- 高价值古籍页
- 需要自训练的晚明 Corpus

Kraken 本体采用 Apache-2.0，可作为 Histora 正式 Adapter 后端。

Adapter：

```text
KrakenHistoricalOCRAdapter
```

---

### 2.3 CHAT Models — 中国历史文献研究模型

CHAT（Chinese Historical documents Automatic Transcription）与 Kraken 配合，对中文历史文献高度匹配，可用于：

- 古籍识别 Benchmark
- Research Mode
- Ground Truth 辅助生成
- Histora 自建模型的对照基线

**重要许可边界：** CHAT Models 当前按 CC BY-NC 4.0 处理，默认不得作为未来商业发行版的内置生产模型。

因此：

```text
Kraken engine = production-capable
CHAT model = research / benchmark only unless future license changes
```

任何打包、分发或商业化前必须再次自动核验模型许可证。

---

### 2.4 eScriptorium — 校对与 Ground Truth 工作流参考

Histora 不直接依赖其产品形态，但吸收其成熟工作流：

```text
OCR
↓
PAGE XML / structured regions
↓
Human Review
↓
Correction
↓
Ground Truth
↓
Golden Corpus
↓
Fine-tuning / Regression
```

目标是让 Histora 的人工校正结果可以反哺自己的历史 OCR 模型，而不是每次重新从零校正。

---

### 2.5 Historical Reading Order

中国古籍 OCR 的难点不仅是认字，还包括：

- 从右到左
- 竖排
- 双栏
- 夹注
- 双行小注
- 眉批
- 版心
- 页码
- 图文混排

v2.1 必须增加：

```text
HistoricalReadingOrderAdapter
```

HanDoc-OrderOCR 等研究项目可作为技术参考和 Benchmark，但在代码/模型许可未确认适合发行前，不作为强依赖。

---

### 2.6 TongGuOCR — Watchlist

TongGuOCR 与 Histora 古籍场景高度匹配，尤其关注复杂版式、生僻字和阅读顺序。

当前策略：

```text
WATCHLIST
```

只有在以下条件全部满足后才进入正式 Adapter：

1. inference code 已公开；
2. model weights 已公开；
3. license 已明确并可满足 Histora 使用方式；
4. 在 Histora Golden Corpus 上独立复测；
5. 不因单一论文 Benchmark 直接替换现有生产链。

预留：

```text
TongGuOCRAdapter
```

但 RC0/v2.1 不以其可用为前置条件。

---

## 3. Histora Historical Document Engine

目标链路：

```text
Acquired Source
      ↓
Digital text available?
  ┌───┴───────────────┐
 YES                  NO
  ↓                    ↓
Reuse text        Facsimile / Scan
  ↓                    ↓
Link image        Layout Detection
  └──────────┬─────────┘
             ↓
    OCR Engine Routing
             ↓
  ┌──────────┼──────────┐
  ↓          ↓          ↓
Paddle     Kraken    Future Adapter
  ↓          ↓          ↓
  └──────────┼──────────┘
             ↓
    Reading Order Fusion
             ↓
    Character Confidence
             ↓
 PAGE XML / Histora JSON
             ↓
      Human Review
             ↓
      Golden Ground Truth
             ↓
   Regression / Fine-tuning
```

---

## 4. OCR Routing Policy

### Tier A — Reliable digital text exists

不重新 OCR 全书。

只保留影像关联，并对关键证据、疑似错误、版本差异进行局部 OCR。

### Tier B — Clean printed facsimile

优先：

```text
PaddleOCR / PaddleOCR-VL
```

### Tier C — Historical print / complex vertical layout

优先：

```text
Paddle Layout Detection
+
Kraken Historical Recognition
+
Historical Reading Order
```

### Tier D — Manuscript / severe degradation / rare script

进入：

```text
SPECIAL_REVIEW_REQUIRED
```

可尝试 Kraken 自训练模型、人工转录或未来 HTR Adapter，但不得伪造高置信输出。

---

## 5. 证据追溯要求

任何 OCR 产生的文本必须可以追溯到原始影像区域。

最低要求：

```text
TextLayer
├─ source_version_id
├─ page_id
├─ region / bbox
├─ line_id
├─ engine
├─ engine_version
├─ model
├─ model_version
├─ confidence
├─ generated_at
└─ parent_layer_id
```

关键 Claim 最终应支持：

```text
Claim
↓
OCR / Transcription
↓
Page / Region
↓
Original Facsimile
↓
SourceVersion
↓
Provider / Institution
```

---

## 6. 古籍专用质量指标

Histora 不接受单一“识别率”指标。

必须至少评估：

- CER — Character Error Rate
- Character Accuracy
- Layout Detection Accuracy
- Reading Order Error
- Rare Character Accuracy
- Person Name Accuracy
- Place Name Accuracy
- Historical Date Accuracy
- Numeric Accuracy
- Sexagenary-cycle Accuracy
- Annotation / Small-note Recall

尤其是人名、日期、数字、干支错误，即使总体 CER 很低，也可能严重破坏历史推理，因此必须单独统计。

---

## 7. Golden Corpus

v2.1 建立 Historical OCR Golden Corpus，来源至少包括：

- 真实晚明影印页
- 不同版刻
- 竖排正文
- 夹注 / 小字
- 模糊 / 透页 / 污损页
- 人名密集页
- 数字 / 年号 / 干支密集页

优先真实来源：

- 《明季北略》
- 《国榷》
- 《崇祯长编》
- 明代地方志

第三方公开 Benchmark（例如 EvaHan、MTHv2、M5HisDoc）可用于外部比较，但不能替代 Histora 自己的真实晚明 Golden Corpus。

---

## 8. 与 Autonomous Research Acquisition Agent 的关系

自动获取智能体必须优先判断：

```text
可靠人工校对全文 + 原图
        ↓
可靠人工校对全文
        ↓
OCR 全文 + 原图
        ↓
只有原图
        ↓
Histora OCR
```

因此 OCR 是 Source Acquisition 的 fallback / verification capability，而不是所有史料的默认入口。

这避免重复数字化，同时保留原始证据链。

---

## 9. Code Lock 边界

本次属于 v2.1 Controlled Extension。

不得为了接入 OCR 项目修改以下核心原则：

- Source 原始文件不可变
- OCR 是派生层
- Claim ≠ FactCandidate
- OCR correction ≠ Textual Variant
- LOCAL_ONLY 不得调用云 OCR
- 每个 OCR 输出必须记录 provenance

若现有 Adapter Contract 无法支持必须的字段或行为，先提交 `CONTRACT_CHANGE_PROPOSAL.md`，不得静默修改 Level A 文件。

---

## 10. v2.1 P0 验收门槛

不得以 fixture-only 宣称完成。

至少必须真实通过：

1. 1 页清晰晚明竖排影印页；
2. 1 页含夹注 / 小字的复杂古籍页；
3. 1 页低质量扫描页；
4. Paddle 路径真实运行；
5. Kraken 路径真实运行；
6. OCR 字符可回跳到原始影像区域；
7. 关键人名 / 日期 / 数字单独评测；
8. Golden Corpus regression 可重复；
9. CHAT 等非商业模型不会进入不允许的发行路径；
10. 无可用 OCR 时返回明确 BLOCKED / REVIEW_REQUIRED，而不是伪造成功。

---

## 结论

Histora 不重新发明古籍 OCR。

其策略是：

> **复用成熟开源识别引擎 + 建立古籍专用 Adapter + 保留原图证据锚点 + 自建晚明 Golden Corpus + 人工校正反哺模型。**

这使古籍识别成为 Histora 严谨研究基础设施的一部分，而不是一个孤立 OCR 功能。
