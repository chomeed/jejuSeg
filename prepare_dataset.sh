# unzip dataset zip files 
unzip aihub_jeju/train/labels/FGT_1024.zip -d /path/to/mmsegmentation/data/train/labels
unzip aihub_jeju/val/labels/FGT_1024.zip -d /path/to/mmsegmentation/data/val/labels
unzip aihub_jeju/train/images/FGT_1024.zip -d /path/to/mmsegmentation/data/train/images
unzip aihub_jeju/val/images/FGT_1024.zip -d /path/to/mmsegmentation/data/val/images

# geo2coco 
python geo2coco.py /path/to/mmsegmentation/data/train/labels/FGT_1024/json /path/to/mmsegmentation/data/train/train.json
# python geo2coco.py mmsegmentation/data/train/labels/FGT_1024/json mmsegmentation/data/train/train.json
python geo2coco.py /path/to/mmsegmentation/data/val/labels/FGT_1024/json /path/to/mmsegmentation/data/val/val.json
# python geo2coco.py mmsegmentation/data/val/labels/FGT_1024/json mmsegmentation/data/val/val.json

# create mask files 
# make sure to have directories set
python maskcoco.py mmsegmentation/data/train/train.json mmsegmentation/data/train/masks
python maskcoco.py mmsegmentation/data/val/val.json mmsegmentation/data/val/masks

# train 
cd mmsegmentation 
# python tools/train.py configs/_ours_/unet-s5-d16_deeplabv3_40k_jeju.py --work-dir experiments
python tools/train.py configs/_ours_/segformer-b0_160k_jeju.py --work-dir experiments