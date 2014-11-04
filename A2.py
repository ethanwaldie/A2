'''Semantic Similarity: 
For a given text file, returns the most similiar word to the word that is 
inputed

Authors: Andrej Janda, Ethan Waldie. Last modified: Nov. 1, 2014.
'''

import math


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 2.
    '''
    
    sum_of_squares = 0.0  # floating point to handle large numbers
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    '''Return the cosine similarity of sparse vectors vec1 and vec2,
    stored as dictionaries as described in the handout for Project 2.
    '''
    
    dot_product = 0.0  # floating point to handle large numbers
    for x in vec1:
        if x in vec2:
            dot_product += vec1[x] * vec2[x]
    
    return dot_product / (norm(vec1) * norm(vec2))


def get_sentence_lists(text):
    """ Returns a new list of every sentence as an element in that list. Each 
    sentence element is split up into its individual words as individual
    strings. Opens file and splits it up into a list of all sentences as
    elements in that list.
    
    Arguments:
    text -- list
    """
    
    # This empty list will store the sentances
    sentances = []
    
    #This will store the location in the text of the last sentance
    lastperiod = 0
    
    # Go through the entire list of words
    for i in range(len(text)):
        #if the word we are on contains a period, remeber we have not stripped punctuation
        if charactercheck(text[i]):
            
            #temporay list
            tmp = []
            
            #If we are on the first sentance
            if lastperiod == 0:
                # Add words from the first word to the end of this #first sentance 
                for x in range (i+1):
                    tmp.append(remove(text[x]))
            else:
                #If not first sentance, Add words from the last sentance
                #period to the end of this sentance to the tmp list
                for u in range(lastperiod + 1, i+1):
                    tmp.append(remove(text[u]))
            #append the tmp list to the sentances list
            sentances.append(tmp)
            
            #set this period to be the last known period.
            lastperiod = i
        
    return sentances
                
        


def get_sentence_lists_from_files(filenames):
    text = text_to_words(filenames)
    return get_sentence_lists(text)


def build_semantic_descriptors(sentences):
    '''Returns a dictionary with the semantic descriptor of everyword. This
    semantic descriptor is stored as a value for the keyword in the dictonary
    
    Arguements
    sentences -- list
    '''
    #set new variable words to be the dictionary with every word in sentences
    #as a key and an emtpy dictionary as it's value
    d = words_in_text(sentences)
    
    #For all keys in the dictionary of all the words in sentences, finds
    #the number of times each word appears in the same sentence as the keyword
    tmp = {}
    
    one_p = len(d.keys())//100
    print(one_p)
    
    count = 0
    
    completed = 0
     
    for keyword in d.keys():
        #create tempary dictionary to hold the values of frequency of everyword
        #so that it can be added to it's appropriate key in the dictionary

        for sentence in sentences:
            if keyword in sentence:
                for word in sentence:
                    if word not in tmp.keys():
                        tmp[word] = 1
                    else:
                        tmp[word] += 1
                del tmp[keyword]
        d[keyword] = tmp
        count += 1
        if count == one_p:
            count = 0
            completed += 1
            print(completed, " %")
            
        
        
    return d
    
        
def most_similar_word(word, choices, semantic_descriptors):
    '''Returns the most smiliar word to the keyword
    
    Arguements:
    word -- string
    choices -- list
    semantic_descriptors -- dictionary
    '''
    
    sim = []

    for choice in choices:
        if word in semantic_descriptors.keys() and choice in semantic_descriptors.keys():
            sim.append(cosine_similarity(semantic_descriptors[word], semantic_descriptors[choice]))
        else:
            sim.append(-1)
    
    
    maxrun = 0
    
    pos = 0
    
    for i in range(len(sim)):
        if sim[i] > maxrun:
            maxrun = sim[i]
            pos = i
    
    if -1 in sim:
        return "Not Found"
    
    return choices[pos]


def run_similarity_test(filename, semantic_descriptors):
    testcases = []
    correct = 0
    trials = 0
    file = open(filename)
    line_strings = file.readlines()
    file.close()
    
    
    for line in  line_strings:
        testcases.append(line.split())
    
    for test in testcases:
        choices = []
        for i in range(2, len(test)):
            choices.append(test[i])
        
        if test[0] in semantic_descriptors.keys():
            synonym = most_similar_word(test[0], choices, semantic_descriptors)
            print(synonym)
            if synonym == test[1]:
                correct += 1
        trials +=1
    
    
    percentage = (correct/trials)*100
    
    return percentage   
    


def text_to_words(text):
    return open(text).read().split()

def remove(word):
    return word.lower().strip("?,.!;:+-/*--")

def charactercheck(word):
    return ("." in word or "!" in word or "?" in word)

def words_in_text(sentances):

    words = {}
    
    for sentance in sentances:
        for word in sentance:
            if word not in words:
                words[word] = {}
    return words
    

if __name__ == '__main__':
    dick = get_sentence_lists_from_files('War and Peace.txt')
    
    print(1)
    sem_des = build_semantic_descriptors(dick)
    
    print(2)
    print (run_similarity_test("testingdata.txt", sem_des))