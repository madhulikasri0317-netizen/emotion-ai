# training/generate_dataset.py
"""
Generate a balanced synthetic emotion dataset.

This script creates:
 - training/data/train_full.csv  (50 examples per class -> 300 examples)
 - training/data/valid_full.csv  (10 examples per class -> 60 examples)

Labels: anger, fear, joy, neutral, sadness, surprise

Run from project root (emotion.ai) with your backend venv active:
    python training/generate_dataset.py

The script uses small templates + synonyms to build varied sentences.
"""
import csv
import random
from pathlib import Path

out_train = Path("training/data/train_full.csv")
out_valid = Path("training/data/valid_full.csv")

random.seed(42)

LABELS = {
    "joy": [
        "I am so happy right now",
        "This makes me smile",
        "I feel amazing and joyful",
        "I couldn't be more pleased",
        "What a wonderful moment",
        "I'm thrilled about this",
        "This fills me with happiness",
        "I love how this turned out",
        "I'm on cloud nine",
        "I feel delighted today"
    ],
    "sadness": [
        "I feel very sad and down",
        "This makes me want to cry",
        "I'm heartbroken about it",
        "I feel empty inside",
        "I'm gloomy and upset",
        "This situation makes me miserable",
        "I can't stop feeling low",
        "It hurts to think about it",
        "I'm feeling sorrowful today",
        "I miss the good times and feel sad"
    ],
    "anger": [
        "I am so angry right now",
        "This makes me furious",
        "I can't stand this, I'm mad",
        "I'm outraged by what happened",
        "This is infuriating and unacceptable",
        "I'm boiling with rage",
        "I want to shout at them",
        "This makes me want to scream",
        "I feel very annoyed and angry",
        "They crossed the line and I'm furious"
    ],
    "fear": [
        "I feel scared about the future",
        "This makes me anxious and afraid",
        "I'm nervous and worried",
        "My heart races when I think about it",
        "I'm terrified right now",
        "I feel a knot of fear in my stomach",
        "I'm uneasy and fearful",
        "I don't feel safe about this",
        "This situation makes me panic",
        "I'm filled with dread"
    ],
    "surprise": [
        "Wow, I did not expect that",
        "This is such a surprise",
        "I'm astonished by the result",
        "That's unexpected and shocking",
        "I can't believe it happened",
        "What an astonishing twist",
        "Oh my, that came out of nowhere",
        "I'm stunned and surprised",
        "That was completely unforeseen",
        "I'm taken aback by that news"
    ],
    "neutral": [
        "It's an ordinary day, nothing special",
        "I'm feeling okay, not much to say",
        "Just a normal routine today",
        "No strong feelings, I'm neutral",
        "This is average and uneventful",
        "Nothing interesting happened today",
        "I feel indifferent about it",
        "It's neither good nor bad",
        "I don't have an opinion either way",
        "Meh, it's just fine"
    ]
}

# helper tweaks to add variety
prefixes = ["", "Honestly, ", "Quite frankly, ", "Right now, ", "To be honest, "]
suffixes = ["", " today.", ".", " lately.", " these days.", " — can't explain it."]

def generate_examples(label, templates, n):
    examples = []
    for i in range(n):
        t = random.choice(templates)
        p = random.choice(prefixes)
        s = random.choice(suffixes)
        # small variation: add connector phrases, emojis rarely
        connector = random.choice(["", " because of this", " and I know why", " and it shows"])
        if random.random() < 0.05:
            emoji = random.choice([" 😊", " 😢", " 😠", " 😱", " 😮"])
        else:
            emoji = ""
        text = (p + t + connector + s).strip()
        # ensure punctuation ends the sentence
        if not text.endswith((".", "!", "?")):
            text = text + "."
        text = text.replace("  ", " ")
        text = text + emoji
        examples.append((text, label))
    return examples

def main():
    train_examples = []
    valid_examples = []

    # create 50 train, 10 valid per label
    for lbl, templates in LABELS.items():
        train_examples += generate_examples(lbl, templates, 50)
        valid_examples += generate_examples(lbl, templates, 10)

    # shuffle
    random.shuffle(train_examples)
    random.shuffle(valid_examples)

    out_train.parent.mkdir(parents=True, exist_ok=True)

    # write CSVs with quoting
    with out_train.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["text", "label"])
        for t, l in train_examples:
            writer.writerow([t, l])

    with out_valid.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["text", "label"])
        for t, l in valid_examples:
            writer.writerow([t, l])

    print(f"Generated {len(train_examples)} train examples -> {out_train}")
    print(f"Generated {len(valid_examples)} valid examples -> {out_valid}")

if __name__ == "__main__":
    main()
