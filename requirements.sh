wget https://www.dropbox.com/s/omo6mbup59r3q3b/fan.mp3 -P ./audio_files/ &&
pip install python_daemon==2.3.0 RPi.GPIO==0.7.0 &&
python3 ./gpio_daemon.py
