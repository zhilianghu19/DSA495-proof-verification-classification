# Classifying the validity of mathematical proofs with NLP

**Liam Hu · DSA 495**

Given a theorem and a proposed proof, can a text classifier tell whether the proof establishes the theorem? The project compares character TF-IDF with logistic regression against four fine-tuned BERT encoders on ProofWiki. A second experiment changes a mathematical step and measures whether the model changes its verdict. The implemented prediction task is **Valid / Invalid**. Four error categories describe the reasons of invalidity. Predicting those categories could be an extension.

## Data and workflow

1. **Clean the source.** Downloaded [naturalproofs_proofwiki.json](https://zenodo.org/records/4902289/files/naturalproofs_proofwiki.json?download=1) from the dataset table in the `wellecks/naturalproofs` GitHub repository and wrote `src/clean_proofwiki.py` to remove incomplete or ambiguous proofs and strip wiki markup while preserving mathematical notation.

   - `Data/naturalproofs_proofwiki_clean.json` contains 6,155 of the original 19,234 theorem–proof pairs, with one record per retained proof version.

2. **Annotate and split.** AI reviewed the first 900 proof versions, gave a reason for each verdict, and assigned one error category to each Invalid proof. Grouped proofs of the same theorem in one review file before splitting the files into training, validation, and test sets.

   - [Data/annotations/](Data/annotations/) contains 30 original review files with 30 theorem–proof pairs each.
   - [Data/splits/](Data/splits/) contains 24 training files, 3 validation files, and 3 test files. In training files 026–030, 122 Valid proofs were replaced with deliberately flawed versions.

   The table counts the proofs used for training and evaluation after those replacements. It excludes 13 proofs whose validity could not be determined.

   | Labeled proof versions | Train | Validation | Test |
   |---|---:|---:|---:|
   | Valid | 474 | 74 | 75 |
   | Invalid | 235 | 15 | 14 |
   | Total | 709 | 89 | 89 |

   An Invalid proof fails to establish its theorem. Each Invalid proof receives one primary error category.

   - **Invalid inference.** A step draws a conclusion that does not follow from the preceding statements.
   - **Unjustified assumption.** The proof assumes a fact that the theorem does not give and earlier steps have not established.
   - **Missing essential justification.** The proof skips a necessary argument, such as the induction step after checking the base case.
   - **Misapplied theorem / unmet conditions.** The proof invokes a theorem without establishing its hypotheses or uses it to claim more than it guarantees.

3. **Train and evaluate.** Trained the TF-IDF baseline and four BERT models with and without review reasons, selected each configuration by validation Macro F1, and evaluated it on the test set. I also evaluated each pretrained BERT with a newly initialized classification head before fine-tuning.

   - [01_Proof_Validity_Baseline.ipynb](Notebooks/01_Proof_Validity_Baseline.ipynb) reports the baseline scores and confusion matrices.
   - BERT notebooks: [DistilBERT](Notebooks/02_DistilBERT.ipynb), [ModernBERT-base](Notebooks/03_ModernBERT_base.ipynb), [MathBERT](Notebooks/04_MathBERT.ipynb), [DeBERTa-v3-base](Notebooks/05_DeBERTa_v3_base.ipynb). Each compares training with and without review reasons and reports test results for both settings.
   - [Results/TF-IDF/](Results/TF-IDF/) contains the baseline settings, validation and test metrics, per-proof predictions, and test confusion matrices for both input settings. In the review-reason setting, the baseline also reads the reason at test time. The BERT models read only the theorem and proof at test time.
   - [Results/model_comparison.csv](Results/model_comparison.csv) lists validation and test metrics for the four fine-tuned BERT models under both training settings.

4. **Review and edit proofs.** Manually reviewed the [25 test proofs](Results/all_five_correct_test_without_review_reason.json) that all five models classified correctly using only the theorem and proof and kept 18 pairs that are unambiguous. Then created one flawed version of each of the 16 retained Valid proofs, plus additional symbol edits and valid rewrites for three of them.

   - [Manual review of 25 proofs](Results/manual_review_25_proofs.md) includes each theorem, submitted proof and manual review decision.
   - [manually_reviewed_test_proofs.json](Results/manually_reviewed_test_proofs.json) contains the 18 proofs retained after review, including 16 Valid and 2 Invalid.
   - [proof_edit_challenge.json](Results/proof_edit_challenge.json) contains 16 Valid originals, 23 distinct flawed edits and 3 valid rewrites, with an expected label for each version.
   - [proof_edit_predictions.csv](Results/proof_edit_predictions.csv) records how each of the five models classified each of those 42 versions.

5. **Compare the results.** Plotted model predictions on the same 89 test proofs and compared each original proof with its edited versions. Notebook 07 also groups test accuracy by the number of mathematical symbols in the proof text.

   - [proof_scores.csv](Results/proof_scores.csv) gives each model’s Invalid score and predicted label for each of the 89 test proofs and 42 challenge versions.
   - Each model's `test_proof_scores.csv` lists the 89 test proofs for the model trained without review reasons. Each row gives the proof title, dataset label, predicted label, Invalid score and outcome. Open a score table for [TF-IDF](Results/TF-IDF/test_proof_scores.csv), [DistilBERT](Results/DistilBERT/test_proof_scores.csv), [ModernBERT-base](Results/ModernBERT-base/test_proof_scores.csv), [MathBERT](Results/MathBERT/test_proof_scores.csv) or [DeBERTa-v3-base](Results/DeBERTa-v3-base/test_proof_scores.csv).
   - [Results/visualizations/](Results/visualizations/) contains 13 plots in PNG and vector PDF. The data plots cover label counts, proof length, proof origin and frequent words. The model plots include [test confusion matrices](Results/visualizations/08_test_confusion_matrices.png), [ROC and precision–recall curves](Results/visualizations/09_test_roc_and_precision_recall.png), [test metrics](Results/visualizations/10_test_metric_comparison.png), a [TF-IDF learning curve](Results/visualizations/11_tfidf_learning_curve.png) and [score histograms](Results/visualizations/12_test_score_histograms.png).
   - In the [test score strip plot](Results/visualizations/01_test_score_strip_plot.png), color and shape show the dataset label. Horizontal position shows the model's Invalid score. A teal point to the right of 0.5 is a Valid proof the model flagged.

## Findings

- **Fine-tuning and review reasons.** All four BERT models improved test Macro F1 over their untrained classification heads when fine-tuned on theorem and proof text. Adding review reasons during training led all four to accept more Valid proofs and catch fewer Invalid ones. For example, MathBERT went from 51 to 71 of 75 Valid proofs accepted and from 7 to 0 of 14 Invalid proofs caught. [Review-reason comparison](Results/visualizations/02_review_reason_dumbbell_plot.png)
- **Symbol count.** All five models had lower accuracy in the highest symbol-count group (89–601 notation tokens per proof) than in the lowest (0–21). These counts include repeated variables, operators and other math tokens in the proof text. The high group contained 7 Invalid proofs out of 30, compared with 2 out of 31 in the low group. Proof length and label mix may also contribute to the accuracy gap. [Accuracy by symbol count](Results/visualizations/13_accuracy_by_proof_symbol_count.png)
- **Controlled proof edits.** The five models detected between 2 and 8 of the 16 main flawed edits. All five still accepted all nine symbol-edit variants drawn from three proofs. These edits show that a change that breaks a proof can leave the model's verdict unchanged. [Proof-edit score changes](Results/visualizations/03_proof_edit_score_change_heatmap.png)

Future work could test whether training on more Invalid proofs, especially ones with subtle mathematical errors, improves detection on new theorems.

## File guide

| Path | Contents |
|---|---|
| [src/proof_experiments.py](src/proof_experiments.py) | Shared split loading, overlap checks, evaluation, confusion matrices and direct prediction for the zero-update controls. |
| `Results/<BERT model>/without_training/` | Predictions, metrics and a confusion matrix from the pretrained encoder with a newly initialized classification head. |
| [pyproject.toml](pyproject.toml) and [uv.lock](uv.lock) | Python dependencies and their locked versions. |

## Reproduce locally

From the repository root, run `uv sync --locked` and select the resulting Python environment as the VS Code Jupyter kernel. The notebooks use `Notebooks/` as their working directory. The training notebooks were run with a local CUDA-capable NVIDIA GPU. The first training run downloads the specified pretrained checkpoints.

- **Inspect one model's test scores** by running the last cell of its notebook (01 to 05). It reads all 89 rows from the saved CSV.
- **Regenerate the visualizations** by running [notebook 07](Notebooks/07_Model_Visualizations.ipynb) in order. It uses the saved predictions and labeled splits. The learning-curve section refits TF-IDF on progressively larger groups of training files and scores each fit on the fixed validation split.
- **Regenerate the scores and edits evaluation** by running [notebook 06](Notebooks/06_Proof_Edit_Challenge.ipynb). It uses the selected configurations from notebooks 02–05 and the original data splits.
- **Repeat model selection** by running notebooks 01–05 before 06 and 07.
- **Recreate the cleaned corpus** by placing the raw JSON in `Data/` and running `python src/clean_proofwiki.py` from the repository root.

## References

1. Welleck, S., et al. (2021). NaturalProofs: Mathematical Theorem Proving in Natural Language. [NeurIPS Datasets and Benchmarks](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/hash/d9d4f495e875a2e075a1a4a6e1b9770f-Abstract-round1.html).
2. Geirhos, R., et al. (2020). Shortcut learning in deep neural networks. [Nature Machine Intelligence](https://doi.org/10.1038/s42256-020-00257-z).
3. Sanh, V., et al. (2019). DistilBERT, a distilled version of BERT: smaller, faster, cheaper and lighter. [arXiv:1910.01108](https://arxiv.org/abs/1910.01108).
4. Warner, B., et al. (2025). Smarter, Better, Faster, Longer: A Modern Bidirectional Encoder for Fast, Memory Efficient, and Long Context Finetuning and Inference. [ACL](https://aclanthology.org/2025.acl-long.127/).
5. Shen, J. T., et al. (2021). MathBERT: A Pre-trained Language Model for General NLP Tasks in Mathematics Education. [arXiv:2106.07340](https://arxiv.org/abs/2106.07340).
6. He, P., Gao, J., and Chen, W. (2023). DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing. [ICLR](https://openreview.net/forum?id=sE7-XhLxHA).

## Attribution and AI use

The corpus is the ProofWiki portion of NaturalProofs by Welleck et al. (2021), derived from ProofWiki contributors’ work. Consult the source dataset’s license and attribution information when redistributing the data. [NaturalProofs dataset and license](https://zenodo.org/records/4902289) · [Source repository](https://github.com/wellecks/naturalproofs)

The project idea and direction are mine. I used AI to help identify and understand the data source, draft documentation, annotate proof versions, generate synthetic errors and implement the experiments. I manually reviewed the 25 selected test proofs and retained 18.
