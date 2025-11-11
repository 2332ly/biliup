# biliup
自动爬取指定 Bilibili UP主空间的视频信息，包括：
- 视频标题  
- 视频链接  
- 播放数  
- 弹幕数  
- 视频时长

结果会保存到一个 Excel 文件中（默认：`D:\bili_videos.xlsx`）

#### 1. 安装依赖包   

```bash
pip install selenium openpyxl
```

#### 2. 安装 对应版本ChromeDriver   

#### 3. 修改配置区参数


```python
vmid = "401315430"          # 改成目标UP主的UID
output_path = r"D:\bili_videos.xlsx"  # 修改为你想保存的路径
wait_login = True            # 是否手动登录（推荐True）
max_scroll = 3               # 想爬几页视频（默认3页）
```
