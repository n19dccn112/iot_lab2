import os
import cv2
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
import numpy as np
from format3d import format_3d_x
num_classes = 2
data_folder_train_val = "dataset_1000"
data_folder_test = "test"
epochs = 1
batch_size = 32
labels = {"benign":0, "malware":1}

X_train_val = []
y_train_val = []
X_test = []
y_test = []
# load_data:
for folder in os.listdir(data_folder_train_val):
    curr_path = os.path.join(data_folder_train_val, folder)
    for file in os.listdir(curr_path):
        curr_file = os.path.join(curr_path,file)
        image = cv2.imread(curr_file)
        X_train_val.append(image)
        y_train_val.append(labels[folder])

for folder in os.listdir(data_folder_test):
    curr_path = os.path.join(data_folder_test, folder)
    for file in os.listdir(curr_path):
        curr_file = os.path.join(curr_path,file)
        image = cv2.imread(curr_file)
        X_test.append(image)
        y_test.append(labels[folder])

# split_data
X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size = 0.25)

print("Training data size:", len(X_train))
print("Test data size:", len(X_test))
print("Validation data size:", len(X_val))


# build model
model = Sequential()
model.add(LSTM(32,input_shape=(65536,3), return_sequences=False))
model.add(Dropout(0.5))
model.add(Dense(10, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# compile model
model.summary()
model.compile(loss='categorical_crossentropy', optimizer = 'adam', metrics=['accuracy'])

y_train = np.asarray(y_train)
X_val = np.asarray(X_val)
y_val = np.asarray(y_val)
X_test = np.asarray(X_test)
y_test = np.asarray(y_test)
# fit model
print('X_train: ', X_train)
print('y_train: ', y_train)
model.fit(format_3d_x(X_train),
          y_train, epochs = epochs, batch_size = batch_size, validation_data = (format_3d_x(X_val), y_val))

# save model
model.save("model/weight.h5")
model_json = model.to_json()
with open("model/model.json", 'w') as json_file:
    json_file.write(model_json)

# evaluate model
loss, acc = model.evaluate(format_3d_x(X_test), y_test)
print("Loss: ",loss)
print("Acc: ",acc)




