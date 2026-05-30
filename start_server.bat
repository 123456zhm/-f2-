@echo off
cd /d C:\Users\123\Desktop\f2-xiaohongshu-changes\f2
python -m uvicorn main:app --host 0.0.0.0 --port 8000
pause