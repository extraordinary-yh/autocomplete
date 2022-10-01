#!/usr/bin/env python
# coding: utf-8

# In[1]:


import heapq

class Node:
    """This class represents one node of a trie tree.
    
    Parameters
    ----------
    The parameters for the Node class are not predetermined.
    However, you will likely need to create one or more of them.
    """

    def __init__(self, text=""):
        self.text = text
        self.children = {}
        self.isWord = False
        self.frequency = 0
    
    def __lt__(self, other):
        if self.frequency == other.frequency:
                return self.text < other.text
        return self.frequency < other.frequency
    
class Trie:
    """This class represents the entirety of a trie tree.
    
    Parameters
    ----------
    The parameters for Trie's __init__ are not predetermined.
    However, you will likely need one or more of them.    
    
    Methods
    -------
    insert(self, word)
        Inserts a word into the trie, creating nodes as required.
    lookup(self, word)
        Determines whether a given word is present in the trie.
    """
    
    def __init__(self, word_list = None, root = None):
        """Creates the Trie instance, inserts initial words if provided.
        
        Parameters
        ----------
        word_list : list
            List of strings to be inserted into the trie upon creation.
        """
        #sort the word_list according to its lower case form
        self.word_list = sorted(word_list, key=str.lower)
              
        #create the root node with no text
        self.root = Node()
        #insert the words in word list into the tree
        
        for word in self.word_list:
            self.insert(word)
        
    
    def insert(self, word):
        """Inserts a word into the trie, creating missing nodes on the go.
        
        Parameters
        ----------
        word : str
            The word to be inserted into the trie.
        """
        word = word.lower()
        
        #check from root node
        curNode = self.root

        for i, char in enumerate(word):
            #if character is not in children, insert it
            if char not in curNode.children:
                prefix = word[0:i+1]
                curNode.children[char] = Node(prefix)
            #go to next character
            curNode = curNode.children[char]
        #set the word to true if we inserted a word
        curNode.isWord = True
        #invert the frequency to implement heapq as a maxheap
        curNode.frequency -= 1

        
    def lookup(self, word):
        """Determines whether a given word is present in the trie.
        
        Parameters
        ----------
        word : str
            The word to be looked-up in the trie.
            
        Returns
        -------
        bool
            True if the word is present in trie; False otherwise.
            
        Notes
        -----
        Your trie should ignore whether a word is capitalized.
        E.g. trie.insert('Prague') should lead to trie.lookup('prague') = True
        """
        #make smaller case
        word = word.lower()
        curNode = self.root
        
        #find the word from root
        for char in word:
            if char not in curNode.children:
                return False
            else:
                curNode = curNode.children[char]
        #return whether the word is previously inserted
        return curNode.isWord
    
    def alphabetical_list(self):
        """Delivers the content of the trie in alphabetical order.

        You can create other methods if it helps you,
        but the tests should use this one.
        
        Returns
        ----------
        list
            List of strings, all words from the trie in alphabetical order.
        """
        lst = []
        root = self.root
        
        #helper function to actually traverse through the tree
        def sub_preorder(curNode):
            #check if the node contains an inserted word
            if curNode.isWord:
                lst.append(curNode.text)
                #check for base case: when a node has no children(is leaf)
                if curNode.children == {}:
                    return None
            #for every child node of current node
            for i in curNode.children:
                #visit child node
                sub_preorder(curNode.children[i])  
        
        #call helper function
        sub_preorder(root)
        return lst
    
    def k_most_common(self, k):
        """Finds k words inserted into the trie most often.

        You will have to tweak some properties of your existing code,
        so that it captures information about repeated insertion.

        Parameters
        ----------
        k : int
            Number of most common words to be returned.

        Returns
        ----------
        list
            List of tuples.
            
            Each tuple entry consists of the word and its frequency.
            The entries are sorted by frequency.

        Example
        -------
        >>> print(trie.k_most_common(3))
        [(‘the’, 154), (‘a’, 122), (‘i’, 122)]
        
        I.e. the word ‘the’ has appeared 154 times in the inserted text.
        The second and third most common words both appeared 122 times.
        """
        #the frequency heap
        freqHeap = []
        #the list of k tuples with most frequency
        lst = []
        root = self.root
        
        #helper function to traverse through the tree and create a maxheap of nodes based on frequency
        def makeheap(curNode):
            #check if the node contains an inserted word
            if curNode.isWord:
                heapq.heappush(freqHeap, curNode)
                #check for base case: when a node has no children(is leaf)
                if curNode.children == {}:
                    return None
            #for every child node of current node
            for i in curNode.children:
                #visit child node
                makeheap(curNode.children[i]) 
        
        makeheap(root)
        #check if k is bigger than heap
        if k > len(freqHeap):
            for i in range(len(freqHeap)):
                node = heapq.heappop(freqHeap)
                lst.append((node.text, -node.frequency))
        else:
            #add tuple to the list
            for i in range(k):
                node = heapq.heappop(freqHeap)
                lst.append((node.text, -node.frequency))
        return lst

    def autocomplete(self, prefix):
        """Finds the most common word with the given prefix.

        You might want to reuse some functionality or ideas from Q4.

        Parameters
        ----------
        prefix : str
            The word part to be “autocompleted”.

        Returns
        ----------
        str
            The complete, most common word with the given prefix.
            
        Notes
        ----------
        The return value is equal to prefix if there is no valid word in the trie.
        The return value is also equal to prefix if prefix is the most common word.
        """
        #the frequency heap
        freqHeap = []
        #set current node to root
        curNode = self.root
        
        #helper function to traverse through the branch and create a maxheap of nodes W/ SAME PREFIX based on frequency
        def makeheap(curNode):
            #check if the node contains an inserted word
            if curNode.isWord:
                heapq.heappush(freqHeap, curNode)
                #check for base case: when a node has no children(is leaf)
                if curNode.children == {}:
                    return None
            #for every child node of current node
            for i in curNode.children:
                #visit child node
                makeheap(curNode.children[i]) 
                
        #find the branch of prefix and make prefix in lower case
        for char in prefix.lower():
            if char not in curNode.children:
                return prefix
            else:
                curNode = curNode.children[char]
                
        #build a max heap containing all words in the subtree with the node of prefix as root 
        makeheap(curNode)
    
        #extract node with the biggest frequency
        maxNode = heapq.heappop(freqHeap)
        return maxNode.text


