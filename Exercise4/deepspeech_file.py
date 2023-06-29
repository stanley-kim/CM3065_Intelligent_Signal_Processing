# adapted from https://github.com/mozilla/DeepSpeech/blob/master/native_client/python/client.py
# which has a Mozzila Public License:
# https://github.com/mozilla/DeepSpeech/blob/master/LICENSE

from deepspeech import Model, version
import librosa as lr
import numpy as np
import os 
from scipy.io import wavfile
from scipy import signal

EN_Original_Dir = 'EN'
IT_Original_Dir = 'IT'
ES_Original_Dir = 'ES'

EN_Modified_Dir = 'EN_M'
IT_Modified_Dir = 'IT_M'
ES_Modified_Dir = 'ES_M'


#Ex4_audio_files_transcriptions.pdf
english_transcriptions = {    
    'checkin.wav': 'Where is the check-in desk',
    'checkin_child.wav': 'Where is the check-in desk',
    'parents.wav': 'I have lost my parents',
    'parents_child.wav': 'I have lost my parents',
    'suitcase.wav': 'Please, I have lost my suitcase',
    'suitcase_child.wav': 'Please, I have lost my suitcase',
    'what_time.wav': 'What time is my plane',
    'what_time_child.wav': 'What time is my plane',
    'where.wav': 'Where are the restaurants and shops',
    'where_child.wav': 'Where are the restaurants and shops'
}
italian_transcriptions = {
    'checkin_it.wav': 'Dove e\' il bancone',
    'parents_it.wav': 'Ho perso i miei genitori',
    'suitcase_it.wav': 'Per favore, ho perso la mia valigia',
    'what_time_it.wav': 'A che ora e’ il mio aereo',
    'where_it.wav': 'Dove sono i ristoranti e i negozi'
}
spanish_transcriptions = {
    'checkin_es.wav': '¿Dónde están los mostradores',
    'parents_es.wav': 'He perdido a mis padres',
    'suitcase_es.wav': 'Por favor, he perdido mi maleta',
    'what_time_es.wav': '¿A qué hora es mi avión',
    'where_es.wav': '¿Dónde están los restaurantes y las tiendas'
}
audio_file_transcriptions = [
    [EN_Original_Dir, EN_Modified_Dir, english_transcriptions],
    [IT_Original_Dir, IT_Modified_Dir, italian_transcriptions],
    [ES_Original_Dir, ES_Modified_Dir, spanish_transcriptions]
]
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

sample_rate, data = wavfile.read("checkin.wav")
print(f'sample rate:{sample_rate}')
b = signal.firwin(101, cutoff=1000, fs=sample_rate, pass_zero='lowpass')
data1 = signal.lfilter(b, [1.0], data)
wav_lpf = r'lpfed.wav'
wavfile.write(wav_lpf, sample_rate, data1.astype(np.int16))

for language  in  audio_file_transcriptions:
    for file in language[2]:
        print(language[0] + '/' + file)
        sample_rate, data = wavfile.read(language[0] + '/' + file)
        b = signal.firwin(101, cutoff=5000, fs=sample_rate, pass_zero='lowpass')
        data1 = signal.lfilter(b, [1.0], data)
        wav_lpf = language[1] + '/' + file
        print(language[1] + '/' + file)
        wavfile.write(wav_lpf, sample_rate, data1.astype(np.int16))
scorer = "deepspeech-0.9.3-models.scorer"
model = "deepspeech-0.9.3-models.pbmm"
#audio_file = "../audio/commands.wav"
#audio_file = "./checkin.wav"
audio_file = "checkin.wav"

assert os.path.exists(scorer), scorer + "not found. Perhaps you need to download a scroere  from the deepspeech release page: https://github.com/mozilla/DeepSpeech/releases"
assert os.path.exists(model), model + "not found. Perhaps you need to download a  model from the deepspeech release page: https://github.com/mozilla/DeepSpeech/releases"
assert os.path.exists(audio_file), audio_file + "does not exist"

ds = Model(model)
ds.enableExternalScorer(scorer)

desired_sample_rate = ds.sampleRate()

audio = lr.load(audio_file, sr=desired_sample_rate)[0]
audio = (audio * 32767).astype(np.int16) # scale from -1 to 1 to +/-32767
res = ds.stt(audio)
#res = ds.sttWithMetadata(audio, 1).transcripts[0]
print(res)

for language, model, scorer in zip(audio_file_transcriptions, language_models, lanaguage_scorers):
    ds = Model(model)
    ds.enableExternalScorer(scorer)
    desired_sample_rate = ds.sampleRate()
    print(model)
    for file in language[2]:
        for dir in language[:2]:
            print(dir + '/' + file)
            #audio_file = file
            audio = lr.load(dir + '/' + file, sr=desired_sample_rate)[0]
            audio = (audio * 32767).astype(np.int16) # scale from -1 to 1 to +/-32767
            res = ds.stt(audio)
            #res = ds.sttWithMetadata(audio, 1).transcripts[0]
            print(res)                

        print(language[2][file])

