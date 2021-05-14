Mojibake puzzle dictionary

With a bit of effort, you can solve the crossword puzzle in last Sunday's paper. But if you think a little harder, you can solve all puzzles, now and in the future, in one go with a program.

For example, let's first solve this simple puzzle:

   ...d...
    ..e.....
     .l...
  ....f.
......t..

We need some sort of dictionary to search. Here is one (this is your `test-input`):

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

If you look closely, there is something weird going on. Some of the words in this puzzle seem garbled. This character soup occurs when two systems disagree about the encoding of a given piece of text. The Japanese, whose rich set of characters has created ample opportunities for message garbling, have dubbed this phenomenon [mojibake](https://en.wikipedia.org/wiki/Mojibake)

All is not lost, however, because if the mistake is known, it could potentially be undone.

In this case, there is a clear pattern.

* Most words are plain utf-8
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

      |     
   dardées
    roekoeën
     blökt
  träffs
orquestrá
      |    

Take the lines of these words in the original dictionary, and add them together. 
So we add 10 + 6 + 20 + 2 + 12 and arrive at `70`. This is the solution for the test problem.


Your puzzle:

           |
      .....t......
       ....o.....
    .......p..............
...........d......
 ..........e......
   ........s......
      .....k..........
           |

Your puzzle dictionary (your `input`) contains mojibake in exactly the same pattern. Decode it, and find words that match the crossword puzzle in the right place. There is only one unique solution. Your solution is the sum of the positions of the words in the puzzle dictionary.
