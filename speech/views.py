import inspect
import os
import sys
import logging

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from speech.Analyzer import analyze

## creating logging instance
logger = logging.getLogger(__name__)

def index(request):
    return render(request, 'index.html')

def record(request):
    if request.method == 'POST' and 'run_analyzer' in request.POST:
        res = analyze()

        if res is None:
            logger.error("Didnt receive result analysis")
        else:
            logger.error("Analysis successful")

        table_1_answers = []
        table_1_sentences = []
        for each in res[0]:
            table_1_answers.append(res[0][each])
            table_1_sentences.append(each)

        table_1 = []
        for i in range(len(table_1_sentences)):
            temp = {}
            temp['Sentence'] = table_1_sentences[i]
            temp['Analysis'] = table_1_answers[i]
            table_1.append(temp)

        if res[1] >= 500:
            vocab_analysis = "Excellent! Your knowledge of english vocabulary is impressive"
        elif res[1] < 500 and res[1] >= 300:
            vocab_analysis = "Above average. You have good understanding of english words. Try fine-tuning the words and aim at highest"
        elif res[1] < 300 and res[1] >= 150:
            vocab_analysis = "Average. Your knowledge of english vocabulary words is average. There is room for improvement"
        elif res[1] < 150 and res[1] >= 75:
            vocab_analysis = "Below average. Your vocabulary is sufficient for casual conversation, but not good for professional use"
        elif res[1] < 75 and res[1] >= 25:
            vocab_analysis = "Poor. You have rudimentary proficiency in english, and need to work hard"
        elif res[1] < 25:
            vocab_analysis = "You hardly know english vocabulary. Learn it before proceeding further"
        else:
            vocab_analysis = "Data not sufficient"


        data = { 'table_1':table_1, 'vocab_strength':res[1], 'vocab_analysis':vocab_analysis, 'unique_words':res[2] }

        return render(request, 'result.html', data )


    return render(request, 'record.html')

def result(request):
    return render(request, 'result.html')