import streamlit as st
from PIL import Image
import io
import zipfile
import os

def main():
    st.title('Batch Image Resizer and Format Changer')

    # Allows multiple files to be uploaded
    uploaded_files = st.file_uploader("Choose images...", type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'], accept_multiple_files=True)
    
    if uploaded_files:
        # Define size options here
        size_options = {
            "Match the Column (540x270)": (540, 270),
            "Multiple Choice (658x539)": (658, 539),
            "Drag&Drop (268x128)": (268, 128),
            "Custom": None
        }

        # Dropdown for selecting size
        size_choice = st.selectbox("Select Size", list(size_options.keys()))

        # Handle size selection
        if size_choice == "Custom":
            width = st.number_input("Custom Width", min_value=10, value=540)
            height = st.number_input("Custom Height", min_value=10, value=270)
        else:
            width, height = size_options[size_choice]
            st.write(f"Selected size: {width} x {height}")

        # Select new image format
        format = st.selectbox("Select New Format", ['JPEG', 'PNG', 'GIF', 'BMP', 'WEBP'])

        # Initialize a list to store all image bytes and their names
        all_images_bytes = []

        # Loop to handle each image
        for uploaded_file in uploaded_files:
            with st.container():
                image = Image.open(uploaded_file)
                st.image(image, caption='Uploaded Image', use_column_width=True)

                # Resize image based on selected size
                if size_choice == "Custom":
                    new_image = image.resize((int(width), int(height)))
                else:
                    new_image = image.resize((width, height))

                # Convert image to 'RGB' if it's not already and if the format is JPEG
                if format == 'JPEG' and new_image.mode != 'RGB':
                    new_image = new_image.convert('RGB')

                # Convert and append image bytes to the list along with their names
                try:
                    img_byte_arr = io.BytesIO()
                    new_image.save(img_byte_arr, format=format)
                    all_images_bytes.append((img_byte_arr.getvalue(), uploaded_file.name))
                except Exception as e:
                    st.error(f"Failed to save the image: {e}")

        # Create a zip file containing all the images
        zip_bytes = create_zip(all_images_bytes)

        # Master download button to download all images together in a zip file
        if st.button("Convert All Images (Zip)"):
            st.download_button(label='Download Zip', data=zip_bytes, file_name='images.zip', mime='application/zip')

        # Individual download buttons for each image
        for img_bytes, img_name in all_images_bytes:
            if st.button(f"Convert {img_name}"):
                st.download_button(label=f'Download {img_name}', data=img_bytes, file_name=img_name, mime=f"image/{format.lower()}")

def create_zip(images):
    zip_bytes = io.BytesIO()
    with zipfile.ZipFile(zip_bytes, 'w') as zip_file:
        for img_bytes, img_name in images:
            zip_file.writestr(img_name, img_bytes)
    return zip_bytes.getvalue()

if __name__ == "__main__":
    main()
