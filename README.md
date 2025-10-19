# OCR_PDR-to-TXT
# PDF OCR 批次處理工具

使用 Google Gemini API 將 PDF 文件批次轉換為文字檔案的 Python 工具。

## 系統需求

- Python 3.7 或更高版本
- Google Gemini API 金鑰




## 設定

### 安裝相依套件

```bash
pip install google-generativeai pdf2image Pillow
```

### 取得 Gemini API 金鑰

1. 前往 [Google AI Studio](https://makersuite.google.com/app/apikey)
2. 登入您的 Google 帳號
3. 點擊「Get API Key」建立新的 API 金鑰
4. 複製您的 API 金鑰

### 設定 API 金鑰

在程式碼中找到以下行：

```python
GEMINI_API_KEY = "APIKEY"  # 請替換成你的API金鑰
```

將 `APIKEY` 替換為您的實際 API 金鑰。

**注意：** 為了安全起見，建議使用環境變數儲存 API 金鑰：

```python
import os
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
```

然後在終端機設定環境變數：
```bash
# Windows
set GEMINI_API_KEY=your_api_key_here

# macOS/Linux
export GEMINI_API_KEY=your_api_key_here
```

## 使用方法

### 1. 準備 PDF 檔案

將要處理的 PDF 檔案放入 `./pdfs` 資料夾中。

### 2. 執行程式

```bash
python main.py
```

### 3. 查看結果

處理完成的文字檔案會儲存在 `./txt_output` 資料夾中。

## 資料夾結構

```
project/
│
├── main.py              # 主程式
├── pdfs/                # 放置 PDF 檔案的目錄
│   ├── file1.pdf
│   ├── file2.pdf
│   └── ...
│
└── txt_output/          # 輸出文字檔的目錄 (自動建立)
    ├── file1.txt
    ├── file2.txt
    └── ...
```

## 自訂設定

您可以在 `main.py` 的最後修改以下參數：

```python
if __name__ == "__main__":
    PDF_DIR = "./pdfs"           # 修改 PDF 來源目錄
    OUTPUT_DIR = "./txt_output"  # 修改輸出目錄
    batch_process_pdfs(PDF_DIR, OUTPUT_DIR)
```

### 調整處理速度

在 `process_single_pdf` 函數中修改延遲時間：

```python
time.sleep(3)  # 每頁處理後等待秒數，避免 API 限制
```

在 `batch_process_pdfs` 函數中修改批次間隔：

```python
if idx % 10 == 0:
    time.sleep(5)  # 每處理 10 個檔案後的暫停秒數
```
