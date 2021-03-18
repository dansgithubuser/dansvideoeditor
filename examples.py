# this wont run, but here are some examples

import dansvideoeditor as dve

import os

def build_ifiles():
    dve.Ifile('b1', '/home/dan/Downloads/bass_1_2.mp4', 38, 40)
    dve.Ifile('b2', '/home/dan/Downloads/bass_2_1.mp4', 70, 72)
    dve.Ifile('b3', '/home/dan/Downloads/bass_3_1.mp4', 40, 42)
    dve.Ifile('b4', '/home/dan/Downloads/bass_4_1.mp4', 90, 92)
    dve.Ifile('a', '/home/dan/Desktop/mess/audio/test16.flac')

if not os.path.exists('output1.mov'):
    build_ifiles()
    dve.concat_copy(
        ['b1', 'b2', 'b3', 'b4'],
        'output1.mov',
    )
    dve.reset()

if not os.path.exists('output2.mov'):
    build_ifiles()
    dve.concat_center(
        ['b1', 'b2', 'b3', 'b4'],
        opath='output2.mov',
    )
    dve.reset()

if not os.path.exists('output3.mov'):
    build_ifiles()
    dve.concat_center(
        ['b1', 'b2', 'b3', 'b4'],
        640,
        480,
        'output3.mov',
    )
    dve.reset()

if not os.path.exists('output4.mov'):
    build_ifiles()
    dve.SetSar('s1', 'b1', 1)
    dve.SetSar('s2', 'b2', 1)
    dve.SetSar('s3', 'b3', 1)
    dve.SetSar('s4', 'b4', 1)
    dve.Split('s1', 3)
    dve.Split('s2', 3)
    dve.Split('s3', 3)
    dve.Split('s4', 3)
    dve.Concat('q1', ['s1_0', 's1_1', 's1_2'], ['b2', 'b3', 'b4'])
    dve.Concat('q2', ['s2_0', 's3_1', 's4_2'], [])
    dve.Concat('q3', ['s3_0', 's4_1', 's2_2'], [])
    dve.Concat('q4', ['s4_0', 's2_1', 's3_2'], [])
    dve.Crop('c2', 'q2', 1080, 1080)
    dve.Hstack('h1', ['q1', 'c2'])
    dve.Hstack('h2', ['q3', 'q4'])
    dve.Pad('ph2', 'h2', 3000)
    dve.Vstack('v', ['h1', 'ph2'])
    dve.render('output4.mov', 'v', 'q1')
    dve.reset()
