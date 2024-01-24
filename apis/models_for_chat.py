import replicate
def llm(input1):
    output = replicate.run(
  "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
  input={
    "debug": False,
    "top_k": 50,
    "top_p": 1,
    "prompt": input1,
    "temperature": 0.5,
    "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe.You are the smartest one in the room and very very cool in attitude and you never break character.  Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
    "max_new_tokens": 4000,
    "min_new_tokens": -1
  }
    )
    output_text = ''.join(str(item) for item in output)
    return output_text
def llama(input1):
  # The meta/llama-2-13b-chat model can stream output as it's running.
  arr=[]
  for event in replicate.stream(
    "meta/llama-2-13b-chat",
    input={
        "debug": False,
        "top_k": 50,
        "top_p": 1,
        "prompt": input1,
        "temperature": 0.75,
        "system_prompt": "You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
        "max_new_tokens": 2000,
        "min_new_tokens": -1
    },
  ):
    arr.append(str(event))
  output_text = ''.join(str(item) for item in arr)
  return output_text  
def Opengpt(input1):
  output = replicate.run(
  "replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b",
  input={
    "seed": -1,
    "debug": False,
    "top_p": 1,
    "prompt": input1,
    "max_length": 2000,
    "temperature": 0.75,
    "repetition_penalty": 1
  })
  output_text = ''.join(str(item) for item in output)
  return output_text
def chat_with_ai(input1):
  output = replicate.run(
    "replicate/dolly-v2-12b:ef0e1aefc61f8e096ebe4db6b2bacc297daf2ef6899f0f7e001ec445893500e5",
    input={
        "top_k": 50,
        "top_p": 1,
        "prompt": input1,
        "decoding": "top_p",
        "max_length": 500,
        "temperature": 0.75,
        "repetition_penalty": 1.2
    })  
  output_text = ''.join(str(item) for item in output)
  return output_text
def text_to_img(input1):
  output = replicate.run(
    "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
    input={"width": 768,
        "height": 768,
        "prompt": input1,
        "scheduler": "K_EULER",
        "num_outputs": 1,
        "guidance_scale": 7.5,
        "num_inference_steps": 50
    })
  return output
if __name__=='__main__':
    print(Opengpt("tell me about chatgpt in the form of a poem in the style of jk rowling in 4 lines"))
