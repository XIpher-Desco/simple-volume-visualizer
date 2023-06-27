import pyaudio
import yaml
import codecs
import chardet

if __name__ == '__main__':
    pa = pyaudio.PyAudio()
    audio_list=[]
    for i in range(pa.get_device_count()):
        # print(pa.get_device_info_by_index(i))
        audio_list.append(pa.get_device_info_by_index(i))

    # print(audio_list)
    audio_list = [{
        'index': i['index'],
        'name':  (i['name'].encode("shift-jis").decode("utf-8", errors="ignore") if ('繝' in i['name']) else i['name']),
        'shift' : '繝' in i['name'],
    } for i in audio_list if i['maxInputChannels'] > 0]

    print(audio_list)

    with open('output.yaml', 'w', encoding='utf-8') as file:
        # yaml.dump(audio_list, file , default_flow_style=False, allow_unicode=True)
        yaml.dump(audio_list,file,encoding='utf-8', allow_unicode=True)
        # yaml.dump(audio_list, file,encoding='shift-jis', allow_unicode=True)