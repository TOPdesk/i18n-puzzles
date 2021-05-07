# Unicode passwords

Most websites that accept passwors have some requirements. For example, they make you include at least one digit and at least one capital letter. The idea is that if you pick passwords from a large set of possible characters, the password will be harder to brute force. It's much harder to brute-force a password that include digits, upper-case and lower-case letters (62 possibilities) instead of just lower-case letters (26 possibilities) You wonder why websites don't encourage you to use accented characters, because it would dramatically increase the possibilities even further. Unicode is a great boon for strong passwords. 

Here we'll look at what such a password system could look like. 

The IT department of a ficticious company named "TOPlap" has decided to introduce new, unicode-based password requirements. These criteria are as follows.

- a length of at least 4 and at most 12
- at least one digit
- at least one uppercase letter (with or without accents, examples: A or Ĳ)
- at least one lowercase letter (with or without accents, examples: a or ŷ)
- at least one 'special' character, that is neither a digit nor part of the standard, unaccented 26-letter alphabet (examples: Ű, æ or ẞ)

Given this [test input](./test-input):
```
d9Ō
IgbZKq3JXrejiPN7Btŷ
žö2á
719ŅTOIY8NU
mAcpKI6Sr
dgxuPfHYýmAB
rdj4XcHŔB
71äĜ3
```

* The first password is invalid because it is too short
* The second is too long
* The third has no uppercase
* The fourth has no lowercase
* The fifth has no 'special' character
* The sixth has no digit
* The seventh and eighth passwords are valid

The IT department decided to do a little research on how well people handle these requirements. So they ask all the people at the company to choose a password, and then the IT department checks how often they manage to meet the password requirements correctly.

Your [input](./input) is a list of passwords, one on each line. Write a program that checks if each password meets the requirements. Your answer should be the number of passwords that are valid. In the test input given above, the number of valid passwords is '2'.