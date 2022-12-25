import cv2
import numpy as np
from tkinter import *
from PIL import Image, ImageTk
from keras_preprocessing.sequence import pad_sequences
from keras.models import model_from_json
from tkinter import filedialog
from format3d import format_3d_x
labels = ["benign","malware"]

json_file = open('model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()

model = model_from_json(loaded_model_json)
model.load_weights('model/weight.h5')

if __name__ == '__main__':

    root = Tk()
    root.geometry("350x350+300+150")
    root.title("LAB2")
    root.resizable(width=True, height=True)
 
    def openfn():
        filename = filedialog.askopenfilename(title='open')
        return filename

    def open_img():
        x = openfn()
        image = cv2.imread(x)
        image = cv2.resize(image, (256, 256), interpolation= cv2.INTER_LINEAR)
        image = np.expand_dims(image, axis =0)
        image_pad = pad_sequences(image)
        pred = model.predict(format_3d_x(image_pad))
        print('1111111111111: ', np.argmax(pred))
        print("%s sentiment; %f%% confidence" % (labels[np.argmax(pred)], pred[0][np.argmax(pred)] * 100))  

        lbl1 = Label(root, text = labels[np.argmax(pred)] + " sentiment - " + str(int(pred[0][np.argmax(pred)] * 1000000)/10000)
                                        + " confidence              ", font = ("Palatino Linotype",11,"bold"))
        lbl1.place(x = 40, y = 310)

        img = Image.open(x)
        img = img.resize((250, 250))
        img = ImageTk.PhotoImage(img)
        panel = Label(root, image=img)
        panel.image = img
        panel.place(x = 50, y = 40)

    btn = Button(root, text='Open Image', command=open_img, font = ("Palatino Linotype",11,"bold") ).pack()
    root.mainloop()

    