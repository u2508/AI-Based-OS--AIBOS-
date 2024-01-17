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
def Opengpt(input1):
  output = replicate.run(
  "replicate/vicuna-13b:6282abe6a492de4145d7bb601023762212f9ddbbe78278bd6771c8b3b2f2a13b",
  input={
    "seed": -1,
    "debug": False,
    "top_p": 1,
    "prompt": input1,
    "max_length": 500,
    "temperature": 0.75,
    "repetition_penalty": 1
  }
)
  output_text = ''.join(str(item) for item in output)
  return output_text
def Google_Summarizer(input1):
  output = replicate.run(
  "replicate/flan-t5-xl:7a216605843d87f5426a10d2cc6940485a232336ed04d655ef86b91e020e9210",
  input={
    "debug": False,
    "top_p": 0.95,
    "prompt": "Answer the following yes/no question by reasoning step by step. Can a dog drive a car?",
    "max_length": 50,
    "temperature": 0.7,
    "repetition_penalty": 1
  }
)

if __name__=='__main__':
    print(Opengpt("tell me about chatgpt in the form of a poem in the style of jk rowling in 4 lines"))
