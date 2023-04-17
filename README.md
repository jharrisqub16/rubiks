# Computer Vision based solver for Rubik's Cube Robot
This is a python based Computer Vision project to operate Rubik's Cube solving robots.
Accompanying GUI included running on Electron JS with REACT JS integration.

Initial development in 2018 by David Ball and built upon in 2023 by Jake Harris.
In association with Queens University Belfast.

## Operation
This is a brief overview of some of the main points of the program flow, rather than an exhaustive explanation.

- The expected number of cameras or cube positions are set from the start. To minimise the overhead of creating and
  destroying the camera objects, these are all created at startup and contained in a list.

- Reading the cube consists of the following:
    + Using the coordinates from the 'correlation' mechanism, the input image is simplified to isolate the areas that
      are of interest. In other words, mask just the 'cubies' in the input image.
    + A representative colour value is taken from each cube region by iteratively masking the image again with small
      colour ranges. For each cubie region, the range which leads to the largest matched contour area is deemed to be
      the best match.
    + The 'correlation' mechanism is used to match the contours to a numerical position of the cube, based on the
      image coordinates of the contour.
    + The orientation of the cube is derived, based on the centre cubies of each face. **Note**: This step is irrelevant in
      cases where the orientation of the cube must be assumed. The orientation is essentially set in the code and must
      be adhered to when inserting the cube into the robot.
    + The 'actual' colour of each contour is derived. This is done by grouping the colours into 6 groups,
      assuming that there will be 6 distinct colours on the cube. **Note**: It is also assumed that white will have the lowest
      Satuation value.
    + These groups are then matched to 6 known 'template' colour values by the permuation of the 6 groups which has the
      lowest sum of deviations.
    + Hence, the colour letter (ie RGBYOW) of each cubie is derived, along with the position number to which it
      corresponds. This is used to build up the expected cube state representation in Singmaster style notation (ie
      RLUDBF) based on the orientation of the cube.

- Once the cube state has been derived, it is passed to the solver object which uses a library implementation of the
  Kociemba algorithm to find a solution.

- Finally, the solution is passed to the motor controller object to perform the moves. This object is meant to be
  abstracted and simply takes the move sequence and 'does the needful'. The specific operations of this can vary based
  on the hardware implementation of each robot.

- Assuming the hardware is set up as expected, simply run the base.py script (from any directory):

e.g `./base.py` or `python2.7 base.py` (or other correct path)


                                  GUI INSTALLATION/STARTUP
===========================================================================================================================
In order to successfully run and execute the new GUI build within electron you must follow these steps.
1. Navigate to the app folder 
```cd app```
2. Navigate to the cuber-electron folder
```cd cuber-electron```
3. Run yarn install
```yarn install```
This may take a while depending if it's your first time starting up
4. Run yarn electron-serve
```yarn electron-serve```
This will start up the React app in the Electron JS envioronment and run the new application! 

Note: Due to timing functionality with the buttons is not currently present however script files in the repository show OpenCV integration 
      and basic Javascript tutorials/functions will allow you to map the current operations in the python based code to this new application.
Good Luck! 


## Structure
```
+-- arduinoMotorControl     (Source code for separate Arduino motor controller implementation)
+-- scripts                 (Misc helper/temporary scripts)
+-- src
|   +-- base.py             (Main GUI launcher for basic functionality)
|   +-- calibrate.py        (Secondary settings GUI window for live camera view and changing parameters)
|   +-- cfg                 (Contains persistent configuration for CV parameters)
|   +-- images              (Contains any other images or displays which are required for GUI)
|   +-- cuber
|       +-- cuber.py            (API container object for all solving related operations)
|       +-- computerVision.py   (Object for CV functionality)
|       +-- correlation.py      (Helper to computerVision - Default coordinate correlation settings)
|       +-- solver.py           (Object for all solving and metric calculation)
|       +-- motorController.py  (Object for interfacing with motors)
+-- app
|   +-- cuber-electron
|       +-- public (Electron associated files)
|       +-- src    (React App associated files)

```

## Known Issues
- **Lighting Conditions** - Some specific lighting conditions (namely overhead) cause reflections off the cube which
  eliminate all colour fidelity. In the most severe cases, these cannot be compensated for by computer vision
  processing.

- **Select timeout** - Decoding the webcam video stream is done by the 'uvcvideo' kernel driver module. In *some*
  environments (but seemingly not all), this module will fail with 'Select timeout' output and totally crash the system.
  The issue seems to occur more readily with multiple cameras and at higher resolutions.  This is relatively widely
  discussed on OpenCV forums with a range of potential solutions suggested but to no avail.

- **Camera Indexing Errors** - some featues of the software may be arise faults this is due ot the changes introduced
  in the updates to the Raspberry Pi Raspbian to Raspberry Pi OS. The latest issue found was problems with the calibration
  screen in that values for certain angles would get mixed upon saving. Something to investigate if time avails otherwise
  calibration is required upon every restart.

## TODOs
- **Exception handling** - The ways in which errors are handled is not well sanitised. A top-to-bottom exception
  handling scheme would be useful. This could include startup scenarios such as ensuring that the expected number of
  cameras are operational, motor operation can be established etc.


- **Rendered cube model** - The 'main' GUI window is simply an image with buttons. It had been thought that this window
  could present a 3D rendered model of the 'live' state of the cube which would be intuitively manipulated by the user.

- **explore react/electron libraries** - the new GUI stored in the cuber-electron folder is a sandbox waiting to be 
  played with. There are a vast amount of libraries available to which can be used at your disposal, including various
  Rubik's cube modelling libraries which would help tackle the Rendered Cube Model todo! 
