# Calculator: Estimation time for laser cutting and 3D printing

## Estimated time for laser cutting with an svg file
### User inputs:
- svg file directory.
- material, possible: ["MDF", "Plywood", "Acrilic"], depending on the stock you have.
- material Thickness, possible options [2, 3, 4, 5, 6] mm, depending on the stock you have.

### Methodology:
- read svg file.
- use the svgpathtools to find the total length of every feature in the svg file,
 including line, polyline, polygon, rect, circle, ellipse, path.
- based on the user inputs and actual test cuts on the laser cutter a percentage of the max speed of the laser is chosen.
- add some preparation time for the technician to setup the laser cutter.


## Estimated time for 3d printing with as stl file
### User inputs:
- stl file directory, the stl file must be saved with ascii encoding and not binary. 
- print quality, possible options [1, 2, 3, 4, 5] with 1 being the worst quality and 5 the best quality. 
- infill percentage.
### Methodology:
- read stl file.
- calculate the volume of the mesh.
- calculate the volume that will be printed based on the infill percentage.
- determine the volume flow based on the print quality. (can be improved a lot by making some actual
 print tests and implementing somthing similar to the laser cutter).
- calculate the estimated time for printing by dividing the volume with the final volume flow.
- add some preparation time for the technician to setup the 3D printer.

#### Libraries used:
- [numpy]
- [svgpathtools]

### Installation
To run the code you need Python3, and the libraries above installed on your computer.
To install a libray for python open the command prompt and follow the example bellow.

```sh
$ pip install svgpathtools
```

To clone the repository, open the command prompt at the directory of choice and type:
```sh
$  git clone --recursive https://github.com/JustMakeItStudio/Estimate-time-of-laser-cutting-and-3D-printing
```

**Use this as you like**

[numpy]: <https://numpy.org/doc/>
[svgpathtools]: <https://github.com/mathandy/svgpathtools>
