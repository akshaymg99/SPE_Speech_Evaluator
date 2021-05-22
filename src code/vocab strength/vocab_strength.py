import pandas as pd

## input text corpus

inp_corpus = """Hey, My name is Akshay. I did my undergraduate major in Electronics & Communication. 
But I later decided to do my masters in Computer Science. I like to solve challenging problems, and apply my
knowledge to help the world in a positive way. I have done several projects in AL ML domain, and would love
to work in a environment with like minded people to help build innovative products and grow professionally."""


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
f = open("dict_10k.txt", "r")

dictonary = dict()

list_lines = f.readlines()

## creating word-frequency dictonary out of words-text file
rank = 1
for line in list_lines:
    li = list(line.split(' '))
    word, frequency = li[0], li[2]
    dictonary[word] = rank
    rank += 1

## scaling the ranks to (1-100) range
def scale_100(no):
    scaled = (no - 1) * 99 / (len(dictonary) - 1) 
    return scaled + 1

for each in dictonary.keys():
    dictonary[each] = scale_100(dictonary[each])

#sorted_dict = dict(sorted(dictonary.items(), key=lambda item: item[1], reverse=True))
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
db = pd.read_csv('intro_Q1.csv')
db_dict = dict(db.values)
for word in corpus_list:
    if word in db_dict.keys():
        if word not in visited:
            score_2 = score_2 + db_dict[word]
            visited.append(word)
            unique += 1

strength = (alpha * score_1) + (beta * score_2)

print("Vocabulary strength: ", strength)
print("Unique words spoken: ", unique)

f.close()