# In[4]:


# Test Cases
# The Complete Works of William Shakespeare is a LARGE book, 

from requests import get
bad_chars = [';', ',', '.', '?', '!', '1', '2', '3', '4',
             '5', '6', '7', '8', '9', '0', '_', '[', ']']

SH_full = get('http://bit.ly/CS110-Shakespeare').text
SH_just_text = ''.join(c for c in SH_full if c not in bad_chars)
SH_without_newlines = ''.join(c if (c not in ['\n', '\r', '\t']) else " " for c in SH_just_text)
SH_just_words = [word for word in SH_without_newlines.split(" ") if word != ""]

SH_trie = Trie(SH_just_words)

assert SH_trie.autocomplete('hist') == 'history'
assert SH_trie.autocomplete('en') == 'enter'
assert SH_trie.autocomplete('cae') == 'caesar'
assert SH_trie.autocomplete('gen') == 'gentleman'
assert SH_trie.autocomplete('pen') == 'pen'
assert SH_trie.autocomplete('tho') == 'thou'
assert SH_trie.autocomplete('pent') == 'pentapolis'
assert SH_trie.autocomplete('petr') == 'petruchio'


# In[5]:


test1 = "To be or not To be: that is the question.".replace(":", "").replace(".","").split()
trie1 = Trie(test1)
assert trie1.autocomplete('t') == 'to'

test2 = "T ten tenet ten T".split()
trie2 = Trie(test2)
assert trie2.autocomplete('Ten') == 'ten'

test3 = "Yes! Yes! Goal! Goal! Goal!".replace("!","").split()
trie3 = Trie(test3)
assert trie3.autocomplete('No') == 'No'


# In[ ]:




