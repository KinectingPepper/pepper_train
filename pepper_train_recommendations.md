# Pepper train future development recommendations

## Combinator

The combinator works in the way it's supposed to. 

It could be improved by using pandas for concattinating and adding the pnum & enum collumns though, since this uses just the python csv reader and writers currently.

## Remove skeletons

No need to change this

## Exercise cutting

Would recommend to replace this completely. The current code(in data_extraction) is unreadable and buggy. Ends up having to skip a lot of people. Especially people with non-standard movements, which is the most valuable data.

Make up a statistical way to work on this, with the scipy and numpy libraries. Don't make your own csv reader/ writer. Don't make you own time interpreters.

Probably use median filter for smoothing out the input signals. find_peaks_cwt in scipy is an interesting function that could be useful.
## Rotating

No need to replace this. Few people get skipped in this step and the results are as expected. The code is good and readable. 

I would only recommend finding out a way to remove the float typecastings. These shouldn't be necesarry but currently they are.

## Calculate angels.

Same as above.

# General ideas.

## Spark-ify

Sparkify this to paralelize the operations. This is not as simple as it sounds because of limitations of spark where you cannot do a map inside a map.

Also this would require making prepared functions out of many current functions.

## Cut on the output of the angles

Currently it's mostly cutting based on the y-coordinate various skeleton-nodes.

After this it does rotation and calculating angles.

I would highly recommend doing rotating and calculating the angles first and then cutting based on this data. The definition if an exercise is the change in the angle, not the y-coordinate of a joint. 

Doing this would simplify recognition and cutting of movements.