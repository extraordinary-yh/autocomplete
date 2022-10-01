# Autocomplete Engine
The Autocomplete Engine implement a functional trie tree. You will be able to insert words into a dictionary, lookup valid and invalid words, print your dictionary in alphabetical order, and suggest appropriate suffixes like an auto-complete bot. The autocomplete() method which will take a string as an input, and return another string as an output. If the string is not present in the tree, the output will be the same as the input. However, if the string is present in the tree, it finds the most common word to which it is a prefix and return that word instead.

## Data Structure
Autocomplete Engine rely on a trie tree and a max heap. The autocompelete function will first find the node that contains the prefix as its text and do so by following each character of the prefix down the tree. Then, the autocomplete function will conduct a pre-order traersal of the subtree whose root is the prefix node and append each node into the maxheap based on frequency. Then, the maxheap will pop the most frequent word. 

## Time Complexity
The time comlexity should be O(N), where N is the number of nodes in the prefix's sub-tree and correspond to the sum of number of letters of all prefix-contained-words excluding the number of letters of the prefix. And this is because traversal of the subtree would go to N nodes and pushing all of them to the maxheap takes N steps. Therefore T = 2*O(N) = O(N)
