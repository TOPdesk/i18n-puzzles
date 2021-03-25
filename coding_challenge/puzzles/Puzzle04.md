## --- I come bearing gifts ---

This year, with the working-from-home situation we have been unable to have our borrels (having a drink on Friday afternoon). To make up for this a little bit, we are getting our people in the European offices some gifts. Let's drive to the offices and deliver some nice goodies. We want to be efficient about it and find the `shortest traveling distance`. We can start and end at any location. Every location needs to be visited once.

For example we have the following distances:
```
Delft to Budapest = 1420
Delft to Kaiserslautern = 497
Budapest to Kaiserslautern = 1031
```

Possible routes are:
```
Delft -> Budapest -> Kaiserslautern = 2451
Delft -> Kaiserslautern -> Budapest = 1528
Budapest -> Delft -> Kaiserslautern = 1917
Budapest -> Kaiserslautern -> Delft = 1528
Kaiserslautern -> Budapest -> Delft = 2451
Kaiserslautern -> Delft -> Budapest = 1917
```

The shortest of these is `Delft -> Kaiserslautern -> Budapest`, so the answer is 1528 in this example.

What `distance is the shortest route` that goes by all cities once?
