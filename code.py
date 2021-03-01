# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 22:54:28 2021

@author: TAC
"""

import pandas as pd
df=pd.read_csv('overview-of-recordings.csv')
from glob import glob
#run this before putting all audio files in one folder
train=glob('recordings/train/*.wav')
train=[i.split('\\')[1] for i in train]
test=glob('recordings/test/*.wav')
test=[i.split('\\')[1] for i in test]
val=glob('recordings/validate/*.wav')
val=[i.split('\\')[1] for i in val]

train=pd.DataFrame(train,columns=['wav_filename'])
train.wav_filename='recordings/'+train.wav_filename

test=pd.DataFrame(test,columns=['wav_filename'])
test.wav_filename='recordings/'+test.wav_filename

val=pd.DataFrame(val,columns=['wav_filename'])
val.wav_filename='recordings/'+val.wav_filename

#now put all audio files in one folder recording
from pathlib import Path
import pandas as pd
df=pd.read_csv('overview-of-recordings.csv')
df=df[['phrase','file_name']]
df.file_name='recordings/'+df.file_name
df['wav_filesize']=df.file_name.apply(lambda x:Path(x).stat().st_size)
df.columns=['transcript','wav_filename','wav_filesize']
df.transcript=df.transcript.str.lower()

train1=pd.merge(df,train,left_on='wav_filename',right_on='wav_filename',how='right')
test1=pd.merge(df,test,left_on='wav_filename',right_on='wav_filename',how='right')
val1=pd.merge(df,val,left_on='wav_filename',right_on='wav_filename',how='right')

train1.to_csv('train.csv',index=False)
val1.to_csv('val.csv',index=False)
test1.to_csv('test.csv',index=False)

#now convert all audios to one channel
import os
os.mkdir('audio')
from glob import glob
from pydub import AudioSegment
for i in glob('recordings/*.wav'):  
    sound = AudioSegment.from_file(i)
    new_sound = sound.set_frame_rate(16000).set_channels(1)
    new_sound.export("audio/{}".format(i.split('\\')[1]),format="wav")