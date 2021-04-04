# Tamagotchi

The idea of the game is an interactive observation of the life of 
a pet. You can feed your pet, play with it, and monitor its health. 
It repeats the interaction with a real living being.

### Goal of the game
Your pet wins if its __satiety__ and __health__ 
simultaneously reach the 100 mark. If at least one of 
these parameters drops to 0, then your pet dies.

### Description of actions

- When you click on the __feed__ button, the pet's __satiety__ 
  increases by 10. 


- When you click on the __train__ button, __satiety__ decreases by 10, 
  and __health__ increases by 10, only if it was originally 
  less than 50, otherwise it decreases by 15.


- When you click on the __heal__ button, __satiety__ also decreases 
  by 10, and __health__ increases by 15 only if it was initially 
  below 50, otherwise it decreases by 20.

