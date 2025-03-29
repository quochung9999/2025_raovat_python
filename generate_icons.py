from PIL import Image, ImageDraw
import os

# Define icon sizes and output directory
icon_sizes = [192, 512]
output_dir = "static/icons"
icon_color = "#007bff" # Blue theme color

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Generate icons
for size in icon_sizes:
    try:
        # Create a new image with the specified size and color
        img = Image.new('RGB', (size, size), color=icon_color)
        
        # Optional: Add a simple shape or text if desired
        # draw = ImageDraw.Draw(img)
        # draw.text((10, 10), f"{size}", fill=(255, 255, 255))

        # Define the output path
        file_path = os.path.join(output_dir, f"icon-{size}x{size}.png")
        
        # Save the image as PNG
        img.save(file_path, "PNG")
        print(f"Successfully created {file_path}")

    except Exception as e:
        print(f"Error creating icon-{size}x{size}.png: {e}")

print("Icon generation complete.")