from bs4 import BeautifulSoup
import requests as req
import pandas as pd
import os
import nltk
nltk.download('punkt')
nltk.download('stopwords')

# Reading the content from the url's
df = pd.read_excel('C:/blackcofferassignment/Input.xlsx')
for index in range(len(df)):
    url = df['URL'][index]
    urlid = df['URL_ID'][index]
    try:
        res = req.get(url)
    except:
        print(f"Error in accessing the data in url:\n {htmltext.title.text.strip()}")
    try:
        htmltext = BeautifulSoup(res.text,'html.parser')
    except :
        print("Error: No text was found in the article:",e)
        print(htmltext.title.text.strip())
    article = ""
    try:
        for p in htmltext.find_all('p'):
             article += p.get_text()

        title = htmltext.find('h1').get_text()
    except:
        print("Error in parsing of ",urlid)
    
    file_name = "C:/blackcofferassignment/content/" + str(urlid) + '.txt'
    # Creating a file of text for each url for easy accesing
    with open(file_name,'w',encoding = 'utf-8') as file:
        file.write(title+'\n'+article)



# Getting stop words
stop = set()
stopwords_dir = "C:/blackcofferassignment/StopWords"
for file in os.listdir(stopwords_dir):
    path = os.path.join(stopwords_dir, file)
    with open(path, 'r', encoding='ISO-8859-1') as f:
        stop.update(set(line.strip().lower() for line in f))

# Load content from text files
content_dir = "C:/blackcofferassignment/content/"
content = []

for text_file in os.listdir(content_dir):
    with open(os.path.join(content_dir, text_file), 'r', encoding='ISO-8859-1') as f:
        text = f.read()
        words = nltk.tokenize.word_tokenize(text)
        clean_text = [word for word in words if word.lower() not in stop]
        content.append(clean_text)

# Load positive and negative words
pos = set()
neg = set()

with open("C:/blackcofferassignment/MasterDictionary/positive-words.txt", 'r', encoding='ISO-8859-1') as f:
    pos.update(f.read().splitlines())

with open("C:/blackcofferassignment/MasterDictionary/negative-words.txt", 'r', encoding='ISO-8859-1') as f:
    neg.update(f.read().splitlines())

# Analyze sentiment scores
pos_words = []
neg_words = []
pos_score = []
neg_score = []
polarity_score = []
subjectivity_score = []

for i in range(len(content)):
    pos_words.append([word for word in content[i] if word.lower() in pos])
    neg_words.append([word for word in content[i] if word.lower() in neg])
    pos_score.append(len(pos_words[i]))
    neg_score.append(len(neg_words[i]))
    polarity_score.append((pos_score[i] - neg_score[i]) / (pos_score[i] + neg_score[i] + 0.000001))
    subjectivity_score.append((pos_score[i] + neg_score[i]) / (len(content[i]) + 0.000001))
# Finding complex and syllable words
import re
avg_sentence_list = []
complex_words_percent_list = []
fog_index_list = []
complex_words_len_list = []
avg_syllable_list = []
 
# function to return for each url
def function(file):
    with open(os.path.join(content_dir,file),'r',encoding= 'ISO-8859-1') as f:
        text = f.read()
        text = re.sub(r'[^\w\s.]','',text)
        sentences = nltk.tokenize.sent_tokenize(text)
        num_sen = len(sentences)
        # using only clean words
        words = [ word for word in text.split() if word.lower() not in stop]
        num_word = len(words)

        avg_sentence = num_word / num_sen

        complex_words = []
        for word in words:
            vowels = 'aeiou'
            # add 1 if its a vowel
            syllable_count = sum(1 for letter in word if letter.lower() in vowels)
            if(syllable_count > 2):
                complex_words.append(word)

        syllable_count = 0
        syllable_words = []

        #counting syllables

        for word in words:
            if(word.endswith("es") or word.endswith("ed")):
                word = word[:-2]
            vowels = "aeiou"
            count = sum(1 for letter in word if letter.lower() in vowels)
            if count>=1:
                syllable_words.append(word)
                syllable_count += count 
            avg_syllable = syllable_count/len(syllable_words)
            complex_words_percent = len(complex_words)/num_word
            fog_index = 0.4 * (avg_sentence + complex_words_percent)

            return avg_sentence,complex_words_percent,fog_index,len(complex_words),avg_syllable
        
for file in os.listdir(content_dir):
    avg_sentence,complex_words_percent,fog_index,complex_words_len,avg_syllable = function(file)
    avg_sentence_list.append(avg_sentence)
    complex_words_percent_list.append(complex_words_percent)
    fog_index_list.append(fog_index)
    complex_words_len_list.append(complex_words_len)
    avg_syllable_list.append(avg_syllable)
            

def cleaned_words(file):
  with open(os.path.join(content_dir,file), 'r',encoding='ISO-8859-1') as f:
    text = f.read()
    text = re.sub(r'[^\w\s]', '' , text)
    words = [word  for word in text.split() if word.lower() not in stop
            ]
    length = sum(len(word) for word in words)
    average_word_length = length / len(words)
  return len(words),average_word_length

word_count = []
average_word_length = []
for file in os.listdir(content_dir):
  x,y = cleaned_words(file)
  word_count.append(x)
  average_word_length.append(y)

  def count_personal_pronouns(file):
    with open(os.path.join(content_dir,file), 'r',encoding='ISO-8859-1') as f:
        text = f.read()
        personal_pronouns = ["I", "we", "my", "ours", "us"]
        count = 0
        for pronoun in personal_pronouns:
            count += len(re.findall(r"\b" + pronoun + r"\b", text)) # \b is used to match word boundaries
    return count

pp_count = []
for file in os.listdir(content_dir):
  x = count_personal_pronouns(file)
  pp_count.append(x)

  answer = pd.read_excel("C:/blackcofferassignment/Output Data Structure.xlsx")

variables= [pos_score, neg_score,polarity_score,subjectivity_score,average_word_length,complex_words_percent_list,fog_index_list,avg_sentence_list,complex_words_len_list,word_count,avg_syllable_list,pp_count,average_word_length]

for i,var in enumerate(variables):
    answer.iloc[:,i+2] = var

answer.to_excel('Output Data Structure.xlsx')

check = pd.DataFrame(variables)
print("The result is")
print(check)