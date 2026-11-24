# Project Synopsis & Formal Research Proposal

## Project Title
**Transformer-Based Multilingual Fake News Detection System with Attention-Based Explainability**

---

### Project Identification & Team Metadata
- **Project Domain:** Natural Language Processing (NLP), Deep Learning, Cross-Lingual Information Retrieval, Explainable AI (XAI)
- **Academic Program:** Master of Computer Applications (MCA - 4th Year)
- **Project Group Code:** 26O4028 (Danger boys)
- **Team Leader:** M. Aqmar Asmeer Iqbal (Roll No: 2501560034)
- **Team Member:** Amandeep (Roll No: 2501560021)
- **Internal Faculty Mentor:** Ms. Lucky Verma
- **Target Publication Venue:** Scopus / IEEE / Springer Indexed Conference or Journal

---

### Response to Faculty Evaluation Feedback
> **Mentor Feedback:** *"The team needs more clarity on the project topic, objectives, and proposed approach."*  
> **Clarification & Action Plan:**  
> This revised synopsis provides an unambiguous, mathematically grounded, and system-level description of:
> 1. Exactly **which transformer architectures** are utilized and how cross-lingual alignment functions.
> 2. The explicit **data augmentation mechanism (Back-Translation & Lexical Perturbation)** utilized to combat low-resource regional language scarcity.
> 3. The **Explainable AI (XAI) mechanism**, replacing opaque black-box deep learning decisions with mathematically verified multi-head attention extraction and SHAP token saliency heatmaps.
> 4. An end-to-end working prototype architecture spanning ingestion, inference, interpretation, and an interactive graphical user interface.

---

## 1. Introduction and Background
The exponential proliferation of digital information across social media and online journalism platforms has democratized content dissemination. However, it has simultaneously accelerated the propagation of fabricated, manipulated, and politically or commercially motivated "fake news." 

While existing automated fact-checking and fake news detection frameworks have shown high benchmark accuracy for high-resource languages—primarily English—they suffer from two catastrophic limitations in real-world deployment:
1. **Linguistic Disparity & Low-Resource Failure:** Monolingual NLP models fail dramatically when deployed in multilingual or regional environments (such as Hindi, Bengali, Tamil, Spanish, etc.), where labeled fact-checking benchmarks are scarce or subject to severe class imbalance.
2. **The "Black-Box" Interpretability Deficit:** Traditional deep neural networks and recurrent models yield classification decisions without interpretable justification. In journalism, judicial governance, and trust-critical content moderation, automated flagging without transparent evidence induces user skepticism and hampers human editorial oversight.

This project introduces a **Transformer-Based Multilingual Fake News Detection System** equipped with an **Attention-Driven Explainability (XAI) layer**. By fine-tuning state-of-the-art multilingual pretrained language models—specifically **mBERT (Multilingual BERT)** and **XLM-RoBERTa (Cross-lingual RoBERTa)**—the system transfers semantic knowledge acquired across diverse languages to low-resource regional dialects. Furthermore, through self-attention matrix decomposition and SHAP (SHapley Additive exPlanations) token attribution, the system visually highlights the exact misleading lexical cues responsible for the classification.

---

## 2. Problem Statement
Given an arbitrary text sequence $T$ written in any supported language $L_i \in \{L_{\text{English}}, L_{\text{Hindi}}, L_{\text{Bengali}}, \dots\}$, where labeled training samples in $L_i$ are disproportionately scarce compared to high-resource languages, the objectives are:
1. **Binary / Fine-Grained Classification:** Predict whether $T$ belongs to class $y \in \{0 (\text{Real}), 1 (\text{Fake})\}$, maximizing macro-averaged $F_1$-score across all languages under both cross-lingual and zero-shot transfer settings.
2. **Class Imbalance Mitigation:** Synthetically augment low-resource representations using a controlled back-translation and lexical-substitution pipeline without corrupting semantic authenticity.
3. **Faithful Interpretability:** Generate a continuous attribution vector $\mathbf{\alpha} = (\alpha_1, \alpha_2, \dots, \alpha_n)$ over the input tokens $(t_1, t_2, \dots, t_n)$, such that $\alpha_k$ quantitatively and visibly represents the contribution of token $t_k$ to the final classification decision $P(y=1|T)$.

---

## 3. Mathematical & Theoretical Framework

### 3.1 Cross-Lingual Semantic Space (XLM-RoBERTa / mBERT)
Multilingual language models map tokens from disparate language alphabets into a shared cross-lingual embedding space $\mathbb{R}^d$. For an input token sequence $\mathbf{X} = [x_1, x_2, \dots, x_N]$:

$$\mathbf{H}^{(0)} = \mathbf{E}_{\text{token}}(\mathbf{X}) + \mathbf{E}_{\text{pos}}(\mathbf{X})$$

At each transformer encoder layer $l \in \{1, \dots, L\}$ with $H$ attention heads:

$$\mathbf{Q}_{h}^{(l)} = \mathbf{H}^{(l-1)}\mathbf{W}_{Q, h}^{(l)}, \quad \mathbf{K}_{h}^{(l)} = \mathbf{H}^{(l-1)}\mathbf{W}_{K, h}^{(l)}, \quad \mathbf{V}_{h}^{(l)} = \mathbf{H}^{(l-1)}\mathbf{W}_{V, h}^{(l)}$$

