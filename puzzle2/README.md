Scientists have built a gravitional wave detector, with detector stations all around the world.
Unfortunately, the gravitational waves are extremely faint, and often, what the sensors pick up is just noise.
Scientist say that the measure can only be trusted if four or more detector stations around the world are triggered at precisely the same time. Only then can we say with a reasonable degree of certainty that we've picked up a gravitational wave.

In the input list, you find the local times when detectors recorded something, and the time zone of that detector station.
Go through the list, and find an instance where four signals were recorded at the same time (at least within the same second).

For example, in the list of four timestamps below:

```
05/06/2019, 8:15:00 Chile Standard Time
05/06/2019, 8:15:00 Eastern Daylight Time
01/02/2011, 9:15:00 Chile Summer Time
01/02/2011, 9:15:00 Eastern Standard Time
```

This list shows some recordings from our stations in New York and Santiago. In this list, the first two recordings took place at the same time. The last two recordings actually differ by two hours (due to daylight savings time changes).

Find the time that a gravitational wave was recorded in four or more places at the same time. To arrive at your final answer, convert that date to number of seconds since `01 Jan 1970 00:00:00 GMT` (i.e. the start of the unix epoch). In the example above, the answer corresponding to the first two recordings would be `1559736900`
