import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

# things we need for Tensorflow
import numpy as np
import tflearn
import tensorflow as tf
import random

# restore all of our data structures
import pickle
from graph import generate_possible_query
import sqlite3
from sqlite3 import Error

data = pickle.load( open( "training_data2", "rb" ) )

words = data['words']
classes = data['classes']
train_x = data['train_x']
train_y = data['train_y']

# import our chat-bot intents file
import json
with open('nrn.json') as json_data:
    intents = json.load(json_data)

# Build neural network
net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
# net = tflearn.lstm(net, 8, dropout=0.8, dynamic=True)
net = tflearn.fully_connected(net, len(train_y[0]), activation='softmax')
net = tflearn.regression(net)

# Define model and setup tensorboard
model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')

def clean_up_sentence(sentence):
    # tokenize the pattern
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=False):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words
    bag = [0]*len(words)
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)

    return(np.array(bag))

p = bow("is your shop open today?", words)
print(p)
print(classes)

# load our saved model
model.load('model2.tflearn')
# create a data structure to hold user context
# context = {}

ERROR_THRESHOLD = 0.20

def classify(sentence):
    # generate probabilities from the model
    results = model.predict([bow(sentence, words)])[0]
    # filter out predictions below a threshold
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)

    return_list = []
    for r in results:
        # return_cata.append((category[r[0]]))
        return_list.append((classes[r[0]], r[1]))
    # return tuple of intent and probability
    return return_list

welcome_msg = "Welcome to Trip TnT. I am  your assistant TnT bot at your service. Ask me your queries "
def generate_p_query(tags):

    possible_query=generate_tags(tags)
    return possible_query


    # for tag in tags:
    #     print("iam tag",tag)
    #     for i in intents['intents']:
    #
    #         if i['intent']==tag:
    #             print(i['intent'])
    #             print(i['query'][0])
    #             possible_query.append(i['query'][0])
    #         else:
    #             continue


def response(sentence, userID='123', show_details=False):
    
    results = classify(sentence)
    print(results[0][0])
    possible_query=generate_possible_query(results[0][0])
    # if we have a classification then find the matching intent tag
    if results:
        if results[0][1]>0.70:
            # loop as long as there are matches to process
            while results:
                for i in intents['intents']:
                    # find a tag matching the first result
                    if i['intent'] == results[0][0]:
                        for q in i['query']:
                            query = q
                            print(query)
                        reply = i['response']
                        intent=i['intent']
                        print(intent)
                        answer = reply[0]
                        intention=intent
                        print(" iam the possible query")
                        return answer,intention,possible_query
            results.pop(0)
        else:
            return ("Sorry I did not understand.","confuse",["what can you do for me?","About NRN"])


# def feedback(sentence, show_details=False):
#     print("Choose 'a' for correct and 'b' for incorrect")
#     feedback = input()
#     if feedback == 'a':
#         print("Thank you for your feedback")
#     else:
#         print("Thank you for your feedback, we will try to fix it as soon as possible")
#         with open('feedback.txt', 'a') as fb:
#             fb.write("\n" + sentence)