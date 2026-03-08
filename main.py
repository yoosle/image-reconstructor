import cv2, os, math, random, numpy as np

def render_image(input_file_path="demo_images/xxxtentacion_demo.png", output_file_path="output.png",blank_width=100,overlay_attempts=10000, overlay_depth=1):
    if blank_width > 350:
        print("**blank_width too high. this will take years to render**")
        return
    if overlay_depth > 250:
        print("**overlay_depth too high. this will take years to render**")
        return
    goal_image = cv2.imread("demo_images/xxxtentacion_demo.png")
    goal_image_ratio = len(goal_image[0]) / len(goal_image) # MAY NEED TO SWAP THESE VALUES
    blank_size = (blank_width, round(blank_width*goal_image_ratio))
    resized_goal_image = cv2.resize(goal_image,blank_size)
    overlay_image_paths = ["source_images/jk-sloan-rescaled/" + f for f in os.listdir("source_images/jk-sloan-rescaled")]
    print(overlay_image_paths)
    stuffplaced = 0
    base_image = np.zeros((blank_size[1], blank_size[0], 3), dtype=np.uint8)
    # make the base image's pixels random colors to encourage new images
    for x in range(blank_size[1]):
        for y in range(blank_size[0]):
            base_image[x,y] = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]
    image_positions = []
    image_paths = []
    image_sizes = []
    concerning_image_paths = []
    for attempt in range(overlay_attempts):
        if attempt % 100 == 0:
            print("iteration:", attempt, "images placed:", stuffplaced)
        best_improvement = 0
        best_x = 0
        best_y = 0
        current_path = random.choice(overlay_image_paths)
        scale_factor = random.randint(5, max(8,round(blank_width/100)))
        if attempt < max(overlay_attempts-5000, overlay_attempts * 7/10):
            scale_factor = random.randint(max(10,max(15,round(blank_width/30))), max(20,round(blank_width/13)))
        overlay_image_pixels = cv2.imread(current_path)
        overlay_image_ratio = len(overlay_image_pixels[0]) / len(overlay_image_pixels)
        overlay_image_size = (round(scale_factor * overlay_image_ratio), round(scale_factor))
        try:
            overlay_image_pixels = cv2.resize(overlay_image_pixels, overlay_image_size)
        except:
            if not current_path in concerning_image_paths:
                concerning_image_paths.insert(0, current_path)
            continue
        for image_num in range(overlay_depth):
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
            for offset_x in range(overlay_image_size[0]):
                for offset_y in range(overlay_image_size[1]):
                    new_pix = overlay_image_pixels[offset_y, offset_x]
                    old_pix = base_image[best_x + offset_y, best_y + offset_x]
                    base_image[best_x + offset_y, best_y + offset_x] = new_pix
    # replace any blank pixels with opaque pixels from the goal image to improve visualization
    for x in range(blank_size[0]):
        for y in range(blank_size[1]):
            if list(base_image[y, x]) == [0,0,0]:
                base_image[y, x] = resized_goal_image[y, x] / 15
    # create big boy (upscaled version)
    image_positions = image_positions[::-1]
    image_paths = image_paths[::-1]
    image_sizes = image_sizes[::-1]
    base_image = np.zeros((blank_size[1] * 5, blank_size[0] * 5, 3), dtype=np.uint8)
    for i in range(len(image_positions)):
        drawing_image = cv2.imread(image_paths[i])
        drawing_image = cv2.resize(drawing_image, (image_sizes[i][0] * 3, image_sizes[i][1] * 3))
        x_end = image_positions[i][0] * 3 + image_sizes[i][0] * 3
        y_end = image_positions[i][1] * 3 + image_sizes[i][1] * 3
        base_image[image_positions[i][1] * 3:y_end, image_positions[i][0] * 3:x_end] = drawing_image
    cv2.imwrite("output_image.png", base_image[0:blank_size[1] * 3, 0:blank_size[0] * 3])
    print("final image saved to output_image.png")

render_image("demo_images/xxxtentacion_demo.png")

while True:
    print("type 'd' to run the demo")
    print("type 'c' to continue in default mode")
    print("type 'a' to enter advanced mode")
    response = "d" # input("type 'h' for help with configurations\n").lower()
    if "d" in response:
        response = None
        while response == None or not ("1" in response or "2" in response or "3" in response):
            print("choose demo image(enter number):")
            print("1: mona lisa")
            print("2: abe lincoln")
            response = input("3: XXXTENTACION\n")
            if "1" in response:
                render_image("demo_images/monalisa_demo.jpg")
            elif "2" in response:
                render_image("demo_images/lincoln_demo.jpg")
            elif "3" in response:
                render_image("demo_images/xxxtentacion_demo.png")
    elif "c" in response:
        continue
    elif "a" in response:
        continue
    elif "h" in response:
        continue
