import multiprocessing
import json
import openai
import wikipedia as wk
from apis.voice_recognition_module import Speech, voice

class VoiceInteractionHandler:
    def __init__(self, api):
        self.is_listening = False
        self.count=0
        self.api_key = api
        self.load_knowledge_base()
        self.gpt3_temperature = 0.7
    def query_gpt3(self, input_text):
        try:
            openai.api_key = self.api_key
            response = openai.Completion.create(
            engine="davinci",
            prompt=input_text,
            max_tokens=50,
            temperature=self.gpt3_temperature
            )
            return response.choices[0].text.strip()
        except Exception as e:
            self.search_wikipedia(input_text)
    def train(self, user_input, user_feedback):
        self.knowledge_base[user_input] = user_feedback
        self.save_knowledge_base()

    def search_wikipedia(self, query):
        try:
            wk.set_lang("en")
            page = wk.page(query)
            if page.pageid!='':
                return page.summary
        except wk.exceptions.DisambiguationError as e:
            return 'similar topics found '+ e.options
        except Exception as e:
            return self.query_gpt3("tell me about "+query)
    def save_knowledge_base(self):
        with open('knowledge_base.json', 'w') as file:
            json.dump(self.knowledge_base, file)

    def load_knowledge_base(self):
        try:
            with open(r'knowledge_base.json', 'r') as file:
                self.knowledge_base = json.load(file)

        except FileNotFoundError:
            self.knowledge_base = {}
    def start_listening(self,count):
        
        if not self.is_listening:
            self.is_listening = True
            self.callback_process = multiprocessing.Process(target=self.listen)
            
            self.callback_process.start()
    def standby(self):
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):
            try:
                Speech("Standby for voice authentication system")
                Speech("Tell the voice authentication password")
                print("Standby for voice authentication system\ntell the voice authentication password")
                passwd = voice()
                keydict = {"jarvis": 1208, "arya": 1312, "gpt 4": 1909}
                if passwd in keydict:
                    self.count += 1                    
                    self.listen()
                else:
                    Speech("Authentication failed. Please try again.")
            except Exception as e:
                Speech("An error occurred during voice authentication. Please try again.")
                print(e)
            if attempt < max_attempts:
                pass
        else:
            Speech("Voice authentication failed after 3 attempts. Exiting.")
            self.exit()
            
    def listen(self):
        Speech("Hello! I AM ALIAB which stands for Ai with learning intelligence Algorithm and Database.")
        Speech("I have access to all of the internet and also having access to the gpt3 ai model.")
        while True:
            try:
                Speech("what can i do for you today")
                user_input = voice().lower()
                print("You: " + user_input)
                self.runloop(user_input)
                    
            except AttributeError:
                pass
            except Exception as e:
                Speech("An error occurred. Please try again.")
                Speech(e)
    def runloop(self,user_input):
        try:
                if 'exit' in user_input:
                    self.exit()

                if user_input in self.knowledge_base:
                    Speech(self.knowledge_base[user_input])
                    print("ALIAB: ", self.knowledge_base[user_input])
                elif user_input.startswith("tell me about "):
                    topic = user_input.replace("tell me about ","")
                    Speech("searching on wikipedia")

                    response = self.search_wikipedia(topic)
                    Speech(response)
                    print("ALIAB: ", response)
                    Speech("did i answer the question correctly ?")
                    user_feedback = voice().lower()
                    if user_feedback == 'no':
                        Speech("enter correct response")
                        user_feedback = input("enter correct response")
                        self.train(user_input, user_feedback)
                    else:
                        self.train(user_input, response)
                else:
                    response = self.query_gpt3(f"User: {user_input}\nAI:")
                    Speech(response)
                    print("ALIAB: ", response)
                    user_feedback = voice()
                    if user_feedback==None:
                        user_feedback=="yes"
                    else:
                        user_feedback.lower()
                    if user_feedback == 'no':
                        Speech("enter correct response")
                        user_feedback = input("enter correct response")
                        self.train(user_input, user_feedback)
                    else:
                        self.train(user_input, response)
        except AttributeError:
                pass
        except Exception as e:
                Speech("An error occurred. Please try again.")
                Speech(e)
    def stop_listening(self):
        self.is_listening = False
        self.callback_process.terminate()
    def exit(self):
        self.stop_listening()
        exit(Speech('goodbye'))