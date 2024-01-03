import json, os
from glob import glob
import argparse

def createCOCO(geojson_filepaths):
    def geojson_to_image_coords(coordinates, image_size, top_left_coords, resolution=0.25, geometry_type="Polygon"):
        
        assert geometry_type in ['Polygon', 'MultiPolygon']

        image_width, image_height = image_size
        scale_x = 1 / resolution
        scale_y = 1 / resolution

        if geometry_type == "MultiPolygon":
            image_coords = []
            for coords in coordinates: 
                new_image_coords = [
                        (int((x - top_left_coords[0]) * scale_x),
                        int((top_left_coords[1] - y) * scale_y)) for x, y in coords[0]
                ]
                image_coords.extend(new_image_coords)
        else: 
            image_coords = [
                            (int((x - top_left_coords[0]) * scale_x),
                            int((top_left_coords[1] - y) * scale_y)) for x, y in coordinates[0]
                    ]
        return image_coords

    info = {}
    licenses = [] 
    images = []
    annotations = []
    categories = [{ 
        "id": 1, 
        "name": "building",
        'supercategory': "building"
    }]



    for i, geojson_filepath in enumerate(geojson_filepaths):

        # geojson_filepath = 'Sample/label/ANN_JSON/LC_JJ_AP25_33606070_002_2019_FGT_1024.json'
        # geojson_meta_filepath = 'Sample/label/META_JSON/LC_JJ_AP25_33606070_002_2019_FGT_META_1024.json'
        
        # check if meta file exists
        geojson_meta_filepath = (geojson_filepath[:-9] + 'META' + geojson_filepath[-10:]).replace('json', 'meta', 1)
        if not os.path.exists(geojson_filepath):
            continue

        geojson = json.load(open(geojson_filepath))
        geojson_meta = json.load(open(geojson_meta_filepath, encoding='cp949'))[0]

        geo_coord = list(map(float, geojson_meta['coordinates'].split(', ')))

        # Images 
        img_width = geojson_meta['img_width']
        img_height = geojson_meta['img_height']
        ann_id = geojson_meta['ann_id']
        img_id = i
        img_filename = os.path.splitext(os.path.basename(geojson_filepath))[0] + ".tif"
        img_res = geojson_meta['img_resolution']

        new_image = {
            "id": img_id,
            "width": img_width,
            "height": img_height,
            "file_name": img_filename
        }
        images.append(new_image)

        # Annotations 
        geojson_features = geojson['features'] 

        for j, feature in enumerate(geojson_features): 
            if feature['properties']['ANN_CD'] != 10: 
                continue
            else: 
                coords = feature['geometry']['coordinates']
                geometry_type = feature['geometry']['type']
                
                try: 
                    normalized_coords = geojson_to_image_coords(coords, (img_width, img_height), geo_coord, resolution=img_res, geometry_type=geometry_type)
                except:
                    print(f"Error at {ann_id}")
                    

                seg = [[coord for point in normalized_coords for coord in point]]
                new_ann = {
                        "id": ann_id + '_' + str(j),
                        "image_id": i,
                        "category_id": 1,
                        "segmentation": seg,
                        "is_crowd": 0
                    }
                annotations.append(new_ann)
    coco = { 
        "info": info, 
        "licenses": licenses, 
        "images": images, 
        "annotations": annotations,
        "categories": categories,
    }

    return coco 


if __name__ == "__main__": 
    parser = argparse.ArgumentParser(description='Splits COCO annotations file into training and test sets.')
    parser.add_argument('geojson')
    parser.add_argument('output')
    
    args = parser.parse_args()

    # geojson_filepaths = glob('ZSample/label/ANN_JSON/*')
    geojson_filepaths = glob(args.geojson + '/*')
    coco = createCOCO(geojson_filepaths)
    json.dump(coco, open(args.output, 'w'), indent=1)




# visualize 
# from pycocotools.coco import COCO

# example = COCO('result.json')
# ann_ids = example.getAnnIds(12)
# print(ann_ids)
# print(images)
# anns = example.loadAnns(ann_ids)
# import skimage.io as io
# import matplotlib.pyplot as plt
# image = io.imread('Sample/images/LC_JJ_AP25_33606070_014_2019_FGT_1024.tif')
# plt.imshow(image)
# print(len(anns))
# example.showAnns(anns)
# plt.show()