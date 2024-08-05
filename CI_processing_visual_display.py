#!/usr/bin/env python
# coding: utf-8

# In[1]:

# import libraries
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.animation as animation
from matplotlib import style
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import pyaudio
from scipy import signal
import math

# In[2]:

# FUNCTIONS

# return filter coefficeints to be used in pre-emphasis filter
def sos_filter(PRE_EMP_CUTOFF, fs):
    sos = signal.butter(1, PRE_EMP_CUTOFF, 'hp', fs=fs, output='sos')
    return(sos)

# pre-emphasis filter to place more emphasis on high frequencies
def pre_emphasis_filter(x):
    y = signal.sosfilt(sos, x)
    return(y)

# applies filterbank to the audio signal
def apply_filterbank(audio_sig):

    filterbank_processed_sig = np.zeros((ELECTRODES, len(audio_sig)))

    for i in range(ELECTRODES):
        filterbank_processed_sig[i,:] = signal.lfilter(b=filter_bank[i][0], a=filter_bank[i][1], x=audio_sig)

    return(filterbank_processed_sig)

# apply fuyll wave rectification
def full_wave_rectify(x):
    y = np.abs(x)
    return(y)

# return filter coefficients for low pass filter
def LP_sos_filter(fs, LP_CUTTOFF):
    sos = signal.butter(1, LP_CUTTOFF, 'lp', fs=fs, output='sos')
    return(sos)
    
# apply low pass filter
def low_pass_filter(sos, x):
    y = signal.sosfilt(sos, x)
    return(y)

# apply low pass-filter to each band to extract the band envelope
def band_envelope(x, LP_sos):

    y = full_wave_rectify(x)

    processed_sig = np.zeros((x.shape))

    for i in range(ELECTRODES):
        processed_sig[i,:] = low_pass_filter(LP_sos, y[i])

    return(processed_sig)


# compression / non-linear mapping
def compression(x, MAX_VOL, indices):

    x = x[:, indices]
    
    x = np.clip(x, 1, MAX_VOL)

    # logarithmic transform
    x = np.log(x)

    # get into scale of 0 to 1 with 1 being MAX_VOL
    x = x/np.log(MAX_VOL)

    return(x)

# Create an area on the canvas for each electrode to be represented
def plot_rectangles(y):

    for i in range(STIM_RATE):
        
        fig.canvas.restore_region(bg)
        
        r0.set_alpha(y[0,i])
        r1.set_alpha(y[1,i])
        r2.set_alpha(y[2,i])
        r3.set_alpha(y[3,i])
        r4.set_alpha(y[4,i])
        r5.set_alpha(y[5,i])
        r6.set_alpha(y[6,i])
        r7.set_alpha(y[7,i])
        r8.set_alpha(y[8,i])
        r9.set_alpha(y[9,i])
        r10.set_alpha(y[10,i])
        r11.set_alpha(y[11,i])
        r12.set_alpha(y[12,i])
        r13.set_alpha(y[13,i])
        r14.set_alpha(y[14,i])
        r15.set_alpha(y[15,i])
        r16.set_alpha(y[16,i])
        r17.set_alpha(y[17,i])
        r18.set_alpha(y[18,i])
        r19.set_alpha(y[19,i])
        r20.set_alpha(y[20,i])
        r21.set_alpha(y[21,i])

        fig.canvas.blit(fig.bbox)
        fig.canvas.flush_events()
      


# In[3]:


# Variables used

fs = 14000              # sample rate
PRE_EMP_CUTOFF = 1200   # Cutoff freq. of the high-pass pre-emph filter (Hz)

AVG_COCHLEA_LENGTH = 35 # (in millimetres)
ELECTRODES = 22         # number of electrodes
FREQ_RANGE = 400, 6000  # freq range of CI processor (in Hz)

LP_CUTTOFF = 200        # Hz (cuttoff for low-pass filter after sig. rectified)

MAX_VOL = 20            # max value of full rectification and LP filter
                        # used to apply compression

STIM_RATE = 2           # How many pulses to be delivered per chunk of audio



# mic recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
CHUNK = 400             # number of samples in audio buffer


# In[4]:

# initialise root window for graphic interface

