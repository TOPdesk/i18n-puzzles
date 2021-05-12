# A trip around the world.

The novel ['Around the world in 80 days' by Jules Verne](https://www.gutenberg.org/cache/epub/103/pg103.txt) tells the story of Phileas Fogg, an eccentric Englishman who speedruns a trip around the world following a daring bet. He is accompanied by his servant Passepartout. The book was published in 1872. Like every good science fiction author, Jules Verne took ideas from the cutting edge of science at the time, and worked it into a thrilling story. A noticeable effect of time differences was a new thing, made possible by the mechanization of transport. Here is an excerpt from the book, where we see Passepartout being completely baffled by this effect: 

> "You have plenty of time; it's only twelve o'clock."
> 
> Passepartout pulled out his big watch.  "Twelve!" he exclaimed; "why,
> it's only eight minutes before ten."
> 
> "Your watch is slow."
> 
> "My watch?  A family watch, monsieur, which has come down from my
> great-grandfather!  It doesn't vary five minutes in the year.  It's a
> perfect chronometer, look you."
> 
> "I see how it is," said Fix.  "You have kept London time, which is two
> hours behind that of Suez.  You ought to regulate your watch at noon in
> each country."
> 
> "I regulate my watch?  Never!"
> 
> "Well, then, it will not agree with the sun."
> 
> "So much the worse for the sun, monsieur.  The sun will be wrong, then!"

Those time differences lead to a major plot twist. Go read the book if you want to know how...

Suppose you follow a similar round-the-world itinerary. This itinerary is your puzzle `input`. It lists a sequence of departures and arrivals, starting from London, taking you around the world, and back again to London. You travel from place to place by airplane or high-speed train. Each step also lists the name of the continent, to help you with any hiatus in your knowledge of topography. As is the habit of airlines and travel agencies, all arrival and departure times are printed in *local time*. 

Write a program that calculates the *total travel time* in minutes, of the input itinerary. How many minutes would you be spending inside a train or airplane?

For example, take the following `test input`:

```
Departure: Europe/London                  10:00  Mar 04, 2020
Arrival:   Europe/Paris                   11:59  

Departure: Europe/Paris                   10:42  Mar 05, 2020
Arrival:   Australia/Adelaide             16:09  +1 day

Departure: Australia/Adelaide             19:54  Mar 06, 2020
Arrival:   America/Argentina/Buenos_Aires 19:10  

Departure: America/Argentina/Buenos_Aires 06:06  Mar 07, 2020
Arrival:   America/Toronto                14:43  

Departure: America/Toronto                04:48  Mar 08, 2020
Arrival:   Europe/London                  16:52  
```

Note that on the trip from Paris to Adelaide, your arrival is on a day after the departure. It's also possible to have an arrival at '-1 day' if you cross the date line and your timing is right.

* From London to Paris, the trip appears to take 1:59 hours but Paris is one hour ahead. The trip from London to Paris takes 59 minutes.
* From Paris to Adelaide, the trip appears to take 29:27 hours (note that we're arriving the next day). Adelaide is 9:30 hours ahead (note that Australia is enjoying daylight savings time in this season), so the trip takes 19:57 hours or 1197 minutes
* From Adelaide to Buenos Aires, we appear to arrive 44 minutes before we depart, but Buenos Aires is 13:30 hours behind Adelaide. So the travel time is 12:46 hours or 766 minutes.
* Toronto is actually 2 hours behind Buenos Aires. So our apparent trip of 8:37 hours actually takes 10:37 hours or 637 minutes.
* The return to London appears to take 12:04 hours, but London is 4 hours ahead. So the trip actually takes 8:04 hours or 484 minutes. Note that Toronto just entered daylight savings time in the night of March 8 2020.

The sum of travel time in minutes is then 3143 minutes, so `3143` would be the answer to the test-input.
