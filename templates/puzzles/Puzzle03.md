## --- Fix your passwords! ---

Great job fixing and restarting our remote-working server! --But now we run into the next problem!

The reboot has triggered an update. The password policy has become much more strict and it has become impossible to login with a password that doesn't follow the policy. Lots of colleagues cannot log in! We need to check the passwords of all 800 employees to see if they need to be changed.

(Maybe later we should also think about not storing our passwords in plain text. I hear crypto hashing is a good idea.)

A **good** password has the following properties:

- It contains at at least 2 vowels (`aeiou` only), like `ae`, `bace`, or `aeiou`
- It does **not** contain more than 6 vowels, like `uboibabecicou`, or `aeiouaeiou`
- It contains at least one letter that appears twice in a row, like `xx`, `abcdde` or `aabbccdd`.
- It does **not** contain the strings `zz`, `ef`, `td` or `er`


For example:
- `becdffa` is good because it contains 2 vowels, a double letter and none of the disallowed substrings.
- `aa` is good because it has 2 vouwels and a double letter even though the letters used by the different rules overlap.
- `bcdaefaa` is bad because it contains `ef`.
- `bpcdaffd` is bad because it contains only 1 vowel.
- `foobarbazquxquux` is bad because it contains more than 6 vowels.

`How many passwords are bad` and need to be changed?
