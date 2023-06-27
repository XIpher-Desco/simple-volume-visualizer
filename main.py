import pyaudio
import tkinter
from tkinter import font
import numpy
import struct
import audioop
import yaml
import sys

# 設定ファイル読み込み
config_file_name = 'visualizer_config.yaml'
try:
    with open(config_file_name) as file:
        config_obj = yaml.safe_load(file)
        print(config_obj)
except Exception as e:
    print('Exception occurred while loading YAML...', file=sys.stderr)
    print(e, file=sys.stderr)
    # ファイル開けなければ、作り直す
    config_obj = {'alert': 80, 'warning': 70, 'mic_index': 1}
    with open(config_file_name, 'w', encoding='utf-8') as file:
        yaml.dump(config_obj, file, encoding='utf-8')
    # sys.exit(1)

# スタート処理
def audiostart():
    audio = pyaudio.PyAudio()
    stream = audio.open( format = pyaudio.paInt16,
                         rate = 44100,
                         channels = 1, 
                         input_device_index = 1,
                        input = True, 
                        frames_per_buffer = 1024)
    return audio, stream

# 終了処理
def audiostop(audio, stream):
    stream.stop_stream()
    stream.close()
    audio.terminate()

def tkinter_root_repeat():
    global max_volume_value
    volume_round = round(read_volume_data(stream))
    max_volume_value = max(volume_round, max_volume_value)

    # 現在の文字とバーの色の更新
    current_text_color = "white"
    current_volume_bar = "white"

    if volume_round > config_obj['alert']:
        current_text_color = "red"
        current_volume_bar = "red"
    elif volume_round > config_obj['warning']:
        current_text_color = "yellow"
        current_volume_bar = "yellow"
    else:
        current_text_color = "white"
        current_volume_bar = "white"

    # 現在ボリューム文字の更新
    current_volume_text.set(volume_round)
    current_volume_label['fg'] = current_text_color

    max_text_color = "white"
    max_volume_bar = "white"

    # 最大値の更新
    if max_volume_value > config_obj['alert']:
        max_text_color = "red"
        max_volume_bar = "red"
    elif max_volume_value > config_obj['warning']:
        max_text_color = "yellow"
        max_volume_bar = "yellow"
    else:
        max_text_color = "white"
        max_volume_bar = "white"

    max_volume_text.set(max_volume_value)
    max_volume_label['fg'] = max_text_color

    canvas.delete('current_volume_rectangle')
    canvas.create_rectangle(
        20, 10, volume_round*5 + 20, 50,
        # 50, 50, 300, 250,
        fill = current_volume_bar,
        tag = "current_volume_rectangle"
    )
    canvas.delete('max_volume_rectangle')
    canvas.create_rectangle(
        20, 60, max_volume_value*5 + 20, 100,
        # 50, 50, 300, 250,
        fill = max_volume_bar,
        tag = "max_volume_rectangle"
    )
    tkinter_root.after(100, tkinter_root_repeat)

def read_volume_data(stream):
    data = stream.read(1024)
    audiodata = numpy.frombuffer(data, dtype='int16')
    # print(audiodata)

    data = stream.read(1024)
    rms = audioop.rms(data,2)
    decibel = 20 * numpy.log10(rms)
    # print(decibel)
    return decibel

if __name__ == '__main__':
    max_volume_value = 0
    # pa = pyaudio.PyAudio()
    # for i in range(pa.get_device_count()):
    #     print(pa.get_device_info_by_index(i))

    (audio,stream) = audiostart()
    
    tkinter_root = tkinter.Tk()
    tkinter_root.configure(bg="green", bd=10)

    tkinter_root.geometry(
        "640x360"
    )
    tkinter_root.title(
        "volumemeter"
    )

    canvas = tkinter.Canvas(
        tkinter_root,
        width = 640,
        height = 120,
        relief = "flat",
        bd = 0,
        bg = "green",
        highlightthickness=0
    )

    canvas.grid()
# 現在ボリュームの数値
    current_volume_text = tkinter.StringVar()
    current_volume_text.set("aaaaaaaaaaaaaaaaaaaaaa")
    current_volume_label_font=font.Font(size=80, family='arial', )
    current_volume_label = tkinter.Label(
        tkinter_root,
        textvariable=current_volume_text,
        fg="white",
        bg="green",
        font=current_volume_label_font,
    )
    current_volume_label.grid()

# 最大ボリュームの数値
    max_volume_text = tkinter.StringVar()
    max_volume_text.set("aaaaaaaaaaaaaaaaaaaaaa")
    max_volume_label_font=font.Font(size=80, family='arial', )
    max_volume_label = tkinter.Label(
        tkinter_root,
        textvariable=max_volume_text,
        fg="white",
        bg="green",
        font=max_volume_label_font,
    )
    max_volume_label.grid()

    tkinter_root.after(1000, tkinter_root_repeat)

    tkinter_root.mainloop()
    audiostop(audio,stream)
