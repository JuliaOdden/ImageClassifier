# ImageClassifier
ImageClassifier sorts images into pass/fail/margin based on 2 factors: percentage of the image that is brighter than a certain threshold and the RMS of the RGB noise.

## Dependencies
```python
import os
from pathlib import Path
from math import sqrt
from PIL import Image
from numpy import mean, std
```

## Functionalities
### Constructor
`ImageClassifier(str: filename, str: basepath)`

`filename` refers to the name of an individual file (e.g. `"fail3.png"`)

`basepath` is the directory up to the point of the filename (e.g. `"/Users/julia/Desktop/Python/TestImages/"`)

The sections are divided so that if you want, you can have the `ImageClassifier()` work on every file in a directory, as shown below.

#### Use
```python
path = "/Users/julia/Desktop/Python/TestImages"
folder = Path(path)
images = os.listdir(folder) # creates a list of filenames

basepath = "/Users/julia/Desktop/Python/TestImages/"

for imagefilename in images:
    if(not image.startswith(".DS")):
        im = ImageClassifier(imagefilename, path)
        #im.show()
        #im.classify()
        #im.DetailedClassify()
```
### Functions
`ImageClassifer.set_resolution(int: resolution) -> None` 

The percentage and RMS calculations are made by measuring each individual pixel in an image; this is immensely slow unless we change the resolution so it only samples one in every "x" number of pixels. `set_resolution` sets that "x" to a given integer. The default is 10.

`ImageClassifier.set_LuminosityThreshold(int: threshold) -> None`

The percentage calculation works by assessing the luminosity of each pixel in the image and comparing it to a given luminosity threshold. The default is 60 (out of 255), but this function lets you change it easily.

`ImageClassifier.set_PercentThreshold(int: threshold) -> None`

The percentage calculation is done to determine whether too much of an image is light to be safe; that line between passing and failing can be set here (the default is 0.05%).

`ImageClassifier.set_RMSThreshold(int: threshold) -> None`

The RMS test works by calculating the R, G, and B noise in each image at a predefined resolution and comparing the RMS of all the noise in the image to a predetermined threshold. The default is 10.0, and you can custom set it with this function.

`ImageClassifier.show() -> None`

Neatly prints the RMS and percentage values for an image.

`ImageClassifier.DetailedClassify() -> None`

Prints the pass/fail results for both the RMS and percentage tests.

`ImageClassifier.classify() -> None`

Simply returns the image name with "pass," "fail," or "on the margin." If an image passes both the RMS and percentage tests, it passes; if it passes one but not the other, it's on the margin; if it fails both, it fails.

### Hidden Functions
`ImageClassifier.makeNoiseData() -> None`

Fills a list with a sublist for each pixel of the image containing the r value, the g value, and the b value of the pixel. Called in `getRMS()`.

`ImageClassifier.getRMS() -> None`

This function (with several helper functions to break down the math) reads in the list generated by `makeNoiseData()`, sums the r, g, and b values, squares each sum, divides that sum by three times the length of the list, then takes the square root of the whole thing (i.e. performs a basic RMS calculation on three numbers to get a convenient quantifier for noise in the image). 

`ImageClassifier.getPercent() -> None`

This is the helper function that gets the percent of the pixels in the image with above-threshold luminosity values.

## Outputs

### With `ImageClassifier.show()`

`Image pass1.PNG's RMS is 8.521676584313003 and percent is 0.0`

### With `ImageClassifier.classify()`

`pass1.PNG passes`

### With `ImageClassifier.DetailedClassify()`

`Image pass1.PNG's RMS is 7.448588856526148 and percent is 0.0`

`Image pass1.PNG passes the percentage test`

`Image pass1.PNG passes the RMS test`
