# This program classifies images based on 2 factors:
# percentage of the image that is bright (light leak)
# and the RMS of the RGB noise

import os
from pathlib import Path
from math import sqrt
from PIL import Image
from numpy import mean, std

class ImageClassifier:

    def __init__(self, filename, basepath):
        self.filename = filename
        self.basepath = basepath
        self.lthreshold = 60
        self.pthreshold = 0.05
        self.rthreshold = 10.0
        self.resolution = 10
        self.image = Image.open(self.basepath+self.filename)
        self.rms = 0.0
        self.percent = 0.0
        self.noisedata = []
    
    def set_resolution(self, res):
        self.resolution = res

    def set_LuminosityThreshold(self, thresh):
        self.lthreshold = thresh
    
    def set_PercentThreshold(self, thresh):
        self.pthreshold = thresh

    def set_RMSThreshold(self, thresh):
        self.rthreshold = thresh

    def makeNoiseData(self):
        if(self.image.mode != 'RGB'):
            self.image = self.image.convert('RGB')
        for x in range(0, self.image.size[0], self.resolution):
            for y in range(0, self.image.size[1], self.resolution):
                r, g, b = self.image.getpixel((x, y))
                self.noisedata.append([r, g, b])
    
    def getRMS(self):
        def total():
            self.makeNoiseData()
            data = self.noisedata
            rval = gval = bval = 0
            for coord in data:
                rval+=(coord[0] ** 2)
                gval+=(coord[1] ** 2)
                bval+=(coord[2] ** 2)
            length = len(data)
            return [rval, gval, bval, length]

        def rtmeansqrd(self):
            totals = total()
            rval = totals[0]
            gval = totals[1]
            bval = totals[2]
            length = 3 * totals[3]
            return(sqrt((rval+gval+bval) / length))

        RMS = rtmeansqrd(self)
        self.rms = RMS

    def getPercent(self):
        if(self.image.mode != 'L'):
            self.image = self.image.convert('L')
        countTHRESHOLD = 0
        count = 0
        for x in range(0, self.image.size[0], self.resolution):
            for y in range(0, self.image.size[1], self.resolution):
                p = self.image.getpixel((x, y))
                if (p > self.lthreshold):
                    countTHRESHOLD+=1
                    count+=1
                else:
                    count+=1
        percent = (countTHRESHOLD / count) * 100
        self.percent = percent

    def show(self):
        self.getRMS()
        self.getPercent()
        print()
        print(f"Image {self.filename}'s RMS is {self.rms} and percent is {self.percent}")
    
    def DetailedClassify(self):
        self.getRMS()
        self.getPercent()
        self.show()
        if(self.percent > 0.05):
            print(f"Image {self.filename} fails the percentage test")
        elif(self.percent <= 0.05):
            print(f"Image {self.filename} passes the percentage test")
        if(self.rms > 10.0):
            print(f"Image {self.filename} fails the RMS test")
        elif(self.rms <= 10.0):
            print(f"Image {self.filename} passes the RMS test")

    def classify(self):
        self.getRMS()
        self.getPercent()
        resultP = True
        resultR = True
        if(self.percent > 0.05):
            resultP = False
        elif(self.percent <= 0.05):
            resultP = True
        if(self.rms > self.rthreshold):
            resultR = False
        elif(self.rms <= self.rthreshold):
            resultR = True
        if(resultP and resultR):
            print(f"{self.filename} passes")
        elif((resultP and not resultR) or (resultR and not resultP)):
            print(f"{self.filename} is on the margin")
        elif(not resultP and not resultR):
            print(f"{self.filename} fails")


basepath = "/Users/julia/Desktop/Python/images"
folder = Path(basepath)
images = os.listdir(folder)

path = "/Users/julia/Desktop/Python/images/"

for image in images:
    if(not image.startswith(".DS")):
        im = ImageClassifier(image, path)
        #im.show()
        im.DetailedClassify()