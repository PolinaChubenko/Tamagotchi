# Tamagotchi

The idea of the game is an interactive observation of the life of 
a pet. You can feed your pet, play with it, and monitor its health. 
It repeats the interaction with a real living being.

### Goal of the game
The task of your pet is to earn as much money as possible. 
You need to take into account two facts. Firstly, the __satiety__
and __health__ of your pet can not be higher than 100. Secondly, if
at least one of these parameters drops to 0, then your pet dies. 

> Note: Do not bring your pet to a deep existential crisis 
> (__happiness__ is less than 0), otherwise your pet 
> will refuse to go to work.

### Description of actions

- When you click on the __feed__ button, the pet's __satiety__ 
  increases by 10. 


- When you click on the __train__ button, __satiety__ decreases by 10, 
  and __health__ increases by 10, only if it was originally 
  less than 50, otherwise it decreases by 15.


- When you click on the __heal__ button, __satiety__ also decreases 
  by 10, __happiness__ decreases by 5, 
  and __health__ increases by 15 only if it was initially 
  below 50, otherwise it decreases by 20.


- When you click on the __play__ button, __satiety__ also decreases
  by 15, and __happiness__ increases by 15.


- When you click on the __work__ button, __all the params__ decreases
  by 10, but your pet earns money. With each subsequent click, your 
  Tamagotchi earns 1 unit more money than the last time.
  
### Additional features

Instead of tapping on the buttons on the screen, you can 
control your Tamagotchi using the keyboard:

- key A = feed
- key S = train
- key D = heal
- key K = play
- key L = work
- ENTER = start / restart
- ESC = quit the game
