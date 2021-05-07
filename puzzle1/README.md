# Length limits on messaging platforms

The venerable SMS system uses a message limit of 160 bytes[^1]. This was designed so that a message could fit in exactly one packet, thus being really cheap and fast to handle on first-generation mobile phone networks. Although the approach makes sense for technical reasons, it unfairly penalizes people who use non-latin (russian, greek, japanese) alphabets - in most encodings, they need more bytes per character than latin alphabets.

Twitter used to have a character limit of 140 characters[^2] (nowadays increased to 280). But this limit is a limitation by design, to emphasize the concise and ephemeral nature of the platform. It's not a technical limitation. So the designers of twitter set the limit at 140 `characters`, NOT the number of bytes.

Write a program that checks whether messages are valid as SMS and / or valid as (old-style) tweet. Your puzzle [input](./input) is a list of messages in different languages, one on each line, *in UTF-8 format*.  Your answer should be the number of messages that can only be sent on one platform, i.e. they must be either valid as tweet or valid as SMS message, but not both.

*Line endings are excluded from bytes count as well as character count.*

For example, given this [test input](./test-input):

```
néztek bele az „ártatlan lapocskába“, mint ahogy belenézetlen mondták ki rá a halálos itéletet a sajtó csupa 20–30 éves birái s egyben hóhérai.
livres, et la Columbiad Rodman ne dépense que cent soixante livres de poudre pour envoyer à six milles son boulet d'une demi-tonne.  Ces
Люди должны были тамъ и сямъ жить въ палаткахъ, да и мы не были помѣщены въ посольскомъ дворѣ, который также сгорѣлъ, а въ двухъ деревянныхъ
Han hade icke träffat Märta sedan Arvidsons middag, och det hade gått nära en vecka sedan dess. Han hade dagligen promenerat på de gator, där
```

* The first message is 162 bytes long and 143 characters long. It's suitable for neither messaging system, so it doesn't count.
* The second message is 138 bytes long and 136 characters long. It's suitable for both messaging system, so it doesn't count.
* The third message is 253 bytes long and 140 characters long. It's only suitable as a tweet, and should count towards the total
* The fourth message is 147 bytes long and 141 characters long. It's only suitable as an SMS message, and should count towards the total.

The solution to the test input would then be `2`

------

[^1]: This is a simplification. The reality is complicated, see https://www.twilio.com/docs/glossary/what-sms-character-limit
[^2]: Also more complicated than described here, see: https://developer.twitter.com/en/docs/counting-characters
