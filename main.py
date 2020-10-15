''' ########################################################################
 ''
 '' File....:	main.py
 '' Function:	Converts DJI Videos and .SRT-logs to 
 ''             images and annotation (xml) files in PASCAL VOC format
 '' Author..:	Alexander Leipnitz
 '' Date....:	05.08.2019
 ''
 ######################################################################### '''

import argparse
import cv2
import os
import xml.etree.cElementTree as ET
from xml.dom import minidom
import create_xml as create_xml #import create_xml.py

#------------------------------------------------------------------
 # main()
 #
 # Open Videos, extract frames, read srt-files and write results
#------------------------------------------------------------------
def main(args):
    # list all subfolders
    dirlist = os.listdir(args.base_path_input)
    print('directory list: ', dirlist)
    # Loop over all folders
    #for i in range(len(dirlist)):
        # Remove everything that is not a folder from the list
        #if os.path.isdir(dirlist[i]) == False:
        #    dirlist.remove(dirlist[i])
        #print('updated directory list: ', dirlist)

    # Loop over all folders
    for i in range(len(dirlist)):
        inputdir = os.path.join(args.base_path_input, dirlist[i])

        filelist = os.listdir(inputdir)
        print('filelist: ', filelist)

        # search for video files in the folder
        for file in range(len(filelist)):
            # DJI MAVIC2 Enterprise uses caps-lock extension-notation
            if os.path.splitext(filelist[file])[1] == ".MP4":
                srt_file_name = filelist[file].replace(".MP4", ".SRT")

            elif os.path.splitext(filelist[file])[1] == ".mp4":
                srt_file_name = filelist[file].replace(".mp4", ".SRT")
            else:
                print("Skipping non-video-file") #if not video found
                continue

            print(dirlist[i] + '/' + filelist[file])
            cap = cv2.VideoCapture(os.path.join(inputdir, filelist[file])) # playing video from file

            currentFrame = 0
            sec_counter = 0

            srt_file = open(os.path.join(inputdir, srt_file_name), "r")
            line_cam = srt_file.readlines()[4] #This line indicates the drone-video type
            line_cam = line_cam.replace('\n', '').replace('\r', '') #suppress linebreak
            print(line_cam)
            # extract relevant line to distinguish between different drone log (srt) files
            value_liste_cam = line_cam.replace(':', ' ').replace('[', ' ').replace(']', ' ').replace(':', ' ').split()
            print(value_liste_cam)

            # DJI MAVIC Pro
            if value_liste_cam[0] == "ISO":
                video_type = "DJI_MAVIC"

            # DJI MAVIC2 Enterprise
            elif value_liste_cam[0] == "iso":
                video_type = "DJI_MAVIC2"
                image_path = os.path.join(args.base_path_output, 'imgs', dirlist[i], os.path.splitext(srt_file_name)[0])
                image_path = image_path.replace("DJI_", "")

            # DJI MAVIC2 Enterprise Thermal Camera
            elif value_liste_cam[0] == "color_md":
                video_type = "DJI_MAVIC2_THERMAL"

            print(video_type)
            # Set output path
            if video_type == "DJI_MAVIC" or video_type == "DJI_MAVIC2":
                image_path = os.path.join(args.base_path_output, 'imgs', dirlist[i], os.path.splitext(srt_file_name)[0])
                annotation_path = os.path.join(args.base_path_output, 'annotations', dirlist[i], os.path.splitext(srt_file_name)[0])
            else:
                image_path = os.path.join(args.base_path_output, 'imgs_thermal', dirlist[i], os.path.splitext(srt_file_name)[0])
                annotation_path = os.path.join(args.base_path_output, 'annotations_thermal', dirlist[i], os.path.splitext(srt_file_name)[0])
           
            image_path = image_path.replace("DJI_", "")
            annotation_path = annotation_path.replace("DJI_", "")

            # create image folder
            try:
                if not os.path.exists(image_path):
                    os.makedirs(image_path)
            except OSError:
                print('Error: Creating directory for images')
            # create annotation folder
            try:
                if not os.path.exists(annotation_path):
                    os.makedirs(annotation_path)
            except OSError:
                print('Error: Creating directory for annotations')

            while (True):
                # Capture frame-by-frame
                ret, frame = cap.read()
                if not ret: break
                # image_name example: 20190407_0021_0000.jpg (foldername_videoname_frame)
                image_name = dirlist[i] + filelist[file] + '_'
                new_image_name = image_name.replace(".mp4", "").replace(".MP4", "")
                end_image_name = new_image_name.replace("DJI", "")
                final_image_name = end_image_name + "{0:05d}.jpg".format(currentFrame)
                
                height, width, depth = frame.shape # extract metadata from image

                srt_file = open(os.path.join(inputdir, srt_file_name), "r")
                srt_lines = srt_file.readlines()
                num_lines = sum(1 for line in srt_lines)
                #num_lines = sum(1 for line in open(os.path.join(inputdir, srt_file_name), "r"))
                srt_value = num_lines / 6
                
                if video_type == "DJI_MAVIC":
                    # Mavic: Line every 29 frames
                    if float(currentFrame/29).is_integer() and sec_counter < srt_value:
                        #print(sec_counter)
                        line_drone = srt_lines[sec_counter * 6 + 3] # get drone-value line
                        line_drone = line_drone.replace('\n', '').replace('\r', '') # suppress linebreak
                        line_cam = srt_lines[sec_counter * 6 + 4] # get camera-value line
                        line_cam = line_cam.replace('\n', '').replace('\r', '') # suppress linebreak
                        # Extract values from lines (remove unnecessary characters)
                        value_list_cam = line_cam.replace(':', ' ').split()
                        value_list_drone = line_drone.replace('(', ' ').replace(')', ' ').replace(',', ' ').replace(':', ' ').split()

                        sec_counter += 1

                elif video_type == "DJI_MAVIC2" or video_type == "DJI_MAVIC2_THERMAL":
                    # Mavic2: Line for each frame                   
                    if srt_value > currentFrame:
                        line_cam = srt_lines[currentFrame * 6 + 4] # get camera-value line
                        line_cam = line_cam.replace('\n', '').replace('\r', '') # suppress linebreak
                        # Extract values from lines (remove unnecessary characters)
                        value_list_cam = line_cam.replace(':', ' ').replace('[', ' ').replace(']', ' ').replace('1/', ' ').split()
                        value_list_drone = [] #not needed as all information is on one line

                # format srt data into xml
                root = create_xml.format_xml(final_image_name, video_type, height, width, depth, value_list_cam, value_list_drone)

                # write xml file
                tree = ET.ElementTree(root)

                if float(currentFrame/args.frame_step).is_integer():
                    print(final_image_name)
                     # Saves image of the current frame in jpg file
                    try:
                        if not os.path.isfile(os.path.join(image_path, final_image_name)):
                            cv2.imwrite(os.path.join(image_path, final_image_name), frame)
                    except OSError:
                        print('Error: Can not write image')
                    try: 
                        xmlstr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
                        with open(os.path.join(annotation_path, end_image_name + "{0:05d}.xml".format(currentFrame)), "w") as f:
                            f.write(xmlstr)
                        #tree.write(os.path.join(annotation_path, end_image_name + "{0:05d}.xml".format(currentFrame)), encoding="utf-8", xml_declaration=True)
                    except OSError:
                        print('Error: Can not write xml-file')
                # To stop duplicate images
                currentFrame += 1

        cap.release()
        cv2.destroyAllWindows()

#------------------------------------------------------------------
 # parse_args()
 #
 # Scan command line arguments
#------------------------------------------------------------------
def parse_args():
    '''parse args'''
    parser = argparse.ArgumentParser()
    parser.add_argument('--base_path_input', default='./example_videos', type=str)
    parser.add_argument('--base_path_output', default='./example_images', type=str)
    parser.add_argument('--frame_step', default=10, type=int, choices=range(1,101), metavar="[1-100]", 
                   help='Threshold (1-100) denoting in which steps an image should extracted from the video. Default is 10.')
    return parser.parse_args()

if __name__ == "__main__":
    main(parse_args())
