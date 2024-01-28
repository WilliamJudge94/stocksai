import torch

def get_batch(data, batch_size, block_size, device, noise_stdev=5):
    """
    Generate a batch of data with added noise.

    Parameters:
    data (Tensor): The input data.
    batch_size (int): Number of sequences in a batch.
    block_size (int): Size of each data block.
    device (str): The device to use ('cuda' or 'cpu').
    noise_stdev (float): Standard deviation of the noise.

    Returns:
    Tuple[Tensor, Tensor]: Tensors x and y representing the input and target data.
    """
    # If data is 1-dimensional, add an extra dimension
    if len(data.shape) == 1:
        data = data.unsqueeze(0)


    ix = torch.randint(0, len(data), (batch_size,))
    iy = torch.randint(0, len(data[0]) - block_size, (batch_size,))
    x = torch.stack([data[j][i:i+block_size] for j, i in zip(ix, iy)])
    y = torch.stack([data[j][i+1:i+block_size+1] for j, i in zip(ix, iy)])

    # Add Gaussian noise
    # noise = torch.normal(mean=0, std=noise_stdev, size=y.size())
    # y = (y.float() + noise).round().long()

    return x.to(device), y.to(device)