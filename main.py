import cv2, os
import numpy as np
import math, time, random


blank_size = (100,150)
overlay_attempts = 25000 # amount of times it attempts to find a good image for it
overlay_depth = 100 # amount of different image positions it tries

def render_image(output_file_path=None, goal_image=None,blank_size=None,overlay_attempts=None):
    blank_size = (220, 320)
    overlay_attempts = 10000  # amount of times it attempts to find a good image for it
    overlay_depth = 100
    goal_image = cv2.imread("C:\\Users\\colin\\Downloads\\monalisa.jpg") # cv2.imread("C:\\Users\\colin\\Downloads\\deathconsciousness.jpg")
    final_scale_factor = 1 # add this in the future. make it so that the output image is
    # relatively similar in size to the rescaled one

    resized_goal_image = cv2.resize(goal_image,blank_size)
    cv2.imshow("goal", resized_goal_image)
    cv2.waitKey(0)
    overlay_image_paths = ["..\\overlay_images\\" + f for f in os.listdir("..\\overlay_images") if os.path.isfile(os.path.join("..\\overlay_images", f))]
    stuffplaced = 0
    base_image = np.zeros((blank_size[1], blank_size[0], 3), dtype=np.uint8)
    # make the pixels random colors to encourage new images
    for x in range(blank_size[1]):
        for y in range(blank_size[0]):
            base_image[x,y] = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    # print(len(base_image), len(resized_goal_image))
    '''for x in range(400):
        print(x)
        for y in range(500):
            if random.randint(0,round(x/10)) == 0:
                base_image[y, x] = resized_goal_image[y,x]
            for i in range(250):
                r = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
                goal_pix = resized_goal_image[y,x]
                base_pix = base_image[y,x]
                if math.sqrt(math.pow(goal_pix[0]-r[0],2)+math.pow(goal_pix[1]-r[1],2)+math.pow(goal_pix[2]-r[2],2)) > math.sqrt(math.pow(goal_pix[0]-base_pix[0],2)+math.pow(goal_pix[1]-base_pix[1],2)+math.pow(goal_pix[2]-base_pix[2],2)):
                    base_image[y,x] = r'''

    '''cv2.imshow('show', cv2.resize(base_image, (500,400)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()'''
    image_positions = []
    image_paths = []
    image_sizes = []
    concerning_image_paths = []
    for attempt in range(overlay_attempts):
        if attempt % 100 == 0:
            print("iteration:", attempt)
        if stuffplaced % 5 == 0 or attempt % 500 == 0:
            cv2.imshow("overlay", base_image)
            cv2.waitKey(1)
        best_improvement = 0
        best_x = 0
        best_y = 0
        current_path = random.choice(overlay_image_paths)
        scale_factor = random.randint(10, 12)
        if attempt < 6000:
            scale_factor = random.randint(12, 24)
        overlay_image_pixels = cv2.imread(current_path)
        overlay_image_ratio = len(overlay_image_pixels[0]) / len(overlay_image_pixels)
        overlay_image_size = (round(scale_factor * overlay_image_ratio), round(scale_factor))
        try:
            overlay_image_pixels = cv2.resize(overlay_image_pixels, overlay_image_size)
        except:
            if not current_path in concerning_image_paths:
                concerning_image_paths.insert(0, current_path)
            continue
        # round(overlay_depth/best_scale_factor*10)
        for image_num in range(35):
            random_position_x = random.randint(0, blank_size[1] - overlay_image_size[1]-1)
            random_position_y = random.randint(0, blank_size[0] - overlay_image_size[0]-1)
            base_copy = base_image.copy()
            # first measure the score before anything is added
            before_score = 0
            for offset_x in range(overlay_image_size[0]):
                for offset_y in range(overlay_image_size[1]):
                    base_pixel, goal_pixel = base_copy[random_position_x + offset_y, random_position_y + offset_x], resized_goal_image[random_position_x + offset_y, random_position_y + offset_x]
                    before_score += math.sqrt(math.pow(base_pixel[0] - goal_pixel[0],2) + math.pow(base_pixel[1] - goal_pixel[1],2) + math.pow(base_pixel[2] - goal_pixel[2],2))
            before_score /= overlay_image_size[0] * overlay_image_size[1]
            new_score = 0
            for offset_x in range(overlay_image_size[0]):
                for offset_y in range(overlay_image_size[1]):
                    overlay_image_pixel, goal_pixel = overlay_image_pixels[offset_y, offset_x], resized_goal_image[random_position_x+offset_y,random_position_y+offset_x]
                    new_score += math.sqrt(math.pow(overlay_image_pixel[0] - goal_pixel[0],2) + math.pow(overlay_image_pixel[1] - goal_pixel[1],2) + math.pow(overlay_image_pixel[2] - goal_pixel[2],2))
            new_score /= overlay_image_size[0] * overlay_image_size[1]
            overlay_image_size[0] * overlay_image_size[1]
            if new_score < before_score and new_score-before_score < best_improvement:
                best_improvement = new_score-before_score
                best_x = random_position_x
                best_y = random_position_y
        if best_improvement != 0:
            image_positions.insert(0, (best_y, best_x))
            image_paths.insert(0, current_path)
            image_sizes.insert(0, overlay_image_size)
            stuffplaced += 1
            if stuffplaced % 5 == 0:
                print("images placed:", stuffplaced)
            for offset_x in range(overlay_image_size[0]):
                for offset_y in range(overlay_image_size[1]):
                    new_pix = overlay_image_pixels[offset_y, offset_x]
                    old_pix = base_image[best_x + offset_y, best_y + offset_x]
                    base_image[best_x + offset_y, best_y + offset_x] = new_pix

    for x in range(blank_size[0]):
        for y in range(blank_size[1]):
            if list(base_image[y, x]) == [0,0,0]:
                base_image[y, x] = resized_goal_image[y, x] / 15

    cv2.imshow('show', cv2.resize(base_image,(blank_size[0]*3,blank_size[1]*3)))
    cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # cv2.imshow("overlay", cv2.resize(base_image, (blank_size[1] * 12, blank_size[0] * 12)))
    # create big boy
    image_positions = image_positions[::-1]
    image_paths = image_paths[::-1]
    image_sizes = image_sizes[::-1]
    base_image = np.zeros((blank_size[1] * 5, blank_size[0] * 5, 3), dtype=np.uint8)
    for i in range(len(image_positions)):
        drawing_image = cv2.imread(image_paths[i])
        drawing_image = cv2.resize(drawing_image, (image_sizes[i][0] * 3, image_sizes[i][1] * 3))
        x_end = image_positions[i][0] * 3 + image_sizes[i][0] * 3
        y_end = image_positions[i][1] * 3 + image_sizes[i][1] * 3
        # 4. Use NumPy slicing to place the 'drawing_image' onto the 'canvas'
        base_image[image_positions[i][1] * 3:y_end, image_positions[i][0] * 3:x_end] = drawing_image
        cv2.imshow("overlay", base_image)
        cv2.waitKey(10)
    print(concerning_image_paths)

    cv2.waitKey(0)

    cv2.destroyAllWindows()

render_image()
