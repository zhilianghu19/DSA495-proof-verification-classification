"""Shared split checks and reports for proof-validity experiments."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

LABELS = ["Valid", "Invalid"]


def load_split(name, split_dir=Path("../Data/splits")):
    files = sorted((split_dir / name).glob("proofwiki_review_*.json"))
    rows = pd.concat([pd.read_json(file) for file in files], ignore_index=True)
    rows = rows.dropna(subset=["validity"]).reset_index(drop=True)
    assert rows["validity"].isin(LABELS).all() and rows["clean_row_index"].is_unique
    if name != "train":
        rows = rows.drop(columns=["review_reason"], errors="ignore")
    return rows


def check_separate(left, right):
    for col in ("clean_row_index", "theorem_id", "theorem_text", "proof_text"):
        assert set(left[col]).isdisjoint(right[col]), f"Shared {col} across splits"


def save_results(output_dir, model, splits, predictions, config):
    """Save the same per-proof predictions, metrics and matrices as the DistilBERT notebook."""
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics, records, matrices = [], [], {}
    for variant, by_split in predictions.items():
        matrices[variant] = {}
        for name, predicted in by_split.items():
            data = splits[name]
            actual = data["validity"]
            assert len(predicted) == len(data) and set(predicted).issubset(LABELS)
            report = classification_report(actual, predicted, labels=LABELS, output_dict=True, zero_division=0)
            metrics.append({"Model": model, "Training input": variant, "Split": name, "Proofs": len(data),
                            "Actual Invalid": int(report["Invalid"]["support"]),
                            "Invalid precision": report["Invalid"]["precision"], "Invalid recall": report["Invalid"]["recall"],
                            "Macro F1": report["macro avg"]["f1-score"]})
            records.append(data[["clean_row_index", "theorem_id"]].assign(
                model=model, training_input=variant, split=name, actual=actual, predicted=predicted))
            matrices[variant][name] = confusion_matrix(actual, predicted, labels=LABELS).tolist()
        matrix = np.array(matrices[variant]["test"])
        chart = ConfusionMatrixDisplay(matrix, display_labels=LABELS)
        chart.plot(cmap="Blues", colorbar=False, values_format="d")
        chart.ax_.set(title=f"{model} · {variant.replace('_', ' ')}", xlabel="Model prediction", ylabel="Review label")
        chart.figure_.tight_layout()
        chart.figure_.savefig(output_dir / f"test_{variant}.png", dpi=150)
        plt.show()
        plt.close(chart.figure_)
        print(f"{variant}: caught {matrix[1,1]} of {matrix[1].sum()} Invalid proofs; flagged {matrix[0,1]} Valid proofs.")
    scores = pd.DataFrame(metrics)
    scores.to_csv(output_dir / "metrics.csv", index=False)
    pd.concat(records, ignore_index=True).to_csv(output_dir / "predictions.csv", index=False)
    config = dict(config, confusion_matrices=matrices)
    (output_dir / "experiment.json").write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return scores


def predict_without_training(model, tokenizer, rows, config):
    """Use the fine-tuning notebook's head/tail token budget and inference precision."""
    import torch

    def keep_ends(tokens, budget):
        if len(tokens) <= budget:
            return tokens
        first = (budget + 1) // 2
        return tokens[:first] + tokens[-(budget - first):]

    text_budget = config["max_length"] - config["reason_limit"] - 4
    theorems = tokenizer(rows["theorem_text"].tolist(), add_special_tokens=False, verbose=False)["input_ids"]
    proofs = tokenizer(rows["proof_text"].tolist(), add_special_tokens=False, verbose=False)["input_ids"]
    encoded = []
    for theorem, proof in zip(theorems, proofs):
        theorem = keep_ends(theorem, config["theorem_limit"])
        proof = keep_ends(proof, text_budget - len(theorem))
        encoded.append([tokenizer.cls_token_id] + theorem + [tokenizer.sep_token_id] + proof + [tokenizer.sep_token_id])

    model.eval()
    batch_size = config["batch_size"]
    predicted = []
    with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
        for start in range(0, len(encoded), batch_size):
            inputs = tokenizer.pad({"input_ids": encoded[start:start + batch_size]}, padding=True,
                                   pad_to_multiple_of=8, return_tensors="pt").to(model.device)
            predicted.extend(LABELS[i] for i in model(**inputs).logits.argmax(dim=1).tolist())
    return predicted


def save_test_scores(output_dir, model, test, predicted, invalid_scores):
    """Save one plotted point per test proof, using the model's own decision."""
    rows = test[["clean_row_index", "theorem_id", "title"]].copy()
    rows.insert(0, "model", model)
    rows["actual"] = test["validity"]
    rows["predicted"] = list(predicted)
    rows["invalid_score"] = list(invalid_scores)
    assert rows["clean_row_index"].is_unique and rows["invalid_score"].between(0, 1).all()
    assert rows["actual"].isin(LABELS).all() and rows["predicted"].isin(LABELS).all()
    non_ties = rows[rows["invalid_score"] != 0.5]
    assert non_ties["predicted"].eq("Invalid").equals(non_ties["invalid_score"].gt(0.5))
    outcomes = {("Valid", "Valid"): "Correctly accepted", ("Valid", "Invalid"): "False alarm",
                ("Invalid", "Valid"): "Missed error", ("Invalid", "Invalid"): "Error caught"}
    rows["outcome"] = [outcomes[pair] for pair in zip(rows["actual"], rows["predicted"])]
    output_dir.mkdir(parents=True, exist_ok=True)
    rows.sort_values("clean_row_index").to_csv(output_dir / "test_proof_scores.csv", index=False)
