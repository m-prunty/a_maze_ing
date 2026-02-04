
## Fix
- ~~wall graphic~~

## Add
- ([x]) ~~ make~~
- ([x]) ~~42 grid element~~
- ([x]) ~~Colors with differents assets~~
- ([]) Keyhooks and event handelin
- ([]) Start screen
- ([x]) ~~File output~~
- ([]) Other mazegen 
- ([x]) ~~Seeding~~
- ([]) Path finding
- ([]) Character animation

 

## Clean
- all


##Notes:
SORRY: didnt save the note that was here^^^^
from memmory:
Start screen 
control flow
keyhooks


data vaildation is janky and incomplete  sorry, it should cover the basic cases and should not be too much of  a problem for now..
add some exceptions to what looks important to whatever youre working on and we'll come back and fix it later.

Seeding is super basic its just the number that you want your "Random" number to start at, 
from there it becomes 100% deterministic so always the same. For now, we'll use python random libs, I've added a line just before the generation start,
that seeds it to 42. If you want to do more and would like to explore RNG in general it could be a nice rabbit hole to build a basic random library.
Will be useful for some of the algo's

For now we need to focus on getting the control flow sorted and keyhooks .You take point here. Don't stress about breaking/adding stuff. 
After that we can switch over to pathfinding stuff and better algos

Basic config class is functioning, add any thing you need and pass it about,  if pytdantic complains add a `type | None = None` or something like that.
theres a couple of functions now for dumping and reloading, gridmap, config etc. I tried to keep them relativley isolated ie each one has basically one function. 
If you feel they'd work better elsewhere move em! The las method worked on is for reloading the generated maze files. Haven't tested fully yet but I think its getting overwritten on instantitaion of grid. 

HAve FUN amigo chat soon!!!!
