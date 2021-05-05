The venerable SMS system uses a message limit of 255 bytes. This was designed so that a message could fit in exactly one packet, thus being really cheap and fast to handle on first-generation mobile phone networks. Although the approach makes sense for technical reasons, it unfairly penalizes people who use non-latin (russian, greek, japanese) alphabets - in most encodings, they need more bytes per character than latin alphabets.

Twitter used to have a character limit of 140 characters (nowadays increased to 280). But this limit is a limitation by design, to emphasize the concise and ephemeral nature of the platform. It's not a technical limitation. So the designers of twitter set the limit at 140 `characters`, NOT the number of bytes.

You have to write a program that checks whether messages are valid as SMS and / or valid as (old-style) tweet. Your puzzle input is a list of messages in different languages, one on each line, *in UTF-8 format*. 

Count the number of messages (again, in UTF-8) that can only be sent on one platform. They must be either valid as tweet or valid as SMS message, but not both.

*Line endings are excluded from bytes count as well as character count.*

Test input
```


```

# TODO: be clear about DOS line endings. Should line endings be counted in the character limit?