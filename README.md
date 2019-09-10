Luke Fahmy
A13849289

CSE 190 - Final Project- Predicting Trajectory of a Basketball

How to use:
1. Download file called trajectory.py
2. Type "python trajectory.py" in cl when, you're in the correct directory
3. You will be prompted for the file. Make sure it has the extension in the name
4. Four new videos will be created in the same dir as the file

Input file best practices:
1. I have not tested on anything other than .mp4, so try to use that
2. I've also only used a Mac with ffmpeg
3. Make sure the file starts right before the shooter shoots (so no dribbling etc 
beforehand)
4. Try to have little or no other balls in the frame
5. Try to have little or no camera movement
6. Try to show as much of the trajectory as possible
7. Try to have as little background noise as possible

System specifications:
1. I have only test this with Python 3.6, using OpenCv 3.4, on a Mac with OS X El Capitan
10.11.6 with ffmpeg.
2. There is a lot of room for clashes between systems, so I will leave a few examples
for those who want to see it in action, but can't get it to work.
3. If you're having problems even producing the 4 video files, and you want to try
and fix it, you're welcome to edit the source code. I would recommend starting at the very
bottom with the ffmpeg commands.

End result:
1. In the end, your directory will contain 5 video files, 4 of which are program output, 1 
of which you provided yourself.
2. The 4 provided by the program will be called:"back.mp4", "back_inv.mp4", "circles.mp4",
and "predicted.mp4". This is the order they are made and the way the program works.
3. "predicted.mp4" is the end result and the point of the whole program, so if you don't
care how it works, you can go there.

Output file descriptions:
1. "back.mp4": is the result of background subtraction to find the ball easier
2. "back_inv.mp4": is the inverse of "back.mp4" because it's easier to detect black blobs
than white blobs
3. "circles.mp4": is the original video with the circles tracking the ball
4. "predicted.mp4": is the original video with green dots for where the ball has been
mapped, and red dots showing the entire predicted trajectory
