import replicate

output = replicate.run(
    "stability-ai/stable-diffusion:ac732df83cea7fff18b8472768c88ad041fa750ff7682a21affe81863cbe77e4",
    input={
        "prompt": "a vision of paradise with ai and human coexisting"
    }
)
print(output)