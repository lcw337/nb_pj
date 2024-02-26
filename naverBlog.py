import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import re

# HTML에서 이미지 정보 추출
def extract_images(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    images = []
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if src:
            images.append(src)
    return images

# URL에서 HTML 가져오기
def fetch_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # 200 OK 코드가 아니면 예외 발생
        return response.text
    except requests.RequestException as e:
        messagebox.showerror("오류", f"웹페이지를 가져올 수 없습니다: {e}")
        return None

# URL 검사 및 이미지 처리
def check_url():
    url = url_entry.get()
    if "blog.naver.com" not in url:
        messagebox.showerror("오류", "네이버블로그 URL이 아닙니다")
        return
    html_content = fetch_html(url)
    if html_content:
        images = extract_images(html_content)
        if len(images) < 1:
            messagebox.showinfo("결과", "가져올 이미지가 없습니다.")
        else:
            process_and_show_images(images)

# 이미지 URL 처리 및 사용자에게 결과 보여주기
def process_and_show_images(images):
    # https://mblogthumb-phinf.pstatic.net/으로 시작하는 이미지 URL만 처리
    processed_images = []
    for img in images:
        if img.startswith("https://mblogthumb-phinf.pstatic.net/"):
            # 도메인 변경 및 URL 맨 끝의 파라미터 제거
            new_img = re.sub(r'https?://[^/]+', 'https://blogfiles.pstatic.net', img)
            new_img = re.sub(r'\?.*$', '', new_img)
            processed_images.append(new_img)

    if not processed_images:
        messagebox.showinfo("결과", "처리할 이미지가 없습니다.")
        return

    image_info = "\n".join(processed_images)

    result_window = tk.Toplevel(root)  # 새 창을 생성합니다.
    result_window.title("이미지 URL 결과")
    result_text = tk.Text(result_window, height=15, width=50)  # 결과를 표시할 Text 위젯을 생성합니다.
    result_text.pack()
    result_text.insert(tk.END, image_info)  # Text 위젯에 이미지 URL 목록을 삽입합니다.
    result_text.config(state=tk.DISABLED)  # Text 위젯을 읽기 전용으로 설정합니다.

root = tk.Tk()
root.title("네이버 블로그 원본 사진 추출기")

root.geometry("400x200")

url_label = tk.Label(root, text="네이버 블로그 URL:")
url_label.pack()

url_entry = tk.Entry(root, width=50)
url_entry.pack()

submit_button = tk.Button(root, text="추출 시작", command=check_url)
submit_button.pack()

root.mainloop()
