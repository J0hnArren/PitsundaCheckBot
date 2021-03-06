from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import model_from_json
import os
import pandas as pd
from numpy import argmax


class Dogs_vs_Cats:
    """ Class for working with an HDF5 file """

    def __init__(self, path, img_size):
        self.path = path
        self.img_size = img_size  # 224
        self.res_sub_aug_map = ImageDataGenerator(preprocessing_function=preprocess_input)

    @staticmethod
    def load_model(directory):
        """ Loading and compiling saved pre-trained model """
        json_file = open(directory + "amazing_cnn.json", "r")
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(directory + "amazing_cnn_w.h5")
        loaded_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        return loaded_model

    def predict(self, directory, filename):
        """ Making prediction with loaded pre-trained model """
        # img_names = [file for file in os.listdir(directory)]
        img_names = [filename]
        submission_image_df = pd.DataFrame({'filename': img_names})

        res_sub_data = self.res_sub_aug_map.flow_from_dataframe(
            submission_image_df, directory,
            x_col="filename",
            y_col=None,
            class_mode=None,
            target_size=(self.img_size, self.img_size),
            shuffle=False
        )

        res_pred_sub = self.load_model(self.path).predict(res_sub_data)
        submission_image_df['res_pred_sub'] = argmax(res_pred_sub, axis=-1)

        return submission_image_df['res_pred_sub'][len(submission_image_df['res_pred_sub']) - 1]

    @staticmethod
    def clear_data():
        """ Deleting already used photos """
        folder = 'data/'
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                    print("Old data has been removed")
            except Exception as e:
                print(e)
