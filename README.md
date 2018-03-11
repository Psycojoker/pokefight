![demo.gif](demo.gif)

A stupid bot that generate images like the one above between 2 mastodon users.

# Installation

You need to have virtualenv installed, on debian/ubuntu:

    sudo apt-get install python-virtualenv

You also need dependencies to compile the python libs. On debian/ubuntu that looks like this:

    sudo apt-get install python-dev python-setuptools libtiff5-dev libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev libharfbuzz-dev libfribidi-dev tcl8.6-dev tk8.6-dev python-tk

And ffmpeg to generate the mp4:

    sudo apt-get install ffmpeg

Then:

    git clone https://github.com/psycojoker/pokefight
    cd pokefight
    virtualenv ve
    ve/bin/pip install -r requirements.txt

Then you need to register the bot on the mastodon by doing (you need an account on a mastodon instance):

    ve/bin/python register.py

Then, you can launch the bot with:

    ve/bin/python bot.py

There is also a standalone script that more or less work to generate 2 images offline:

    ve/bin/python fight.py username@domain.com another_user@domain.com "some power"
