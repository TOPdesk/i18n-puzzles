# Mojibake puzzle dictionary

Why solve a single crossword puzzle, when we can write a program to solve them all? Let's write such a program. In our case, the crosswords are multi-lingual. We start from a simple grid that is partially filled in, and we search through a dictionary for words that we could put in there. For example, let's start with this simple grid:

```
      |
   ...D...   (7)
    ..E..... (8)
     .L...   (5)
  ....F.     (6)
......T..    (9)
      |
```

Each horizontal line, you need to fill in a word of the right length, that matches the letter that is already filled in. There are no constraints on the vertical lines, i.e. the vertical lines do not have to form real words (apart from the one that is already filled in). To fill in the blanks, we need to search through a dictionary of words.

Your `test-input` contains two parts. The first part is a list of words. Then follows a blank line, and then the second part contains the  crossword, with periods (`.`) representing the letters that need to be filled in.

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

   ...d...
    ..e.....
     .l...
  ....f.
......t..
```

But, there is a catch! Something weird is going on with the dictionary. If you look closely, you see that some of the words in this dictionary appear garbled. This character soup is typical *when two programs disagree about the encoding of a piece of text*. And this is exactly what happened during the compilation of this dictionary.

The Japanese, whose rich set of characters has created ample opportunities for message garbling, have dubbed this phenomenon [mojibake](https://en.wikipedia.org/wiki/Mojibake).

All is not lost, however, because if the mistake is known, it could potentially be undone. In this case, there is a clear pattern.

* The entire file is encoded as utf-8. Most words are correct with this encoding.
* For every 3rd line, the original word was encoded in utf-8 but loaded by a system that expected iso-latin-1. The resulting character mash was stored with utf-8 encoding.
* The same has happened every 5th line.
* Where the two series overlap (every 15th line), the word was *doubly-miscoded*.

Thus we can deduce that:

* the 3rd word in the test-input should be `religiën`
* the 5th word is `kürst`
* the 6th word is `roekoeën`
* etc. etc.
* the 15th word is `pugilarão`

Scanning the `test-input` for words that fit in our crossword, we can complete it like so:

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

Your `input` contains another list of words, followed by an empty line, followed by a (new) blank crossword. The dictionary was mangled in exactly the same pattern. Decode it, and find words that match the crossword puzzle in the right place. There is only one unique solution. Matching is case-insensitive and accent-sensitive. Take the sum of line-numbers of the words that fit, this is your solution.

### Reading & reference materials

* [What is UTF-8?](https://en.wikipedia.org/wiki/UTF-8)
* [Experiment with encoding](https://onlinetools.com/utf8/convert-utf8-to-bytes) while learning how bytes can become characters, codepoints

------