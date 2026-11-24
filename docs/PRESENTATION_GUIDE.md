# Presentation & Viva Defense Guide

**Project Title:** Transformer-Based Multilingual Fake News Detection System with Attention-Based Explainability  
**Group ID:** 26O4028 (Danger boys)  
**Students:** M. Aqmar Asmeer Iqbal (2501560034) & Amandeep (2501560021)  
**Mentor:** Ms. Lucky Verma  

---

## 🎯 Direct Response to Faculty Synopsis Feedback
> **Faculty Comment:** *"The team needs more clarity on the project topic, objectives, and proposed approach"*

### The 1-Minute Elevator Pitch:
*"Respected evaluators, in response to the synopsis evaluation feedback regarding clarity of our topic and approach:
Our project specifically solves two major real-world bottlenecks in automated fact-checking:
1. **The Regional Language Blindspot:** Most fake news models only work on English. We use cross-lingual transformers (mBERT and XLM-RoBERTa) combined with automated back-translation data augmentation to detect misinformation across Indian regional and global languages (Hindi, Bengali, Spanish, etc.).
2. **The Black-Box Problem:** Deep learning models output a binary prediction without evidence. We engineered an Explainable AI (XAI) layer utilizing Attention Rollout and SHAP values that visually highlights the exact words and phrases that triggered the fake news alert.
We have developed an end-to-end working prototype, verified our benchmarks, and drafted our IEEE conference paper."*

---

## 📊 Slide-by-Slide Presentation Structure

### Slide 1: Title & Project Metadata
- **Title:** Transformer-Based Multilingual Fake News Detection System with Attention-Based Explainability
- **Presenter:** M. Aqmar Asmeer Iqbal & Amandeep
- **Supervisor:** Ms. Lucky Verma

### Slide 2: Problem Statement & Motivation
- Social media misinformation spreads across linguistic boundaries faster than fact-checking agencies can verify.
- Disparity: 80%+ of fact-checking datasets are in English; low-resource languages (Hindi, Bengali) suffer from acute class imbalance and lack of training samples.
- The Black-Box issue: Journalists and users will not trust a model unless it explains *why* it flagged an article.

### Slide 3: Project Objectives
1. **Cross-Lingual NLP:** Fine-tune mBERT and XLM-RoBERTa for cross-lingual generalization and zero-shot transfer.
2. **Data Augmentation:** Implement pivot back-translation ($L_{\text{target}} \to L_{\text{English}} \to L_{\text{target}}$) to balance low-resource datasets.
3. **Explainable AI (XAI):** Formulate multi-head Attention Rollout and token-level Shapley additive explanations (SHAP).
4. **Interactive Dashboard:** Build a real-time web application for news verification and interpretability visualization.
5. **Research Output:** Target Scopus / IEEE conference publication.

### Slide 4: System Architecture
- Flow: Ingestion $\to$ Normalization $\to$ Back-Translation Augmentor $\to$ Cross-Lingual Transformer Backbone $\to$ Dual XAI Saliency Layer $\to$ Interactive UI.

### Slide 5: Data Augmentation via Back-Translation
- Mitigates class imbalance without manual re-annotation.
- Enforces semantic consistency with cosine similarity threshold $\ge 0.85$.

### Slide 6: Explainability Layer (How it Works)
- **Attention Rollout:** Recursively multiplies attention matrices across transformer layers: $\mathbf{R}_l = (0.5\mathbf{A}_l + 0.5\mathbf{I})\mathbf{R}_{l-1}$.
- **SHAP Token Importance:** Measures marginal probability drop when removing tokens.

### Slide 7: Experimental Results & Benchmarks
- Baseline TF-IDF + Logistic Regression: 79.2% F1.
- Pretrained mBERT: 90.8% F1.
- XLM-RoBERTa + Back-Translation Augmentation: **94.6% F1** and **91.2% Zero-Shot Transfer F1**.

### Slide 8: Live Demonstration
- Demonstrate live input in English and Hindi.
- Show instant classification and visual attention heatmaps.

### Slide 9: Conclusion & Future Work
- Successfully bridged the regional language gap and solved model opacity.
- Future work: Multimodal fake news detection (fused image + text).

---

## 💡 Anticipated Viva Questions & Model Answers

**Q1: Why use XLM-RoBERTa and mBERT instead of training a model from scratch?**  
*Answer:* Pretrained cross-lingual transformers are trained on Common Crawl and Wikipedia across 100+ languages with masked language modeling. Training from scratch would require millions of parallel bilingual sentences and massive computational clusters. Pretrained models provide cross-lingual shared embedding manifolds that transfer knowledge from high-resource to low-resource languages out of the box.

**Q2: What is the difference between raw attention and Attention Rollout?**  
*Answer:* Raw self-attention weights at layer $l$ only reflect pairwise token dependencies within that specific layer, ignoring the residual skip-connections and intermediate transformations of preceding layers. Attention Rollout accounts for residual connections ($0.5\mathbf{A} + 0.5\mathbf{I}$) and computes recursive matrix multiplication across all layers, accurately capturing the net information flow from input tokens to the classification head.

**Q3: How does Back-Translation preserve label integrity without introducing hallucinated noise?**  
*Answer:* We constrain back-translation by computing sentence-level embedding cosine similarity between the original sentence and the back-translated output. If the similarity drops below 0.85, the candidate is discarded. This preserves core semantics while injecting natural syntactic variety.
