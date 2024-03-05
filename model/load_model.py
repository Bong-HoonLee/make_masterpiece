import torch
import os

from my_vgg import VGG

def load_model():
    model = VGG()
    try:
        model.load_state_dict(torch.load('/vgg_conv.pth'))
        print("Model loaded!!")
    except:
        print("Cannot load model, downloading new model!!")
        os.system('rm vgg_conv.pth')
        os.system('wget -c --no-check-certificate https://bethgelab.org/media/uploads/pytorch_models/vgg_conv.pth')
    
    return model