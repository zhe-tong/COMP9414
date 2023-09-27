import numpy as np
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import precision_recall_fscore_support, accuracy_score,classification_report
from sklearn import tree
import sys
import re

predict_z = []
def predict_and_test(model, x_test_bag_of_words):
    num_dec_point = 3
    predicted_z = model.predict(x_test_bag_of_words)
    #print(z_test, predicted_z)
    #print(model.predict_proba(x_test_bag_of_words))
    a_mic = accuracy_score(z_test, predicted_z)
    p_mic, r_mic, f1_mic, _ = precision_recall_fscore_support(z_test,
                        predicted_z,
                        average='micro',
                        warn_for=())
    p_mac, r_mac, f1_mac, _ = precision_recall_fscore_support(z_test,
                        predicted_z,
                        average='macro',
                        warn_for=())
    for i in predicted_z:
        predict_z.append(i)
    #print('micro acc,prec,rec,f1: ',round(a_mic,num_dec_point), round(p_mic,num_dec_point), round(r_mic,num_dec_point), round(f1_mic,num_dec_point),sep="\t")
    #print('macro prec,rec,f1: ',round(p_mac,num_dec_point), round(r_mac,num_dec_point), round(f1_mac,num_dec_point),sep="\t")

# Create text
temp_train = []
for i in open(sys.argv[1], "r"):
    line = i.strip('\n')
    temp_train.append(line)
text_data_train = np.array(temp_train)

temp_test = []
for i in open(sys.argv[2], "r"):
    line = i.strip('\n')
    temp_test.append(line)
text_data_test = np.array(temp_test)

# split into train and test
x_train = []
x_test = []
y_train_temp = []
y_test_temp = []
z_train = []
z_test = []
for i in text_data_train:
    j = i.split('\t')
    x_train.append(j[0])
    y_train_temp.append(j[1])
    z_train.append(j[2])
for i in text_data_test:
    j = i.split('\t')
    x_test.append(j[0])
    y_test_temp.append(j[1])
    z_test.append(j[2])


y_train = []
y_test = []
for i in y_train_temp:
    temp = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " ", i)
    temp = "".join(temp)
    temp = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]|[#@%$]|[ ]+', temp, re.S)
    temp = "".join(temp)
    temp = re.findall(r'\S{2,}', temp, re.S)
    temp = " ".join(temp)
    y_train.append(temp)
for i in y_test_temp:
    temp = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', " ", i)
    temp = "".join(temp)
    temp = re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]|[#@%$]|[ ]+', temp, re.S)
    temp = "".join(temp)
    temp = re.findall(r'\S{2,}', temp, re.S)
    temp = " ".join(temp)
    y_test.append(temp)

# create count vectorizer and fit it with training data
count = CountVectorizer(lowercase=False)
y_train_bag_of_words = count.fit_transform(y_train)

# transform the test data into bag of words creaed with fit_transform
y_test_bag_of_words = count.transform(y_test)


#print("----bnb")
clf = BernoulliNB()
model = clf.fit(y_train_bag_of_words, z_train)
predict_and_test(model, y_test_bag_of_words)

for i in range(len(predict_z)):
    print(x_test[i], predict_z[i])
