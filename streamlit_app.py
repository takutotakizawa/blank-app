import streamlit as st
import requests
from io import BytesIO
from PIL import Image

st.title("Stable Diffusion Image Generator v1")

# ユーザーにAPIキーを入力させる
api_key = st.text_input("Enter your Stability AI API key:", type="password")

# モデル選択肢
model_options = ["SD Ultra", "SD3 Large", "SD3 Large Turbo", "SD3 Medium"]
selected_model_option = st.selectbox("Select Model:", model_options, index=0)

# モデルとエンドポイントのマッピング
# SD Ultraはultraエンドポイント、SD3.5系はsd3エンドポイントで対応するmodel名を定義
model_endpoints = {
    "SD Ultra": {"endpoint": "ultra", "model": None},
    "SD3 Large": {"endpoint": "sd3", "model": "sd3.5-large"},
    "SD3 Large Turbo": {"endpoint": "sd3", "model": "sd3.5-large-turbo"},
    "SD3 Medium": {"endpoint": "sd3", "model": "sd3.5-medium"}
}

prompt = st.text_area("Enter your prompt:", value="Lighthouse on a cliff overlooking the ocean", height=200)
negative_prompt = st.text_input("Negative Prompt (optional):", value="")

aspect_ratios = ["16:9", "1:1", "21:9", "2:3", "3:2", "4:5", "5:4", "9:16", "9:21"]
aspect_ratio = st.selectbox("Aspect Ratio:", aspect_ratios, index=0)  # デフォルト16:9

seed = st.number_input("Seed (0 for random):", min_value=0, max_value=4294967294, value=0)

output_formats = ["jpeg", "png", "webp"]
output_format = st.selectbox("Output Format:", output_formats, index=1)  # デフォルト: png

if st.button("Generate Image"):
    if not api_key:
        st.error("Please enter your API key.")
    else:
        endpoint_key = model_endpoints[selected_model_option]["endpoint"]
        model_name = model_endpoints[selected_model_option]["model"]
        
        url = f"https://api.stability.ai/v2beta/stable-image/generate/{endpoint_key}"

        data = {
            "prompt": prompt,
            "output_format": output_format,
            "aspect_ratio": aspect_ratio,
            "seed": seed if seed else 0
        }

        if negative_prompt.strip():
            data["negative_prompt"] = negative_prompt

        if model_name is not None:
            data["model"] = model_name

        response = requests.post(
            url,
            headers={
                "authorization": f"Bearer {api_key}",
                "accept": "image/*"
            },
            files={"none": ''},
            data=data
        )

        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            st.image(img, caption="Generated Image", use_container_width=True)
        else:
            try:
                st.error(response.json())
            except:
                st.error("Error occurred. Status code: " + str(response.status_code))
