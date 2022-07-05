from nltk.tokenize import WhitespaceTokenizer
from collections import Counter
import random
import re

file_name = input()
with open(file_name, "r", encoding="utf-8") as f:
    corpus = f.read()

def find_tail(tail_list, search):
    for tail in tail_list:
        if re.match(search, tail[0]):
            return tail[0]

wst = WhitespaceTokenizer()
all_words = wst.tokenize(corpus)
unique_words = set(all_words)
bigram_no = len(all_words) - 1

trigram_words = {}
for index, word in enumerate(all_words):
    try:
        head = f'{word} {all_words[index + 1]}'
        trigram_words.setdefault(head, []).append(all_words[index + 2])
    except IndexError:
        continue

trigram_word_count = {}

for head in trigram_words:
    trigram_word_count[head] = Counter(trigram_words[head])

chain = 0
while chain < 10:
    while True:
        while True:
            head = random.choice(list(trigram_word_count))
            if re.match(r'^[A-Z].*[^.!?]\s.*[^.!?]$', head):
                break

        sentence = head.split()
        for link in range(8):
            tails = trigram_word_count[head].most_common()
            tail = find_tail(tails, r'^[a-z].*[^.?!]$')
            if tail:
                sentence.append(tail)
            head = ' '.join(sentence[-2:])
            if head == None:
                break

        if len(sentence) > 4:
            while True:
                tails = trigram_word_count[head].most_common()
                tail = find_tail(tails, r'^[a-z].*[.?!]$')
                if tail:
                    sentence.append(tail)
                    print(*sentence)
                    chain += 1
                    break
                else:
                    break
            break
