# -*- coding: utf-8 -*-
"""BACKPROPAGATION-Oct11-7-26.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17pWjz3YBIBK92rJh78xX7krhPG3-EPKV

MINA RAHMANIAN


BACKPROPAGATION NETWORK

2019-10-10

===========================================================================================================

Import required libraries
"""

import numpy
import gzip
import pickle
import struct
import pylab
import random
from copy import copy
from sklearn.datasets import load_digits, fetch_openml
from sklearn.model_selection import train_test_split
from builtins import range
from csv import reader
from random import randrange
import numpy as np
import pandas as pd 
import csv
import random
import math
random.seed(113)
import warnings
from sklearn.metrics import classification_report
from sklearn import datasets
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

"""Network Class Definition"""

# this is the main directory for importing all files and also exporting results
mainDirPath = ""

class Network:
	
  # constructor
  # two parameters are required for constructor; one is the array of dimentions for 
  # all layers (input, hidden layers, output respectively); the other one is a flag indicating
  # if the user wants to use the already trained wigthing factors and biosed values or he wants to train the 
  # network from scratch.
	def __init__(self, layerDimensions, shouldUsedExistingTrainedValues = False):
		
		self._layerDimensions = layerDimensions
		self.nLayers = len(layerDimensions)
		self._weightingFactorList = []
		self._biasValueList = []
		
		if shouldUsedExistingTrainedValues == True:
			with open("C:/Assignment2/weights", "rb") as file_weights:
				mon_pickler = pickle.Unpickler(file_weights)
				self._weightingFactorList = mon_pickler.load()
			
			with open("C:/Assignment2/biases", "rb") as file_biases:
				mon_pickler = pickle.Unpickler(file_biases)
				self._biasValueList = mon_pickler.load()
		
		else:
			i = 1
			while i < self.nLayers:
				self._number_current = self._layerDimensions[i]
				self._number_previous = self._layerDimensions[(i-1)]
        
        # use random values intially
				wighting = numpy.random.normal(0, 1, (self._number_current, self._number_previous))
				biais = numpy.random.normal(0, 1, self._number_current) 
				self._weightingFactorList += [wighting]
				self._biasValueList += [biais]
				i += 1
						
	def _get_poids(self):
		return(self._weightingFactorList)
		
	def _get_biais(self):
		return(self._biasValueList)
		
	#feed forward method	
	def _feedforward(self, input):
		inp = numpy.ndarray.flatten((1/255)*input) 
		N = len(self._weightingFactorList)
		i = 0
		
		while i < N:
			inp = numpy.dot(self._weightingFactorList[i], inp) + self._biasValueList[i]
			inp = sigmoid_vec(inp)
			i +=1
			
		return inp
		
	
  # Using the testing data, this method display the acuracy of network prediction
  # according to its trained values.
	def _test(self, data):
		if len(data[0]) != len(data[1]):
			raise Exception("No of images and number of labels are not equal !")
		else:
			N = len(data[0])
			number_success = 0
			i = 0
			while i < N:
				result = self._feedforward(data[0][i])
				number = result.argmax()
				if number == data[1][i]:
					number_success += 1
					
				if i% 100 == 0:
					print("# Tested  {}".format(i))
					
				i += 1
					
			print("Accuracy : {} %".format(number_success/N))
			
			return number_success/N
	
  # method of back propagation during the training process
	def _backpropagation(self, input, true_output):
		inp = input
		N = len(self._weightingFactorList)
		i = 0
		list_wsum = []
		list_outputs = [input]
		
		while i < N:
			inp = numpy.dot(self._weightingFactorList[i], inp) + self._biasValueList[i]
			list_wsum += [inp]
			inp = sigmoid_vec(inp)
			list_outputs += [inp]
			i += 1
			
		list_vec_errors = [(inp - true_output)*sigmoid_derivative_vec(list_wsum[(N-1)])]
		i = 1
		while i < N:
			transp = numpy.transpose(self._weightingFactorList[(N-i)])
			error = numpy.dot(transp, list_vec_errors[0])*sigmoid_derivative_vec(list_wsum[(N-i-1)])
			list_vec_errors = [error] + list_vec_errors
			i += 1
		

		list_part_deriv = []
		list_part_bias = []
		l = 0
		while l < N:
			matrice = copy(self._weightingFactorList[l])
			bias = copy(self._biasValueList[l])
			for i in range(0, len(matrice[:, 1])):
				for j in range(0, len(matrice[1, :])):
					matrice[i, j] = list_outputs[l][j]*list_vec_errors[l][i]
				
				bias[i] = list_vec_errors[l][i]
				
			list_part_deriv += [matrice]
			list_part_bias += [bias]
			l += 1
			
		
		return (list_part_deriv, list_part_bias)
		
	# the minibactch data are getting updated in this method	
	def _update_mini_batch(self, list_images, list_labels, rate):
		N = len(list_images)
		Nb_layers = self.nLayers
		if N != len(list_labels):
			raise Exception("Number of images and labels are not equal!")
		else:
			list_weight = self._weightingFactorList.copy()
			list_bias = self._biasValueList.copy()
				
			i = 0
			while i < N:
				desired_output = numpy.zeros(self._layerDimensions[-1])
				desired_output[list_labels[i]] = 1
				weightings, bias = self._backpropagation(numpy.ndarray.flatten((1/255)*list_images[i]), desired_output)
				for l, elt in  enumerate(weightings):
					list_weight[l] += (-rate/N)*elt
					list_bias[l] += (-rate/N)*bias[l]
					
				i += 1
			
			self._weightingFactorList = list_weight.copy()
			self._biasValueList = list_bias.copy()
	
		
		
	def _train(self, training_set, number_epochs, size_mini_batch, rate):
		if len(training_set[0])% size_mini_batch != 0:
			raise Exception("Size of training set is not a multiple of mini-batch size !")
		else:
			training_images = training_set[0]
			training_labels = training_set[1]
		
			i = 0
			while i < number_epochs:
			  print("Epoch {} Started".format(i+1))
			  tempImg = copy(training_images)
			  tempLabel = copy(training_labels)
			  j = 0
			  m = len(training_set[0])/size_mini_batch
			  print(m)
			  while j < m:
			    mini_batch_images = []
			    mini_batch_labels = []
			    l = 0
			    while l < size_mini_batch:
			      random_index = random.randint(0, (len(tempImg)-1))
			      mini_batch_images += [tempImg[random_index]]
			      mini_batch_labels += [tempLabel[random_index]]
			      del tempImg[random_index]
			      del tempLabel[random_index]
			      l += 1
			      self._update_mini_batch(mini_batch_images, mini_batch_labels, rate)
			    j +=1
					
			  print("Epoch {} complete".format(i+1))
			  i += 1
				
			with open("C:/Assignment2/weights", "wb") as fichier_weights:
				my_pickler = pickle.Pickler(fichier_weights)
				my_pickler.dump(self._weightingFactorList)
				
			with open("C:/Assignment2/biases", "wb") as fichier_biases:
				my_pickler = pickle.Pickler(fichier_biases)
				my_pickler.dump(self._biasValueList)
				
	liste_weightings = property(_get_poids)
  
  
