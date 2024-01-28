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


def append_to_tensor(original_tensor, values_to_append):
    # Convert values_to_append to a tensor if it is not already
    if not isinstance(values_to_append, torch.Tensor):
        values_to_append = torch.tensor(values_to_append,
                                        dtype=original_tensor.dtype)

    # Create a new tensor with the size of the original tensor plus the size of values_to_append
    new_tensor_size = original_tensor.nelement() + values_to_append.nelement()
    new_tensor = torch.empty(new_tensor_size, dtype=original_tensor.dtype)

    # Fill the new tensor with the original values and the new values
    new_tensor[:original_tensor.nelement()] = original_tensor
    new_tensor[original_tensor.nelement():] = values_to_append

    return new_tensor