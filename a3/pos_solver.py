###################################
# CS B551 Fall 2019, Assignment #3
#
# (Based on skeleton code by D. Crandall)
#

import pandas as pd
import numpy as np
import random
import math


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#
class Solver:
    
    def __init__(self):    
        self.word_freq = 0
        self.pos_freq = 0
        self.transition_table = 0 
        self.p = 0 

    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def posterior(self, model, sentence, label):
        if model == "Simple":
            word_freq = self.word_freq
            word_list = list(word_freq['word'])
            prob = 0
            for i in sentence:
                if i not in word_list:
                    prob += - 999
                else: 
                    id = word_list.index(i) 
                    prob += math.log(max(word_freq.iloc[id,1:])/sum(word_freq.iloc[id,1:]))   
            return prob
        elif model == "Complex":
            return -999
        elif model == "HMM":
            return self.p            
        else:
            print("Unknown algo!")

    # Do the training!
    #
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
        df = pd.DataFrame({'word':word_list,'pos':pos_list})
        df1 = pd.DataFrame({'qi':q_i,'qj':q_j})
        df2 = pd.DataFrame({'pos':pos_list})
        word_freq = pd.crosstab(df.word,df.pos).reset_index()
        pos_freq = df2.groupby(['pos']).size().to_frame(name = 'freq').reset_index()
        transition_table = df1.groupby(['qi','qj']).size().to_frame(name = 'freq').reset_index()
        self.word_freq = word_freq
        self.pos_freq = pos_freq
        self.transition_table = transition_table

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    #
    def simplified(self, sentence):
        word_freq = self.word_freq
        word_list = list(word_freq['word'])
        pos = []
        for i in sentence:
            if i not in word_list:
                pos.append('noun')
            else: 
                id = word_list.index(i) 
                colnames = word_freq.columns[1:]
                row = word_freq.iloc[id,1:]
                pos.append(colnames[np.argmax(row.values)])   
        return pos
    
