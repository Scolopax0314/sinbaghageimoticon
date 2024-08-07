from PIL import ImageFont, ImageDraw, Image
import os

def get_text_size(text, font_path, font_size):
    # 폰트 로드
    font = ImageFont.truetype(font_path, font_size)
    
    # 임시 이미지 생성
    image = Image.new('RGB', (1, 1))
    draw = ImageDraw.Draw(image)
    
    # 텍스트 크기 계산
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    return (text_width, text_height)

# 예시 사용
font_path = os.path.join("font", "malgunbd.ttf")
font_size = 20
text = ""

text_size = get_text_size(text, font_path, font_size)
print(f"Text size (width, height): {text_size}")
