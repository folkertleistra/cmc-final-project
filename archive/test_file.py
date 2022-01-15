print('hello world')
import pickle
with open('streamers_dict.p', 'rb') as fp:
    streamer_dict = pickle.load(fp)

print(len(streamer_dict))
print(streamer_dict.keys())
print(len(streamer_dict['fps_shaka']['viewers']))
print(streamer_dict['fps_shaka']['languages'])
print(streamer_dict['fps_shaka']['games'])
# 15191

if 'TEST_VIEWER_01' in streamer_dict['fps_shaka']['viewers']:
    print('werkt')