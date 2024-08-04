# Length limits on messaging platforms

The venerable SMS system uses a message limit of 160 bytes[^1]. This was designed so that a message could fit in exactly one packet, thus being really cheap and fast to handle on first-generation mobile phone networks. Although the approach makes sense for technical reasons, it unfairly penalizes people who use non-latin (russian, greek, japanese) alphabets - in most encodings, they need more bytes per character than latin alphabets.

Twitter used to have a character limit of 140 characters[^2] (nowadays increased to 280). But this limit is a limitation by design, to emphasize the concise and ephemeral nature of the platform. It's not a technical limitation. So the designers of twitter set the limit at 140 `characters`, NOT the number of bytes.

You are working for a fictious company named "TOPlap", which sends messages to customers using both SMS and twitter, via a message broker. The message broker charges a fee for each message sent, as follows:

* For each SMS: 11 cents.
* For each tweet: 7 cents.
* Discount rate for messages sent as SMS and tweet together: 13 cents.

Write a program that checks whether messages are valid as SMS and / or valid as (old-style) tweet. Your puzzle `input` is a list of messages in different languages, one on each line, *in UTF-8 format*. Calculate your total bill with the message broker, assuming that you will not sent any messages that are too long. So a message that is valid for the SMS platform, but not as tweet, will only incur the charge of 11 cents for a single SMS message. 

*Line endings are excluded from bytes count as well as character count.*

For example, given this `test input`:

```
néztek bele az „ártatlan lapocskába“, mint ahogy belenézetlen mondták ki rá a halálos itéletet a sajtó csupa 20–30 éves birái s egyben hóhérai.
livres, et la Columbiad Rodman ne dépense que cent soixante livres de poudre pour envoyer à six milles son boulet d'une demi-tonne.  Ces
Люди должны были тамъ и сямъ жить въ палаткахъ, да и мы не были помѣщены въ посольскомъ дворѣ, который также сгорѣлъ, а въ двухъ деревянныхъ
Han hade icke träffat Märta sedan Arvidsons middag, och det hade gått nära en vecka sedan dess. Han hade dagligen promenerat på de gator, där
```

* The first message is 162 bytes long and 143 characters long. It's suitable for neither messaging system, so nothing will be sent and the charge is zero.
* The second message is 138 bytes long and 136 characters long. It's suitable for both messaging system, so apply the discount rate of 13 cents
* The third message is 253 bytes long and 140 characters long. It's only suitable as a tweet, and incurs a charge of 7 cents.
* The fourth message is 147 bytes long and 141 characters long. It's only suitable as an SMS message, and incurs a charge of 11 cents.

The solution to the test input would then be 0 + 13 + 7 + 11 totalling `31`

### Reading & reference materials

* [The absolute minimum every programmer should know about Unicode, no excuses](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/)

------

[^1]: This is a simplification. The reality is complicated, see https://www.twilio.com/docs/glossary/what-sms-character-limit
[^2]: Also more complicated than described here, see: https://developer.twitter.com/en/docs/counting-characters
