"""Example model training script.
"""
from typing import Optional

import torch
from torch import nn
from torch.utils.data import Dataset
import torch.nn.functional as F
import torchvision
import pytorch_lightning as pl


class ToyCNN(pl.LightningModule):
    """
    ToyCNN model implementing the standard PyTorch CNN example in the
    PyTorch Lightning interface.

    Note: This model is intended for pedagogical purposes, and as such the
    specific architecture is not of importance.
    """
    def __init__(self, train_dataset: Optional[Dataset]):
        super().__init__()

        self.train_dataset = train_dataset

        self.conv1 = nn.Conv2d(3, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 5 * 5, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

        self.criterion = torch.nn.CrossEntropyLoss()

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 5 * 5)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def train_dataloader(self):
        dl = torch.utils.data.DataLoader(
            self.train_dataset, batch_size=4, shuffle=True, num_workers=2
        )
        return dl

    def training_step(self, batch, batch_idx):
        inputs, labels = batch
        outputs = self(inputs)
        loss = self.criterion(outputs, labels)
        self.log("loss", loss)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

if __name__ == "__main__":

    # download CIFAR 10 data
    train_dataset = torchvision.datasets.CIFAR10(
        root="./data",
        train=True,
        download=True,
        transform=torchvision.transforms.ToTensor(),
    )

    # creating lightning module
    model = ToyCNN(train_dataset=train_dataset)

    # train model
    trainer = pl.Trainer(max_epochs=2)
    trainer.fit(model)
