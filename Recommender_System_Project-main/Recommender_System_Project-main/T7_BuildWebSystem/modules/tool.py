import streamlit as st
import base64
import requests

# Hàm để đọc file hình ảnh và chuyển đổi sang base64
def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
# Hàm để tạo và hiển thị các cột
def display_columns(items, cols=3):
    for i in range(0, len(items), cols):
        cols_list = st.columns(cols)
        for j, col in enumerate(cols_list):
            if i + j < len(items):
                local_image_path = "images\\image1.jpg"

                try: 
                    url = "https://imdb-api.huyvongmongmanh75.workers.dev/title/" + items['movie_id'][i+j]
                    response = requests.get(url)
                    data = response.json()
                except:
                    data = {"image":local_image_path}
                # Đường dẫn tới hình ảnh cục bộ
                image_url = data.get("image", local_image_path)


                # URL đích khi nhấp vào hình ảnh
                link_url = "https://www.facebook.com/"

                # Chuyển đổi hình ảnh sang base64
                # local_image_base64 = get_image_base64(local_image_path)

                # Sử dụng HTML để chèn hình ảnh, thêm caption và liên kết
                image_html = f'''
                    <a href="{link_url}" target="_blank" style="text-decoration: none;">
                        <div style="width: 150px; height: 225px; overflow: hidden; margin: 0 auto;">
                            <img src="{image_url}" style="width: 100%; height: 100%; object-fit: cover;">
                        </div>
                        <div style="text-align:center; ">{items['title'][i + j]}</div>
                    </a>
                '''
                with col:
                    st.markdown(image_html, unsafe_allow_html=True)

# Hàm để tạo và hiển thị các cột
def display_columnsv2(items, cols=3):
    for i in range(0, len(items), cols):
        cols_list = st.columns(cols)
        for j, col in enumerate(cols_list):
            if i + j < len(items):
                idx = (i+j) % 10 + 1
                # Đường dẫn tới hình ảnh cục bộ
                local_image_path = f"images\image{idx}.jpg"

                # URL đích khi nhấp vào hình ảnh
                link_url = "https://www.facebook.com/"

                # Chuyển đổi hình ảnh sang base64
                local_image_base64 = get_image_base64(local_image_path)

                # Sử dụng HTML để chèn hình ảnh, thêm caption và liên kết
                image_html = f'''
                    <a href="{link_url}" target="_blank" style="text-decoration:none;">
                        <div style="text-align:center; width:100%;">
                            <div style="display:inline-block; width:100%; height:auto;">
                                <img src="data:image/jpeg;base64,{local_image_base64}" style="width:100%; height:300px; object-fit:cover;">
                            </div>
                            <div style="margin-top: 10px;">{items['title'][i + j]}</div>
                        </div>
                    </a>
                '''
                with col:
                    st.markdown(image_html, unsafe_allow_html=True)