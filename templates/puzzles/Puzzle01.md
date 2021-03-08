## --- Working from home ---

We need some help over here!

We just had a power outage and our server for working remotely has been powered off! Timing couldn't be worse. Our entire office is working from home and our IT server guy has booked a vacation to sunny Barbados. We need to find the server and power it on!

First we need to find the machine. Not as easy as you'd hope. Our servers have been arranged in a very peculiar way and only server guy understands how the layout works. Luckily he left you instructions on where to find the remote server. Unluckily, he's a rather eccentric guy and has left rather eccentric instructions.

His system is based on a grid position relative to the server in the middle of the data center. `n, s, w, e` for north, south, west and east. This wil give you the coordinates of our remote working server.

For example:

- `ne` results in `(1, 1)`
- `sw` results in `(-1, -1)`   
- `nn` and `nnnnssew` both result in `(0, 2)`
- `eew` and `ewe` both result in `(1, 0)`
- `nsnnwweee` and `nwsewnene` both result in `(1, 2)`

What are the `coordinates of the remote server`?
