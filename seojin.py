import os
import json
import numpy as np
from tqdm import tqdm

def normalize_coordinates(coordinates, width, height):
    normalized_coords = []
    for coord in coordinates:
        x_normalized = coord[0] / width
        y_normalized = coord[1] / height
        normalized_coords.append([x_normalized, y_normalized])
    return normalized_coords

def aihub_to_coco(aihub_json_path):
    with open(aihub_json_path, 'r', encoding='utf-8') as f:
        aihub_data = json.load(f)

    coco_data = {
        "info": {"version": "1.0", "description": "AIHUB to COCO Conversion", "year": 2024, "contributor": "Your Name", "date_created": "2024-01-02"},
        "licenses": [],
        "categories": [],
        "images": [],
        "annotations": [],
    }

    nia_classes = ['background', 'ac74ubb3c']  
    coco_categories = [{"id": i + 1, "name": name, "supercategory": name} for i, name in enumerate(nia_classes)]
    coco_data["categories"] = coco_categories

    image_id = 1
    annotation_id = 1

    for entry in tqdm(aihub_data['features'], desc="Converting AIHUB to COCO"):
        coordinates_list = entry["geometry"]["coordinates"]

        for polygon_coords in coordinates_list:
            x_coords = np.array([coord[0] for coord in polygon_coords])
            y_coords = np.array([coord[1] for coord in polygon_coords])
            xmin, ymin, xmax, ymax = np.min(x_coords), np.min(y_coords), np.max(x_coords), np.max(y_coords)
            width, height = xmax - xmin, ymax - ymin

            normalized_polygon_coords = normalize_coordinates(polygon_coords, width, height)

            image_info = {
                "id": image_id,
                "file_name": os.path.basename(aihub_json_path),
                "width": int(width),
                "height": int(height),
            }
            coco_data["images"].append(image_info)

            annotation_info = {
                "id": annotation_id,
                "image_id": image_id,
                "category_id": nia_classes.index("ac74ubb3c") + 1,
                "segmentation": [np.array(normalized_polygon_coords).ravel().tolist()],
                "area": int(width) * int(height),
                "bbox": [int(xmin), int(ymin), int(width), int(height)],
                "iscrowd": 0,
            }
            coco_data["annotations"].append(annotation_info)

            annotation_id += 1
            image_id += 1

    return coco_data


aihub_json_path = 'LC_JJ_AP25_33606070_001_2019_FGT_1024.json'

coco_data = aihub_to_coco(aihub_json_path)


output_folder_path = "."
os.makedirs(output_folder_path, exist_ok=True)
output_json_path = os.path.join(output_folder_path, "coco.json")
with open(output_json_path, 'w') as json_file:
    json.dump(coco_data, json_file, indent=2)