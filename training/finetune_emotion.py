# training/finetune_emotion.py
"""
Small, safe fine-tuning script for text -> emotion classification.
Uses the local CSVs at training/data/train.csv and training/data/valid.csv.

Notes:
- This is written to work on CPU (but will automatically use GPU if torch sees one).
- Install dependencies in your backend venv before running:
    pip install transformers datasets evaluate accelerate torch sentencepiece
  (I'll give the exact install command next, one step at a time.)
- Run this script from the project root (where training/ is located) inside the Python venv:
    python training/finetune_emotion.py
"""

from datasets import load_dataset, ClassLabel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer
import numpy as np
import evaluate
import os

MODEL_NAME = "distilbert-base-uncased"   # small, fast base model for tests
TRAIN_CSV = "training/data/train_full.csv"
VALID_CSV = "training/data/valid_full.csv"
OUTPUT_DIR = "training/results-distilbert"

def main():
    assert os.path.exists(TRAIN_CSV), f"Train file not found at {TRAIN_CSV}"
    assert os.path.exists(VALID_CSV), f"Valid file not found at {VALID_CSV}"

    # 1) load CSVs
    raw = load_dataset("csv", data_files={"train": TRAIN_CSV, "validation": VALID_CSV})

    # 2) build label set from training data
    labels = sorted(list({l for l in raw["train"]["label"]}))
    label2id = {l: i for i, l in enumerate(labels)}
    id2label = {i: l for l, i in label2id.items()}
    num_labels = len(labels)
    print("Labels:", labels)

    # 3) tokenizer + model
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    def preprocess(batch):
        toks = tokenizer(batch["text"], truncation=True, padding="max_length", max_length=128)
        toks["labels"] = [label2id[l] for l in batch["label"]]
        return toks

    encoded = raw.map(preprocess, batched=True, remove_columns=raw["train"].column_names)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME, num_labels=num_labels, id2label=id2label, label2id=label2id
    )

    # 4) metrics
    accuracy = evaluate.load("accuracy")
    f1 = evaluate.load("f1")

    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=-1)
        acc = accuracy.compute(predictions=preds, references=labels)
        # for f1, compute macro average (works for multi-label)
        f1m = f1.compute(predictions=preds, references=labels, average="macro")
        return {"accuracy": acc["accuracy"], "f1_macro": f1m["f1"]}

    # 5) training arguments (compatible names for your transformers version)
    args = TrainingArguments(
        output_dir=OUTPUT_DIR,
        overwrite_output_dir=False,
        do_train=True,
        do_eval=True,
        eval_strategy="epoch",          # was evaluation_strategy
        save_strategy="epoch",          # was save_strategy
        per_device_train_batch_size=8,
        per_device_eval_batch_size=16,
        num_train_epochs=3,
        logging_steps=50,
        logging_strategy="steps",       # explicit logging strategy
        load_best_model_at_end=True,
        metric_for_best_model="accuracy",
        save_total_limit=2,
        fp16=False,
    )
    # 6) create the Trainer (must come AFTER TrainingArguments)
    from transformers import Trainer  # ensure Trainer is available

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=encoded["train"],
        eval_dataset=encoded["validation"],
        compute_metrics=compute_metrics,
    )

    # 7) run training and save
    trainer.train()
    trainer.save_model(OUTPUT_DIR)
    print(f"Training complete — model saved to {OUTPUT_DIR}")


    # 6) run training
    trainer.train()

    # 7) save final model
    trainer.save_model(OUTPUT_DIR)
    print(f"Training complete — model saved to {OUTPUT_DIR}")

if __name__ == "__main__":
    main()

