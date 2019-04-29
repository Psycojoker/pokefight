import os
import argh
import shutil
import tempfile

from urllib import urlretrieve

from mastodon import Mastodon
from PIL import Image, ImageDraw, ImageFont


TEMPLATE = os.path.join(os.path.realpath("."), "./template_gold_2.png")
FONT = os.path.join(os.path.realpath("."), 'font/Pokemon GB.ttf')


class Player():
    def __init__(self, name, acct, level, image):
        self.name = name.upper()
        self.acct = acct
        self.level = str(level)
        self.image = image


def pixelise(image, side=120, resize_side=40):
    def _to_16bits(number):
        return int((((number + 1) / 16) * 16) - 1)

    image = image.resize((resize_side, resize_side), Image.NEAREST)
    image = image.resize((side, side), Image.NEAREST)

    pixel = image.load()

    for i in range(0, image.size[0]):
        for j in range(0, image.size[1]):
            try:
                pixel[i,j] = tuple(map(_to_16bits, pixel[i, j]))
            except Exception:
                pass

    return image.convert("P", palette=Image.ADAPTIVE)


def generate_images(attacker, defender, power, text=("It's super-", "effective!")):
    template = Image.open(TEMPLATE)
    template = template.convert("RGBA")

    # duplicate image for alpha handling (weird stuff)
    template.paste(pixelise(attacker.image), (18, 70), pixelise(attacker.image).convert("RGBA"))
    template.paste(pixelise(defender.image, side=100, resize_side=50), (195, 10), pixelise(defender.image, side=100, resize_side=50).convert("RGBA"))

    font = ImageFont.truetype(FONT, 14)
    level = ImageFont.truetype(FONT, 14)

    draw = ImageDraw.Draw(template)

    draw.text((160, 118), attacker.name, font=font, fill="black")
    draw.text((240, 131), (attacker.level), font=level, fill="black")
    draw.text((18, 5), defender.name.upper(), font=font, fill="black")
    draw.text((110, 19), defender.level, font=level, fill="black")

    template.resize((640, 576))

    action = template.copy()
    draw = ImageDraw.Draw(action)
    draw.text((18, 225), attacker.name, font=font, fill="black")
    draw.text((18, 255), 'used %s!' % power.upper(), font=font, fill="black")

    result = template.copy()
    draw = ImageDraw.Draw(result)
    draw.text((18, 225), text[0], font=font, fill="black")
    draw.text((18, 255), text[1], font=font, fill="black")

    return action, result


def get_user_name_avatar(mastodon, mastodon_name):
    local_user_id = mastodon.search(mastodon_name)["accounts"][0]["id"]

    account = mastodon.account(local_user_id)

    if "#nobot" in account.note:
      raise Exception # TODO

    return account["username"], account["acct"], account["avatar_static"]


def fill_users(mastodon, attacker, defender):
    level = 15

    try:
        working_dir = tempfile.mkdtemp()
        current_directory = os.path.realpath(os.curdir)
        os.chdir(working_dir)

        username, acct, avatar_url = get_user_name_avatar(mastodon, attacker)
        filename, _ = urlretrieve(avatar_url)
        attacker = Player(username, acct, level, Image.open(filename))

        username, acct, avatar_url = get_user_name_avatar(mastodon, defender)
        filename, _ = urlretrieve(avatar_url)
        defender = Player(username, acct, level, Image.open(filename))
    except Exception as e:
        raise e
    finally:
        os.chdir(current_directory)
        shutil.rmtree(working_dir, ignore_errors=True)

    return attacker, defender


def main(attacker, defender, power, effective=True):
    mastodon = Mastodon(client_id='pokefight.secret', access_token='user_pokefight.secret', api_base_url='https://botsin.space')

    attacker, defender = fill_users(mastodon, attacker, defender)

    action, result = generate_images(attacker, defender, power, text=("It's super-", "effective!") if effective else ("It's not very", "effective..."))

    base_filename = "%s_%s_%s" % (attacker.name, defender.name, power)


    if not os.path.exists("fights"):
        os.makedirs("fights")

    action.save("fights/" + base_filename + "_action.png")
    result.save("fights/" + base_filename + "_result.png")

    print base_filename + "_action.png"
    print base_filename + "_result.png"


if __name__ == '__main__':
    argh.dispatch_command(main)
