# a3
## Part 1: Part-of-speech tagging

### Training
- Training for the model using bc.train dataset
- Extracting words and corresponding part of speech from a sentence and appending them into word and pos list
- For transition patterns, extracting Q(t+1) and Q(t) from a sentence where qj is Q(t+1) and qi is Q(t). For last pos, Q(t+1) is empty and Q(t) is the last word in a sentence.
- Creating dataframe word_freq which is count of different pos for a given word, pos_freq which is count of different pos in a corpus of words, and transition table which is count of unique transition pos from Q(t) to Q(t+1)

Here is the sample code for extracting words and pos from corpus of words :

```
    def train(self, data):
        word_list = []
        pos_list = []
        q_i = []
        q_j = [] 
        for s in data:
            for i in range(len(s[0])):
                if (i == len(s[0])-1):
                    word_list.append(s[0][i])
                    pos_list.append(s[1][i])
                    q_j.append('')
                    q_i.append(s[1][i])
                else :
                    word_list.append(s[0][i])
                    pos_list.append(s[1][i])
                    q_j.append(s[1][i+1])
                    q_i.append(s[1][i])
```

### Simplified Model
- Using the word_freq dataframe which is distribution of different pos counts for a given word
- For a given sentence, for each word taking the maximum occurence of pos count and extracting the pos column name
- Appending the pos column name for each word in a pos list and returning the list
- For posterior probability calculations, for each word in a sentence, taking log of max pos column by total sum of all pos occurence of a given word. Summing the probabilities for all word in a given sentence in order to get posterior probability

#### Assumptions
- For a word which is not in the training file, tagging them as 'noun' since most of them which were missing from training file was noun and probablity as -999

### HMM viterbi model
- Using the word_freq, pos_freq and transition table from training function
- Creating pos dictionary with pos as key and initialising value as 0
- For each word in a given sentence, checking whether the word is the first one in a sentence or not. For first word in a sentence, for each pos, calculating the emission and prior probabilities, summing them to get the posterior probability and updating the value of pos_dict
- Extracting the key i.e. pos and probablity i.e. posterior probability of max value as s and p from pos_dict and appending in a pos list
- For words after the first one, getting prior probabilities from pos_dict values. For each pos, calculating the transition probabilities for each pos combination. Calculating emission probabilities for each pos
- Using viterbi logic to calculate the posterior probability for each pos and updating the value of pos_dict
- Extracting the key i.e. pos and probablity i.e. posterior probability of max value as s and p from pos_dict and appending in a pos list
- Return the pos list and the corresponding p as a self variable

#### Assumptions
- Using log for each probabilities
- For a word in a given sentence which is not in the training file, assigning emission probability as -9999
- While calculating emission probability for each combination of pos with a given word, if there is no occurence of a word with a particular pos assigning them with emission probability as -9999
- For transition probabilities, for each pos combination transition, if there is no occurence of a given pos transition, assigning them with a transition probability as -9999

#### Simplification 
- Did not take into account backtracking if the posterior probabilities of a given word is equal because of high computational time

### MCMC complex model
- Initialing s with noun as part of speech for a given sentence
- Creating sample list with initially s value 
Sample code
```
s = ['noun']*len(sentence)
samples = [s]

```
- Using the word_freq, pos_freq and transition table from training function
- Iterating over 520 samples, and calculating probability distribution for a given pos in a word of a sentence
- Checking whether the word is first in a sentence, then for each pos, probability will be P(Q(t+1)|Q(t))*P(Q(t))*P(O(t)|Q(t))
- For last word in a sentence, then for each pos, probability will be P(Q(t)|Q(t-1))*P(O(t)|Q(t))
- For any other word in a sentence, then for each pos, probability will be P(Q(t+1)|Q(t))*P(O(t)|Q(t))*P(Q(t)|Q(t-1))
- For a given word in a sentence, appending the pos and probability distribution for all combination in pos_dist and prob_dist
- Creating a float variable with random generator and checking whether fraction of prob_dist with sum of prob_dist is greater than float variable, then adding the corresponding pos to the s. After iterating over entire sentence, a new s list of pos will be generated which will be added to the samples
- Removing first 20 samples

#### Assumptions
- Using log for each probabilities
- For a word in a given sentence which is not in the training file, assigning emission probability as -999
- For transition probabilities, for each pos combination, if there is no occurence of a given pos transition, assigning them with a transition probability as -999

#### Challenges
- Computational time is exceptionally high so unable to test on large test file
- Returning samples with same pos combination for a given sentence
- Not sure if this is a right approach for mcmc



### Results 
#### Simplified model
- Word accuracy     : 94%
- Sentence accuracy : 40%

#### HMM Viterbi model
- Word accuracy     : 85%
- Sentence accuracy : 13%