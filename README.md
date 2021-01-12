# Backpropagation Network ANN (Using MNIST Data)
<br />

Useful bits of knowledge before start:
+ First of all, please read The Artificial Neural Networks book in second edition from this link ["Elements of Artificial Neural Networks" ](https://www.academia.edu/23714658/Elements_of_Artificial_Neural_Networks). 
+ There are absolutely free resources for Deep Learning (online book) in [Here](http://neuralnetworksanddeeplearning.com/chap1.html).
+  Also if you want to work Convolutional network you can read this link [Convolutional network](https://ujjwalkarn.me/2016/08/11/intuitive-explanation-convnets/) too. 
<br /><br /><br />


## Data MNIST handwritten digit Description

+ You will use the handwritten character database for this practice by Lecunet al available at the following [here](https://github.com/Mina-Rahmanian/Backpropagation-Network-ANN/blob/main/MNIST%20handwritten%20digit%20database%2C%20Yann%20LeCun%2C%20Corinna%20Cortes%20an.pdf).
+ Four files are available as bellow written:

| Files                     | Data Size   | Task                               | 
| --------------------------|-------|:----------------------------------:|
|[train-images-idx3-ubyte.gz](https://github.com/Mina-Rahmanian/Backpropagation-Network-ANN/blob/main/train-images-idx3-ubyte.gz) | 9912422 bytes  | training set images                   |
|[train-labels-idx1-ubyte.gz](https://github.com/Mina-Rahmanian/Backpropagation-Network-ANN/blob/main/train-labels-idx1-ubyte.gz)               | 28881 bytes  | training set labels         | 
|[t10k-images-idx3-ubyte.gz](https://github.com/Mina-Rahmanian/Backpropagation-Network-ANN/blob/main/t10k-images-idx3-ubyte.gz)               | 1648877 bytes  | test set images |
|[t10k-labels-idx1-ubyte.gz](https://github.com/Mina-Rahmanian/Backpropagation-Network-ANN/blob/main/t10k-labels-idx1-ubyte.gz)  |   4542 bytes   |   test set labels                             |<br /><br />


+ MNIST dataset can also be loaded directly in Python using packages such as Kerasand scikit-learn.<br />

-----------------------------------------------------------------------------------------------------

# Introduction

+ We implemented a Backpropagation training algorithm in a multilayer perception to learn to classify handwritten characters using the MNIST training dataset and the corresponding label dataset.
+ The input should be the training data and the output should be the corresponding digit class. In other words, we must decide the following design criteria: <br />
  - Initial weights and learning rate
  - Training iterations and terminating criteria
  - Number of layers and nodes
  - Momentum
+ We implemented the Backpropagation algorithm to solve this problem. Use sigmoidal output function at every layer and node. ``We did not use any GUI based tool or built-in libraries to create/train/test the ANN``.
+ 


# Solution


Here I used ``50 hidden nodes``, ``784 input nodes`` and ``10 output nodes``. And also, I consider ``Learning rate 0.1``, ``the number of epoch 10``.


<p align="center">
<img width="700" height="350" alt="gg" src="https://user-images.githubusercontent.com/71558720/104351744-c8e1b580-54d3-11eb-9cc1-dcd2f7e79706.PNG">
<p align="center"><br /><br />

Also, I have calculated the results using the ready functions from Keras [Keras_Backpropagation .ipynb](https://github.com/Mina-Rahmanian/Backpropagation-Network-ANN/blob/main/Keras_Backpropagation%20.ipynb), and the corresponding result is attached in a [Keras_ready function.txt](https://github.com/Mina-Rahmanian/Backpropagation-Network-ANN/blob/main/keras-%20ready%20function.txt).<br />


**Problem**: For the analytic code, first, I tried my first code [Backpropagation_Oct11_2019.ipynb](https://github.com/Mina-Rahmanian/Backpropagation-Network-ANN/blob/main/Backpropagation_Oct11_2019.ipynb) or [Backpropagation_oct11_2019.py](https://github.com/Mina-Rahmanian/Backpropagation-Network-ANN/blob/main/Backpropagation_oct11_2019.py). which gave me a good result of ``%97.5 accuracy`` with ``10 epoch``, ``100 batches`` and with ``learning rate 0.4`` and ``30 hidden nodes``. It took 3 hours, but unfortunately for the second time I was not able to rerun it, So I change my programme completely to [MNIST_Backpropagation.ipynb](https://github.com/Mina-Rahmanian/Backpropagation-Network-ANN/blob/main/MNIST_Backpropagation.ipynb) or  [mnist_backpropagation.py](https://github.com/Mina-Rahmanian/Backpropagation-Network-ANN/blob/main/mnist_backpropagation.py) files. <br /><br />




### Critical discussion:


The overall result is acceptable with the range of 97%, before adding the momentum the result was weaker but thenafter and by choosing alpha=0.5 the obtained results were more convincing. The reason of picking 0.5 value is that the 0 value neglects its effect and the value of 1 reduces the effects of the error value of the previous step on the estimation of the correct weight update for the current step.

The main factors in determining the quality of the results and timing are the number of hidden nodes, learning rate and the momentum value. The higher hidden nodes and lower learning rate increases the accuracy but also the running time.<br /><br />




## ** Mina R **






