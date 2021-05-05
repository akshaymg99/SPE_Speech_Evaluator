# !/usr/bin/venv python

import speech_recognition as sr
from keras.preprocessing.sequence import pad_sequences
from pytorch_pretrained_bert import BertTokenizer
from pytorch_pretrained_bert import BertForSequenceClassification
from pydub import AudioSegment
from pydub.silence import split_on_silence
import numpy as np
import pandas as pd
import gc
import os
import torch
import time

from spe1.settings import DEPENDENCIES_DICT_DIR, Q1_CSV, BERT_MODEL


def analyze():
    seconds = 60
    minute = 1
    t_end = time.time() + (seconds * minute)  ## Takes voice input for this time-frame
    r = sr.Recognizer()
    sentences = []
    inp_corpus = ""
    print("Starting voice recording")

    while time.time() < t_end:
        try:
            with sr.Microphone() as source2:
                r.adjust_for_ambient_noise(source2, duration=1)
                audio2 = r.listen(source2)
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                inp_corpus += MyText
                sentences.append(MyText)

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occured")

    print("Finished recording in analyzer.py")
    ## Pre-processing
    bad_chars = [';', ':', '!', "*", ",", "."]

    inp_corpus = ''.join(i for i in inp_corpus if not i in bad_chars)
    inp_corpus = inp_corpus.replace('&', 'and')
    inp_corpus = inp_corpus.replace('@', 'at')
    inp_corpus = inp_corpus.lower()
    corpus_list = list(inp_corpus.split(' '))

    ## setting weightage parameters for scores
    alpha = 0.4
    beta = 0.6

    ## textfile contatining words and their usage frequency
    # script_dir = Path(__file__).parent
    f = open(DEPENDENCIES_DICT_DIR, "r")
    dictonary = dict()
    list_lines = f.readlines()

    ## creating word-frequency dictonary out of words-text file
    rank = 1
    for line in list_lines:
        li = list(line.split(' '))
        word, frequency = li[0], li[2]
        dictonary[word] = rank
        rank += 1

    for each in dictonary.keys():
        temp = (dictonary[each])
        scaled = (temp - 1) * 99 / (len(dictonary) - 1)
        scaled += 1
        dictonary[each] = scaled

    visited = []
    score_1 = 0
    unique = 0
    for word in corpus_list:
        if word in dictonary.keys():
            if word not in visited:
                score_1 = score_1 + dictonary[word]
                visited.append(word)
                unique += 1

    ## calculating score_2 with tag ranks
    score_2 = 0
    db = pd.read_csv(Q1_CSV)
    db_dict = dict(db.values)
    for word in corpus_list:
        if word in db_dict.keys():
            if word not in visited:
                score_2 = score_2 + db_dict[word]
                visited.append(word)
                unique += 1

    strength = (alpha * score_1) + (beta * score_2)
    strength = float("{:.2f}".format(strength))
    f.close()

    print("Starting syntax analysis")

    device = "cpu"
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()
    model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
    model.load_state_dict(torch.load(BERT_MODEL, map_location='cpu'))
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

    model.eval()
    sentences = ["[CLS] " + sentence + " [SEP]" for sentence in sentences]
    labels = [0]
    tokenized_texts = [tokenizer.tokenize(sent) for sent in sentences]
    MAX_LEN = 128
    predictions = []
    true_labels = []
    input_ids = pad_sequences([tokenizer.convert_tokens_to_ids(txt) for txt in tokenized_texts], maxlen=MAX_LEN,
                              dtype="long", truncating="post", padding="post")
    input_ids = [tokenizer.convert_tokens_to_ids(x) for x in tokenized_texts]
    input_ids = pad_sequences(input_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")

    attention_masks = []
    for seq in input_ids:
        seq_mask = [float(i > 0) for i in seq]
        attention_masks.append(seq_mask)

    prediction_inputs = torch.tensor(input_ids)
    prediction_masks = torch.tensor(attention_masks)
    prediction_labels = torch.tensor(labels)
    model.eval()

    with torch.no_grad():
        logits = model(prediction_inputs.to(device).long(), token_type_ids=None,
                       attention_mask=prediction_masks.to(device).long())
    logits = logits.detach().cpu().numpy()
    predictions.append(logits)

    flat_predictions = [item for sublist in predictions for item in sublist]
    flat_predictions = np.argmax(flat_predictions, axis=1).flatten()
    flat_true_labels = [item for sublist in true_labels for item in sublist]

    result = {}
    for i in range(len(flat_predictions)):
        if flat_predictions[i] == 1:
            result[sentences[i]] = 'Correct'
        elif flat_predictions[i] == 0:
            result[sentences[i]] = 'Wrong'

    # print('\n Captured text from audio: \n', inp_corpus, '\n')
    # print('\n Grammatical Syntax Analysis\n', result, '\n')
    # print("\n Vocabulary strength: ", strength)
    # print("\n Unique words spoken: ", unique)

    res = [result, strength, unique]
    print("Finished processing in analyzer function")
    return res


if __name__ == "__main__":
    print("Here calling main function")
    return_val = analyze()

