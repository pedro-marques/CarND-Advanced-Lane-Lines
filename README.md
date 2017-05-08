## Advanced Lane Finding
[![Udacity - Self-Driving Car NanoDegree](https://s3.amazonaws.com/udacity-sdc/github/shield-carnd.svg)](http://www.udacity.com/drive)

## Writeup Pedro Marques

---

**Advanced Lane Finding Project**

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image1]: ./output_images/undistorted_chessboard.jpg "Undistorted Chessboard"
[image2]: ./output_images/undistorted_project_image.png "Undistorted Test Image"
[image3]: ./output_images/undistorted_and_warped.png "Road Transformed"
[image4]: ./output_images/combined_binary.png "Binary Example"
[image5]: ./output_images/undistorted_and_warped.png "Warp Example"
[image6]: ./output_images/sliding_window.png "Fit Visual"
[image7]: ./output_images/image3 "Output"
[video1]: ./project.mp4 "Video"

## [Rubric](https://review.udacity.com/#!/rubrics/571/view) Points

### Here I will consider the rubric points individually and describe how I addressed each point in my implementation.  

---

### Writeup / README

### Camera Calibration

#### 1. Briefly state how you computed the camera matrix and distortion coefficients. Provide an example of a distortion corrected calibration image.

The code for this step is contained in the lines 17 through 76 of the file called `lane_finding.py`.  

I start by preparing "object points", which will be the (x, y, z) coordinates of the chessboard corners in the world. Here I am assuming the chessboard is fixed on the (x, y) plane at z=0, such that the object points are the same for each calibration image.  Thus, `objp` is just a replicated array of coordinates, and `objpoints` will be appended with a copy of it every time I successfully detect all chessboard corners in a test image.  `imgpoints` will be appended with the (x, y) pixel position of each of the corners in the image plane with each successful chessboard detection.  

I then used the output `objpoints` and `imgpoints` to compute the camera calibration and distortion coefficients using the `cv2.calibrateCamera()` function.  I applied this distortion correction to the test image using the `cv2.undistort()` function and obtained this result:

![alt text][image1]

### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this one:
![alt text][image2]

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image (thresholding steps at lines 199 through 230 in `lane_finding.py`).  Here's an example of my output for this step.

![alt text][image4]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warp()`, which appears in lines 125 through 158 in the file `lane_finding.py`.

To perform the perspective transformation I have defined four source points on the image which represent my region of interest, the part of the image that I desire to have a birds-eye view, next I define four destination points in to which I am going to shift the region of interest to, these destination points have to represent a rectangle so that the lane lines are parallel.

The perspective transform matrix is computed by the function getPerspectiveTransform(), I have also computed the inverse matrix by swapping the source and destination points using the same function, so that I could unwarp the image should I need to do so.

Next I applied the transform matrix M to the original image to get the warped image by calling the warpPerspective() function, this function takes in the image, the perspective matrix M, the size we want the warped image to be, and how to interpolate points - fill in missing points as it warps an image.

The `warp()` function takes as input only an image (`img`). I chose the hardcode the source and destination points in the following manner:

```python
src = np.float32([[200./1280*w,720./720*h],
                [453./1280*w,547./720*h],
                [835./1280*w,547./720*h],
                [1100./1280*w,720./720*h]])
    dst = np.float32([[(w-x)/2.,h],
                    [(w-x)/2.,0.82*h],
                    [(w+x)/2.,0.82*h],
                    [(w+x)/2.,h]])
```

This resulted in the following source and destination points:

| Source        | Destination   |
|:-------------:|:-------------:|
| 200, 720      | 320, 720      |
| 453, 547      | 320, 590.4    |
| 835, 547      | 960, 590.4    |
| 1100, 720     | 960, 720      |

Here is an image of the original and the transformed images.

![alt text][image3]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

To identify the lane-line pixels the approach taken was to convert the undistorted image to the HLS and LAB color spaces, then apply a threshold to the L channel of the HLS color space and a threshold to the B channel of the LAB color space, then I combined those two thresholds into one binary image.

Next step was to take an histogram of the bottom half of the binary image, on it I would then search for the spikes on the left and right halves of the histogram, those spikes would represent the starting points for the left and right lane-lines respectively.

I have used the sliding window method to find the lane line pixels. The method consists in defining a number of windows, and using the starting points identified previously draw a window fitting the points inside it. On that window I find all the nonzero pixels in x and y, and I repeat that process moving each window upwards, and to adjust on the x axis (because the lines may curve) I verify if the number of pixels found on the left or right line are higher than a certain number of pixels (50 in this case), if so then I recenter the next window on the mean position of the number of pixels. Next I fit my lane lines with a 2nd order polynomial and I practically have my lane.

You can find the code in lines 233 through 317 in `lane_finding.py`.


#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in lines 372 through 407 in my code in `lane_finding.py`.

First off I found the x and y points for the left and right lines of the lane on the current frame and converted them to their equivalent in meters. Then I fit a second order polynomial like on the sliding window search but this time using the real world values.

To calculate the position of the vehicle with respect to the center I assumed that the car was in the center of the image, then I find the middle point between the left and right lines of the lane, that point is the middle of the lane, next I subtract the vehicle's position to the middle of the lane and voilá, I have the offset (how much the car deviates to the left or right depending whether the value is negative or positive).   

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines 409 through 432 in my code in `lane_finding.py` in the function `draw_detected_lane_lines()`.  Here is an example of my result on a test image:

![alt text][image7]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

I am really sad I did not manage to implement the Line class on my project, I did try to do it but I just could not get it to work, as a result my pipeline fails on the two challenge videos, where there is a lot more noise on the thresholded images (shadows and such).

I think color, gradient thresholding and the perspective transformation are crucial for the success of this project, I did not feel the effect of the undistort method on these test images, but I get why we do it, it's good to do it as rule because in case we get images that need to be undistorted we already know how to do it and that we should do it.

As I could not implement the Line class I was left wondering, the same color and gradient thresholding combination does not work well for all occasions and other combinations work better for certain images, so maybe having the pipeline switch between color and gradient thresholding combinations depending on the number of spikes the histogram has could be an idea, I have not tried it really.
