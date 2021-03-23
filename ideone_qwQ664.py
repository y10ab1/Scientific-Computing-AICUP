import os
import json

ans = {}

for dir in os.listdir('./'):

    if len(dir) > 4:
        continue

    path = str(dir)+'/'+str(dir)+'_vocal.json'
    #os.path.join(dir, dir + '_vocal.json')
    with open(path, 'r') as fp:
        frame_data = json.load(fp)
        fp.close()

    print(os.path.join(dir, dir + '_vocal.json'))
    print('===================')

    start = 0.0
    last_pitch = 0.0
    last_sum = 0.0
    count = 0
    tmp = len(frame_data)
    prediction = []
    for i, frame in enumerate(frame_data):
        if abs(frame[1] - last_pitch) > 1.0:
            if i < tmp-1:
                next_frame = frame_data[i+1]
            if abs(frame[1] - next_frame[1]) <= 1.0:
                if last_pitch != 0.0:
                    prediction.append(
                        [start, round(frame[0], 3), round(last_sum / count)])
                last_sum = 0.0
                count = 0
                start = frame[0]
            else:
                last_sum -= frame[1]
                count -= 1
        if abs(frame[1] - last_pitch) > 1.0 and abs(frame[1] - next_frame[1]) <= 1.0:
            last_pitch = frame[1]
        last_sum += frame[1]
        count += 1

    ans[dir] = prediction

with open('prediction.json', 'w') as fp:
    json.dump(ans, fp, sort_keys=True, indent=4)
