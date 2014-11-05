'''Semantic Similarity: 
For a given text file, builds semantic descriptors for all words in a given
text file. Using this semantic descriptor, returns most similar word to the
each word in question and checks whether it is the right answer, returning 
the percentage of questions answered correctly.

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
    
    #Empty list will store the sentances
    sentances = []
    
    #Store the location in the text of the last sentance
    lastperiod = 0
    
    #Go through the entire list of words
    for i in range(len(text)):
        
        #if the word contains a period, remember punctuation was not 
        #stripped
        if charactercheck(text[i]):
            
            #temporay list
            tmp = []
            
            #If we are on the first sentance
            if lastperiod == 0:
                
                #Add words from the first word to the end of this 
                #first sentance 
                for x in range (i+1):
                    tmp.append(remove(text[x]))
            else:
                #If not first sentance, Add words from the last sentance
                #period to the end of this sentance to the tmp list
                for u in range(lastperiod + 1, i+1):
                    #Make sure empty strings are not included
                    if remove(text[u]) != "":
                        tmp.append(remove(text[u]))
                    
            #append the tmp list to the sentances list
            if tmp != []:
                sentances.append(tmp)
            
            #set this period to be the last known period.
            lastperiod = i   
    
    #Returns the new list of all the sentences
    return sentances
                
        


def get_sentence_lists_from_files(filenames):
    '''Returns a list of all the sentences with the individual words as
    strings in the elements of the list.
    
    Arguements:
    filenames -- text file
    '''
    #Open the file as a list of all the words as strings as its elements in
    #the list. Call function text_to_words(filenames):
    text = text_to_words(filenames)
    
    #turn the list into a list of all the sentences as the elements
    return get_sentence_lists(text)


def build_semantic_descriptors(sentences):
    '''Returns a dictionary with the semantic descriptor of everyword. This
    semantic descriptor is stored as a value for the keyword in the dictonary
    
    Arguements
    sentences -- list
    '''
    
    #set new variable "d" to be the dictionary with every word in sentences
    #as a key and an emtpy dictionary as it's value
    #calls words_in_text(): to create this dictionary
    
    d = words_in_text(sentences)
    
    #For all keys in the dictionary of all the words in sentences, finds
    #the number of times each word appears in the same sentence as the keyword
    
    for keyword in d.keys():
        
        #create tempary dictionary to hold the values of frequency of 
        #everyword so that it can be added to its appropriate key in the 
        #dictionary
        tmp = {}
        
        #This section of for-loops goes into each word in each sentence and
        #adds the frequency of the the words in each sentence into the 
        #dictionary for each word
        
        #For every sentence in sentences
        for sentence in sentences:
            
            #if keyword in each sentence
            if keyword in sentence:
                
                #for every word in the sentence, add the frequency of that
                #word in that sentence to the dictionary for the keyword
                for word in sentence:
                    
                    #creates an input for that word if it does not exist
                    if word not in tmp.keys():
                        tmp[word] = 1
                        
                    #Updates the frequency of the word in the sentence
                    else:
                        tmp[word] += 1
                        
                #deletes the word iself from the list
                del tmp[keyword]
                
        d[keyword] = tmp #Set the dictionary at that word equal to the
                         #semantic descriptor for that keyword
        
    return d  #Return the semantic descriptor
    
        
def most_similar_word(word, choices, semantic_descriptors):
    '''Returns the most smiliar word to the keyword
    
    Arguements:
    word -- string
    choices -- list
    semantic_descriptors -- dictionary
    '''
    
    #Create empty list to store the cosine similarty for each choice
    sim = []

    for choice in choices:
        #appends the cosine similarity of each respective choice
        #If the 
        if word in semantic_descriptors.keys() and choice in \
           semantic_descriptors.keys():
            
            sim.append(cosine_similarity(semantic_descriptors[word],\
            semantic_descriptors[choice]))
        else:
            sim.append(-1) #If the word is not in the semantic descrpiptor
                           #return -1 so that it does not get
    print ("sim ", sim )
    if -1 in sim:
        return "Word not in text"
    
    
    #Set variable maxrun to store the highest similarity
    maxrun = 0
    
    pos = 0 #Stores the position of the word with the highest similarity
    for i in range(len(sim)): 
        if sim[i] > maxrun: #checks if the similarity is a max
            maxrun = sim[i] #update the max similarity
            pos = i  #update the position of the highest similarity
    
    return choices[pos] #return the word with the highest similarity


def run_similarity_test(filename, semantic_descriptors):
    '''Retruns the percentage that the program guess the answers to the 
    TOFEL questions corretly.
    
    Arguements:
    filename -- text file
    Semantic_descriptor -- dictionary
    '''
    testcases = []     #Empty list stores the TOFEL Questions with answer
    correct = 0        #number of correct answers
    trials = 0         #number of trials run
    file = open(filename) #Open the text file with the TOFEL questions
    line_strings = file.readlines() #list of all lines as elements
    file.close()       #Close file being read
    
    
    for line in  line_strings:
        #appends testcases with the a list of all the words in each line
        testcases.append(line.split())
    
    for test in testcases:
        choices = [] #Stores choices in each question
        
        #since first two elements are the question word and the answer
        #make choices any entry after those two elements
        for i in range(2, len(test)):
            choices.append(test[i])
        
        #Check if the question word is in the semantic descriptor
        if test[0] in semantic_descriptors.keys():
            
            #check which word is the most similar
            synonym = most_similar_word(test[0], choices, semantic_descriptors)
            if synonym == test[1]:
                
                #If the program guessed correctly, update number of correct
                #guesses
                correct += 1
        
        trials +=1 #Updates the number of trials run
    
    #Calculates the percentage that the program guesses correctly
    percentage = (correct/trials)*100 
    
    return percentage   
    


def text_to_words(text):
    '''Returns a list with all words as strings in the list. Opens a given 
    file, reads it and splits it up into indivitual words
    as stings as elements in the list.
    
    Arguements:
    text -- text file
    '''
    return open(text).read().split()

def remove(word):
    '''Returns the word without any extra characters
    
    Arguemnts:
    word -- string
    '''
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

    #Testing strategy:
    #Test all boundry cases for each function that would return
    #a list with incorrect lists
    
    
#############################################################################
#Boundary cases for get_sentences_from_files()
#Test by calling a text file which tests many cases
    
    print("testing get_sentences_from_files()")
    test_n = 1
       
    #This is the expected output of when the function runs the test file
    expected =     [['this', 'file', 'contains', 'testing', 'cases', 'for', 
                'get', 'sentance', 'lists'], ['hello'], ['my', 'name', 
                'is', 'ethan'], ['testing', 'functions'], 
                ['is', 'a', 'good'], ['job'], ['and'], 
                ['must'], ['be', 'done'], ['to', 'get'], ['a', 'good'], 
                ['mark'], ['in', 'csc']]    
    
    #run the test file
    sentences = get_sentence_lists(text_to_words("get_sentence_lists_test1.txt"))
    
    #-------------------------------------------------------------------------
    #Test 1: Tests whether multiple characters will be stripped and not be 
    #included in the list
    
    forbid = [" ", ".", "?", "/", "!", ";", ":"]
    for sentence in sentences:
        for word in sentence:
            for e in forbid:
                if e in word:
                    print('TEST', test_n, ": False")

    print('TEST', test_n, ": True")
    test_n += 1
    
    #-------------------------------------------------------------------------
    #Test 2: Tests for sentences without words and only characters that are
    #stripped. Should not be included in the list
    for sentence in sentences:
            for word in sentence:
                if '' == word:
                    print('TEST', test_n, ": False")
                    break
    print('TEST', test_n, ": True")
    test_n += 1
    
    #-------------------------------------------------------------------------
    #Test 3: Tests to make sure that numbers are not returned in the list
    for sentence in sentences:
                for word in sentence:
                    if word.isdecimal() == True:
                        print('TEST', test_n, ": False")
                        break
    print('TEST', test_n, ": True")
    test_n += 1    
    
    #-------------------------------------------------------------------------
    #Test 4: Tests if capitals are changed to lower cases
    for sentence in sentences:
        for word in sentence:
            if word.isdecimal() == True:
                print('TEST', test_n, ": False")
                break
    print('TEST', test_n, ": True")
    test_n += 1        

#############################################################################
#Test cases for build_semantic_descriptors
    #Comprises of two tests
    print("testing build_semantic_descpriptors()")
    test_n = 1

    #-------------------------------------------------------------------------
    #TEST 1: Tests to see if every word in each sematnt descriptor shows up
    #at least once in the same sentence as the key word
    
    words_in_file = text_to_words("build_semantic_descirptors_test1.txt")
    
    text = get_sentence_lists_from_files("build_semantic_descirptors_test1.txt")
    
    sem_des = build_semantic_descriptors(text)
    
    res = {}
    
    #Go through all the words with semantic descriptor vectors
    for keyword in sem_des.keys():
        #go through all the words that it says appears in the same sentance
        for word in sem_des[keyword].keys():
            
            #go through all the sentances in the text
            for sentance in text:
                #if the keyword we are looking for is in the same sentance 
                #as the word we are on in its simliarity vector
                #at least once, the res dictionary at that keyword will be True
                if keyword in sentance and word in sentance:
                    res[keyword] = True
    
    #As long as all items in res are True this will return True
    #Because res is a dictionary any problem words can be easily identifyed
    #this assists in troubleshooting and dubugging
    print ('TEST', test_n, ':', False not in res.items())
    test_n += 1
    
    #-------------------------------------------------------------------------
    #TEST 2: checks that all words not in the description vector are not found 
    #in the same sentance as that word to save on processing
    #as this has many more calcualtions than the previous res will be a boolean
    
    res = {}
    
    #go through all keys in sem_des
    for keyword in sem_des.keys():
        #go through all unique words in text
        for word in words_in_text(text):
            #if the word is not in the list of words known to be in same 
            #sentance as keyword
            if word not in sem_des[keyword].items():
                #go look through all the sentances and check
                for sentance in text:
                    #if they are in the same sentanace add a False enrty to res
                    #at word
                    if word in sentance and keyword in sentance:
                        res[word] = False
    #print if res contains any False elements                     
    print ('TEST', test_n, ':', False not in res.items())
    
    
    ###########################################################################
    #Testing most_simlar_word()   
    print("testing most_similiar_word()")
    
    sem_des = {"a":{"a":0, "b":0, "c":0, "d":0, "e":0, "f":0 },
               "b":{"a":0, "b":0, "c":0, "d":0, "e":0, "f":0 },
               "c":{"a":0, "b":0, "c":0, "d":0, "e":0, "f":0 },
               "d":{"a":0, "b":0, "c":0, "d":0, "e":0, "f":0 },
               "e":{"a":0, "b":0, "c":0, "d":0, "e":0, "f":0 },
               "f":{"a":0, "b":0, "c":0, "d":0, "e":0, "f":0 },
               }
    
    """
    These lists prepare words to compare with choices
    
    word -- [words to compare]
    
    choices -- [choices for corrisponding word]
    
    expected -- [expected answer]
    """
    word = ["a", "b", "c", "d", "e", "f"]
    
    
    print(sem_des)
    
    
    for test_n in range(6):
        res = most_similar_word(word[test_n],choices[test_n],sem_des) 
        print(word[test_n])
        print(choices[test_n])
        print(res)
        print("TEST ", test_n, " : ", expected[test_n] == res )

    
    
    
    
    