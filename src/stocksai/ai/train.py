from stocksai.ta import calculate_indicators
from stocksai.ai.model import TransformerModel
from stocksai.ai.utils import get_batch
from torch.nn import functional as F
import plotly.express as px
import torch.optim as optim
from tqdm import tqdm
import torch.nn as nn
import numpy as np
import torch
import logging

device = 'cuda' if torch.cuda.is_available() else 'cpu'

hist = calculate_indicators(period='10y',
                            interval='1d')


# take an input sequence
data = hist['Close'].to_numpy()  
data = data * 10

data = np.expand_dims(data, axis=0)
data = torch.tensor(data)

training_data = data[:, :2000]
testing_data = data[:, 2000:]


# Example hyperparameters
batch_size = 10
vocab_size = len(np.unique(data.numpy().flatten())) * 10
d_model = 10
nhead = 1
num_encoder_layers = 1
dim_feedforward = 1
max_seq_length = 30

# Create and move the model to the appropriate device
model = TransformerModel(vocab_size, d_model,
                         nhead, num_encoder_layers,
                         dim_feedforward, max_seq_length).to(device)


# Define Loss Function and Optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.AdamW(model.parameters(), lr=3e-4)

# Number of epochs for training
num_epochs = 40

training_data = training_data.to(device)

for epoch in range(num_epochs):
    model.train()  # Set the model to training mode
    total_loss = 0

    # Iterate over the training data in batches
    for _ in tqdm(range(training_data.shape[1] // batch_size), desc="Batch"):
        # Generate a batch of data
        src, tgt = get_batch(training_data, batch_size, max_seq_length, device)

        optimizer.zero_grad()  # Clear the gradients from the previous iteration

        # Forward pass: Compute predicted output by passing src to the model
        output = model(src.long().to(device))
        B, T, C = output.shape
        output = output.view(B*T, C)  # Reshape for loss computation
        tgt = tgt.view(B*T).long()    # Reshape target to match output dimensions

        # Calculate loss
        loss = criterion(output, tgt)

        # Backward pass: Compute gradient of the loss with respect to model parameters
        loss.backward()

        # Perform a single optimization step (parameter update)
        optimizer.step()

        total_loss += loss.item()  # Accumulate the loss

    # Compute average loss for the epoch
    avg_loss = total_loss / (training_data.shape[1] // batch_size)
    print(f'Epoch: {epoch}, Average Loss: {avg_loss}')

# Save model
torch.save(model.state_dict(), 'model.pt')