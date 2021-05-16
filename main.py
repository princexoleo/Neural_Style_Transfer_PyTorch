# python3 -m venv venv
# . venv/bin/activate
# pip install streamlit
# pip install torch torchvision
# streamlit run main.py

import streamlit as st
from PIL import Image
import time
import os 
import sys
from io import BytesIO, StringIO


import style

###########

# if not os.path.exists("savel_models"):
#     # run download_savel_models,pu

if not os.path.exists("images/output-images"):
    os.mkdir("images/output-images")



@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return img



# App Tile Name Set
st.title('Welcome to Neural Style Transfer')


# Side bar deign
img = st.sidebar.selectbox(
    'Select Image',
    ('amber.jpg', 'cat.png')
)
style_name = st.sidebar.selectbox(
    'Select Style',
    ('candy', 'mosaic', 'rain_princess', 'udnie')
)
# Model Load
model= "saved_models/" + style_name + ".pth"

st.sidebar.write("Alternative, You can upload an Image")
# Custom Image File Upload Options #
# Image Upload
show_file = st.empty()
custom_file = st.sidebar.file_uploader(
    "Upload you custom Images",
    type=['png', 'jpg']
    )
if not custom_file:
    input_image = "images/content-images/" + img
    output_image = "images/output-images/" + style_name + "-" + img
    show_file.info("Please Slect/upload a file: {}".format(
        " ".join(['png', 'jpg'])
    ))
    # By default Source Images
    st.write('### Source image:')
    image = load_image(input_image)
    st.image(image, width=300) # image: numpy array
   
else:
    content = custom_file.getvalue()
    # if isinstance(content, BytesIO):
    # st.write(custom_file.name)
    input_image = load_image(custom_file)
    with open(os.path.join("images/content-images",custom_file.name),"wb") as f:
        f.write(custom_file.getbuffer())
    
    st.write("File uploaded ...")
    #show_file.image(custom_file)
    st.image(input_image, width=400)
    input_image = "images/content-images/" + custom_file.name
    output_image = "images/output-images/"+style_name+ custom_file.name
    


## continue


## Button Clicked
clicked = st.button('Stylize')

if clicked:
    model = style.load_model(model)
    style.stylize(model, input_image, output_image)
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        # Update the progress bar with each iteration.
        latest_iteration.text(f'Iteration {i+1}')
        bar.progress(i + 1)
        time.sleep(0.1)

    st.write('### Output image:')
    image = Image.open(output_image)
    st.image(image, width=400)

