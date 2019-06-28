
# coding: utf-8

# In[14]:


import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from word_forms.word_forms import get_word_forms
import re

# nltk.download('wordnet')
# Just to make it a bit more readable

 
def convert(word, from_pos, to_pos):    
    """ Transform words given from/to POS tags """
 
    synsets = wn.synsets(word, pos=from_pos)
 
    # Word not found
    if not synsets:
        return []
    WN_NOUN = 'n'
    WN_VERB = 'v'
    WN_ADJECTIVE = 'a'
    WN_ADJECTIVE_SATELLITE = 's'
    WN_ADVERB = 'r'           
        
    # Get all lemmas of the word (consider 'a'and 's' equivalent)
    lemmas = [l for s in synsets
                for l in s.lemmas() 
                if s.name().split('.')[1] == from_pos
                    or from_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)
                        and s.name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)]
     
    # Get related forms
    derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]
 
    #filter only the desired pos (consider 'a' and 's' equivalent)
    related_noun_lemmas = [l for drf in derivationally_related_forms
                             for l in drf[1] 
                             if l.synset().name().split('.')[1] == to_pos
                                or to_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)
                                    and l.synset().name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE)]
    
    
    regex = re.compile('[^a-zA-Z0-9]')
    # Extract the words from the lemmas 
    #apply regex to remove non-alpha numeric characters
    #Assume that the string will not be completely non-alphanumeric
    #Even otherwise when we join the strings back to form the query the empty string will not impact :)
    words = [regex.sub('',l.name()).lower() for l in related_noun_lemmas]
#     len_words = len(words)
 
    # Build the result in the form of a list containing tuples (word, probability)
    #result = [(w, float(words.count(w))/len_words) for w in set(words)]
    
    #result.sort(key=lambda w: -w[1])
    return list(set(words))

def generate_synonyms(word):
    WN_NOUN = 'n'
    WN_VERB = 'v'
    WN_ADJECTIVE = 'a'
    WN_ADJECTIVE_SATELLITE = 's'
    WN_ADVERB = 'r'
    pos_tags = [WN_NOUN, WN_VERB, WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE, WN_ADVERB]
    syn_lemmas = []

    for from_pos in pos_tags:
        for to_pos in pos_tags:
            result = convert(word, from_pos, to_pos)
            syn_lemmas.extend(result)
    syn_lemmas = list(set(syn_lemmas))
    return syn_lemmas


# In[20]:


def generate_inflections(word):
    inflections_dict = get_word_forms(word)
    inflections = set()
    for forms in inflections_dict.values():
        for form in forms:
            inflections.add(form.lower())
    return list(inflections)


# In[31]:


def expand_query(query):
    expanded_query = ''
    stop_words = set(stopwords.words('english'))
    for word in re.findall(r"[\w']+",query.lower()):
        if word in stop_words:
            continue
        expanded_word = [word]

        synonyms = generate_synonyms(word)
        inflections = generate_inflections(word)
        
        expanded_word.extend(synonyms)
        expanded_word.extend(inflections)
        expanded_word = list(set(expanded_word))
        expanded_query = expanded_query + ' '.join(expanded_word) + ' '
        
    return expanded_query.strip()





# In[45]:




