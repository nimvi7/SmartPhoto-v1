import streamlit as st
import cv2
import numpy as np 
from PIL import Image 
import io
st.set_page_config(page_title="Smartphoto", page_icon="📸", layout="wide")
st.title("SmartPhoto📸")
st.header("-Помошник с фотками!")
st.write("Загрузи фото и установи фильтры")

st.sidebar.header("Настройка фильтров")
uploaded_file = st.sidebar.file_uploader("Выберите фото...", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    img_arr = np.array(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ориг,фото")
        st.image(img_arr, use_container_width=True)

    filter_option = st.sidebar.selectbox("Выберите фильтр:",
                                         ["Ориг", "Черно-белый",
                                          "blur", "Ярче",
                                          "Контраст", "Инверсия",
                                          "Colour-splash"])
    splash_colour = None
    if filter_option == "Colour-splash":
                                        splash_colour = st.sidebar.selectbox(
                                        "Новые настройки beta тест:",
                                        ["Красный","Оранжевый","Жёлтый","Зелёный","Голубой","Синий","Фиолетовый"])

    processed_img = img_arr.copy()

    if filter_option == "Черно-белый":
        gray = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)
        processed_img = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    elif filter_option  == "blur":
        processed_img = cv2.GaussianBlur(img_arr, (15,15),0 )
    elif filter_option == "Ярче":
        processed_img = cv2.convertScaleAbs(img_arr, alpha=1.0, beta=50)
    elif filter_option == "Контраст":
        processed_img = cv2.convertScaleAbs(img_arr, alpha=1.7, beta=0)
    elif filter_option == "Инверсия":
        processed_img = 255 - img_arr
    elif filter_option == "Colour-splash":
                hsv = cv2.cvtColor(img_arr, cv2.COLOR_RGB2HSV)
                gray = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)
                gray_rgb = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB) # Долго делал 

                if splash_colour == "Красный":
                    low_red1 = np.array([0, 50, 50]) 
                    high_red1 = np.array([10, 255, 255]) 
                    low_red2 = np.array([170, 50, 50]) 
                    high_red2 = np.array([180, 255, 255])

                    mask1 = cv2.inRange(hsv, low_red1, high_red1)
                    mask2 = cv2.inRange(hsv, low_red2, high_red2)
                    mask = mask1 | mask2
                    processed_img = np.where(mask[..., None] > 0, img_arr, gray_rgb)

                elif splash_colour == "Оранжевый":
                    low = np.array([11, 50, 50])
                    high = np.array([22, 255, 255])
                    mask = cv2.inRange(hsv, low, high)
                    processed_img = np.where(mask[..., None] > 0, img_arr, gray_rgb)

                elif splash_colour == "Жёлтый":
                    low = np.array([23, 50, 50])
                    high = np.array([33, 255, 255])
                    mask = cv2.inRange(hsv, low, high)
                    processed_img = np.where(mask[..., None] > 0, img_arr, gray_rgb)

                elif splash_colour == "Зелёный":
                    low = np.array([34, 50, 50])
                    high = np.array([85, 255, 255])
                    mask = cv2.inRange(hsv, low, high)
                    processed_img = np.where(mask[..., None] > 0, img_arr, gray_rgb)   

                elif splash_colour == "Голубой":
                    low = np.array([86, 50, 50])
                    high = np.array([100, 255, 255])
                    mask = cv2.inRange(hsv, low, high)
                    processed_img = np.where(mask[..., None] > 0, img_arr, gray_rgb)
                elif splash_colour == "Синий":
                    low = np.array([101, 50, 50])
                    high = np.array([130, 255, 255])
                    mask = cv2.inRange(hsv, low, high)
                    processed_img = np.where(mask[..., None] > 0, img_arr, gray_rgb)
                elif splash_colour == "Фиолетовый":
                    low = np.array([131, 50, 50])
                    high = np.array([169, 255, 255])
                    mask = cv2.inRange(hsv, low, high)
                    processed_img = np.where(mask[..., None] > 0, img_arr, gray_rgb)

    with col2:
        st.subheader("Фото зделано")
        st.image(processed_img,caption=filter_option, width="stretch")
        result_image = Image.fromarray(processed_img)
        buf = io.BytesIO()
        result_image.save(buf,format= "JPEG")
        byte_im = buf.getvalue()

        st.download_button(label="Скачать",data=byte_im,file_name="Smart_edit.jpeg",mime="image/jpeg")




