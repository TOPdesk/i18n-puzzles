# The audit trail fixer

"TOPlap" keeps audit trails on all modifications made to its records. This audit trail keeps track, for example, each time you change the status of a record. Later you could run a report and find out how long this record was in a certain state.

Now it turns out that there was a small bug in the software, that made some of the audit trails unreliable. For example, the report may show that a record was in state X for 1720 minutes, but in actuality it was only 1360 minutes. We are going to write a script to recalculate audit trails for affected customers.

Fixing the audit trails is not simple. One major challenge is that all timestamps are kept as *local times with a GMT offset*. Unfortunately, [GMT offsets are not time zones](https://spin.atomicobject.com/2016/07/06/time-zones-offsets/). The difference between time zones and GMT offsets is subtle but important: with just a GMT offset, you can't know if you have to apply daylight savings time changes, or not.

Through a lucky coincidence, it is possible to deduce timezones in this particular scenario. You see, we know that only two customers were affected by this bug: 1. FaxSchool, the Halifax school board, and 2. El Universidad Libre de Santiago (EULS). That means that each timestamp can be one of two timezones:

1. America/Halifax, which is GMT-4 (North hemisphere summer) or GMT-3 (North hemisphere winter)
2. America/Santiago[^1], which is GMT-3 (South hemisphere winter) or GMT-4 (South hemisphere summer)

Based on the time of year and GMT offset, we can make a pretty good guess.

In the `test-input` below, you see three columns. The first column is the timestamp (with GMT offset) that we want to 'fix'. The second column is the correct audit trail duration in minutes. The third column is the wrong audit trail duration in minutes. To arrive at the correct time, we must substract the incorrect minutes and then add again the correct minutes. The resulting timestamp must, of course, be converted to local time again, because otherwise we'd risk subtle bugs elsewhere in the system.

```
2012-11-05T09:39:00.000-04:00	969	3358
2012-05-27T17:38:00.000-04:00	2771	246
2001-01-15T22:27:00.000-03:00	2186	2222
2017-05-15T07:23:00.000-04:00	2206	4169
2005-09-02T06:15:00.000-04:00	1764	794
2008-03-23T05:02:00.000-03:00	1139	491
2016-03-11T00:31:00.000-04:00	4175	763
2015-08-14T12:40:00.000-03:00	3697	568
2013-11-03T07:56:00.000-04:00	402	3366
2010-04-16T09:32:00.000-04:00	3344	2605
```

* The 1st record happens during the northern winter, so we can deduce that the -4:00 offset indicates Halifax.
That year, summer time in Halifax ended on Sun, 4 Nov, 02:00. We substract 3358 and add 969 minutes, and arrive at 2012-11-03T18:50:00.000-03:00 (Halifax DST).
* Lines 7 and 9 are from Halifax as well.
* Lines 2,3,4,5 and 10 are from Santiago.
* Records 6 and 8 are ambiguous: both Halifax and Santiago are in the same GMT offset on those days. But the calculation happens to be the same for both places so it makes no difference (You may assume that your input will always produce an unambiguous result, even when the place can not be deduced).

In the end, here are the corrected times corresponding to the `test input`:

```
2012-11-03T18:50:00.000-03:00
2012-05-29T11:43:00.000-04:00
2001-01-15T21:51:00.000-03:00
2017-05-13T23:40:00.000-03:00
2005-09-02T22:25:00.000-04:00
2008-03-23T15:50:00.000-03:00
2016-03-13T10:23:00.000-03:00
2015-08-16T16:49:00.000-03:00
2013-11-01T07:32:00.000-03:00
2010-04-16T21:51:00.000-04:00
```

Now to arrive at your final answer, do the following.
For each record, take just the hour in local time and multiply it by the line number.
Sum all these products, this is your result. For the test-input above, the answer is: 18 * 1 + 11 * 2 + 21 * 3 + 23 * 4 + 22 * 5 + 15 * 6 + 10 * 7 + 16 * 8 + 7 * 9 + 21 * 10 = `866`

### Reading & reference materials

* [IANA Time Zone database](https://www.iana.org/time-zones) is the official source of time zone data used by libraries and operating systems. It's not easy to parse the information here, but it's good to know where it all comes from.
* [timeanddate.com](https://www.timeanddate.com/) is incredibly useful. You can find all kinds of useful time-related information, such as when daylight savings time starts and ends for each time zone around the world. You can find DST-corrected time and date at any instant in history. 

--------

[^1]: For more fun with daylight savings time, read up on [Time in Chile](https://en.wikipedia.org/wiki/Time_in_Chile)
