import os
import re
import time
import html2text

from mastodon import Mastodon

from fight import generate_images, fill_users

REGEX = re.compile("@pokefight ([a-zA-Z.@]+) used (.+) on ([a-zA-Z.@]+), (effective|not effective)")

def main():
    if not os.path.exists("bot-fights"):
        os.makedirs("bot-fights")

    h = html2text.HTML2Text()
    h.ignore_links = True

    mastodon = Mastodon(client_id='pokefight.secret', access_token='user_pokefight.secret', api_base_url='https://social.wxcafe.net')

    if os.path.exists(".since_id") and open(".since_id").read().isdigit():
        since_id = int(open(".since_id").read())
    else:
        since_id = 0

    while 42:
        for i in reversed(mastodon.notifications(since_id=since_id)):
            # we don't care about the rest
            if i["type"] != "mention":
                continue

            status = i["status"]
            status_id = status["id"]
            visibility = status["visibility"]

            since_id = max(since_id, i["id"])

            message = h.handle(status["content"]).strip()
            # repr to avoid writting on several lines
            print "[%s] %s" % (i["id"], repr(message))

            if not message.startswith("@pokefight"):
                # we ignore status where we aren't directly mentionned
                continue

            match = REGEX.search(message.lower())

            if not match:
                # answer that you've failed
                print "message '%s' didn't matched regex" % message
                continue

            attacker, power, defender, effectiveness = match.groups()

            effective = effectiveness == "effective"

            attacker, defender = fill_users(mastodon, attacker, defender)

            action, result = generate_images(attacker, defender, power, text=("It's super-", "effective!") if effective else ("It's not very", "effective..."))

            action_filename = "bot-fights/" + str(status_id) + "_action.png"
            result_filename = "bot-fights/" + str(status_id) + "_result.png"

            action.save(action_filename)
            result.save(result_filename)
            print "-> %s %s" % (action_filename, result_filename)

            action_media_post = mastodon.media_post(action_filename)
            result_media_post = mastodon.media_post(result_filename)

            mastodon.status_post(
                ".%s used %s on %s! (from @%s)" % (attacker.acct, power, defender.acct, i["account"]["acct"]),
                in_reply_to_id=status_id,
                media_ids=[action_media_post, result_media_post],
                visibility=visibility,
            )

        # open(".since_id", "w").write(str(since_id))
        time.sleep(5)



if __name__ == '__main__':
    main()
