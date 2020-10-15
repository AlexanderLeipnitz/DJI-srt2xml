# DJI-srt2xml
Split videos from a DJI-drone into individual images and create a .xml-file in the PASCAL VOC format for each of them from the .SRT-logfile

## Usage:

`python main.py --base_path_input example_videos/ --base_path_output example_images/ --frame_step 10`
- `--base_path_input`: Path to the .mp4-videos and .SRT-logfiles sorted in subfolders (e.g. by shooting date)
- Example folder-structure:
  ```
  --example_videos/
    |-- subfolder1/ (e.g. shooting date)
        -- 1_visual.mp4  ("normal" video)
        -- 1_visual.SRT  (logfile)
        -- 1_thermal.mp4 (thermal video)
        -- 1_thermal.SRT (logfile)
        -- ...
  ```
- `base_path_output`: Output path: images and xml-files will be sorted into subfolders:
  ```
  -- example_images/
     |-- images/                (images from "normal" video)
     |   |-- subfolder1/        (e.g. shooting date)
     |       |-- 1_visual/      (individual video)
     |           -- *.jpg       (list of images)
     |-- annotations/           (xml-files from "normal" video)
     |   |-- subfolder1/        (e.g. shooting date)
     |       |-- 1_visual/      (individual video)
     |           -- *.xml       (list of xml-files)
     |-- images_thermal/        (images from thermal video)
     |   |-- subfolder1/        (e.g. shooting date)
     |       |-- 1_thermal/     (individual video)
     |           -- *.jpg       (list of images)
     |-- annotations_thermal/   (xml-files from thermal video)
         |-- subfolder1/        (e.g. shooting date)
             |-- 1_thermal/     (individual video)
                 -- *.xml       (list of xml-files)
  ```
- Works with https://github.com/AlexanderLeipnitz/Online-Image-Annotator to annotate the images with bounding boxes or polygons
- The folder-structure and xml-format is compatible between both projects

- `frame_step`: frame-steps to extract a frame from the video and save it (e.g. 10 for every tenth frame)