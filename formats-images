import streamlit as st
from PIL import Image
import io

def main():
    st.title('Image Resizer and Format Changer')

    uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'])
    if uploaded_file is not None:
        with st.container():  # This will create a container for the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Image', use_column_width=True)

        # Define size options here
        size_options = {
            "Match Column (540x270)": (540, 270),
            "Multiple Choice Question (658x539)": (658, 539),
            "Custom": None
        }

        # Dropdown for selecting size
        size_choice = st.selectbox("Select Size", list(size_options.keys()))

        # Handle size selection
        if size_choice == "Custom":
            width = st.number_input("Custom Width", min_value=10, value=540, max_value=max(1000, image.width))
            height = st.number_input("Custom Height", min_value=10, value=270, max_value=max(1000, image.height))
        else:
            width, height = size_options[size_choice]
            st.write(f"Selected size: {width} x {height}")

        # Resize image based on selected size
        new_image = image.resize((int(width), int(height)))

        # Select new image format
        format = st.selectbox("Select New Format", ['JPEG', 'PNG', 'GIF', 'BMP', 'WEBP'])

        # Convert and download image
        if st.button('Convert Image'):
            img_byte_arr = io.BytesIO()
            new_image.save(img_byte_arr, format=format)
            st.download_button(label='Download Image',
                               data=img_byte_arr.getvalue(),
                               file_name=f"converted_image.{format.lower()}",
                               mime=f"image/{format.lower()}")

if __name__ == "__main__":
    main()
