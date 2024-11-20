# galton-board
## 製作動機
陳昭羽教授曾說過，他希望有人能夠做出一個巨大的Galton board，讓大家可以丟蘋果進去。然而因為我的能力與財力不足，無法做出如此巨大的Galton board，所以我決定改成做電腦遊戲，讓大家無論身處何處都能夠體驗丟蘋果、玩Galton board的樂趣。
## 安裝方法
    1. 請先安裝Python。[下載連結](https://www.python.org/downloads/)
    2. 下載本專案，包含main.py、requirements.txt、voice/、image/。
    3. 安裝必要的套件
        ```bash
            pip install -r requirements.txt
        ```
    4. 執行main.py
    5. 接著就能夠開始玩了！
## 一些可能的問題
- 在下面的位置報錯
    ```python
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
    ```
    解決方法：將這兩行刪掉。因為我的win11有一些問題，所以我加上這兩行，但是可能會導致作業系統報錯。
- 畫面太小或是太大
    解決方法：
    ```python
        # scale(1)
    ```
    將第44行取消註解，並將1改成你想要的倍率。

