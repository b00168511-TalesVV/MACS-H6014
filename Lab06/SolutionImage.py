from collections import Counter
from math import ceil, sqrt
from PIL import Image

def main():

    input_file = 'aes.bmp.enc'
    output_file = 'NewImage.jpg'

    # Read the input file, skipping the header 54 bytes
    with open(input_file, 'rb') as f:
        data = f.read()[54:]

    # Truncate the data to a length that's a multiple of 16
    data_length = len(data)
    truncated_length = (data_length // 16) * 16
    truncated_data = data[:truncated_length]

    # Split the data into 16-byte blocks
    blocks = [truncated_data[i*16 : (i+1)*16] for i in range(len(truncated_data) // 16)]

    if not blocks:
        print("No blocks found after processing the file.")


    # Count the frequency of each block
    block_counter = Counter(blocks)
    most_common = block_counter.most_common(2)

    # Determine the most common and second most common blocks
    most_common_block = most_common[0][0] if most_common else None
    second_common_block = most_common[1][0] if len(most_common) > 1 else None

    # Create the pixel list
    pixels = []
    for block in blocks:
        if block == most_common_block:
            pixels.append(255)  # White for most common
        elif block == second_common_block:
            pixels.append(0)    # Black for second most common
        else:
            pixels.append(0)    # Black for all others

    # Calculate the dimensions for a square image
    num_pixels = len(pixels)
    side_length = ceil(sqrt(num_pixels))
    total_pixels_needed = side_length * side_length

    # Pad the pixel list with black (0) if necessary
    pixels += [0] * (total_pixels_needed - num_pixels)

    # Create and save the image
    img = Image.new('L', (side_length, side_length))
    img.putdata(pixels)
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img.save(output_file)

if __name__ == "__main__":
    main()