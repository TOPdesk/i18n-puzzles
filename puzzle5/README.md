# Mojibake puzzle dictionary

We're writing a program that generates a multi-lingual crossword puzzle. We start drawing a simple grid, and then we search a dictionary for words that we could put in there. For example, let's start with this simple grid:

```
      |
   ...D...   (7)
    ..E..... (8)
     .L...   (5)
  ....F.     (6)
......T..    (9)
      |
```

To fill in the blanks, we need ot search through a list of words. Here is one (this is your `test-input`):

```
geléet
träffs
religiÃ«n
tancées
kÃ¼rst
roekoeÃ«n
skälen
böige
fÃ¤gnar
dardÃ©es
amènent
orquestrÃ¡
imputarão
molières
pugilarÃÂ£o
azeitámos
dagcrème
zÃ¶ger
ondulât
blÃ¶kt
```

Unfortunately, something weird is going on. If you look closely, you see that some of the words in this dictionary appear garbled. This character soup is typical when two systems disagree about the encoding of a given piece of text. The Japanese, whose rich set of characters has created ample opportunities for message garbling, have dubbed this phenomenon [mojibake](https://en.wikipedia.org/wiki/Mojibake)

All is not lost, however, because if the mistake is known, it could potentially be undone. In this case, there is a clear pattern.

* Most of the words are stored as plain utf-8
* For every 3rd line, the original word was encoded in utf-8 but loaded by a system that expected iso-latin-1. The resulting character mash was exported again in utf-8. 
* The same has happened every 5th line.
* Where the two series overlap (every 15th line), the word was doubly-miscoded.

Thus we can deduce that:

* the 3rd word in the test-input should be `religiën`
* the 5th word is `kürst`
* the 6th word is `roekoeën`
* etc. etc.
* the 15th word is `pugilarão`

Scanning the `test-input` for words that fit in our crossword, we arrive at this solution. 

```
      |     
   darDées   (7)
    roEkoeën (8)
     bLökt   (5)
  träfFs     (6)
orquesTrá    (9)
      |    
```

To arrive at your solution, take the line-number of each word in the original list, and add them together. 
So we add 10 + 6 + 20 + 2 + 12 and arrive at `50`. This is the solution for the test problem.

That was just an example. For the real puzzle, take this empty crossword grid:

```
           |
      .....T......          (12)
       ....O.....           (10)
    .......P..............  (22)
...........D......          (18)
 ..........E......          (17)
   ........S......          (15)
      .....K..........      (16)
           |
```

Your puzzle dictionary (your `input`) was mangled in exactly the same pattern. Decode it, and find words that match the crossword puzzle in the right place. There is only one unique solution. Matching is case-insensitive and accent-sensitive. Take the sum of line-numbers of the words that fit, this is your solution.