root = tkinter.Tk()  
root.geometry('300x150')
root.title('CI simulator')
root.state('zoomed')
root.config(background='white')

style.use('ggplot')


# In[5]:

# prepare graph used to display CI output visually

fig = plt.figure(figsize=(ELECTRODES, 1), dpi=100)
ax = fig.add_subplot(1, 1, 1)
ax.set_ylim(0, 1)
ax.set_xlim(0, ELECTRODES)

(ln,) = ax.plot([0, 0],[0, 0], color='white', animated=True)
plt.show(block=False)

#################### 

bg = fig.canvas.copy_from_bbox(fig.bbox)
ax.draw_artist(ln)
fig.canvas.blit(fig.bbox)

ax.set_xticks([])
ax.set_yticks([])
plt.xlim(0, ELECTRODES)
ax.draw_artist(ln)

cmap = matplotlib.colormaps['hsv']
colours = np.linspace(0,1,(ELECTRODES))


ax.text(0.1, -1, "BASE", size=40)
ax.text(ELECTRODES-2, -1, "APEX", size=40)


r0 = ax.add_patch(Rectangle((0, 0), 1, 1, facecolor=cmap(colours[0]),
                            alpha=0, edgecolor='black'))
r1 = ax.add_patch(Rectangle((1, 0), 1, 1, facecolor=cmap(colours[1]),
                            alpha=0, edgecolor='black'))
r2 = ax.add_patch(Rectangle((2, 0), 1, 1, facecolor=cmap(colours[2]),
                            alpha=0, edgecolor='black'))
r3 = ax.add_patch(Rectangle((3, 0), 1, 1, facecolor=cmap(colours[3]),
                            alpha=0, edgecolor='black'))
r4 = ax.add_patch(Rectangle((4, 0), 1, 1, facecolor=cmap(colours[4]),
                            alpha=0, edgecolor='black'))
r5 = ax.add_patch(Rectangle((5, 0), 1, 1, facecolor=cmap(colours[5]),
                            alpha=0, edgecolor='black'))
r6 = ax.add_patch(Rectangle((6, 0), 1, 1, facecolor=cmap(colours[6]),
                            alpha=0, edgecolor='black'))
r7 = ax.add_patch(Rectangle((7, 0), 1, 1, facecolor=cmap(colours[7]),
                            alpha=0, edgecolor='black'))
r8 = ax.add_patch(Rectangle((8, 0), 1, 1, facecolor=cmap(colours[8]),
                            alpha=0, edgecolor='black'))
r9 = ax.add_patch(Rectangle((9, 0), 1, 1, facecolor=cmap(colours[9]),
                            alpha=0, edgecolor='black'))
r10 = ax.add_patch(Rectangle((10, 0), 1, 1, facecolor=cmap(colours[10]),
                             alpha=0, edgecolor='black'))
r11 = ax.add_patch(Rectangle((11, 0), 1, 1, facecolor=cmap(colours[11]),
                             alpha=0, edgecolor='black'))
r12 = ax.add_patch(Rectangle((12, 0), 1, 1, facecolor=cmap(colours[12]),
                             alpha=0, edgecolor='black'))
r13 = ax.add_patch(Rectangle((13, 0), 1, 1, facecolor=cmap(colours[13]),
                             alpha=0, edgecolor='black'))
r14 = ax.add_patch(Rectangle((14, 0), 1, 1, facecolor=cmap(colours[14]),
                             alpha=0, edgecolor='black'))
r15 = ax.add_patch(Rectangle((15, 0), 1, 1, facecolor=cmap(colours[15]),
                             alpha=0, edgecolor='black'))
r16 = ax.add_patch(Rectangle((16, 0), 1, 1, facecolor=cmap(colours[16]),
                             alpha=0, edgecolor='black'))
r17 = ax.add_patch(Rectangle((17, 0), 1, 1, facecolor=cmap(colours[17]),
                             alpha=0, edgecolor='black'))
r18 = ax.add_patch(Rectangle((18, 0), 1, 1, facecolor=cmap(colours[18]),
                             alpha=0, edgecolor='black'))
r19 = ax.add_patch(Rectangle((19, 0), 1, 1, facecolor=cmap(colours[19]),
                             alpha=0, edgecolor='black'))
