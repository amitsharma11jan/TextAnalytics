
# coding: utf-8

# 
# 
# <ul>
# <li>Solve simple mathematical word problem using natural language processing and text analytics.</li>
# <li>Use PoS Tagging, Parsing and Typed Dependency to analyze the math query.</li>
# </ul>
# 
# Example:
# <ol>
# <li>Jack had 15 pencils. Jack found three pencils more. How many pencils do Jack have now?</li>
# <li>Jill had 40 toys. Jill lost seventeen toys. How many toys are left with Jill?</li>
# <li>John had 20 apples. John added 6 apples. How many apples are there with John?</li>
# </ol>
# <br>
# Exception: 
# 
# John had 20 apples. John gave 26 apples to Jill. How many apples are there with John? 
# 
# This should not give the answer as -6, rather show a message to correct the query.
# 
# Take only few verbs e.g. took | gave, found | lost, increased | decreased, added | removed (or subtracted)
# 
# 
# ### Solutions:
# 
# Please set path variable as path of stanfordcorenlp before executing below code.
# 
# verbMap : Dictionary object for simple addition and subtraction word problem.
# 
# <b>parseStatement</b> : This method is the main method to solve simple word problem. This method requires 2 parameter. User can pass simple text file (File should be present in stanfordcorenlp directory) and user needs to pass isInputFileAlreadyParsed as False and this method will generate parse XML file before further processing.
# 
# If user already parsed text file into XML filr, then user can call parseStatement method and pass xml file as input and pass isInputFileAlreadyParsed as True.
# 
# Example: 
# 
# Adam had one hundred twenty three billion four hundred fifty six million seven hundred eighty nine thousand twelve apples. Adam gave one billion fifty hundred sixty three apples to Eve. Adam gave two billion fifty hundred sixty three apples to Amit. How many apples are left with Adam?
# 
# fname = 'adam.txt'<br>
# parseStatement(fname, isInputFileAlreadyParsed=False)
# 
# Output:<br>
# Adam have 120456778886 apples now.
# 
# fname = 'adam.txt.xml'<br>
# parseStatement(fname, isInputFileAlreadyParsed=True)
# 
# Output:<br>
# Adam have 120456778886 apples now.

# In[1]:


import os
from bs4 import BeautifulSoup
import subprocess


# ###### Please set path variable as path of stanfordcorenlp before executing below code.

# In[2]:


path = "/Users/a5sharma/Documents/ISB/TA/stanford/stanford-corenlp-full-2017-06-09/"
os.chdir(path)


# #### verbMap
# Dictionary object for simple addition and subtraction word problem.

# In[3]:


verbMap = {'added':'add',
           'add':'add',
           'increased':'add',
           'increase':'add',
           'take':'add',
           'took':'add',
           'found':'add',
           'find' : 'add',
           'got':'add',
           'accumulated':'add',
           'collected':'add',
           'earned':'add',
           'give':'subtract',
           'gave':'subtract',
           'ate':'subtract',
           'lost':'subtract',
           'lose':'subtract',
           'subtracted':'subtract',
           'put':'subtract',
           'cut':'subtract',
           'paid':'subtract',
           'spent':'subtract',
           'consumed':'subtract',
           'have':'equal',
           'had':'equal',
           'left':'equal',
           'leave':'equal',
           'How many':'equal'}


# #### Variables:
# 
# These variables are required in parseStatement method to solve simple word problem.

# In[4]:


verb = ['VB','VBD','VBG','VBN','VBP','VBZ']
wh = ['WDT','WP','WP$','WRB']
Small = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90
}

Magnitude = {
    'thousand':     1000,
    'million':      1000000,
    'billion':      1000000000,
    'trillion':     1000000000000,
    'quadrillion':  1000000000000000,
    'quintillion':  1000000000000000000,
    'sextillion':   1000000000000000000000,
    'septillion':   1000000000000000000000000,
    'octillion':    1000000000000000000000000000,
    'nonillion':    1000000000000000000000000000000,
    'decillion':    1000000000000000000000000000000000,
}


# #### convertTextToNum method:
# 
# This method is required to convert string to number.
# 
# example:
# 
# String = one hundred twenty three billion four hundred fifty six million seven hundred eighty nine thousand twelve
# 
# This method convert above string to 123456789012.

# In[5]:


def convertTextToNum(w):
    n = 0
    g = 0
    try:
        n = int(w)
    except:
        for i in w.split():
            x = Small.get(i, None)
            if x is not None:
                g += x
            elif i == "hundred" and g != 0:
                g *= 100
            else:
                x = Magnitude.get(i, None)
                if x is not None:
                    n += g * x
                    g = 0
                else:
                    print(i)
    return n+g


# In[6]:


s = 'one hundred twenty three billion four hundred fifty six million seven hundred eighty nine thousand twelve'
convertTextToNum(s)


