# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai
from PIL import Image
from streamlit_extras.let_it_rain import rain

# 1. Cấu hình bảo mật
# Yêu cầu: đặt GOOGLE_API_KEY trong .streamlit/secrets.toml (hoặc Secrets của Streamlit Cloud)
# Ví dụ:
#   GOOGLE_API_KEY = "YOUR_KEY"

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

st.set_page_config(
    page_title="Vietnam Travel AI Designer",
    page_icon="🇻🇳",
    layout="wide",
)

# 2. Thư viện nhạc & hiệu ứng
TRAVEL_DATA = {
    "Đà Lạt": {
        "music": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        "emoji": "🌸",
    },
    "Phú Quốc": {
        "music": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3",
        "emoji": "🏝️",
    },
    "Cố đô Huế": {
        "music": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3",
        "emoji": "🏯",
    },
    "Hà Giang": {
        "music": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-10.mp3",
        "emoji": "⛰️",
    },
}

RATIO_MAP = {
    "9:16 (TikTok/Shorts)": "9:16",
    "16:9 (YouTube)": "16:9",
    "1:1 (Instagram)": "1:1",
}

st.title("🇻🇳 Vietnam Travel AI: Hành Trình Ảo")
st.markdown("---")

# 3. Giao diện Sidebar
with st.sidebar:
    st.header("Cài đặt chuyến đi")
    destination = st.selectbox("Điểm đến mơ ước:", list(TRAVEL_DATA.keys()))
    ratio_label = st.radio(
        "Tỉ lệ khung hình (dành cho):",
        list(RATIO_MAP.keys()),
    )
    st.info("App sẽ tự động chọn nhạc và hiệu ứng phù hợp!")

# 4. Giao diện chính
uploaded_file = st.file_uploader(
    "Tải ảnh chân dung hoặc phong cảnh của bạn...",
    type=["jpg", "png", "jpeg"],
)

if uploaded_file:
    col1, col2 = st.columns(2)
    img = Image.open(uploaded_file)

    with col1:
        st.image(img, caption="Ảnh bạn đã tải lên", use_container_width=True)

    if st.button("🚀 Bắt đầu thiết kế hành trình"):
        with st.spinner(f"Đang đưa bạn tới {destination}..."):
            # A. Phân tích ảnh với Gemini
            model_vision = genai.GenerativeModel("gemini-1.5-flash")
            prompt_analysis = (
                "Describe the person's appearance, hair, and clothing in this photo briefly."
            )
            response = model_vision.generate_content([prompt_analysis, img])

            # B. Tạo Prompt nghệ thuật
            ratio = RATIO_MAP[ratio_label]
            final_prompt = (
                f"A professional travel photograph of a person with {response.text}, "
                f"standing in the iconic scenery of {destination}, Vietnam. "
                f"High quality, cinematic lighting, aspect ratio {ratio}."
            )

            # C. Hiển thị kết quả (gợi ý prompt)
            st.balloons()
            with col2:
                st.success(f"Chào mừng bạn đến với {destination}!")
                st.code(final_prompt, language="markdown")
                st.info(
                    "Dán prompt trên vào Midjourney/Leonardo để nhận ảnh chất lượng cao nhất!"
                )

            # D. Hiệu ứng và nhạc
            rain(
                emoji=TRAVEL_DATA[destination]["emoji"],
                font_size=25,
                falling_speed=3,
                animation_length=5,
            )
            st.audio(
                TRAVEL_DATA[destination]["music"],
                format="audio/mp3",
                autoplay=True,
            )

st.markdown("---")
st.caption("Phát triển bởi Google AI Studio x Streamlit")
