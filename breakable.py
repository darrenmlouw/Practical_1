# An agent which plays randomly without repeated the objects it plays until a specific
#  sequence is played by its opponent.  The agent then repeats the last object it played a
#  random number of times before resuming its normal sequence.
#
# Uses ideas from information in agents submitted to http://www.rpscontest.com
# Written by: W. P. du Plessis
# Last update: 2019-02-07


import random

if input == "":

    # The range of possible lengths of the break sequence.
    break_min = 2
    break_max = 5
    # The maximum number of repeats when repeating.
    repeat_max = 10

    ## This line allows repeatable results.
    #random.seed(0)

    # The length of the break sequence is break_min to break_max objects.
    length = random.randint(break_min, break_max)

    # Generate the random break sequence.
    sequence = [ "X" ]*length
    for counter in range(length):
        sequence[counter] = random.choice(["R", "P", "S"])

    # Initialise the history.
    # Use "X" as the initial value because it does not match any of the objects.
    history = [ "X" ]*length

    # Initialise the variable for the number of repeats.
    repeat = 0

    # Play randomly for the first move.
    previous = random.choice(["R", "P", "S"])
    #print(previous)

else:

    # Update the history.
    history.pop(0)
    history.append(input)

    # Initialise the repeat counter if the opponent's last objects match the break sequence.
    if history == sequence:
        repeat = random.randint(length, repeat_max)

        
# If the bot has entered a repeat cycle.
if repeat > 0:

    # Reduce the repeat counter because a repeat will now take place.
    repeat -= 1

    # The history needs to be reset to ensure that repeats cannot be continuously triggered.
    history = [ "X" ]*length

else:

    # Play randomly while storing the value played and without repeating a move.
    if previous == "R":
        previous = random.choice(["P", "S"])
    elif previous == "P":
        previous = random.choice(["R", "S"])
    else:
        previous = random.choice(["R", "P"])

output = previous
