from PIL import Image

# Open an image file
with Image.open('blogpost-lotr.jpg') as img:
    # Get image size
    width, height = img.size
    max_height = 1450
    max_width = 650
    min_height = 1400
    min_width = 600
    height = img.height 
    width = img.width
    if width > max_width:
        print("Width is larger than what is allowed")
    if height > max_height:
        print("Height is larger than what is allowed")
    if width < min_width:
        print("Width is smaller than what is allowed")
    if height < min_height:
        print("Height is smaller than what is allowed")
    # Print image size
    print(f"Width: {width}, Height: {height}")
