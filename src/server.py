from datetime import datetime, timedelta
from sys import flags
from dateutil import parser
from shutil import copy
from flask import Flask, request, abort
from ahk import AHK
from time import sleep

ahk = AHK()
app = Flask(__name__)

FILE_TO_WRITE_TO = './chatlog.txt' # <------- change this line
VID_PATH = 'C:\\Users\\Stream\\Desktop\\utils\\videos'
SAVE_PATH = 'Z:\\video\\timelapse'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        message = request.json.get('eventData').get('body')
        user = request.json.get('eventData').get('user').get('displayName')
        timestamp = request.json.get('eventData').get('timestamp')
        # formatted = datetime.strftime(parser.isoparse(timestamp), '%H:%M:%S')

        if user and message and timestamp:
            # write_out_chatlog(formatted, user, message)
            play_timelapse_video(message, "ysYShfHF延时回放timelapseTIMELAPSE", 150)
            stop_timelapse_video(message, "停止stopSTOP")
            save_timelapse_video(message, "bcBCsvSV保存saveSAVE", timestamp)
        return 'success', 200
    else:
        abort(400)

def match_message(message, keywords):
    if len(message) > 1 and message in keywords:
        return "1"
    elif message.split(" ")[0] in keywords:
        if message.split(" ")[1] in ["1", "2", "3"]:
            return message.split(" ")[1]
        else:
            return False
    return False

def play_timelapse_video(message, keywords, cutscene_delay):
    scene_flag = match_message(message, keywords)
    if scene_flag:
        change_scene(scene_flag)
        print(f"Change Scene {scene_flag}")
        sleep(cutscene_delay)
        change_scene("0")
    return None

def stop_timelapse_video(message, keywords):
    scene_flag = match_message(message, keywords)
    if scene_flag:
        print(f"Change Scene 0")
        change_scene("0")
    return None

def save_timelapse_video(message, keywords, timestamp):
    scene_flag = match_message(message, keywords)
    if scene_flag:
        vid_match_dic = {"1":"3", "2":"2", "3":"1"}
        days = timedelta(days=int(scene_flag))
        formatted = datetime.strftime(parser.isoparse(timestamp)-days, '%Y-%m-%d')
        copy(f"{VID_PATH}/{vid_match_dic[scene_flag]}.mp4", f"{SAVE_PATH}/{formatted}.mp4")
        print(f"Save Vid {VID_PATH}/{vid_match_dic[scene_flag]}.mp4 -> {SAVE_PATH}/{formatted}.mp4")
    return None

def change_scene(scene_num):
    ahk.send_input("{Alt down}{Shift down}{%s down}" % (scene_num, ))
    sleep(0.1)
    ahk.send_input("{Alt up}{Shift up}{%s up}" % (scene_num, ))

def write_out_chatlog(timestamp, user, message):
    with open(FILE_TO_WRITE_TO, mode='a') as chatlog:
        chatlog.write(f"{timestamp} {user}: {message}\n")


if __name__ == "__main__":
    app.run(host='0.0.0.0')