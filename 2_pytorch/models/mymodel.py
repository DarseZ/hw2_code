import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F


class MyModel(nn.Module):
    def __init__(self, im_size, hidden_dim, kernel_size, n_classes):
        '''
        Extra credit model

        Arguments:
            im_size (tuple): A tuple of ints with (channels, height, width)
            hidden_dim (int): Number of hidden activations to use
            kernel_size (int): Width and height of (square) convolution filters
            n_classes (int): Number of classes to score
        '''
        super(MyModel, self).__init__()
        #############################################################################
        # TODO: Initialize anything you need for the forward pass
        #############################################################################
        C, H, W = im_size
        self.filter_size = kernel_size
        self.filter_num = hidden_dim
        self.conv_param = {'stride': 1, 'pad': (self.filter_size - 1) // 2}
        self.pool_size = 2
        
        self.conv1_1 = nn.Conv2d(C, self.filter_num, kernel_size=self.filter_size, stride=self.conv_param['stride'], padding=self.conv_param['pad'])
        self.conv1_2 = nn.Conv2d(self.filter_num, self.filter_num, kernel_size=self.filter_size, stride=self.conv_param['stride'], padding=self.conv_param['pad'])
         
        self.conv2_1 = nn.Conv2d(self.filter_num, 2*self.filter_num, kernel_size=self.filter_size, stride=self.conv_param['stride'], padding=self.conv_param['pad'])
        self.conv2_2 = nn.Conv2d(2*self.filter_num, 2*self.filter_num, kernel_size=self.filter_size, stride=self.conv_param['stride'], padding=self.conv_param['pad'])
        
        self.activation = nn.LeakyReLU(inplace=True)
        self.pool = nn.MaxPool2d(kernel_size=self.pool_size)
        self.affine = nn.Linear(2*self.filter_num * (H // (self.pool_size**2)) * (W // (self.pool_size**2)), n_classes)
        self.softmax = nn.Softmax()
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################

    def forward(self, images):
        '''
        Take a batch of images and run them through the model to
        produce a score for each class.

        Arguments:
            images (Variable): A tensor of size (N, C, H, W) where
                N is the batch size
                C is the number of channels
                H is the image height
                W is the image width

        Returns:
            A torch Variable of size (N, n_classes) specifying the score
            for each example and category.
        '''
        scores = None
        #############################################################################
        # TODO: Implement the forward pass.
        #############################################################################
        N = images.shape[0]
        # Conv - ReLU - Conv - ReLU - Pool 1
        out = self.conv1_1(images) # self.filter_num*32*32
        out = self.activation(out) # self.filter_num*32*32
        out = self.conv1_2(out) # self.filter_num*32*32
        out = self.activation(out) # self.filter_num*32*32
        out = self.pool(out) # self.filter_num*16*16
        # Conv - ReLU - Conv - ReLU - Pool 2
        out = self.conv2_1(out) # 2*self.filter_num*16*16
        out = self.activation(out) # 2*self.filter_num*16*16
        out = self.conv2_2(out) # 2*self.filter_num*16*16
        out = self.activation(out) # 2*self.filter_num*16*16
        out = self.pool(out) # 2*self.filter_num*8*8
        
        # affine 1
        out = self.affine(out.view(N, -1)) # 2*self.filter_num*8*8
        # softmax 1
        out = self.softmax(out) # 2*self.filter_num*8*8
        scores = out
        #############################################################################
        #                             END OF YOUR CODE                              #
        #############################################################################
        return scores

