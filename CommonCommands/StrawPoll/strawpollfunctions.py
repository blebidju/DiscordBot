import discord
import requests

def find_title(message):
    # this is the index of the first character of the title
    first = message.find('{') + 1
    # index of the last character of the title
    last = message.find('}')
    if first == 0 or last == -1:
        # TODO: Send a message telling the use how they are using it incorrectly.
        return "Not using the command correctly"
    return message[first:last]

def find_options(message, options):
    # first index of the first character of the option
    first = message.find('[') + 1
    # index of the last character of the title
    last = message.find(']')
    if (first == 0 or last == -1):
        if len(options) < 2:
            # TODO: Send a message telling the use how they are using it incorrectly.
            return "Not using the command correctly"
        else:
            return options
    options.append(message[first:last])
    message = message[last+1:]
    return find_options(message, options) 


async def makeStrawpoll(ctx, bot):
    message = ctx.message.clean_content

    title = find_title(message)

    options = find_options(message, [])
    
    requestData = {
            'poll': {
                'title': title,
                'answers': options
            }
        }
        
    headerData = {
            'Content-Type': 'application/json'
        }

    try:
        request = requests.post('https://strawpoll.com/api/poll', json = requestData, headers = headerData)
        print(request.text)
        await ctx.message.channel.send(
            "https://strawpoll.com/" + str(request.json()["content_id"])
        )
        
    except KeyError:
        return "Please make sure you are using the format '!strawpoll {title} [Option1] [Option2] [Option 3]'"