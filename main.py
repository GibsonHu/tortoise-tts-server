from flask import Flask
# !pip install flask flask-restful
from flask_restful import Resource, Api, reqparse
from flask import send_from_directory
import pandas as pd
import ast
import os
from api import TextToSpeech, MODELS_DIR
from utils.audio import load_voices, load_audio
import torch
import torchaudio

voice_sel = 'barney'
test_txt = 'Testing Server Audio Sampl'

app = Flask(__name__, static_folder='results')
api = Api(app)
print('initialising tts...')
tts = TextToSpeech()
print('init completed')



@app.route('/tts/<path:filename>')  # for per-URL settings
def send_data(filename):
	print(filename)
	return send_from_directory(app.static_folder, filename,as_attachment=True)

class TTS(Resource):

	def get(self):
		voice_samples, conditioning_latents = load_voices([voice_sel])
		print('generating tts module')
		gen, dbg_state = tts.tts_with_preset(test_txt, k=2, voice_samples=voice_samples, conditioning_latents=conditioning_latents,
								  preset='ultra_fast', use_deterministic_seed=None, return_deterministic_state=True, cvvp_amount=.0)

		if isinstance(gen, list):
			for j, g in enumerate(gen):
				output_path = os.path.join('results/', f'{voice_sel}_{j}.wav')
				print(output_path)
				torchaudio.save(output_path, g.squeeze(0).cpu(), 24000)
		else:
			return 'Error in Saving'
				   
		print('predicting .. ')
		return send_from_directory(app.static_folder, 'barney_0.wav',as_attachment=True)
	

	def post(self):
		parser = reqparse.RequestParser()  # initialize
	   
	def put(self):
		parser = reqparse.RequestParser()  # initialize
	   

	def delete(self):
		parser = reqparse.RequestParser()  # initialize
	   


api.add_resource(TTS, '/tts')  # add endpoints

if __name__ == '__main__':
	app.run()  # run our Flask app