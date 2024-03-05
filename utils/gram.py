import torch
import torch.nn as nn


# gram matrix and loss
class GramMatrix(nn.Module):
    def forward(self, x):

        b, c, h, w = x.size()
        F = x.view(c, h * w)
        out = torch.mm(F, F.t())

        return out

class GramMSELoss(nn.Module):
    def forward(self, x, y):

        out = nn.MSELoss()(GramMatrix()(x), y)

        return out