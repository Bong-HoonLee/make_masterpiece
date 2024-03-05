import time
import os

import torch
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
from torch import optim
import matplotlib.pyplot as plt
import torchvision
from torchvision import transforms
from PIL import Image
from collections import OrderedDict

from model.load_model import load_model
from utils.gram import GramMSELoss, GramMatrix


def main(cfg):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    img_size = cfg.get('img_size')
    lr = cfg.get('lr')
    max_iter = cfg.get('max_iter')
    show_iter = cfg.get('show_iter')

    style_layers = ['r11','r21','r31','r41','r51']
    content_layers = ['r42']

    style_weights = cfg.get('style_weights')
    content_weights = cfg.get('content_weights')

    # pre and post processing for images
    prep = transforms.Compose([transforms.Resize(img_size),
                            transforms.ToTensor(),
                            transforms.Lambda(lambda x: x[torch.LongTensor([2,1,0])]), #turn to BGR
                            transforms.Normalize(mean=[0.40760392, 0.45795686, 0.48501961], #subtract imagenet mean
                                                    std=[1,1,1]),
                            transforms.Lambda(lambda x: x.mul(255)),
                            ])
    postpa = transforms.Compose([transforms.Lambda(lambda x: x.mul(1./255)),
                            transforms.Normalize(mean=[-0.40760392, -0.45795686, -0.48501961], #add imagenet mean
                                                    std=[1,1,1]),
                            transforms.Lambda(lambda x: x[torch.LongTensor([2,1,0])]), #turn to RGB
                            ])
    postpb = transforms.Compose([transforms.ToPILImage()])

    # to clip results in the range [0,1]
    def postp(tensor): 
        t = postpa(tensor)
        t[t>1] = 1
        t[t<0] = 0
        img = postpb(t)
        return img


    # load model
    model = load_model()

    for param in model.parameters():
        param.requires_grad = False
    if torch.cuda.is_available():
        model.cuda()

    #load images, ordered as [style_image, content_image]
    # 겸재정선 - 금강내산전도
    path = cfg.get('path')
    style_image = path.get('style_image')
    # 성산일출봉
    content_image = path.get('content_image')

    img_names = [style_image, content_image]

    imgs = [Image.open(name) for name in img_names]

    imgs_torch = [prep(img) for img in imgs]
    imgs_torch = [img.unsqueeze(0).to(device) for img in imgs_torch]
    style_image, content_image = imgs_torch

    opt_img = content_image.data.clone()

    opt_img.requires_grad = True

    #define layers, loss functions, weights and compute optimization targets

    loss_layers = style_layers + content_layers
    style_loss = [GramMSELoss()] * len(style_layers)
    content_loss = [nn.MSELoss()] * len(content_layers)
    loss_fns = style_loss + content_loss
    loss_fns = [loss_fn.to(device) for loss_fn in loss_fns]

    #weights setting:
    weights = style_weights + content_weights

    #compute optimization targets
    style_targets = [GramMatrix()(A).detach() for A in model(style_image, style_layers)]
    content_targets = [A.detach() for A in model(content_image, content_layers)]
    targets = style_targets + content_targets


    # Define optimizer
    # Note that we optimize the opt_image, not model weight.
    optimizer = optim.Adam([opt_img], lr)

    #run style transfer
    for n_iter in range(max_iter):
        out = model(opt_img, loss_layers)
        optimizer.zero_grad()
        layer_losses = [weights[a] * loss_fns[a](A, targets[a]) for a, A in enumerate(out)]
        loss = sum(layer_losses)
        loss.backward()

        optimizer.step()

        # Print loss and Show output image
        if n_iter % show_iter == 0:
            print('Iteration: {:03d}, loss: {}'.format(n_iter+1, loss.item()))
            #display result
            out_img = postp(opt_img.data[0].cpu().squeeze())
            out_img.save(f'./style_transfer_{n_iter}.png')
            #gcf().set_size_inches(10,10)


def get_args_parser(add_help=True):
    import argparse
  
    parser = argparse.ArgumentParser(description="Pytorch models trainer", add_help=add_help)
    parser.add_argument("-c", "--config", default="./config.py", type=str, help="configuration file")

    return parser

if __name__ == "__main__":
    args = get_args_parser().parse_args()
    exec(open(args.config).read())
    main(config)