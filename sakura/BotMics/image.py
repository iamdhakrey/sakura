
import PIL
from PIL import Image, UnidentifiedImageError
from PIL import ImageOps
from PIL import ImageDraw
from PIL import ImageFont
import os
from random import choice,randint
import requests
from io import BytesIO

from django.conf import settings
ROOT_PATH = str(settings.MEDIA_ROOT)
def save_image(bot,guild,member):
    is_w_images = False
    count_list = []
    for i in range(5):
        if os.path.isfile(os.path.join(ROOT_PATH,"images/backgrounds/"+str(guild.id)+'/'+str(guild.id)+"_"+str(i)+".jpg")):
            is_w_images = True
            count_list.append(i)
        else:
            pass

    if len(count_list) == 0:
        image_num = randint(1,5)
    else:
        image_num = choice(count_list)

    W,H = 1920,872
    # messeges
    hello = "Hey Buddy,"
    username = str(bot.get_user(member.id))
    msg = 'You Are {}th Member of The Server'.format(guild.member_count)
    url = requests.get(member.avatar_url)
    avatar = Image.open(BytesIO(url.content))
    avatar = avatar.resize((380, 380))
    bigsize = (avatar.size[0] * 3,  avatar.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(avatar.size)
    avatar.putalpha(mask)
    output = ImageOps.fit(avatar, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)
    output.save(str(ROOT_PATH)+'/images/'+str(guild.id)+'/avatar.png')
    ava = Image.open(str(ROOT_PATH)+'/images/'+str(guild.id)+'/avatar.png')
    ava_draw = ImageDraw.Draw(ava)
    ava_draw.arc((0, 0, 380, 380), start=0, end=360, fill=(194,83,111),width=12)
    ava.save(str(ROOT_PATH)+'/images/'+str(guild.id)+'/avatar.png')
    if is_w_images:
        welc = Image.open(ROOT_PATH+'/images/backgrounds/'+str(guild.id)+"/"+str(guild.id)+"_"+str(image_num)+'.jpg' )
    else:
        welc = Image.open(ROOT_PATH+'/default/welcome'+str(image_num)+'.jpg' )
    font1 = ImageFont.truetype(ROOT_PATH+'/fonts/UbuntuMono-B.ttf', 90)
    font2 = ImageFont.truetype(ROOT_PATH+'/fonts/Caveat-Bold.ttf', 100)
    welc_draw = ImageDraw.Draw(welc)
    hello_w,hello_h = welc_draw.textsize(hello,font2)
    user_w,user_h = welc_draw.textsize(username,font1)
    msg_w,msg_h = welc_draw.textsize(msg,font2)
    welc_draw.text(xy=((W-hello_w)/2,(H-hello_h)/1.44), text=hello, fill=(190,222,203), font=font2,align='center')
    welc_draw.text(xy=((W-user_w)/2,(H-user_h)/1.2), text=username, fill=(222,239,90), font=font1,align='center')
    welc_draw.text(xy=((W-msg_w)/2,(H-msg_h)/1), text=msg, fill=(248,206,160), font=font2,align = 'center')
    welc.paste(ava, (760, 150), ava)
    welc.save(str(guild.id)+'_out_welcome.png', format='PNG')