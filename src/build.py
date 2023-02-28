import os, glob, shutil

IMG_PATH = './images'
TEMP_PATH = './temp'
VID_PATH = './videos'
FFMPEG_PATH = 'ffmpeg'
os.makedirs(TEMP_PATH, exist_ok=True)
os.makedirs(VID_PATH, exist_ok=True)

imgs = glob.glob(IMG_PATH + '/*.png')
vids = glob.glob(VID_PATH + '/*.mp4')

assert len(imgs) > 0, 'No images found in ' + IMG_PATH

imgs.sort(key=lambda x: os.path.getmtime(x))
vids.sort(key=lambda x: os.path.getmtime(x))


for i, img in enumerate(imgs):
    shutil.move(img, f"{TEMP_PATH}/{i:08d}.png")
    print(f"{img} -> {TEMP_PATH}/{i:08d}.png")

vids_num = len(vids)
if vids_num == 3:
    shutil.move(vids[1], f"{VID_PATH}/1.mp4")
    shutil.move(vids[2], f"{VID_PATH}/2.mp4")
    print(f"{vids[1]} -> {VID_PATH}/1.mp4")
    print(f"{vids[2]} -> {VID_PATH}/2.mp4")
    vids_num = 2
os.system(f'{FFMPEG_PATH} -y -framerate 30 -i "{TEMP_PATH}/%08d.png" -c:a copy -shortest -c:v libx264 -pix_fmt yuv420p {VID_PATH}/{vids_num+1}.mp4')
# remove temp files
shutil.rmtree(TEMP_PATH)