$$\mathbf{A}_{h}^{(l)} = \text{Softmax}\left(\frac{\mathbf{Q}_{h}^{(l)} (\mathbf{K}_{h}^{(l)})^T}{\sqrt{d_k}}\right)$$

$$\text{Head}_h^{(l)} = \mathbf{A}_{h}^{(l)} \mathbf{V}_{h}^{(l)}$$

$$\mathbf{H}^{(l)} = \text{LayerNorm}\left(\mathbf{H}^{(l-1)} + \text{Concat}(\text{Head}_1^{(l)}, \dots, \text{Head}_H^{(l)})\mathbf{W}_O^{(l)}\right)$$

The sequence classification representation is extracted from the special classification token (e.g., `[CLS]` or `<s>`):

$$\hat{y} = \sigma\left(\mathbf{W}_c \mathbf{h}_{\text{CLS}}^{(L)} + b_c\right)$$

### 3.2 Data Augmentation via Back-Translation
To address data scarcity in low-resource regional languages, we implement pivot-based Back-Translation:
Given a low-resource sample $T_{\text{target}}$:
1. Translate to a pivot language (English): $T_{\text{pivot}} = \mathcal{M}_{L_{\text{target}} \to L_{\text{pivot}}}(T_{\text{target}})$
2. Translate back to the original dialect: $T'_{\text{target}} = \mathcal{M}_{L_{\text{pivot}} \to L_{\text{target}}}(T_{\text{pivot}})$
3. Semantic Consistency Check: Validate cosine similarity $\cos(\mathbf{e}(T_{\text{target}}), \mathbf{e}(T'_{\text{target}})) \ge \tau$ (where $\tau = 0.85$).

### 3.3 Explainability Framework (Attention Rollout & SHAP)
1. **Multi-Head Attention Saliency:** We compute the cross-layer attention rollout to quantify information flow from token $j$ to the classification token `[CLS]`:
   $$\bar{\mathbf{A}}^{(l)} = \frac{1}{H} \sum_{h=1}^H \mathbf{A}_{h}^{(l)} + \mathbf{I}$$
   $$\mathbf{R} = \prod_{l=1}^L \bar{\mathbf{A}}^{(l)}$$
2. **Shapley Value Formulation:** For an individual token $x_i$, its marginal contribution $\phi_i$ across all possible token subsets $S \subseteq X \setminus \{i\}$ is formulated as:
   $$\phi_i(f, X) = \sum_{S \subseteq X \setminus \{i\}} \frac{|S|!(|X| - |S| - 1)!}{|X|!} \left[ f(S \cup \{i\}) - f(S) \right]$$

---

## 4. System Architecture
The proposed system comprises four sequential modules:

```
[Raw Multilingual Ingestion]
      │ (English, Hindi, Bengali, Spanish, etc.)
      ▼
[Preprocessing & Augmentation Engine]
      ├─ Normalization, De-noising, Script Detection
      └─ Back-Translation & Class-Balancing Augmentor
      ▼
[Cross-Lingual Transformer Backbone]
      ├─ mBERT (bert-base-multilingual-cased)
      └─ XLM-RoBERTa (xlm-roberta-base)
      ▼
[Dual Inference & Explainability Layer]
      ├─ Classification Head: P(Fake) vs P(Real)
      ├─ Multi-Head Attention Rollout Visualizer
      └─ SHAP Token Importance Heatmap Generator
      ▼
[Interactive Web Application & Dashboard]
      (Real-time Text Input, Language Tag, Confidence Gauges, Token Saliency)
```

---

## 5. Objectives & Deliverables
1. **Model Implementation:** Build and fine-tune mBERT and XLM-RoBERTa architectures on multilingual fake news corpora.
2. **Augmentation Pipeline:** Implement programmatic Back-Translation to expand regional language datasets by up to 200%.
3. **Explainability Dashboard:** Deliver interactive visual token heatmaps enabling non-technical users to inspect flagged words.
4. **Benchmarking & Validation:** Conduct zero-shot cross-lingual transfer experiments (train on English, evaluate on Indic languages).
5. **Scholarly Output:** Publish findings in an IEEE/Springer indexed venue detailing cross-lingual transfer efficiency and interpretability faithfulness.

---

## 6. Implementation Timeline & Work Breakdown

| Phase | Milestone / Task | Responsible | Duration | Status |
|---|---|---|---|---|
| **Phase 1** | Requirement analysis, dataset collection, baseline TF-IDF & BiLSTM pipeline | M. Aqmar Asmeer Iqbal | Weeks 1–2 | Complete |
| **Phase 2** | Preprocessing, back-translation data augmentation, linguistic balance | Amandeep | Weeks 3–4 | Complete |
| **Phase 3** | Transformer fine-tuning (mBERT & XLM-RoBERTa) & Hyperparameter tuning | Team (Both) | Weeks 5–7 | In Progress |
| **Phase 4** | XAI layer integration (Attention rollout, SHAP saliency extraction) | M. Aqmar Asmeer Iqbal | Weeks 8–9 | Complete |
| **Phase 5** | Web dashboard development, REST API, system integration | Amandeep | Weeks 10–11 | Complete |
| **Phase 6** | Empirical benchmarking, ablation studies, IEEE manuscript finalization | Team & Mentor | Weeks 12–14 | In Progress |
