import os

import numpy as np
from keras.models import model_from_json
from keras.utils import pad_sequences

from format3d import format_3d_x
import cv2
from sklearn import metrics

def figure_confusion_matrix(actual, predict):
    confusion_matrix = metrics.confusion_matrix(actual, predict)
    print(confusion_matrix)
    # Dương tính sai
    FP = confusion_matrix[1][0]
    # Âm tính sai
    FN = confusion_matrix[0][0]
    # Dương tính đúng
    TP = confusion_matrix[1][1]
    # Âm tính đúng
    TN = confusion_matrix[0][1]

    print("Dương tính giả:",FP,"âm tính giả:", FN,"Dương tính thật:", TP,"âm tính thật:", TN)

    # Độ chính xác = Accuracy
    ACC = (TP + TN) / (TP + FP + FN + TN)
    print("Độ chính xác: ", ACC)
    # Tỷ lệ dương tính - Sensitivity, hit rate, recall, or true positive rate
    TPR = TP / (TP + FN)
    print("Tỷ lệ dương tính: ", TPR)
    # Tỉ lệ dương tính đoán đúng - Precision or positive predictive value
    PPV = TP / (TP + FP)
    print("Tỉ lệ dương tính đoán đúng: ", PPV)
    # Tỷ lệ âm tính toán đúng - Negative predictive value
    NPV = TN / (TN + FN)
    print("Tỷ lệ âm tính toán đúng: ", NPV)
    # Tỷ lệ dương tính giả - False negative rate
    FNR = FN / (TP + FN)
    print("Tỷ lệ dương tính giả: ", FNR)
    # Tỷ lệ âm tính giả - Fall out or false positive rate
    FPR = FP / (FP + TN)
    print("Tỷ lệ âm tính giả: ", FPR)
    # Tỷ lệ dương tính sai - False discovery rate
    FDR = FP / (TP + FP)
    print("Tỷ lệ dương tính sai: ", FDR)
    # Tỷ lệ âm tính sai - False Omission rate
    FOR = FN / (FN + TN)
    print("Tỷ lệ âm tính sai: ", FOR)
    # f1 score Điểm trung bình hài hòa
    f1 = (2 * PPV * TPR) + (PPV + TPR)
    print("f1_score: ", f1)

y_actual = []
y_pre = []
data_folder_test = "test"
labels = {"benign":0, "malware":1}

json_file = open('model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

model = model_from_json(loaded_model_json)
model.load_weights('model/weight.h5')


for folder in os.listdir(data_folder_test):
    curr_path = os.path.join(data_folder_test, folder)
    for file in os.listdir(curr_path):
        curr_file = os.path.join(curr_path,file)
        image = cv2.imread(curr_file)

        image = cv2.resize(image, (256, 256), interpolation=cv2.INTER_LINEAR)
        image = np.expand_dims(image, axis=0)
        image = pad_sequences(image)


        y_pre.append(model.predict(format_3d_x(image)))
        y_actual.append(labels[folder])
        print('1: ', type(y_pre), ', ', y_pre)
        print('2: ', type(y_actual), ', ', y_actual)

figure_confusion_matrix(y_actual, y_pre)




