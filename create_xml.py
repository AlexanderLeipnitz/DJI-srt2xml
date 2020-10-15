''' ########################################################################
 ''
 '' File....:	create_xml.py
 '' Function:	format raw data to xml
 '' Author..:	Alexander Leipnitz
 '' Date....:	05.08.2019
 ''
 ######################################################################### '''

import xml.etree.cElementTree as ET
import os

#------------------------------------------------------------------
 # format_xml()
 #
 # Format the raw data from the srt-file into xml (dependend on drone-type)
#------------------------------------------------------------------
def format_xml(final_image_name, video_type, height, width, depth, value_list_cam, value_list_drone = None):
    root = ET.Element("annotation")
    ET.SubElement(root, "dataset").text = "EXAMPLE"
    ET.SubElement(root, "filename").text = os.path.splitext(final_image_name)[0] #remove file extension

    size = ET.SubElement(root, "size")
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "depth").text = str(depth)

    cam = ET.SubElement(root, "cam") # Camera-information
    GPS = ET.SubElement(root, "gps")  # Position of the drone
    drone = ET.SubElement(root, "drone")  # extra information about the drone

    if video_type == "DJI_MAVIC":
        if value_list_cam[0] == "iso":
            ET.SubElement(cam, "iso").text = value_list_cam[1]
        if value_list_cam[2] == "shutter":
            ET.SubElement(cam, "shutter").text = value_list_cam[3]
        if value_list_cam[4] == "ev":
            ET.SubElement(cam, "ev").text = value_list_cam[5]
        if value_list_cam[6] == "fnum":
            ET.SubElement(cam, "fnum").text = value_list_cam[7]

        ET.SubElement(GPS, "longitude").text = value_list_drone[1]
        ET.SubElement(GPS, "latitude").text = value_list_drone[2]
        ET.SubElement(GPS, "barometer").text = value_list_drone[5]

    elif video_type == "DJI_MAVIC2":#
        if value_list_cam[0] == "iso":
            ET.SubElement(cam, "iso").text = value_list_cam[1]
        if value_list_cam[2] == "shutter":
            ET.SubElement(cam, "shutter").text = value_list_cam[3]
        if value_list_cam[6] == "ev":
            ET.SubElement(cam, "ev").text = value_list_cam[7]
        if value_list_cam[4] == "fnum":
            ET.SubElement(cam, "fnum").text = str(float(value_list_cam[5]) / 100)
        if value_list_cam[8] == "ct":
            ET.SubElement(cam, "ct").text = value_list_cam[9]
        if value_list_cam[10] == "color_md":
            ET.SubElement(cam, "color_md").text = value_list_cam[11]
        if value_list_cam[12] == "focal_len":
            ET.SubElement(cam, "focal_len").text = value_list_cam[13]

        print(value_list_cam)
        if value_list_cam[16] == "longitude" or value_list_cam[16] == "longtitude": #spelling error in SRT-File
            ET.SubElement(GPS, "longitude").text = value_list_cam[17]
        if value_list_cam[14] == "latitude":
            ET.SubElement(GPS, "latitude").text = value_list_cam[15]
        if value_list_cam[18] == "altitude":
            ET.SubElement(GPS, "altitude").text = value_list_cam[19]

        # Additional drone information in newer versions
        if len(value_list_cam) > 21:
            if value_list_cam[21] == "Yaw":
                ET.SubElement(drone, "yaw").text = value_list_cam[22].replace(',','')
            if value_list_cam[23] == "Pitch":
                ET.SubElement(drone, "pitch").text = value_list_cam[24].replace(',','')
            if value_list_cam[25] == "Roll":
                ET.SubElement(drone, "roll").text = value_list_cam[26]

    elif video_type == "DJI_MAVIC2_THERMAL":
        #ET.SubElement(cam, "iso").text = value_list_cam[1]
        #ET.SubElement(cam, "shutter").text = value_list_cam[3]
        #ET.SubElement(cam, "ev").text = value_list_cam[7]
        #ET.SubElement(cam, "fnum").text = str(float(value_list_cam[5]) / 100)
        #ET.SubElement(cam, "ct").text = value_list_cam[9]
        if value_list_cam[0] == "color_md":
            ET.SubElement(cam, "color_md").text = value_list_cam[1]
        #ET.SubElement(cam, "focal_len").text = value_list_cam[13]

        if value_list_cam[4] == "longitude" or value_list_cam[4] == "longtitude": #spelling error in SRT-File
            ET.SubElement(GPS, "longitude").text = value_list_cam[5]
        if value_list_cam[2] == "latitude":
            ET.SubElement(GPS, "latitude").text = value_list_cam[3]
        if value_list_cam[6] == "altitude":
            ET.SubElement(GPS, "altitude").text = value_list_cam[7]
    else:
        print('video_type unknown')


    return root
