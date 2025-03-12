import openai

openai.api_key = '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'

running = True
while running:
    question = str(input('What program do you want to write?'))

    if question.upper() == 'STOP':
        break
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
        {'role':'system','content':'you are a robot'},
        {'role':'system','content':f'code {str(question)} in python'},
        ]
    )

    result = []
    for choice in response.choices:

        result.append(choice.message.content)

    openfile = open('gptcreatedcode.txt','w')
    for i in range(1,len(result)):
        openfile.write(result[i])
        print(result[i])
    openfile.close()

    print(result)