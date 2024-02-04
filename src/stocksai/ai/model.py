# import torch
# import torch.nn as nn
# import torch.optim as optim
# #from mamba_ssm import Mamba

# class FeedForward(nn.Module):
#     """
#     A feedforward neural network module.

#     Attributes:
#     ffn (nn.Sequential): A sequential container of layers including
#     Linear, ReLU, Linear, and Dropout.

#     Parameters:
#     n_embed (int): The size of the input and output embeddings.
#     """

#     def __init__(self, n_embed, dropout=0.1) -> None:
#         super().__init__()
#         self.ffn = nn.Sequential(
#             nn.Linear(n_embed, 4 * n_embed),
#             nn.ReLU(),
#             nn.Linear(4 * n_embed, n_embed),
#             nn.Dropout(dropout),
#         )

#     def forward(self, x):
#         """
#         Defines the computation performed at every call.

#         Parameters:
#         x (Tensor): The input tensor.

#         Returns:
#         Tensor: The output tensor after passing through the
#                 feedforward network.
#         """
#         return self.ffn(x)


# class MambaEncodingLayer(nn.Module):
#     """
#     A custom encoding layer using Mamba for self-attention.

#     Attributes:
#     head_size (int): The size of each attention head.
#     sa_head (Mamba): Mamba self-attention module.
#     ffn (FeedForward): Feedforward neural network module.
#     ln1 (nn.LayerNorm): Layer normalization before self-attention.
#     ln2 (nn.LayerNorm): Layer normalization before feedforward network.

#     Parameters:
#     n_embed (int): The size of the input and output embeddings.
#     n_heads (int): The number of attention heads.
#     """

#     def __init__(self, n_embed, n_heads, device) -> None:
#         super().__init__()
#         self.head_size = n_embed // n_heads
#         self.sa_head = Mamba(
#             d_model=n_embed,  # Model dimension d_model
#             d_state=16,       # SSM state expansion factor
#             d_conv=4,         # Local convolution width
#             expand=2,         # Block expansion factor
#         ).to(device)

#         self.ffn = FeedForward(n_embed).to(device)
#         self.ln1 = nn.LayerNorm(n_embed).to(device)
#         self.ln2 = nn.LayerNorm(n_embed).to(device)

#     def forward(self, x):
#         """
#         Defines the computation performed at every call.

#         Parameters:
#         x (Tensor): The input tensor.

#         Returns:
#         Tensor: The output tensor after processing through the encoding layer.
#         """
#         x = self.ln1(x)
#         x = x + self.sa_head(x)
#         x = self.ln2(x)
#         x = x + self.ffn(x)

#         return x


# class TransformerModel(nn.Module):
#     """
#     Transformer Model for sequence prediction.

#     Attributes:
#     model_type (str): Model type identifier.
#     token_embedding_table (nn.Embedding): Embedding for token encoding.
#     position_embedding_table (nn.Embedding): Embedding for position encoding.
#     encoder_layer (nn.TransformerEncoderLayer): Transformer encoder layer.
#     transformer_encoder (nn.TransformerEncoder): Transformer encoder.
#     decoder (nn.Linear): Linear layer for decoding.
#     """

#     def __init__(self,
#                  vocab_size,
#                  d_model,
#                  nhead,
#                  num_encoder_layers,
#                  dim_feedforward,
#                  max_seq_length,
#                  device,
#                  og_or_mamba="og"):

#         super(TransformerModel, self).__init__()
#         self.model_type = 'Transformer'
#         self.device = device
#         self.token_embedding_table = nn.Embedding(vocab_size, d_model)

#         self.position_embedding_table = nn.Embedding(max_seq_length, d_model)


#         if og_or_mamba == "og":
#           self.encoder_layer = nn.TransformerEncoderLayer(d_model=d_model,
#                                                           nhead=nhead,
#                                                           dim_feedforward=dim_feedforward)

#           self.transformer_encoder = nn.TransformerEncoder(self.encoder_layer,
#                                                           num_layers=num_encoder_layers)

#         elif og_or_mamba == "mamba":
#           self.encoder_layer = MambaEncodingLayer(d_model, nhead, device=device)
#           self.transformer_encoder = nn.Sequential(*[self.encoder_layer for _ in range(num_encoder_layers)])

#         self.decoder = nn.Linear(d_model, vocab_size)

#     def forward(self, src):
#         """
#         Forward pass of the model.

#         Parameters:
#         src (Tensor): Input tensor.

#         Returns:
#         Tensor: Output tensor from the model.
#         """
#         B, T = src.shape
#         tok_emb = self.token_embedding_table(src)
#         pos_emb = self.position_embedding_table(torch.arange(T,
#                                                              device=self.device))
#         x = tok_emb + pos_emb
#         x = self.transformer_encoder(x)
#         x = self.decoder(x)

#         return x
