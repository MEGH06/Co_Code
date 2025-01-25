def filter_images(list_of_images):
    # add logic to decide which images to keep and which to discard
    filtered_images = []
    for image in list_of_images:
        if len(image) > 1:
            filtered_images.append(image)
    return filtered_images