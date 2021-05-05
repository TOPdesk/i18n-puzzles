Which match criteria?

- at least 4 characters, maxiumum 12 characters
- at least one digit
- at least one uppercase letter (examples: A or Ĳ)
- at least one lowercase letter (examples: a or ŷ)
- at least one 'special' character, that is neither a digit nor part of the standard 26-letter alphabet (examples: Ű, æ or ẞ)


Given this test input:
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
* The seventh and eighth are passwords are valid

Your answer should be the number of passwords that are valid. In the test input given above, the number of valid passwords is '2'.