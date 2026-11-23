# Data log

## 1. Cleaned ProofWiki proofs

- [Original ProofWiki JSON](https://zenodo.org/records/4902289/files/naturalproofs_proofwiki.json?download=1)
- Removed empty or incomplete proofs, proofs that only point to references, and records with ambiguous notation or markup.
- Removed Wiki formatting while keeping mathematical notation and visible link text.
- Kept 6,155 of 19,234 theorem–proof pairs, covering 5,845 theorems. [Cleaned JSON](../Data/naturalproofs_proofwiki_clean.json)

## 2. Proof validity annotations

- AI reviewers assess each proof version against its theorem and give a reason for each judgment. Invalid proofs receive one primary error type. A null validity marks a record whose mathematical claim cannot be determined from the supplied text.
- Reviewed the first 900 cleaned theorem–proof pairs (797 theorem IDs). Of these, 745 were labeled Valid, 142 Invalid, and 13 had no identifiable claim. [Review batches](../Data/annotations/)
- Regrouped the reviews into 30 files of 30 for file-level splitting. Each theorem ID, identified restatement, and repeated proof text stays within one file. Use `clean_row_index` to recover the original source order.

## 3. Train, validation, and test splits

- Copied the review files into 24 train, 3 validation, and 3 test files (80/10/10). The splits contain 709, 89, and 89 labeled rows, respectively. Skip records with null validity for supervised training and evaluation. [Split folders](../Data/splits/)
- Reserved reviews 026–030 in the training split as sources for new invalid proofs. They contain 122 proofs labeled Valid.

## 4. Synthetic invalid training proofs

- Replaced the 122 valid proofs in training reviews 026–030 with flawed versions. Assigned 31 to Invalid inference, 31 to Unjustified assumption, 30 to Missing essential justification, and 30 to Misapplied theorem / unmet conditions.
- Each replacement has `is_synthetic: true`, a reason for its error label, and the original `clean_row_index`. The training split now contains 474 valid, 235 invalid, and 11 unclassified records.

## 5. TF-IDF baseline

- Trained logistic regression on character TF-IDF features from the theorem and proof. A second version also read `review_reason` during training, validation, and testing.
- Tried six combinations of character range and regularization strength for each version. Selected by validation Macro F1 and reported test Macro F1, Invalid precision and recall, and a confusion matrix. [Baseline notebook](../Notebooks/01_Proof_Validity_Baseline.ipynb)

## 6. Fine-tuned BERT models

- Fine-tuned DistilBERT, ModernBERT-base, MathBERT, and DeBERTa-v3-base on the same splits. Each model trained once per learning rate with the theorem and proof alone, and again with the review reason added during training only. Validation and test inputs contained only the theorem and proof.
- Tried two learning rates and scored each after one and two epochs. Selected each version by validation Macro F1 and saved its metrics, predictions, confusion matrices, and settings. [Model comparison](../Results/model_comparison.csv)

## 7. BERT evaluation without fine-tuning

- Loaded each of the four pretrained checkpoints with a fresh, randomly initialized validity classification head. Evaluated the same validation and test proofs with zero training updates. Each model's `without_training` folder contains its results. [Results by model](../Results/)

## 8. Manual review of test proofs

- I asked AI to extract the 25 test proofs for which the TF-IDF baseline and all four BERT models matched the existing validity label using only the theorem and proof. [25 extracted proofs](../Results/all_five_correct_test_without_review_reason.json)
- I manually reviewed all 25, excluded 7, and kept 18 (16 Valid and 2 Invalid). [18 retained proofs](../Results/manually_reviewed_test_proofs.json)

## 9. Evaluate edited proofs

- Starting from the 16 manually retained Valid proofs, AI prepared one flawed version per proof. For three proofs, AI also prepared a series of one, two, and three symbol changes and a valid rewrite. Two single-symbol edits also serve as the main flawed version. The set contains 16 originals and 26 distinct edits. [Proofs and edit explanations](../Results/proof_edit_challenge.json)
- Tested the five models using only theorem and proof text. All five still accepted every valid rewrite and all nine flawed symbol-edit versions. These results describe the selected proofs that all five originally accepted. [Evaluation notebook](../Notebooks/06_Proof_Edit_Challenge.ipynb) · [Predictions](../Results/proof_edit_predictions.csv)

## 10. Model visualizations and scores

- Exported the Invalid score from the five theorem-and-proof models for 89 test proofs and 42 challenge versions. Checked the decisions against the recorded predictions. [Score table](../Results/proof_scores.csv)
- Generated visualizations for the test score distributions, the effect of training with review reasons, and the score change after editing each proof. [Visualization notebook](../Notebooks/07_Model_Visualizations.ipynb) · [PNG and PDF figures](../Results/visualizations/)
