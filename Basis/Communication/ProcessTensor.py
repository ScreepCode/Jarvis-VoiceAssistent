import io
import os
import pathlib
import time
import wave

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from IPython import display


class ProcessTensor(object):
    def __init__(self):
        self.model = tf.keras.models.load_model('/home/pi/Jarvis/Basis/Communication/ModelSave')
        # self.model.summary()
        self.commands = np.array(["andere", "jarvis"])

    def decode_audio(self, audio_binary):
        audio, _ = tf.audio.decode_wav(audio_binary)
        return tf.squeeze(audio, axis=-1)

    def get_label(self, file_path):
        parts = tf.strings.split(file_path, os.path.sep)
        return parts[-2]

    def get_waveform_and_label(self, file_path):
        label = self.get_label(file_path)
        audio_binary = tf.io.read_file(file_path)
        waveform = self.decode_audio(audio_binary)
        return waveform, label

    def get_spectrogram(self, waveform):
        zero_padding = tf.zeros([300000] - tf.shape(waveform), dtype=tf.float32)
        waveform = tf.cast(waveform, tf.float32)
        equal_length = tf.concat([waveform, zero_padding], 0)
        spectrogram = tf.signal.stft(
            equal_length, frame_length=255, frame_step=128)

        spectrogram = tf.abs(spectrogram)
        return spectrogram

    def get_spectrogram_and_label_id(self, audio, label):
        spectrogram = self.get_spectrogram(audio)
        spectrogram = tf.expand_dims(spectrogram, -1)
        label_id = tf.argmax(label == self.commands)
        return spectrogram, label_id

    def preprocess_dataset(self, files):
        files_ds = tf.data.Dataset.from_tensor_slices(files)
        output_ds = files_ds.map(self.get_waveform_and_label, num_parallel_calls=tf.data.AUTOTUNE)
        output_ds = output_ds.map(
            self.get_spectrogram_and_label_id,  num_parallel_calls=tf.data.AUTOTUNE)
        return output_ds

    def predict(self):
        sample_ds = self.preprocess_dataset([str('/home/pi/Jarvis/Basis/Communication/ModelSave/tmp.wav')])

        for spectrogram, label in sample_ds.batch(1):
            prediction = self.model(spectrogram)
            # print("Prediction:")
            # print(prediction)
            # print("Prediction softmax:")
            # print(tf.nn.softmax(prediction[0]))
            # print("Prediction argmax:")
            # print(tf.argmax(prediction[0]))
            # print("Erkannt:")
            # print(self.commands[tf.argmax(prediction[0])])

            # plt.bar(self.commands, tf.nn.softmax(prediction[0]))
            # plt.show()

            result = self.commands[tf.argmax(prediction[0])]
            print(result)
            return result
