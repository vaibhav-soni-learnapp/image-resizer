import streamlit as st
from PIL import Image
import io

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

                # Convert and prepare for download
                try:
                    img_byte_arr = io.BytesIO()
                    new_image.save(img_byte_arr, format=format)
                    download_name = f"{uploaded_file.name.split('.')[0]}_converted.{format.lower()}"

                    # Create download button for each image
                    st.download_button(label='Download Image',
                                       data=img_byte_arr.getvalue(),
                                       file_name=download_name,
                                       mime=f"image/{format.lower()}")
                except Exception as e:
                    st.error(f"Failed to save the image: {e}")

if __name__ == "__main__":
    main()
