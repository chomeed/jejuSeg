# bash jejuSeg/prepare_dataset
mkdir -p jejuSeg/mmsegmentation/data/train/labels
mkdir -p jejuSeg/mmsegmentation/data/train/images
mkdir -p jejuSeg/mmsegmentation/data/train/masks
mkdir -p jejuSeg/mmsegmentation/data/val/labels
mkdir -p jejuSeg/mmsegmentation/data/val/images
mkdir -p jejuSeg/mmsegmentation/data/val/masks

# unzip dataset zip files 
cd jejuSeg
unzip /dataset/jeju/aihub_jeju/train/labels/FGT_1024.zip -d mmsegmentation/data/train/labels
unzip /dataset/jeju/aihub_jeju/val/labels/FGT_1024.zip -d mmsegmentation/data/val/labels
unzip /dataset/jeju/aihub_jeju/train/images/FGT_1024.zip -d mmsegmentation/data/train/images
unzip /dataset/jeju/aihub_jeju/val/images/FGT_1024.zip -d mmsegmentation/data/val/images

# geo2coco 
python geo2coco.py mmsegmentation/data/train/labels/FGT_1024/json mmsegmentation/data/train/train.json
# python geo2coco.py mmsegmentation/data/train/labels/FGT_1024/json mmsegmentation/data/train/train.json
python geo2coco.py mmsegmentation/data/val/labels/FGT_1024/json mmsegmentation/data/val/val.json
# python geo2coco.py mmsegmentation/data/val/labels/FGT_1024/json mmsegmentation/data/val/val.json

# create mask files 
# make sure to have directories set
python maskcoco.py mmsegmentation/data/train/train.json mmsegmentation/data/train/masks
python maskcoco.py mmsegmentation/data/val/val.json mmsegmentation/data/val/masks

# train 
cd mmsegmentation 
# python tools/train.py configs/_ours_/unet-s5-d16_deeplabv3_40k_jeju.py --work-dir experiments
python tools/train.py configs/_ours_/segformer-b0_160k_jeju.py --work-dir /output