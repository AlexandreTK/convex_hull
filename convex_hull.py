import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def plot_0_1_image(img, description):
    img = img.copy()
    img = (img - 1)*(-255)
    plt.title(description)
    plt.imshow(img, cmap='gray', vmin=0, vmax=255)
    plt.axis('off')
    plt.show()



image_9_19_b = np.matrix([[0,0,0,0,0,0,0,0,0,0,0],
                          [0,0,0,1,1,1,0,0,0,0,0],
                          [0,0,1,1,1,1,1,0,0,0,0],
                          [0,0,1,1,1,1,0,0,0,0,0],
                          [0,0,0,0,1,1,0,1,0,0,0],
                          [0,0,0,0,1,1,0,1,0,0,0],
                          [0,0,0,0,1,1,1,0,0,0,0],
                          [0,0,0,0,0,0,1,0,0,0,0],
                          [0,0,0,0,0,0,1,0,0,0,0],
                          [0,0,0,0,0,1,1,0,0,0,0],
                          [0,0,0,0,0,1,0,0,0,0,0],
                          [0,0,0,0,0,0,0,0,0,0,0]])


structuring_element_b1 = np.matrix([[1,-1,-1],
                                   [1,0,-1],
                                   [1,-1,-1]])
structuring_element_b2 = np.matrix([[1,1,1],
                                   [-1,0,-1],
                                   [-1,-1,-1]])

structuring_element_b3 = np.matrix([[-1,-1,1],
                                   [-1,0,1],
                                   [-1,-1,1]])

structuring_element_b4 = np.matrix([[-1,-1,-1],
                                   [-1,0,-1],
                                   [1,1,1]])



#plot_0_1_image(image_9_19_b, 'img 9.19b')

def compare_subimage(subimage, structuring_elem):
    subimage_shape = subimage.shape

    if subimage_shape != structuring_elem.shape:
        return False


    for x in range(subimage_shape[0]):
        for y in range(subimage_shape[1]):
            if ((subimage[x,y] != structuring_elem[x,y]) \
                and (structuring_elem[x,y] != -1)):
                return False
    return True

def hit_or_miss(img, structuring_elem):
    num_of_hits = 0
    img_shape = img.shape

    for x in range(1, (img_shape[0]-1)):
        for y in range(1, (img_shape[1]-1)):
            hit = compare_subimage(img[x-1:x+2, y-1:y+2], structuring_elem)
            # display(img[x-1:x+2, y-1:y+2])
            # display(structuring_elem)
            if (hit == True):
                img[x,y] = 2
                num_of_hits += 1
    img[img == 2] = 1
    return num_of_hits


def iterate_hit_or_miss(img, structuring_elements):
    img = img.copy()
    img = np.pad(img, ((1, 1), (1, 1)), 'constant')
    element_counter = 1

    plot_0_1_image(img, 'Original image with padding')
    for str_elem in structuring_elements:
        num_of_hits = 1 # >= 1
        while(num_of_hits > 0):
            num_of_hits = hit_or_miss(img, str_elem)
            #display(num_of_hits)
            str_description = 'element: '+str(element_counter)+' | hits: '+ str(num_of_hits)
            plot_0_1_image(img, str_description)
        #plot_0_1_image(img, 'iterations')

        element_counter += 1
    img = img[1:-1,1:-1]

    plot_0_1_image(img, 'Final Image')
    return img



structuring_elements = [structuring_element_b1, structuring_element_b2, \
                       structuring_element_b3, structuring_element_b4]


convex_image = iterate_hit_or_miss(image_9_19_b, structuring_elements)


def get_image_boundaries(img):
    counter_rows = np.zeros(img.shape[1])
    for rows in img:
        counter_rows = np.add(rows, counter_rows)
    boundary_indices = np.where(counter_rows > 0)
    column_boundaries = ([boundary_indices[1][0], boundary_indices[1][-1]])

    counter_cols = np.zeros(img.shape[0])
    for cols in img.transpose():
        counter_cols = np.add(cols, counter_cols)
    boundary_indices = np.where(counter_cols > 0)
    row_boundaries = ([boundary_indices[1][0], boundary_indices[1][-1]])

    return [column_boundaries, row_boundaries]


def get_limited_convex_hull(original_img, convex_image):
    [column_limit, row_limit] = get_image_boundaries(original_img)
    column_limit_left = column_limit[0]
    column_limit_right = column_limit[1]
    row_limit_up = row_limit[0]
    row_limit_down = row_limit[1]

    convex_image = convex_image.copy()
    convex_image[:, 0:column_limit_left] = 0
    convex_image[:, column_limit_right+1:-1] = 0
    convex_image[0:row_limit_up, :] = 0
    convex_image[row_limit_down+1:-1, :] = 0
    return (convex_image)



limited_convex_image = get_limited_convex_hull(image_9_19_b, convex_image)
plot_0_1_image(limited_convex_image, "Limited convex image")
