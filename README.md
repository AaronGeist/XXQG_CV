# XXQG_CV
图像识别(OCR)---模拟器 or MIUI+ or 多屏协同---答题 MySQL题库模糊查询 涵盖精准、快速、无封号风险

先行开源，后续进行详细介绍。

使用方法：
1、注册百度ocr，获取AK导入srdt_accurate.py和tzdt_accurate.py
2、安装python环境，并pip install pymysql keyboard pyautogui pyttsx3 keyboard re
3、安装并将words.txt导入MySQL数据库或使用云数据库，更新searchsql.py程序
4、将模拟器、MIUI+或华为多屏协同置屏幕中央
按下键盘Q进行截图、OCR识别、数据库题库查询、模拟鼠标位置（随机点防检测）点击
按下键盘S停止并退出程序