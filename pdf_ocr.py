import os
import google.generativeai as genai
from pathlib import Path
import time
from PIL import Image
import pdf2image
import io

# 設定你的Gemini API金鑰
GEMINI_API_KEY = "APIKEY"  # 請替換成你的API金鑰
genai.configure(api_key=GEMINI_API_KEY)

# 初始化模型
model = genai.GenerativeModel('models/gemini-2.5-flash')

def pdf_to_images(pdf_path):
    """將PDF轉換為圖片列表"""
    try:
        images = pdf2image.convert_from_path(pdf_path, dpi=300)
        return images
    except Exception as e:
        print(f"轉換PDF失敗 {pdf_path}: {str(e)}")
        return []

def ocr_with_gemini(image):
    """使用Gemini API進行OCR"""
    try:
        # 將PIL Image轉換為bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # 呼叫Gemini API
        prompt = "請提取這張圖片中的所有文字內容,保持原有的格式和排版。只輸出文字內容,不要加入任何說明或註解。"
        response = model.generate_content([prompt, {"mime_type": "image/png", "data": img_byte_arr}])
        
        return response.text
    except Exception as e:
        print(f"OCR處理失敗: {str(e)}")
        return ""

def process_single_pdf(pdf_path, output_dir):
    """處理單個PDF檔案"""
    pdf_name = Path(pdf_path).stem
    output_path = os.path.join(output_dir, f"{pdf_name}.txt")
    
    # 如果已經處理過,跳過
    if os.path.exists(output_path):
        print(f"已存在,跳過: {pdf_name}")
        return True
    
    print(f"正在處理: {pdf_name}")
    
    # 將PDF轉換為圖片
    images = pdf_to_images(pdf_path)
    if not images:
        return False
    
    # 處理每一頁
    all_text = []
    for i, image in enumerate(images, 1):
        print(f"  處理第 {i}/{len(images)} 頁...")
        text = ocr_with_gemini(image)
        if text:
            all_text.append(f"--- 第 {i} 頁 ---\n{text}\n")
        
        # 避免API請求過快
        time.sleep(3)
    
    # 儲存為文字檔
    if all_text:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(all_text))
        print(f"✓ 完成: {pdf_name}.txt")
        return True
    else:
        print(f"✗ 失敗: {pdf_name}")
        return False

def batch_process_pdfs(pdf_dir, output_dir):
    """批次處理所有PDF"""
    # 建立輸出目錄
    os.makedirs(output_dir, exist_ok=True)
    
    # 取得所有PDF檔案
    pdf_files = list(Path(pdf_dir).glob("*.pdf"))
    total = len(pdf_files)
    
    print(f"找到 {total} 個PDF檔案")
    print(f"輸出目錄: {output_dir}\n")
    
    success_count = 0
    fail_count = 0
    
    for idx, pdf_path in enumerate(pdf_files, 1):
        print(f"\n[{idx}/{total}] ", end="")
        
        try:
            if process_single_pdf(str(pdf_path), output_dir):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"處理失敗: {str(e)}")
            fail_count += 1
        
        # 每處理10個檔案暫停一下
        if idx % 10 == 0:
            print("\n暫停5秒避免API請求過快...")
            time.sleep(5)
    
    print(f"\n{'='*50}")
    print(f"處理完成!")
    print(f"成功: {success_count} 個")
    print(f"失敗: {fail_count} 個")
    print(f"總計: {total} 個")

if __name__ == "__main__":
    # 設定路徑
    PDF_DIR = "./pdfs"          # PDF檔案所在目錄
    OUTPUT_DIR = "./txt_output" # 輸出文字檔目錄
    
    # 開始批次處理
    batch_process_pdfs(PDF_DIR, OUTPUT_DIR)