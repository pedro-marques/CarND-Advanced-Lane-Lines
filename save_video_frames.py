import cv2
file_name = 'harder_challenge_video'
destination_folder = 'frames/'
vidcap = cv2.VideoCapture(file_name+'.mp4')
total_jump_miliseconds = 0
jump_miliseconds = 2000 #  jump every 1 seconds
#vidcap.set(cv2.CAP_PROP_POS_MSEC,20000) # start at 20s
success,image = vidcap.read()
count = 0
success = True
while success:
    vidcap.set(cv2.CAP_PROP_POS_MSEC,total_jump_miliseconds)
    success,image = vidcap.read()
    print('Read a new frame: ', success)
    cv2.imwrite(destination_folder+file_name+"_frame%d.jpg" % count, image)     # save frame as JPEG file
    count += 1
    total_jump_miliseconds = total_jump_miliseconds + jump_miliseconds
