import speech_recognition as sr
import pyttsx3
speak = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
def Speech(audio,voice_type=voice_id, speed=125):
    
	engine.setProperty('rate', speed)
	# Use given voice
	engine.setProperty('voice', voice_type)
	engine.say(audio)
	engine.runAndWait()
    
def voice ():
		
		try:
			with sr.Microphone() as mic:
	
		# adjust the energy threshold based on
				# the surrounding noise level
				speak.adjust_for_ambient_noise(mic)
				
		
		# listens for the user's input
				searchquery = speak.listen(mic)
		
		# Using google to recognize audio
				MyText = speak.recognize_google(searchquery)
				text = MyText.lower()
				return text
		except Exception as e:
			pass
			#return type(e).__name__ +"occured."
if __name__ == '__main__':
    Speech("hello sir")
    voice()