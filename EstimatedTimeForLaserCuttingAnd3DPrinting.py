from svgpathtools import svg2paths
import numpy

# Estimated time for laser cutting with an svg file

# User inputs for Laser cutting estimation time:
# -svg file directory.
# -material, possible: ["MDF", "Plywood", "Acrilic"], depending on the stock you have.
# -material Thickness, possible options [2, 3, 4, 5, 6] mm, depending on the stock you have.

# Methodology:
# -read svg file.
# -use the svgpathtools to find the total length of every feature in the svg file,
#  including line, polyline, polygon, rect, circle, ellipse, path.
# -based on the user inputs and actual test cuts on the laser cutter a percentage of the max speed of the laser is chosen.
# -add some preparation time for the technician to setup the laser cutter.

def getTotalLengthOfSVG(SVGDirectory: str):
    totalLengthPaths = 0
    paths, _ = svg2paths(SVGDirectory) # _ is a way to show that that variable is not used
    for path in paths:
        totalLengthPaths += path.length()
    return totalLengthPaths / 2.8346

def getSpeedOfLaser(material: str, thickness: float):
    # These values must be derived from testing the laser cutter you have.
    # Returns a value from 0 to 1, the percantage of the max speed of the laser cutter.
    if material == "MDF":
        if thickness == 2:
            return 0.3
        if thickness == 3:
            return 0.25
        if thickness == 4:
            return 0.2
        if thickness == 5:
            return 0.15
        if thickness == 6:
            return 0.1
    if material == "Plywood":
        if thickness == 2:
            return 0.35
        if thickness == 3:
            return 0.3
        if thickness == 4:
            return 0.25
        if thickness == 5:
            return 0.2
        if thickness == 6:
            return 0.15
    if material == "Acrilic":
        if thickness == 2:
            return 0.25
        if thickness == 3:
            return 0.20
        if thickness == 4:
            return 0.15
        if thickness == 5:
            return 0.1
        if thickness == 6:
            return 0.05
    return None
        
def calculateEstimatedTimeForLaserCutting(SVGDirectory: str, material: str, materialThickness: int):
    maxSpeedOfLaser = 1 # m/s, depending on the laser cutter you have
    preparationOfTheFileTime = 15 # minutes, change as you see fit
    preparationOfLaserTime = 15 # mintutes, change as you see fit
    speedPercentage = getSpeedOfLaser(material, materialThickness)
    totalLengthWithPaths = getTotalLengthOfSVG(SVGDirectory)
    return round(totalLengthWithPaths * maxSpeedOfLaser * speedPercentage / 60 + preparationOfTheFileTime + preparationOfLaserTime)

print("Laser cutting from SVG file - Estimated time: ",calculateEstimatedTimeForLaserCutting("Downloads/test.svg", "MDF", 2) , " minutes.")


##############################################################################################################

# Estimated time for 3d printing with as stl file

# User inputs for 3D printing estimation time:
# -stl file directory, the stl file must be saved with ascii check box selected and not binary. 
# -print quality, possible options [1, 2, 3, 4, 5] with 1 being the worst quality and 5 the best quality. 
# -infill percentage.

# Methodology:
# -read stl file.
# -calculate the volume of the mesh.
# -calculate the volume that will be printed based on the infill percentage.
# -determine the volume flow based on the print quality. (can be improved a lot by making some actual
#  print tests and implementing somthing similar to the laser cutter).
# -calculate the estimated time for printing by dividing the volume with the final volume flow.
# -add some preparation time for the technician to setup the 3D printer.


def calculateVolumeOf3Ponts(p1, p2, p3):
    # The three points in 3D space that form one triangle
    # p1 = (x1, y1, z1)
    # p2 = (x2, y2, z2)
    # p3 = (x3, y3, z3)
    return 1/6 * numpy.dot(numpy.cross(p1, p2), p3)

def findVertex(indexToSartSearchingFrom: int, STLfile: str):
    i = indexToSartSearchingFrom
    while True:
        if STLfile[i:i+6] == "vertex":
            return i
        i += 1
        if i >= len(STLfile)-1:
            return None 

def convertVertexToFloats(indexToSartSearchingFrom: int, STLfile: str):
    i = indexToSartSearchingFrom
    numberOfVariablesFound = 0
    xFound = False
    yFound = False
    zFound = False
    while numberOfVariablesFound < 3 and i < len(STLfile):
        if STLfile[i:i+1] == " ":
            if xFound == False:
                xStartIndex = i + 1
                i += 1
                numberOfVariablesFound += 0.5
                while i < len(STLfile):
                    if STLfile[i:i+1] == " ":
                        xEndIndex = i
                        numberOfVariablesFound += 0.5
                        xFound = True
                        break
                    i += 1
            if yFound == False:
                yStartIndex = i + 1
                i += 1
                numberOfVariablesFound += 0.5
                while i < len(STLfile):
                    if STLfile[i:i+1] == " ":
                        yEndIndex = i
                        numberOfVariablesFound += 0.5
                        yFound = True
                        break
                    i += 1
            if zFound == False:
                zStartIndex = i + 1
                i += 1
                numberOfVariablesFound += 0.5
                while i < len(STLfile):
                    if STLfile[i:i+1] == " ":
                        zEndIndex = i
                        numberOfVariablesFound += 0.5
                        zFound = True
                        break
                    i += 1
        i += 1
    if numberOfVariablesFound == 3:
        return (float(STLfile[xStartIndex:xEndIndex]), float(STLfile[yStartIndex:yEndIndex]), float(STLfile[zStartIndex:zEndIndex]))
    else:
        return 0    

def getTotalVolumeOfSTLfile(STLDirectory: str):
    with open(file=STLDirectory, mode="r") as f:
        file = f.read()
    totalVolume = 0
    i = 0
    vertex = []
    while i < len(file):
        iTemp = findVertex(i, file)
        if iTemp is not None:
            i = iTemp
            vertex.append(convertVertexToFloats(i, file))
            if len(vertex) % 3 == 0:
                totalVolume += calculateVolumeOf3Ponts(vertex[-3], vertex[-2], vertex[-1])
        else:
            break
        i += 1
    return totalVolume

def calculateEstimatedTimeFor3DPrinting(STLDirectory: str, printQuality: int, infillPercentage: int):
    # infillPercentage is in percentage form so 0 is 0% and 100 is 100%.
    # printQuality possible options [1, 2, 3, 4, 5] with 1 being the worst quality and 5 the best quality.
    maxVolumeFlowOf3DPrinter = 1 # m**3/s, depending on the 3D pinter you have
    preparationOfTheFileTime = 15 # minutes, change as you see fit
    preparationOf3DPrinterTime = 15 # mintutes, change as you see fit
    postProcessingOf3DPrinterTime = 10 # minutes
    totalVolume = getTotalVolumeOfSTLfile(STLDirectory)
    volumeThatWillBePrinted = totalVolume * infillPercentage / 100
    actualVolumeFlow = maxVolumeFlowOf3DPrinter / printQuality
    estimatedTimeFor3DPrinter = volumeThatWillBePrinted / actualVolumeFlow / 60 # in minutes
    return round(estimatedTimeFor3DPrinter + preparationOfTheFileTime + preparationOf3DPrinterTime + postProcessingOf3DPrinterTime)

print("3D Print from STL - Estimated time: ",calculateEstimatedTimeFor3DPrinting("Downloads/test2.stl", 5, 50) , " minutes.")