# #### parse_nlp method:
# This method is used to parse simple text file. This method is getting invoked in parseStatement method if isInputFileAlreadyParsed parameter is False to generate parsed XML file.<br>
# 
# This method requires below parameter<br>
# <ul><li>fname : File Name</li></ul>
# 
# Also, Please set path variable before execuing parseStatement method.
# 
# This method generate parsed XML file in above mentioned path.

# In[7]:


def parse_nlp(fname):
    subprocess.run(
                'java -cp "'+path+'*"'
                ' -mx5g'
                ' edu.stanford.nlp.pipeline.StanfordCoreNLP'
                ' -annotators tokenize,ssplit,pos,lemma,ner,parse'
                ' -file ' + fname + ' 2>parse.out',
                shell=True,     # execute with shell
                check=True      # error check
            )


# In[8]:


#parse_nlp(fname)


# ### parseStatement method:
# This method is used to parse statement and solve simple word problem.<br>
# This method requires below parameters:<br>
#     <ul>
#     <li>
#     fname : File name is required parameter
#     </li>
#     <li>
#     isInputFileAlreadyParsed : isInputFileAlreadyParsed is not required parameter. 
#     </li>
#     </ul>
#     Default value for isInputFileAlreadyParsed parameter is True.<br>
#     If isInputFileAlreadyParsed is False, parseStatement method requires text file with simple statement and this will execute parse_nlp method before executing below code.<br>
#     If isInputFileAlreadyParsed is True, parseStatement method requires parsed XML file.<br>

# In[9]:


"""
This method is used to parse statement and solve simple word problem.
This method requires below parameters:
    fname : File name is required parameter
    isInputFileAlreadyParsed : isInputFileAlreadyParsed is not required parameter. Default value for this parameter is False.
    If isInputFileAlreadyParsed is False, parseStatement method requires text file.
    If isInputFileAlreadyParsed is True, parseStatement method requires parsed xml file.

"""
def parseStatement(fname, isInputFileAlreadyParsed = True):
    if isInputFileAlreadyParsed:
        fname_parsed = fname 
    else:
        parse_nlp(fname)
        fname_parsed = fname+'.xml'
    with open(fname_parsed) as fp:
        soup = BeautifulSoup(fp, 'lxml')
        sentences = [i for i in soup.select('sentence') if i.attrs.get('id') != None]
        questionMap = {}
        dataMap = {}
        numList = []
        numString = ''
        num = 0
        personList = []
        personName = set()
        for sentence in sentences:
            tokens = sentence.find_all("token")
            sentenceId = sentence.attrs.get('id')
            fromSubject = ''
            fromVerb = ''
            numString = ''
            numList = []
            num = 0
            obj = ''
            toSubject = ''
            questionVerb = ''
            questionSubject = ''
            personList = []
            p = ''
            ques = [k.select('lemma')[0].getText() for k in tokens if k.find_all('pos')[0].getText() =='WRB']
            depd = [dependency for dependency in sentence.find_all("dependencies") 
                    if dependency.attrs.get('type') == 'basic-dependencies']
            if(len(ques) ==0):
                nsub = [j for j in depd[0].find_all("dep") if j.get('type') == 'nsubj']
                if len([i.find('dependent').getText() for i in nsub]) > 0:
                    fromSubject = [i.find('dependent').getText() for i in nsub][0]
                    fromVerb = [i.find('governor').getText() for i in nsub][0]
                    fromVerb = verbMap.get(fromVerb)
                    numList = [k.select('lemma')[0].getText() for k in tokens if k.find_all('pos')[0].getText() =='CD']
                    numString = ' '.join(numList)
                    num = convertTextToNum(numString)
                    obj = [j.find("governor").getText() for j in depd[0].find_all("dep") if j.get('type') == 'nummod'][0]

                case = [j for j in depd[0].find_all("dep") if j.get('type') == 'case']
                if len([i.find('governor').getText() for i in case]) > 0:
                    toSubject = [i.find('governor').getText() for i in case][0]  

                if num != 0:
                    if toSubject == '':
                        dataMap[sentenceId] = {'from':fromSubject, 'operation': fromVerb, 'number': num, 'object':obj}
                    else:
                        dataMap[sentenceId] = {'from':fromSubject, 'operation': fromVerb, 'number': num, 'object':obj, 'to':toSubject}
            else:   
                adverb = [j.find('governor').getText() for j in depd[0].find_all("dep") if j.get('type') == 'advmod'][0]
                qverb = [j.find('dependent').getText() for j in depd[0].find_all("dep") if j.get('type') == 'advmod'][0]
                questionVerb = qverb + ' '+adverb
                questionVerb = verbMap.get(questionVerb)
                questionSubject= [j.find('governor').getText() for j in depd[0].find_all("dep") 
                                  if j.get('type') == 'amod' and j.find('dependent').getText()==adverb][0]

                personList = [j for j in depd[0].find_all("dep") if j.get('type') == 'nmod']
                if(len(personList) ==0):
                    personList = [j for j in depd[0].find_all("dep") if j.get('type') == 'nsubj']
                if questionVerb != '':
                    if len([i.find('dependent').getText() for i in personList]) > 0:
                        p = [i.find('dependent').getText() for i in personList][0] 
                        questionMap[sentenceId] = {p: {'object':questionSubject, 'operation':questionVerb}}
                        personName.add(p)
        result = 0
        resultedMap = {}
        obj = ''
        for i in dataMap:
            result = 0
            tmp = dataMap.get(i)
            operation = tmp.get('operation')
            if tmp.get('to') == None and operation == 'equal':
                resultedMap[tmp.get('from')] = tmp.get('number')
                obj = tmp.get('object')
            else:
                if operation == 'add':
                    resultedMap[tmp.get('from')] = resultedMap[tmp.get('from')] + tmp.get('number')
                elif operation == 'subtract':
                    if resultedMap[tmp.get('from')] > tmp.get('number'):
                        resultedMap[tmp.get('from')] = resultedMap[tmp.get('from')] - tmp.get('number')
                        resultedMap[tmp.get('to')] = tmp.get('number')
                    else:
                        result = resultedMap[tmp.get('from')] - tmp.get('number')
                        print("There are no sufficient %s with %s and %s cannot give %s to %s. %d more apples required."%(tmp.get('object'),tmp.get('from'),tmp.get('from'), tmp.get('object'), tmp.get('to'), abs(result)))
                else:
                    resultedMap[tmp.get('from')] = tmp.get('number')
        questionList= list(questionMap.values())
        for p in personName:
            quesMap = [j for j in questionList if j.get(p)][0]
            obj = quesMap.get(p).get('object')
            print("%s have %s %s now."%(p, resultedMap.get(p), obj)) 


