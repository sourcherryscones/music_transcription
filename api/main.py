from flask import request, jsonify, redirect, Blueprint, current_app, render_template, current_app, send_from_directory, send_file, url_for, session
import os
import re
import abjad


import scipy.io.wavfile as wf
from scipy import fftpack
import numpy as np


#WORKS ONLY WITH STEREO
#TO CHANGE TO MONO, LOOK AT LINE 43!!!
import math
def freq_to_note(freq):
    if freq < 16:
        return "rest", 0

    notes = ['a', 'as', 'b', 'c', 'cs', 'd', 'ds', 'e', 'f', 'fs', 'g', 'gs']

    note_number = 12 * math.log2(freq / 440) + 49
    note_number = round(note_number)

    note = (note_number - 1) % len(notes)
    note = notes[note]

    octave = (note_number + 8) // len(notes)

    return [note, octave]
def createFFT(clip, rate):#Takes the fft of the clip and normalizes it so it is easy to work with. It returns this array as well as the
    fftThing = fftpack.fft(clip)
    n = fftThing.size
    freq = np.fft.fftfreq(n, 1 / rate)
    f = abs(fftThing[0:int(n / 2)])
    w = freq[0:int(n / 2)]
    f /= len(f)
    return f, w

def pitchDict(filename):
    rate, samples = wf.read(filename)
    print(len(samples))
    print(int(60 * rate/ 500))
    tempo = 120
    NoteAndMeasure = {}

    for i in range(0, len(samples), int(60 * rate/ tempo)):
        clip = samples[i: i + rate]

        fleft, wleft = createFFT(clip[:,0], rate) #change clip[:,0] to clip for mono! it is currently in stereo format of clip[:,0]
        NoteAndMeasure.update({i/int(60 * 4 * rate/tempo) : freq_to_note(int(wleft[np.where(fleft == max(fleft))][0]))})
    lilyNotes = ''
    for beat, note in NoteAndMeasure.items():
        lilyNotes += note[0]
        lilyNotes += "4 "
        print('LILYNOTES IS')
        print(lilyNotes)

    return lilyNotes



from werkzeug.utils import secure_filename
main = Blueprint('main', __name__)

UPLOAD_FOLDER = './storage_temp'

def process_audio(input_file):
    output_dir = current_app.config['OUTPUT_FOLDER']
    string = pitchDict(input_file)
    voice = abjad.Voice(string, name="RH_Voice")
    staff = abjad.Staff([voice], name="RH_Staff")
    score = abjad.Score([staff], name="Score")
    path = input_file
    print("INPUT FILENAME:")
    output_filename = os.path.basename(path).split('/')[-1]
    abjad.persist.as_pdf(score, './output_cautious/' + output_filename) # probably needs to be changed
    return output_dir, output_filename

# ADVAIYT'S FUNCTION: DEF GENERATE_LILYPOND_FORMAT

@main.route('/')
def firstpage():
    return render_template('index.html')

@main.route('/postaudio', methods=['POST'])
def audio():
    fdata = dict(request.form)
    print(fdata)
    audio_file = request.files['audiophile']
    print('THE FOLLOWING SHOULD BE FORM DATA:')
    print(audio_file)
    if audio_file.filename == '':
        return '<h>NO FILE UPLOADED HAHA L BOZO SOMETHING SOMETHING IDK SLANG</h1>'
    if audio_file:
        filename = secure_filename(audio_file.filename)
        file_loc = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        print(file_loc)
        audio_file.save(file_loc)
        opdir, opfile = process_audio(file_loc)
        # return send_from_directory(opdir, opfile)
        pp = "http://localhost/output_cautious/" + opfile
        session['opfile'] = opfile
        session['pp'] = pp
        return redirect('/testing/' + opfile)

    # THE ABOVE WORKS
    # return send_from_directory(current_app.config['UPLOAD_FOLDER_OUTPUT'], filename)


@main.route('/showoutput')
def show():

    print(current_app.config['OUTPUT_FOLDER'])
    return send_from_directory(current_app.config['OUTPUT_FOLDER'], 'sargamTest.wav')

@main.route('/temp')
def temp():
    return '<h1>hello world!</h1>'

@main.route('/testing/<path:filename>')
def see_file(filename):
    filename = filename[:len(filename)-3] + 'pdf'
    print(filename)
    print(current_app.config['OUTPUT_FOLDER'])
    print('ROOT APP IS')
    print(current_app.root_path)
    print(current_app.instance_path)
    return send_from_directory(current_app.config['OUTPUT_FOLDER'], filename)