r20 = ax.add_patch(Rectangle((20, 0), 1, 1, facecolor=cmap(colours[20]),
                             alpha=0, edgecolor='black'))
r21 = ax.add_patch(Rectangle((21, 0), 1, 1, facecolor=cmap(colours[21]),
                             alpha=0, edgecolor='black'))


ax.set_title('CI simulator', size=18, pad=1)
ax.set_xlabel('  BASE                                                      ' + 
              '                                                            ' + 
              '                                                            ' + 
              '                                APEX', loc='left', size=12)

# In[6]:


# Filter bank
# Gammtone FIR

##########################################################################
# DETERMINE CENTRE FREQS. OF FILTER BANK BASED ON THE GREENWOOD FUNCTION #
##########################################################################

# distance from apex

def distance_from_apex(f):
    # depth in mm from apex
    depth = (math.log10((f/165.4) + 0.88) / 2.1) * AVG_COCHLEA_LENGTH   
    return depth

def Greenwood_function(dist):
    f = 165.4 * ( (10**(2.1*(dist/AVG_COCHLEA_LENGTH))) -0.88)
    return(f)
    

deepest_electrode_depth = distance_from_apex(FREQ_RANGE[0])
shallowest_electrode_depth = distance_from_apex(FREQ_RANGE[1])

# electrodes are assumed to be linearly spaced beteen deepest and shallowest 
#      electrode depth
# calcualte the depth of each linearly spaced electrode
electrode_dist_from_apex = np.linspace(start=deepest_electrode_depth, 
                                       stop=shallowest_electrode_depth, 
                                       num=ELECTRODES, endpoint=True)

# calculate electrode freq. for each electrode depth
filterbank_freqs = np.empty(ELECTRODES)

for i in range(ELECTRODES):
    filterbank_freqs[i] = int(np.rint
                              (Greenwood_function(electrode_dist_from_apex[i])))


#############################################################
# GENERATE FILTER BANK BASED ON THE DEPTH OF EACH ELECTRODE #
#############################################################

filter_bank = []

for i in range(ELECTRODES):
    # produces filter coefficients
    filter_bank.append(signal.gammatone(freq=filterbank_freqs[i], 
                                        ftype='fir', fs=fs))


# In[7]:


# get filter coefficients
sos = sos_filter(PRE_EMP_CUTOFF, fs)

# low-pass filter coefficients to be applied after signal rectification
LP_sos = LP_sos_filter(fs, LP_CUTTOFF)


# In[8]:


# get indices for sampling data allong the processed signal
gap = int(np.floor(CHUNK / (STIM_RATE+1)))
indices = np.arange(gap, (STIM_RATE*gap)+1, gap)



# record audio contunuously and apply function to each chunk over time
def animate(i):

    data = stream.read(CHUNK)
    numpydata = np.frombuffer(data, dtype=np.int16)

    
    # pre-emphasis filtering
    y = pre_emphasis_filter(numpydata)

    # filter bank
    y = apply_filterbank(y)

    # full rectification and LP filter
    band_envelope(y, LP_sos)

    # compression and non-linear mapping
    sampled_data = compression(y, MAX_VOL, indices)

    # flip data so that BASAL data is on the left and APICAL data on the right
    y = np.flip(sampled_data, axis=0)

    # plot rectangles
    plot_rectangles(y)
    


# In[9]:

# record audio in chunks

audio = pyaudio.PyAudio()
  
# start recording sound signal
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=fs, input=True,
                frames_per_buffer=CHUNK)

##############################################

# draw canvas and update after each chunk of audio is processed

canvas = FigureCanvasTkAgg(fig, root)   
canvas.draw()


canvas1 = tkinter.Frame(master=root, width=500, height=300, bg="white") 
canvas1.pack(fill=tkinter.Y, side=tkinter.TOP)


canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
ani = animation.FuncAnimation(fig, animate, interval=0, blit=False, 
                              cache_frame_data=False)


canvas2 = tkinter.Frame(master=root, width=500, height=300, bg="white") 
canvas2.pack(fill=tkinter.Y, side=tkinter.BOTTOM)


root.mainloop()



