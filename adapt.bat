@echo off

ffmpeg ^
    -i .\20251105_104320_2.jpg ^
    -y ^
    -compression_level 100 ^
    jtag.jpg
    @REM -vf scale=300:-1 ^
    @REM -q:v 31 ^

wsl base64 jtag.jpg -w 0 > image.txt