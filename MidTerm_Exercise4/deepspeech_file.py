# adapted from https://github.com/mozilla/DeepSpeech/blob/master/native_client/python/client.py
# which has a Mozzila Public License:
# https://github.com/mozilla/DeepSpeech/blob/master/LICENSE

from deepspeech import Model, version
import librosa as lr
import numpy as np
import os 
from scipy.io import wavfile
from scipy import signal

import jiwer

EN_Original_Dir = 'EN'
IT_Original_Dir = 'IT'
ES_Original_Dir = 'ES'

EN_Modified_Dir = 'EN_M'
IT_Modified_Dir = 'IT_M'
ES_Modified_Dir = 'ES_M'

#Ex4_audio_files_transcriptions.pdf
english_transcriptions = {    
    'checkin.wav': 'where is the check in desk',
#    'checkin.wav': 'Where is the check-in desk',
    'checkin_child.wav': 'where is the check in desk',
#    'checkin_child.wav': 'Where is the check-in desk',
    'parents.wav': 'i have lost my parents',
#    'parents.wav': 'I have lost my parents',
    'parents_child.wav': 'i have lost my parents',
#    'parents_child.wav': 'I have lost my parents',
    'suitcase.wav': 'please I have lost my suitcase',
#    'suitcase.wav': 'Please, I have lost my suitcase',
    'suitcase_child.wav': 'please I have lost my suitcase',
#    'suitcase_child.wav': 'Please, I have lost my suitcase',
    'what_time.wav': 'what time is my plane',
#    'what_time.wav': 'What time is my plane',
    'what_time_child.wav': 'what time is my plane',
#    'what_time_child.wav': 'What time is my plane',
    'where.wav': 'where are the restaurants and shops',
#    'where.wav': 'Where are the restaurants and shops',
    'where_child.wav': 'where are the restaurants and shops',
#    'where_child.wav': 'Where are the restaurants and shops'
    'your_sentence1.wav': 'i love you',
    'your_sentence2.wav': 'you love me'
}
italian_transcriptions = {
    'checkin_it.wav': 'dove e il bancone',
#    'checkin_it.wav': 'Dove e\' il bancone',
    'parents_it.wav': 'ho perso i miei genitori',
#    'parents_it.wav': 'Ho perso i miei genitori',
    'suitcase_it.wav': 'per favore ho perso la mia valigia',
#    'suitcase_it.wav': 'Per favore, ho perso la mia valigia',
    'what_time_it.wav': 'a che ora e il mio aereo',
#    'what_time_it.wav': 'A che ora e’ il mio aereo',
    'where_it.wav': 'dove sono i ristoranti e i negozi'
#    'where_it.wav': 'Dove sono i ristoranti e i negozi'
}
spanish_transcriptions = {
    'checkin_es.wav': 'donde estan los mostradores',
#    'checkin_es.wav': '¿Dónde están los mostradores',
    'parents_es.wav': 'he perdido a mis padres',
#    'parents_es.wav': 'He perdido a mis padres',
    'suitcase_es.wav': 'por favor he perdido mi maleta',
#    'suitcase_es.wav': 'Por favor, he perdido mi maleta',
    'what_time_es.wav': 'a que hora es mi avion',
#    'what_time_es.wav': '¿A qué hora es mi avión',
    'where_es.wav': 'donde estan los restaurantes y las tiendas'
#    'where_es.wav': '¿Dónde están los restaurantes y las tiendas'
}
language_models = [
    "deepspeech-0.9.3-models.pbmm",
    "output_graph_it.pbmm",
    "output_graph_es.pbmm"
]
lanaguage_scorers = [
    "deepspeech-0.9.3-models.scorer",
    "kenlm_it.scorer",
    "kenlm_es.scorer"
]
audio_file_dirs = [
    [EN_Original_Dir, EN_Modified_Dir],
    [IT_Original_Dir, IT_Modified_Dir],
    [ES_Original_Dir, ES_Modified_Dir]
]
audio_file_transcriptions = [
    english_transcriptions,
    italian_transcriptions,
    spanish_transcriptions
]

padding_length = [
    0,
    1000,
    1000
]

def generate_Modified_Files():
    for [dir_source, dir_target], files, padding  in  zip(audio_file_dirs, audio_file_transcriptions, padding_length):
        if not os.path.exists(dir_target):
            os.mkdir(dir_target)
        for file in files:
            source_file = os.path.join(dir_source, file)
            sample_rate, data = wavfile.read(source_file)
            if padding != 0:
                data = np.concatenate((np.array([0] * padding), data))
            b = signal.firwin(101, cutoff=7500, fs=sample_rate, pass_zero='lowpass')
            data = signal.lfilter(b, [1.0], data)
            target_file = os.path.join(dir_target, file)
            wavfile.write(target_file, sample_rate, data.astype(np.int16))

def make_predictions():
    wers = {dir:[] for dirs in audio_file_dirs for dir in dirs}
    for model, scorer, dirs, transcriptions, in zip(
        language_models, 
        lanaguage_scorers,
        audio_file_dirs, 
        audio_file_transcriptions 
        ):

        assert os.path.exists(scorer), scorer + "not found. Perhaps you need to download a scroere  from the deepspeech release page: https://github.com/mozilla/DeepSpeech/releases"
        assert os.path.exists(model), model + "not found. Perhaps you need to download a  model from the deepspeech release page: https://github.com/mozilla/DeepSpeech/releases"

        ds = Model(model)
        ds.enableExternalScorer(scorer)
        desired_sample_rate = ds.sampleRate()
        print(model)

        for dir in dirs[1:]:
            for filename, transcript in transcriptions.items():
                audio_file = os.path.join(dir, filename) 
                assert os.path.exists(audio_file), audio_file + "does not exist"
                print(audio_file)
                audio = lr.load(audio_file, sr=desired_sample_rate)[0]
                audio = (audio * 32767).astype(np.int16) # scale from -1 to 1 to +/-32767
                res = ds.stt(audio)
                wers[dir].append(jiwer.wer(transcript, res))              
                print(f'pred: {res} / wer: {jiwer.wer(transcript, res)}')  
                print(f'true:{transcript}')
    return wers

def print_wers(wers):
    for dirs in audio_file_dirs:
        print('-' * 50)
        for dir in dirs[1:]:
            print(f'WER AVG of {dir} : {sum(wers[dir])/len(wers[dir])}')
            print(f'WER SUM / LEN of {dir}: {sum(wers[dir])} / {len(wers[dir])}')
            print(f'WER List of {dir}: {wers[dir]}')
        print('-' * 50)

if __name__ == "__main__":
    generate_Modified_Files()
    wers = make_predictions()
    print_wers(wers)
