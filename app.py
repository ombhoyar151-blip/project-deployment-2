
import streamlit as st
import os
from PIL import Image
import io

# --- Configuration --- #
BASE_DRIVE_PATH = "/content/drive/MyDrive/projet/"
IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.bmp', '.tiff')

# --- Helper Functions ---
def get_image_paths(folder_path):
    """Returns a list of image file paths from a given folder."""
    if not os.path.isdir(folder_path):
        return []
    image_files = []
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(IMAGE_EXTENSIONS):
            image_files.append(os.path.join(folder_path, filename))
    return sorted(image_files)

def display_image_with_caption(image_data, caption):
    """Displays an image with a caption."""
    try:
        if isinstance(image_data, str): # Path to image
            image = Image.open(image_data)
        elif isinstance(image_data, io.BytesIO): # BytesIO object from upload
            image = Image.open(image_data)
        else:
            st.error("Invalid image data type provided.")
            return
        
        st.image(image, caption=caption, use_column_width=True)
    except Exception as e:
        st.error(f"Error displaying image: {e}")

# --- Streamlit App Layout --- #
st.set_page_config(layout="wide", page_title="Colab Image Viewer")

st.title("🖼️ Colab Image Viewer and Processor")
st.markdown("--- ")

# --- Sidebar --- #
st.sidebar.header("📂 Folder and Upload Options")

# Folder Selection
selected_folder_name = st.sidebar.radio(
    "Select a predefined image folder:",
    ("augmented_images", "resized_images")
)

selected_folder_path = os.path.join(BASE_DRIVE_PATH, selected_folder_name)

# User Image Upload
uploaded_file = st.sidebar.file_uploader(
    "Or upload your own image (PNG, JPG, JPEG, GIF, WEBP):", 
    type=list(ext.lstrip('.') for ext in IMAGE_EXTENSIONS)
)

# --- Main Content Area --- #

st.subheader(f"Exploring Images in: `{selected_folder_name}/`")

if uploaded_file is not None:
    st.success("Image uploaded successfully!")
    # Display uploaded image
    st.markdown("### Uploaded Image")
    display_image_with_caption(io.BytesIO(uploaded_file.getvalue()), f"Uploaded: {uploaded_file.name}")
    
    st.markdown("### Uploaded Image Preprocessing Preview (e.g., Resized)")
    try:
        img_to_resize = Image.open(io.BytesIO(uploaded_file.getvalue()))
        original_size = img_to_resize.size
        resized_img = img_to_resize.copy()
        resized_img.thumbnail((250, 250)) # Resize to fit within 250x250
        st.image(resized_img, caption=f"Resized preview (original: {original_size[0]}x{original_size[1]}, preview: {resized_img.size[0]}x{resized_img.size[1]})", use_column_width=False)
    except Exception as e:
        st.error(f"Could not create resized preview for uploaded image: {e}")
    
    st.markdown("--- ")

# List and Display Images from Selected Folder
image_paths = get_image_paths(selected_folder_path)

if not os.path.exists(selected_folder_path):
    st.error(f"The folder `{selected_folder_path}` does not exist. Please ensure your Google Drive is mounted correctly and the path is valid.")
elif not image_paths:
    st.warning(f"No images found in `{selected_folder_path}`. Please check the folder content and image extensions.")
else:
    st.markdown("### Select an Image from the Folder")
    
    # Create a list of display names for the selectbox
    image_display_names = [os.path.basename(path) for path in image_paths]
    selected_image_name = st.selectbox(
        "Choose an image to view:",
        image_display_names
    )
    
    if selected_image_name:
        # Find the full path of the selected image
        full_selected_image_path = os.path.join(selected_folder_path, selected_image_name)
        
        st.markdown("### Selected Image View")
        display_image_with_caption(full_selected_image_path, f"Selected: {selected_image_name}")

        st.markdown("### Selected Image Preprocessing Preview (e.g., Resized)")
        try:
            img_to_resize = Image.open(full_selected_image_path)
            original_size = img_to_resize.size
            resized_img = img_to_resize.copy()
            resized_img.thumbnail((250, 250)) # Resize to fit within 250x250
            st.image(resized_img, caption=f"Resized preview (original: {original_size[0]}x{original_size[1]}, preview: {resized_img.size[0]}x{resized_img.size[1]})", use_column_width=False)
        except Exception as e:
            st.error(f"Could not create resized preview for {selected_image_name}: {e}")


st.markdown("--- ")
st.header("🚀 Future ML Model Prediction Placeholder")
st.info(
    "This section can be extended to integrate your machine learning model.
    You could add options here to run predictions on the displayed or uploaded images."
)

st.markdown("--- ")
st.caption("Developed in Google Colab using Streamlit, OS, and PIL.")
