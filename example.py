#this wont run, but here's a real-world usage example

from dansvideoeditor import Node

result =Node('../android/VID_20160901_202505.3gp')
result+=Node('../android/VID_20160905_151200.3gp')
result+=Node('../android/VID_20160907_234206.3gp')
result+=Node('../android/VID_20160908_110507.3gp')
result+=Node('../android/VID_20160908_202325.3gp')
result+=Node('../android/VID_20160908_203316.3gp')
result+=Node('../android/VID_20160909_103228.3gp')
result+=Node('../IMG_0127.MOV')
result+=Node('../IMG_0132.MOV').trim(65, 72)
result+=Node('../IMG_0133.MOV')
result+=Node('../IMG_0134.MOV')
result+=Node('../IMG_0135.MOV')
result+=Node('../IMG_0136.MOV')
result+=Node('../IMG_0138.MOV')
result+=Node('../IMG_0139.MOV')
result+=Node('../IMG_0140.MOV')
result+=Node('../IMG_0141.MOV')
result+=Node('../IMG_0142.MOV')
result+=Node('../IMG_0143.MOV')
result+=Node('../IMG_0145.MOV')
result+=Node('../IMG_0146.MOV')
result+=Node('../IMG_0147.MOV')
result+=Node('../IMG_0148.MOV')
result+=Node('../android/VID_20160924_182813.3gp')
result+=Node('../IMG_0149.MOV')
result+=Node('../android/VID_20160924_224451.3gp').trim(4, 11)
result+=Node('../IMG_0150.MOV')
result+=Node('../IMG_0151.MOV')
result+=Node('../IMG_0152.MOV')
result+=Node('../IMG_0157.MOV')
result+=Node('../IMG_0158.MOV')
result+=Node('../IMG_0159.MOV')
result+=Node('../IMG_0160.MOV')
result+=Node('../IMG_0163.MOV')
result+=Node('../IMG_0164.MOV')
result+=Node('../IMG_0165.MOV')

result.render(1920, 1080, dry=0)