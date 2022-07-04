# Nine Eleven

The phrase 'nine eleven' immediately reminds us of the [terrorist attacks of 11 September 2001](https://en.wikipedia.org/wiki/September_11_attacks). On that day, terrorists from Al-Qaeda crashed airplanes into the World Trade Center in New York City, killing nearly 3000 people. 

This phrase 'nine eleven' also reflects the American habit of writing a date with the month before the day - whereas in most European countries, dates are written the other way around.

The event of 'nine eleven' had a great emotional impact on people all over the globe. It would be possible to study this impact through diary entries written at the time. For this puzzle, we have a collection of diary entries from the past 100 years (between 1-1-1920 and 1-1-2020). Unfortunately, the diary pages are jumbled up. Each diary author has his own habit for the way they write dates. A date like 12-01-05 would be interpreted in the UK as 12 jan 2005, but in the United States as 1 dec 2005. But in some countries (e.g. Hungary, Japan) people write dates with the year first so this would be: 5 Jan 2012. Or even (not so common): 1 May 2012. But, at least each person is consistent, the same person always writes a date the same way.

Diary entries are indexed by their apparent date. Considering the `test input`:

```
16-05-18: Margot, Frank
02-17-04: Peter, Elise
06-02-29: Peter, Margot
31-09-11: Elise, Frank
09-11-01: Peter, Frank, Elise
11-09-01: Margot, Frank
```

By a process of elimination, we can figure out that

* Margot always writes the date as DMY
* Peter always writes the date as MDY
* Frank always writes the date as YMD
* Elise always writes the date as YDM

This means that both Peter and Margot wrote about the events of 'nine-eleven' in their diary, but not Frank or Elise.

To arrive at your answer, sort the names alphabetically and join them with spaces. The answer to the test-input is `Margot Peter`

By the way: writing year, then month, then day, as is common in e.g. Hungary and Japan, has certain advantages. For example, a plain text sort of dates written this way, will order dates neatly as expected. Use it in file names and have your files always neatly organized by date. Writing dates this way is also the standard set by [ISO-8601](https://en.wikipedia.org/wiki/ISO_8601). But in spite of standardization efforts, date formats remain a source of confusion.

![Localization workgroup date confusion](./formatting_meeting.png) [^1]
![Date formats by country](https://en.wikipedia.org/wiki/Date_format_by_country)

------

[^1]: Source: https://xkcd.com/2562/
