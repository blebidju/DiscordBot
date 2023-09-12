import discord
import random

from PIL import Image
import requests

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

async def pinMessage(ctx, bot):
    message = ctx.message.clean_content

    options = find_options(message, [])

    await pinMessageForReal(bot, await ctx.message.channel.fetch_message(options[0]))
    
    await ctx.message.channel.send("test")
    
async def pinMessageForReal(bot, message):
    """Forwards a message to the archive channel."""
    pinChannelID = "Redacted";
    channel = bot.get_channel(pinChannelID)
    
    avatar = message.author.avatar_url
     
    #urllib.request.urlretrieve(avatar, "local-filename.webp")
    img_data = requests.get(avatar).content
    with open('avatar.webp', 'wb') as handler:
        handler.write(img_data)
        
    img = Image.open("avatar.webp")
    rgb = get_dominant_color(img)
    
    try:
        name = message.author.display_name 
        avatar = message.author.avatar_url
        pin_content = message.content 
        server = message.guild.id 
        current_date = datetime.datetime.utcfromtimestamp(int(time.time())) 
 
        emb = discord.Embed( 
            description=pin_content, 
            color=discord.Color.from_rgb(rgb[0], rgb[1], rgb[2]), 
            timestamp=current_date)  # Initalizes embed with description pin_content. 
        emb.set_author( 
            name=name, 
            icon_url=avatar, 
            url='https://discordapp.com/channels/{0}/{1}/{2}'.format( 
                server, message.channel.id, message.id) 
            )  # Sets author and avatar url of the author of pinned message. 
 
            # Set attachemnt image url as embed image if it exists 
        if message.attachments: 
            img_url = message.attachments[0].url 
            emb.set_image(url=img_url) 
 
        # Sets footer as the channel the message was sent and pinned in. 
        emb.set_footer(text='Sent in #{}'.format(message.channel)) 
 
        channel.send(embed=emb) 
 
    except discord.errors.Forbidden: 
        await error(message, 'Pin Archiver does not have permission to send messages in #pin-archive.')
        
def get_dominant_color(pil_img, palette_size=16):
    # Resize image to speed up processing
    img = pil_img.copy()
    img.thumbnail((100, 100))

    # Reduce colors (uses k-means internally)
    paletted = img.convert('P', palette=Image.ADAPTIVE, colors=palette_size)

    # Find the color that occurs most often
    palette = paletted.getpalette()
    color_counts = sorted(paletted.getcolors(), reverse=True)
    palette_index = color_counts[0][1]
    dominant_color = palette[palette_index*3:palette_index*3+3]

    return dominant_color

