from typing import Dict, List, Optional, Tuple, Union
import numpy as np

class AttentionExplainer:
    """
    Attention-Based Explainability (XAI) Engine for Multilingual Transformers.
    Extracts multi-head attention matrices, computes Attention Rollout, and maps
    token-level saliency weights to explain why a news item was flagged as FAKE or REAL.
    """
    def __init__(self, discard_ratio: float = 0.9):
        self.discard_ratio = discard_ratio

    @staticmethod
    def compute_attention_rollout(
        all_layer_attentions: Union[List[np.ndarray], Tuple[np.ndarray, ...]]
    ) -> np.ndarray:
        """
        Computes Attention Rollout across transformer encoder layers:
        R_{l} = (0.5 * A_{l} + 0.5 * I) * R_{l-1}
        where A_{l} is the mean attention across all attention heads.
        """
        if not all_layer_attentions:
            raise ValueError("No attention matrices provided.")

        # Number of layers
        num_layers = len(all_layer_attentions)
        
        # Take first layer to get sequence length
        first_layer = np.array(all_layer_attentions[0])
        # Expected shape: [batch_size, num_heads, seq_len, seq_len] or [num_heads, seq_len, seq_len]
        if first_layer.ndim == 4:
            first_layer = first_layer[0]  # Take first batch item
            
        seq_len = first_layer.shape[-1]
        rollout = np.eye(seq_len)

        for layer_attn in all_layer_attentions:
            layer_arr = np.array(layer_attn)
            if layer_arr.ndim == 4:
                layer_arr = layer_arr[0]
            # Average across attention heads: [seq_len, seq_len]
            mean_head_attn = np.mean(layer_arr, axis=0)
            
            # Add identity matrix to account for residual connections
            residual_attn = 0.5 * mean_head_attn + 0.5 * np.eye(seq_len)
            # Row-normalize to keep stochastic distribution
            residual_attn = residual_attn / (np.sum(residual_attn, axis=-1, keepdims=True) + 1e-9)
            # Recursive matrix multiplication
            rollout = np.matmul(residual_attn, rollout)

        return rollout

    def extract_token_saliency(
        self,
        tokens: List[str],
        attentions: Union[List[np.ndarray], Tuple[np.ndarray, ...]],
        cls_token_idx: int = 0
    ) -> List[Dict[str, Union[str, float]]]:
        """
        Extracts the attention weights allocated from the [CLS] / <s> classification
        token to every other token in the sequence.
        """
        rollout_matrix = self.compute_attention_rollout(attentions)
        # Saliency of all tokens relative to classification token
        cls_saliency = rollout_matrix[cls_token_idx, :len(tokens)]
        
        # Min-max normalization for interpretable scaling [0, 1]
        min_v = np.min(cls_saliency)
        max_v = np.max(cls_saliency)
        if max_v > min_v:
            normalized_saliency = (cls_saliency - min_v) / (max_v - min_v)
        else:
            normalized_saliency = np.ones_like(cls_saliency)

        results = []
        for token, raw_score, norm_score in zip(tokens, cls_saliency, normalized_saliency):
            # Filter special tokens from visual highlighting if desired
            results.append({
                "token": token,
                "raw_attention": float(raw_score),
                "saliency_weight": float(norm_score),
                "is_special": token in ["[CLS]", "[SEP]", "<s>", "</s>", "<pad>"]
            })

        return results

    @staticmethod
    def render_html_heatmap(
        token_saliencies: List[Dict[str, Union[str, float]]],
        highlight_color: str = "#ff4b4b"
    ) -> str:
        """
        Renders an interactive HTML snippet displaying colored token heatmaps.
        Higher attention weights are highlighted in darker intensity.
        """
        spans = []
        for item in token_saliencies:
            token = item["token"]
            weight = item["saliency_weight"]
            
            # Subword token cleanup for mBERT (##) or XLM-RoBERTa ( )
            display_token = token.replace("##", "").replace(" ", " ")
            alpha = max(0.08, min(1.0, weight * 0.95))
            
            style = (
                f"background-color: rgba(255, 75, 75, {alpha:.2f}); "
                f"padding: 2px 5px; margin: 2px; border-radius: 4px; "
                f"display: inline-block; font-family: monospace; font-size: 14px;"
            )
            tooltip = f"Attention Weight: {weight:.4f}"
            spans.append(f'<span style="{style}" title="{tooltip}">{display_token}</span>')
            
        return f'<div style="line-height: 2.2; background-color: #f8f9fa; padding: 15px; border-radius: 8px; border: 1px solid #e2e8f0;">{" ".join(spans)}</div>'
