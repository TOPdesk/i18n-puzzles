# Don't step in it...

It's a pleasant day for a walk in the park. The park in our neighborhood is lush and lovely. There are trees, flowers, and even some rabbits live here. Many people come here to walk their dog. Unfortuntaly, the owners don't always clean up after their pets. It's nearly impossible to walk through this park without stepping in a pile of poo.

You walk through the dog park in a diagonal line, going 1 down and 2 right with each step. The way the local geometry works is a bit weird (probably due to the nearby gravitational wave research station), so when you reach the right side of the park, you wrap around to the left side. 

In the following `test-input`, the park is 7 units wide and 13 units high. Note that even with monospace fonts, emojis may appear wider than regular characters. Depending on the font used, the park may appear to have a jagged edges. When expressed as unicode code points however, it is perfectly rectangular.

```
 ⚘   ⚘ 
  ⸫   ⸫
    💩  
     ⸫⸫
 🐇    💩
⸫    ⸫ 
⚘🌲 ⸫  🌲
⸫    🐕 
  ⚘  ⸫ 
⚘⸫⸫   ⸫
  ⚘⸫   
 💩  ⸫  
     ⸫⸫
```

You walk from the top-left corner all the way to the bottom, stepping 1 down and 2 right each time, wrapping around the edge. This means you follow this pattern:

```
x      
  x    
    x  
      x
 x     
   x   
     x 
x      
  x    
    x  
      x
 x     
   x   
```

Consequently, on your walk you would step in it twice: on the 3rd and 12th rows. The solution to the test-input is `2`.

Your real `input` is a similar rectangular park, only much larger. If you walk in the same pattern, how many times do you step in a pile of poo?
