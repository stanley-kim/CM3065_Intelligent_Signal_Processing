# adapted from https://github.com/mozilla/DeepSpeech/blob/master/native_client/python/client.py
# which has a Mozzila Public License:
# https://github.com/mozilla/DeepSpeech/blob/master/LICENSE

from deepspeech import Model, version
import librosa as lr
import numpy as np
import os 

#Ex4_audio_files_transcriptions.pdf
english_transcriptions = {    
    'EN/' + 'checkin.wav': 'Where is the check-in desk',
#    'EN/' + 'checkin_child.wav': 'Where is the check-in desk',
    'EN/' + 'parents.wav': 'I have lost my parents',
#    'EN/' + 'parents_child.wav': 'I have lost my parents',
    'EN/' + 'suitcase.wav': 'Please, I have lost my suitcase',
#    'EN/' + 'suitcase_child.wav': 'Please, I have lost my suitcase',
    'EN/' + 'what_time.wav': 'What time is my plane',
#    'EN/' + 'what_time_child.wav': 'What time is my plane',
    'EN/' + 'where.wav': 'Where are the restaurants and shops',
#    'EN/' + 'where_child.wav': 'Where are the restaurants and shops'
}
italian_transcriptions = {
    'IT/' + 'checkin_it.wav': 'Dove e\' il bancone',
    'IT/' + 'parents_it.wav': 'Ho perso i miei genitori',
    'IT/' + 'suitcase_it.wav': 'Per favore, ho perso la mia valigia',
    'IT/' + 'what_time_it.wav': 'A che ora e’ il mio aereo',
    'IT/' + 'where_it.wav': 'Dove sono i ristoranti e i negozi'
}
spanish_transcriptions = {
    'ES/' + 'checkin_es.wav': '¿Dónde están los mostradores',
    'ES/' + 'parents_es.wav': 'He perdido a mis padres',
    'ES/' + 'suitcase_es.wav': 'Por favor, he perdido mi maleta',
    'ES/' + 'what_time_es.wav': '¿A qué hora es mi avión',
    'ES/' + 'where_es.wav': '¿Dónde están los restaurantes y las tiendas'
}
audio_file_transcriptions = [
    english_transcriptions,
    italian_transcriptions,
    spanish_transcriptions
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
    for file in language:
        print(file)
        audio_file = file
        audio = lr.load(file, sr=desired_sample_rate)[0]
        audio = (audio * 32767).astype(np.int16) # scale from -1 to 1 to +/-32767
        res = ds.stt(audio)
        #res = ds.sttWithMetadata(audio, 1).transcripts[0]
        print(res)                
