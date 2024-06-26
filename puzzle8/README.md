# Unicode passwords redux

Following up from puzzle 3, the IT department at "TOPlap" didn't like the results of their first study. They decided to try out a different password policy.

The new requirements are as follows:

- a length of at least 4 and at most 12
- at least one digit
- at least one accented or unaccented vowel (a, e, i, o, u) (examples: i, Á or ë). Note: we use the definition of vowel according to English.
- at least one accented or unaccented consonant, examples: s, ñ or ŷ
- no double letters in any form. Ignoring accents and case, letters should not recur. For example, in 'Daniël' no letters recur. But in 'Drieën' the 'e' occurs twice, one time with accent and one time without. 'Uusi' is out because the 'u' occurs twice, first uppercase and then lowercase.

Given this `test input`:
```
iS0
V8AeC1S7KhP4Ļu
pD9Ĉ*jXh
E1-0
ĕnz2cymE
tqd~üō
IgwQúPtd9
k2lp79ąqV
```

* The first password is invalid because it is too short
* The second is too long
* The third has no vowel
* The fourth has no consonant
* The fifth has a double letter 'e'
* The sixth has no digit
* The seventh and eighth passwords are valid

Your `input` is a list of passwords, one on each line. Write a program that checks if each password meets the requirements. Your answer should be the number of passwords that are valid. In the test input given above, the number of valid passwords is '2'.

### Reading & reference materials

* [What on Earth is Unicode Normalization?](https://towardsdatascience.com/what-on-earth-is-unicode-normalization-56c005c55ad0)
* [Unicode normalization forms](https://unicode.org/reports/tr15/#Norm_Forms) is a way for handling character composition (eg. &ijlig;, &auml;, &odblac;)
* [Comparing Unicode codepoints](https://en.wikipedia.org/wiki/Unicode_equivalence) can be tricky, but it's essential when searching in texts
* [Attributes of a Unicode character](https://en.wikipedia.org/wiki/Unicode_character_property) on Wikipedia, or check your favourite string manipulation library's API
* [Finding characters by attributes](https://www.regular-expressions.info/unicode.html) using a regular expressions is achievable in a lot of programming environments
* [Useful unicode lookup table](https://unicode-table.com/)

------
