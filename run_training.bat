@echo off
echo =====================================================================
echo  Training & Benchmarking Multilingual Fake News Transformer
echo =====================================================================
python src/train.py --augment --model all --epochs 3
pause