# Logic code for complex_mcmc function inspired from https://github.com/pmpande/part-of-speech-tagger
    def complex_mcmc(self, sentence):
      s = ['noun']*len(sentence)
      samples = [s]
      pos_dict = {'.':0, 'adj':0,'adp':0,'adv':0,'conj':0,'det':0,'noun':0,'num':0,'pron':0,'prt':0,'verb':0,'x':0}
      word_freq = self.word_freq
      pos_freq = self.pos_freq
      transition_table = self.transition_table
      word_list = list(word_freq['word'])
      for n in range(0,520):
         for i in range(len(s)):
            prob_dist = []
            pos_dist = []
            if i == 0 :
               if sentence[i] in word_list:
                  id = word_list.index(sentence[i])
                  pos_col = word_freq.columns.get_loc(s[i])
                  for pos in pos_dict.keys():
                     prior = math.log(pos_freq.loc[pos_freq['pos'] == s[i] , 'freq']/sum(pos_freq['freq']))
                     row =  transition_table.loc[(transition_table['qi'] == s[i]) & (transition_table['qj'] == pos)]
                     row_j = transition_table.loc[(transition_table['qi']==s[i])]
                     transition = math.log(row['freq']/sum(row_j['freq'])) if len(row) != 0 else -999
                     emission = math.log((word_freq.iloc[id,pos_col])/(pos_freq.loc[pos_freq['pos'] == s[i], 'freq'])) if word_freq.iloc[id,pos_col] != 0 else -999
                     prob_dist += [prior + transition + emission]
                     pos_dist += [pos]
               else :
                  for pos in pos_dict.keys():
                     prior = math.log(pos_freq.loc[pos_freq['pos'] == s[i] , 'freq']/sum(pos_freq['freq']))
                     row =  transition_table.loc[(transition_table['qi'] == s[i]) & (transition_table['qj'] == pos)]
                     row_j = transition_table.loc[(transition_table['qi']==s[i])]
                     transition = math.log(row['freq']/sum(row_j['freq'])) if len(row) != 0 else -999
                     emission = -999
                     prob_dist += [prior + transition + emission]
                     pos_dist += [pos] 
            elif i == len(s) - 1:
               if sentence[i] in word_list:
                  id = word_list.index(sentence[i])
                  pos_col = word_freq.columns.get_loc(s[i])
                  for pos in pos_dict.keys():
                     row =  transition_table.loc[(transition_table['qi'] == s[i-1]) & (transition_table['qj'] == pos)]
                     row_j = transition_table.loc[(transition_table['qi']==s[i-1])]
                     transition = math.log(row['freq']/sum(row_j['freq'])) if len(row) != 0 else -999
                     emission = math.log((word_freq.iloc[id,pos_col])/(pos_freq.loc[pos_freq['pos'] == s[i], 'freq'])) if word_freq.iloc[id,pos_col] != 0 else -999
                     prob_dist += [transition + emission]
                     pos_dist += [pos]
               else :
                  for pos in pos_dict.keys():
                     row =  transition_table.loc[(transition_table['qi'] == s[i-1]) & (transition_table['qj'] == pos)]
                     row_j = transition_table.loc[(transition_table['qi']==s[i-1])]
                     transition = math.log(row['freq']/sum(row_j['freq'])) if len(row) != 0 else -999
                     emission = -999
                     prob_dist += [transition + emission]
                     pos_dist += [pos]
            else:
               if sentence[i] in word_list:
                  id = word_list.index(sentence[i])
                  pos_col = word_freq.columns.get_loc(s[i])
                  for pos in pos_dict.keys():
                     row1 =  transition_table.loc[(transition_table['qi'] == s[i-1]) & (transition_table['qj'] == pos)]
                     row_j1 = transition_table.loc[(transition_table['qi']==s[i-1])]
                     transition1 = math.log(row1['freq']/sum(row_j1['freq'])) if len(row1) != 0 else -999
                     row2 =  transition_table.loc[(transition_table['qi'] == pos) & (transition_table['qj'] == s[i+1])]
                     row_j2 = transition_table.loc[(transition_table['qi']==pos)]
                     transition2 = math.log(row2['freq']/sum(row_j2['freq'])) if len(row2) != 0 else -999
                     emission = math.log((word_freq.iloc[id,pos_col])/(pos_freq.loc[pos_freq['pos'] == s[i], 'freq'])) if word_freq.iloc[id,pos_col] != 0 else -999
                     prob_dist += [transition1 + emission + transition2]
                     pos_dist += [pos]
               else:
                  for pos in pos_dict.keys():
                     row1 =  transition_table.loc[(transition_table['qi'] == s[i-1]) & (transition_table['qj'] == pos)]
                     row_j1 = transition_table.loc[(transition_table['qi']==s[i-1])]
                     transition1 = math.log(row1['freq']/sum(row_j1['freq'])) if len(row1) != 0 else -999
                     row2 =  transition_table.loc[(transition_table['qi'] == pos) & (transition_table['qj'] == s[i+1])]
                     row_j2 = transition_table.loc[(transition_table['qi']==pos)]
                     transition2 = math.log(row2['freq']/sum(row_j2['freq'])) if len(row2) != 0 else -999
                     emission = -999
                     prob_dist += [transition1 + emission + transition2]
                     pos_dist += [pos]

            a = 0
            rand = random.random()
            for j in range(len(prob_dist)):
               a += prob_dist[j]/sum(prob_dist)
               if rand <= a :
                  s[i] = pos_dist[j]
                  break
         samples += [s]
      samples1 = []
      for i in samples[-500:]:
         samples1.append(i)
      return samples1[-1]

    def hmm_viterbi(self, sentence):
         word_freq = self.word_freq
         pos_freq = self.pos_freq
         transition_table = self.transition_table
         word_list = list(word_freq['word'])
         pos_dict = {'.':0, 'adj':0,'adp':0,'adv':0,'conj':0,'det':0,'noun':0,'num':0,'pron':0,'prt':0,'verb':0,'x':0}
         pos = []
         for i in range(len(sentence)):
            if i == 0 :
               if sentence[i] not in word_list:
                  for j in pos_dict.keys():
                     pos_col = word_freq.columns.get_loc(j)
                     prior_prob =  math.log(pos_freq.loc[pos_freq['pos'] == j, 'freq']/sum(pos_freq['freq']))
                     emission_prob =  -9999
                     pos_dict[j] =  prior_prob + emission_prob
                  s, p = max(pos_dict.items(), key=lambda x:x[1])
               else :
                  for j in pos_dict.keys():
                     id = word_list.index(sentence[i])
                     pos_col = word_freq.columns.get_loc(j)
                     prior_prob =  math.log(pos_freq.loc[pos_freq['pos'] == j, 'freq']/sum(pos_freq['freq']))
                     emission_prob = math.log((word_freq.iloc[id,pos_col])/(pos_freq.loc[pos_freq['pos'] == j, 'freq'])) if word_freq.iloc[id,pos_col] != 0 else -9999
                     pos_dict[j] =  prior_prob + emission_prob
                  s, p = max(pos_dict.items(), key=lambda x:x[1])
               pos.append(s)
            else :
               if sentence[i] not in word_list:
                  for j in pos_dict.keys():
                     emission_prob = -9999
                     value = []
                     for k in pos_dict.keys():
                        row =  transition_table.loc[(transition_table['qi'] == k) & (transition_table['qj'] == j)]
                        row_j = transition_table.loc[(transition_table['qi']==k)]
                        transition_prob = math.log(row['freq']/sum(row_j['freq'])) if len(row) != 0 else -9999
                        prior_prob = pos_dict[k]
                        value.append(transition_prob+prior_prob)
                     max_value = max(value)
                     pos_dict[j] = emission_prob + max_value
                  s, p = max(pos_dict.items(), key=lambda x:x[1]) 
               else:
                  for j in pos_dict.keys():
                     id = word_list.index(sentence[i])
                     pos_col = word_freq.columns.get_loc(j)
                     emission_prob = math.log((word_freq.iloc[id,pos_col])/(pos_freq.loc[pos_freq['pos'] == j, 'freq'])) if word_freq.iloc[id,pos_col] != 0 else -9999
                     value = []
                     for k in pos_dict.keys():
                        row =  transition_table.loc[(transition_table['qi'] == k) & (transition_table['qj'] == j)]
                        row_j = transition_table.loc[(transition_table['qi']==k)]
                        transition_prob = math.log(row['freq']/sum(row_j['freq'])) if len(row) != 0 else -9999
                        prior_prob = pos_dict[k]
                        value.append(transition_prob+prior_prob)
                     max_value = max(value)
                     pos_dict[j] = emission_prob + max_value
                  s, p = max(pos_dict.items(), key=lambda x:x[1])
               pos.append(s)
         self.p = p
         return pos
 
        

    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        else:
            print("Unknown algo!")