#sigmoid function calculation method 
def sigmoid(z):
	return(1.0/(1.0+numpy.exp(-z)))
	
sigmoid_vec = numpy.vectorize(sigmoid)
			
#sigmoid function derivative calculation method 
def sigmoid_derivative(z):
	return sigmoid(z)*(1-sigmoid(z))
	
sigmoid_derivative_vec = numpy.vectorize(sigmoid_derivative)

from tensorflow.examples.tutorials.mnist import input_data
input_data.read_data_sets('C:/Assignment2')

# method for loading training data

def load_training_data():
	train = gzip.open("C:/Assignment2/train-images-idx3-ubyte.gz", "rb")
	labels = gzip.open("C:/Assignment2/train-labels-idx1-ubyte.gz", "rb")
	
	train.read(4)
	labels.read(4)
		
	number_images = train.read(4)
	number_images = struct.unpack(">I", number_images)[0]
		
	rows = train.read(4)
	rows = struct.unpack(">I", rows)[0]
		
	cols = train.read(4)
	cols = struct.unpack(">I", cols)[0]
		
	number_labels = labels.read(4)
	number_labels = struct.unpack(">I", number_labels)[0]
	
	image_list = []
	label_list = []
	if number_images != number_labels:
		raise Exception("The number of labels doesn't match with the number of images")
	else:
		for l in range(number_labels):
			if l % 1000 == 0:
				print("# loaded data :{}".format(l))
				
			mat = numpy.zeros((rows, cols), dtype = numpy.uint8)
			for i in range(rows):
				for j in range(cols):
					pixel = train.read(1)
					pixel = struct.unpack(">B", pixel)[0]
					mat[i][j] = pixel
					
			
			image_list += [mat]
			lab = labels.read(1)
			lab = struct.unpack(">B", lab)[0]
			label_list += [lab]
		
	
	train.close()
	labels.close()
		
	return ([image_list, label_list])

# method for loading tes data

def load_test_data():
	test = gzip.open("C:/Assignment2/t10k-images-idx3-ubyte.gz", "rb")
	labels = gzip.open("C:/Assignment2/t10k-labels-idx1-ubyte.gz", "rb")
	
	test.read(4)
	labels.read(4)
		
	number_images = test.read(4)
	number_images = struct.unpack(">I", number_images)[0]
		
	rows = test.read(4)
	rows = struct.unpack(">I", rows)[0]
		
	cols = test.read(4)
	cols = struct.unpack(">I", cols)[0]
		
	number_labels = labels.read(4)
	number_labels = struct.unpack(">I", number_labels)[0]
	
	image_list = []
	label_list = []
	if number_images != number_labels:
		raise Exception("The number of labels are not equal to the number of images")
	else:
		for l in range(number_labels):
			if l % 1000 == 0:
				print("# loaded data :{}".format(l))
				
			mat = numpy.zeros((rows, cols), dtype = numpy.uint8)
			for i in range(rows):
				for j in range(cols):
					pixel = test.read(1)
					pixel = struct.unpack(">B", pixel)[0]
					mat[i][j] = pixel
					
			#view(mat)
			image_list += [mat]
			lab = labels.read(1)
			lab = struct.unpack(">B", lab)[0]
			label_list += [lab]
		
	
	test.close()
	labels.close()
		
	return ([image_list, label_list])	

# auxillary method to display the image if required	
def view(image, label=""):
	#print("Number : {}".format(label))
	pylab.imshow(image, cmap = pylab.cm.gray)
	pylab.show()

# 1. load the training data if you want to train the model from scratch.
trainingData = load_training_data()

# 2. construct a network 
inputLayerSize = 28 * 28
hiddenLayerSize = 30
outputLayerSize = 10

shouldUsedExistingTrainedValues = False
 
net = Network([inputLayerSize, hiddenLayerSize, outputLayerSize], shouldUsedExistingTrainedValues)

# 3. (optional)
# this section will override the previously trained values
# NOTE: do not run if you want to reuse the trained values

nEpoch = 10
nBatch = 100
learningRate = 0.4

net._train(trainingData, nEpoch, nBatch, learningRate)

# 4. load the test data
testData = load_test_data()

# 5. test the network predition acuracy
result = net._test(testData)