# <b>Example -1</b>
# 
# Sample Data:
# 
# <b>adam.txt</b>:
# 
# Adam had one hundred twenty three billion four hundred fifty six million seven hundred eighty nine thousand twelve apples.
# Adam gave one billion fifty hundred sixty three apples to Eve.
# Adam gave two billion fifty hundred sixty three apples to Amit.
# How many apples are left with Adam?
# 
# Output: <br>
# <b>Adam have 120456778886 apples now.</b>

# In[10]:


fname = 'adam.txt'
parseStatement(fname, isInputFileAlreadyParsed=False)


# In[11]:


fname = 'adam.txt.xml'
parseStatement(fname, isInputFileAlreadyParsed=True)


# In[12]:


parseStatement()


# <b>Example -2</b><br>
# 
# Sample Data:
# 
# <b>jack.txt</b>:
# 
# Jack had 15 pencils. Jack found three pencils more. How many pencils do Jack have now?
# 
# Output:<br>
# 
# <b>Jack have 18 pencils now.</b>
# 

# In[13]:


fname = 'jack.txt'
parseStatement(fname, isInputFileAlreadyParsed=False)


# <b>Example -3</b><br>
# 
# Sample Data:<br>
# 
# <b>jill.txt</b>:
# 
# Jill had 40 toys. Jill lost seventeen toys. How many toys are left with Jill?
# 
# Output:<br>
# 
# <b>Jill have 23 toys now.</b>

# In[14]:


fname = 'jill.txt'
parseStatement(fname, isInputFileAlreadyParsed=False)


# <b>Example -4</b><br>
# 
# Sample Data:<br>
# 
# <b>john.txt</b>:
# 
# John had 20 apples. John added 6 apples. How many apples are there with John?
# 
# Output:<br>
# 
# <b>John have 26 apples now.</b>

# In[15]:


fname = 'john.txt'
parseStatement(fname, isInputFileAlreadyParsed=False)


# <b>Example -5</b><br>
# 
# Sample Data:<br>
# 
# <b>john-1.txt</b>:
# 
# John had 20 apples. John gave 26 apples to Jill. How many apples are there with John?
# 
# Output:<br>
# 
# <b>There are no sufficient apples with John and John cannot give apples to Jill. 6 more apples required.
# John have 20 apples now.</b>
# 

# In[16]:


fname = 'john-1.txt'
parseStatement(fname, isInputFileAlreadyParsed=False)


# <b>Example -6</b><br>
# 
# Sample Data:<br>
# 
# <b>test.txt</b>:
# 
# Adam had sixty three apples.<br>
# Adam gave 20 apples to Eve.<br>
# Adam gave forty five apples to Amit.<br>
# How many apples are left with Adam?<br>
# How many apples are left with Amit?<br>
# How many apples are left with Eve?<br>
# How many apples are left with Raju?<br>
# 
# Output:<br>
# 
# There are no sufficient apples with Adam and Adam cannot give apples to Amit. 2 more apples required.<br>
# Eve have 20 apples now.<br>
# Raju have None apples now.<br>
# Amit have None apples now.<br>
# Adam have 43 apples now.

# In[17]:


fname = 'test.txt'
parseStatement(fname, isInputFileAlreadyParsed=False)

