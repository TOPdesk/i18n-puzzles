## --- Broken bits ---

You power on the server. But, oh no! One of the hard disks has failed!

Not all is lost however. The server uses multiple hard disks to have redundancy in case one of the drives fails. There are 3 disks in the server. They are configured in some kind of `RAID4`. That means it has 2 disks are used to store data and one disk that only saves a `parity bit`. This gives us a way to canculate the original state if one of the drives fails.

In this case the parity bit is derived from the other two disks using an exclusive or (XOR) operator. In a working system the bits on the disks would look like this:

```
Disk A  Disk B  Disk C (A XOR B)

1       1       0
0       1       1
1       1       0
1       0       1
1       0       1
0       1       1
...     ...     ...
```

So for example: `if A is 1 and C is 1, we know that B has to be 0`.

Only disk B is broken, so we have the original contents of disk A and the parity disk, disk C.
Use the contents of disk A and C to calculate the lost content of disk B. Then restart the server!

`How many bits are set to 1 on disk B?`
