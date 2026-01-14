
import os
from PIL import Image
from torch.utils.data import Dataset
import torchvision.transforms as T

class FacesFolderDataset(Dataset):
    def __init__(self, root_dir, classes=None, transform=None):
        """
        root_dir: path to folder containing class subfolders
        classes: optional list of class names; if None, reads dir names sorted
        """
        self.root_dir = root_dir
        if classes is None:
            classes = sorted([d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))])
        self.classes = classes
        self.class2idx = {c:i for i,c in enumerate(self.classes)}
        self.samples = []
        for cls in self.classes:
            p = os.path.join(root_dir, cls)
            for fname in os.listdir(p):
                if fname.lower().endswith((".jpg",".jpeg",".png")):
                    self.samples.append((os.path.join(p, fname), self.class2idx[cls]))
        self.transform = transform or self.default_transform()

    def default_transform(self):
        return T.Compose([
            T.Resize((224,224)),
            T.RandomHorizontalFlip(),
            T.ToTensor(),
            T.Normalize(mean=[0.485,0.456,0.406], std=[0.229,0.224,0.225])
        ])

    def __len__(self): return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = Image.open(path).convert("RGB")
        img = self.transform(img)
        return img, label
