def geojson_to_image_coords(image_size, top_left_coords, resolution):
    # Extract coordinates from GeoJSON
    multipoly = [ [ [ [ 151613.410699998115888, 99653.104300000355579 ], [ 151617.802899998932844, 99656.438099998427788 ], [ 151622.832547867379617, 99652.0 ], [ 151610.034410693886457, 99652.0 ], [ 151612.511099998431746, 99653.527699999627657 ], [ 151613.410699998115888, 99653.104300000355579 ] ] ], [ [ [ 151624.303933943476295, 99652.0 ], [ 151624.311599997687154, 99652.045999998634215 ], [ 151630.079499997606035, 99657.337700000352925 ], [ 151632.619499998079846, 99659.824799998663366 ], [ 151639.392899998580106, 99652.628099999943515 ], [ 151638.780114568129648, 99652.0 ], [ 151624.303933943476295, 99652.0 ] ] ] ]

    # Get image size, top-left coordinates, and resolution
    image_width, image_height = image_size
    resolution_x, resolution_y = resolution

    # Calculate scaling factors
    scale_x = 1 / resolution_x
    scale_y = 1 / resolution_y

    image_coords = []
    for poly in multipoly: 
        # Apply scaling and translation to each coordinate
        new_coords = [
                (int((x - top_left_coords[0]) * scale_x),
                int((top_left_coords[1] - y) * scale_y)) for x, y in poly[0]
        ]
        image_coords.append(new_coords)

    return image_coords

image_size = (1024, 1024)
top_left_coords = [151225.125, 100099.875]
resolution = (0.25, 0.25)  # Resolution in meters per pixel

image_coordinates = geojson_to_image_coords(image_size, top_left_coords, resolution)
print(image_coordinates)
