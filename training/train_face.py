

from __future__ import annotations

from pathlib import Path
import time

import torch
from torch import nn, optim
from torch.utils.data import DataLoader
from torchvision import models

from faces_dataset import FacesFolderDataset

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / "data"
TRAIN_DIR = DATA_DIR / "train"
VAL_DIR = DATA_DIR / "test"
OUT_DIR = ROOT_DIR / "results-face"

BATCH_SIZE = 64
NUM_EPOCHS = 5
LEARNING_RATE = 1e-4
WEIGHT_DECAY = 1e-4


def main() -> None:
    # sanity prints
    print("Train dir:", TRAIN_DIR)
    print("Val dir  :", VAL_DIR)

    # ---------- datasets & loaders ----------

    train_ds = FacesFolderDataset(str(TRAIN_DIR))
    val_ds = FacesFolderDataset(str(VAL_DIR))

    # class names (assume FacesFolderDataset exposes .classes)
    if hasattr(train_ds, "classes"):
        class_names = list(train_ds.classes)
    else:
        # fallback: infer from subfolders
        class_names = sorted({p.name for p in TRAIN_DIR.iterdir() if p.is_dir()})

    print("Classes:", class_names)

    train_loader = DataLoader(
        train_ds,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=0,
        pin_memory=False,
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0,
        pin_memory=False,
    )



    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)


    weights = models.ResNet18_Weights.DEFAULT
    model = models.resnet18(weights=weights)

    num_features = model.fc.in_features
    num_classes = len(class_names)
    model.fc = nn.Linear(num_features, num_classes)

    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)


    best_val_acc = 0.0

    for epoch in range(1, NUM_EPOCHS + 1):
        print(f"\nEpoch {epoch}/{NUM_EPOCHS}")
        print("-" * 40)

        model.train()
        running_loss = 0.0
        running_correct = 0
        running_total = 0
        t0 = time.time()

        for step, (imgs, labels) in enumerate(train_loader, start=1):
            imgs = imgs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()
            outputs = model(imgs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item() * imgs.size(0)
            preds = outputs.argmax(dim=1)
            running_correct += (preds == labels).sum().item()
            running_total += labels.size(0)

            if step % 20 == 0:
                avg_loss = running_loss / max(running_total, 1)
                avg_acc = running_correct / max(running_total, 1)
                print(
                    f"  [step {step:4d}] "
                    f"train_loss={avg_loss:.4f}  train_acc={avg_acc*100:5.1f}%"
                )

        epoch_train_loss = running_loss / max(running_total, 1)
        epoch_train_acc = running_correct / max(running_total, 1)
        print(
            f"Train:  loss={epoch_train_loss:.4f}  "
            f"acc={epoch_train_acc*100:5.1f}%  "
            f"time={time.time()-t0:.1f}s"
        )

        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs = imgs.to(device)
                labels = labels.to(device)

                outputs = model(imgs)
                loss = criterion(outputs, labels)

                val_loss += loss.item() * imgs.size(0)
                preds = outputs.argmax(dim=1)
                val_correct += (preds == labels).sum().item()
                val_total += labels.size(0)

        epoch_val_loss = val_loss / max(val_total, 1)
        epoch_val_acc = val_correct / max(val_total, 1)
        print(
            f"Valid:  loss={epoch_val_loss:.4f}  "
            f"acc={epoch_val_acc*100:5.1f}%"
        )

        if epoch_val_acc > best_val_acc:
            best_val_acc = epoch_val_acc
            print(f"  New best val acc: {best_val_acc*100:5.1f}%")

   

    OUT_DIR.mkdir(exist_ok=True)
    model_path = OUT_DIR / "face_model.pt"
    torch.save(model.state_dict(), model_path)
    print("Saved model to:", model_path)

    class_file = OUT_DIR / "class_names.txt"
    with class_file.open("w", encoding="utf-8") as f:
        for name in class_names:
            f.write(str(name) + "\n")
    print("Saved class names to:", class_file)


if __name__ == "__main__":
    main()
