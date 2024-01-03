import numpy as np
import cv2
from pycocotools.coco import COCO
from glob import glob 
import argparse


def createMasks(cocojson_path, mask_folder):
    # Load COCO annotations file
    coco = COCO(cocojson_path)
    imgs = coco.imgs
    print(len(imgs))
    for img in imgs.values(): 
        # Load a specific image from the dataset
        img_id = img['id']  # Change this to the desired image ID
        img_width = img['width']
        img_height = img['height']
        img_path = img['file_name']  # Change this to the path of your images
        # img = cv2.imread(f'Sample/images/{img_path}')

        # Load annotations for the image
        ann_ids = coco.getAnnIds(imgIds=img_id)
        anns = coco.loadAnns(ann_ids)

        # Create an empty mask
        mask = np.zeros((img_width, img_height), dtype=np.uint8)

        # Draw each segmentation on the mask
        for ann in anns:
            seg = ann['segmentation']
            for poly in seg:
                poly = np.array(poly).reshape((int(len(poly) / 2), 2)).astype(int)
                cv2.fillPoly(mask, [poly], 1)

        # Save the mask image
        # cv2.imwrite('mmsegmentation/data/masks/' + img_path[:-4] + '_MASK.png', mask)
        cv2.imwrite(mask_folder + '/' + img_path[:-4] + '_MASK.png', mask)


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Splits COCO annotations file into training and test sets.')
    parser.add_argument('cocojson_path')
    parser.add_argument('mask_folder')
    
    args = parser.parse_args()
    # mask_folder ex: mmsegmentation/data/train/masks
    createMasks(args.cocojson_path, args.mask_folder)