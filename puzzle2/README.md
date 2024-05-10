# Detecting gravitational waves

Scientists have built a gravitational wave detector, with detector stations all around the world.
Unfortunately, the gravitational waves are extremely faint, and often, what the sensors pick up is just noise.
Scientist say that a recording can only be trusted if four or more detector stations around the world are triggered at precisely the same time. Only then can we say with a reasonable degree of certainty that we've picked up a gravitational wave[^1].

In the input list, you find the local times when detectors recorded something, and the time zone of that detector station.
Go through the list, and find an instance where four signals were recorded at the same time (at least within the same minute).

For example, in the list of six timestamps below (your `test-input`):

```
2019-06-05T08:15:00-04:00
2019-06-05T14:15:00+02:00
2019-06-05T17:45:00+05:30
2019-06-05T05:15:00-07:00
2011-02-01T09:15:00-03:00
2011-02-01T09:15:00-05:00
```

In this list, the first four recordings took place at the same time, in different time zones. 08:15 in timezone GMT-04:00 (Toronto summer time) happened at the same time as 14:15 in timezone GMT+02:00 (Paris summer time). The last two recordings were both made at 09:15, but they actually differ by two hours.

Your puzzle `input` is a complete list of recordings. Find the time that a gravitational wave was recorded in four or more places at the same time. Give your final answer in the exact same format, but with the timezone offset normalised to '+00:00'. In the example above, the answer corresponding to the four contemporary recordings would be `2019-06-05T12:15:00+00:00`

### Reading & reference materials

* [UTC on Wikipedia](https://en.wikipedia.org/wiki/Coordinated_Universal_Time), a time standard
* [UTC offset](https://en.wikipedia.org/wiki/UTC_offset), how the same moment in time has different time reading around the globe

-------

[^1]: To be fair, there are a lot of challenges in detecting gravitational waves. Timezone problems are the least of it. Watch this if you want to know more: https://www.youtube.com/watch?v=iphcyNWFD10
