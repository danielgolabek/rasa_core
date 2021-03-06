from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json

from httpretty import httpretty

from rasa_core import utils
from rasa_core.channels import console
from tests import utilities
from tests.conftest import MOODBOT_MODEL_PATH

# this is needed so that the tests included as code examples look better
MODEL_PATH = MOODBOT_MODEL_PATH


def test_console_input():
    import rasa_core.channels.console

    # Overwrites the input() function and when someone else tries to read
    # something from the command line this function gets called.
    with utilities.mocked_cmd_input(rasa_core.channels.console,
                                    text="Test Input"):
        httpretty.register_uri(httpretty.POST,
                               'https://abc.defg/webhooks/rest/webhook',
                               body='')

        httpretty.enable()
        console.record_messages(
                server_url="https://abc.defg",
                max_message_limit=3)
        httpretty.disable()

        assert (httpretty.latest_requests[-1].path ==
                "/webhooks/rest/webhook?stream=true&token=")

        b = httpretty.latest_requests[-1].body.decode("utf-8")

        assert json.loads(b) == {"message": "Test Input", "sender": "default"}


# USED FOR DOCS - don't rename without changing in the docs
def test_facebook_channel():
    from rasa_core.channels.facebook import FacebookInput
    from rasa_core.agent import Agent
    from rasa_core.interpreter import RegexInterpreter

    # load your trained agent
    agent = Agent.load(MODEL_PATH, interpreter=RegexInterpreter())

    input_channel = FacebookInput(
            fb_verify="YOUR_FB_VERIFY",
            # you need tell facebook this token, to confirm your URL
            fb_secret="YOUR_FB_SECRET",  # your app secret
            fb_access_token="YOUR_FB_PAGE_ACCESS_TOKEN"
            # token for the page you subscribed to
    )

    # set serve_forever=False if you want to keep the server running
    s = agent.handle_channels([input_channel], 5004, serve_forever=False)
    # END DOC INCLUDE
    # the above marker marks the end of the code snipped included
    # in the docs
    assert s.started
    routes_list = utils.list_routes(s.application)
    assert routes_list.get("/webhooks/facebook/").startswith(
            'fb_webhook.health')
    assert routes_list.get("/webhooks/facebook/webhook").startswith(
            'fb_webhook.webhook')
    s.stop()


# USED FOR DOCS - don't rename without changing in the docs
def test_slack_channel():
    from rasa_core.channels.slack import SlackInput
    from rasa_core.agent import Agent
    from rasa_core.interpreter import RegexInterpreter

    # load your trained agent
    agent = Agent.load(MODEL_PATH, interpreter=RegexInterpreter())

    input_channel = SlackInput(
            slack_token="YOUR_SLACK_TOKEN",
            # this is the `bot_user_o_auth_access_token`
            slack_channel="YOUR_SLACK_CHANNEL"
            # the name of your channel to which the bot posts (optional)
    )

    # set serve_forever=False if you want to keep the server running
    s = agent.handle_channels([input_channel], 5004, serve_forever=False)
    # END DOC INCLUDE
    # the above marker marks the end of the code snipped included
    # in the docs
    assert s.started
    routes_list = utils.list_routes(s.application)
    assert routes_list.get("/webhooks/slack/").startswith(
            'slack_webhook.health')
    assert routes_list.get("/webhooks/slack/webhook").startswith(
            'slack_webhook.webhook')
    s.stop()


# USED FOR DOCS - don't rename without changing in the docs
def test_mattermost_channel():
    from rasa_core.channels.mattermost import MattermostInput
    from rasa_core.agent import Agent
    from rasa_core.interpreter import RegexInterpreter

    # load your trained agent
    agent = Agent.load(MODEL_PATH, interpreter=RegexInterpreter())

    input_channel = MattermostInput(
            # this is the url of the api for your mattermost instance
            url="http://chat.example.com/api/v4",
            # the name of your team for mattermost
            team="community",
            # the username of your bot user that will post
            user="user@email.com",
            # messages
            pw="password"
            # the password of your bot user that will post messages
    )

    # set serve_forever=False if you want to keep the server running
    s = agent.handle_channels([input_channel], 5004, serve_forever=False)
    # END DOC INCLUDE
    # the above marker marks the end of the code snipped included
    # in the docs
    assert s.started
    routes_list = utils.list_routes(s.application)
    assert routes_list.get("/webhooks/mattermost/").startswith(
            'mattermost_webhook.health')
    assert routes_list.get("/webhooks/mattermost/webhook").startswith(
            'mattermost_webhook.webhook')
    s.stop()


# USED FOR DOCS - don't rename without changing in the docs
def test_telegram_channel():
    # telegram channel will try to set a webhook, so we need to mock the api

    httpretty.register_uri(
            httpretty.POST,
            'https://api.telegram.org/bot123:YOUR_ACCESS_TOKEN/setWebhook',
            body='{"ok": true, "result": {}}')

    httpretty.enable()

    from rasa_core.channels.telegram import TelegramInput
    from rasa_core.agent import Agent
    from rasa_core.interpreter import RegexInterpreter

    # load your trained agent
    agent = Agent.load(MODEL_PATH, interpreter=RegexInterpreter())

    input_channel = TelegramInput(
            # you get this when setting up a bot
            access_token="123:YOUR_ACCESS_TOKEN",
            # this is your bots username
            verify="YOUR_TELEGRAM_BOT",
            # the url your bot should listen for messages
            webhook_url="YOUR_WEBHOOK_URL"
    )

    # set serve_forever=False if you want to keep the server running
    s = agent.handle_channels([input_channel], 5004, serve_forever=False)
    # END DOC INCLUDE
    # the above marker marks the end of the code snipped included
    # in the docs
    assert s.started
    routes_list = utils.list_routes(s.application)
    assert routes_list.get("/webhooks/telegram/").startswith(
            'telegram_webhook.health')
    assert routes_list.get("/webhooks/telegram/webhook").startswith(
            'telegram_webhook.message')
    s.stop()
    httpretty.disable()


# USED FOR DOCS - don't rename without changing in the docs
def test_twilio_channel():
    from rasa_core.channels.twilio import TwilioInput
    from rasa_core.agent import Agent
    from rasa_core.interpreter import RegexInterpreter

    # load your trained agent
    agent = Agent.load(MODEL_PATH, interpreter=RegexInterpreter())

    input_channel = TwilioInput(
            # you get this from your twilio account
            account_sid="YOUR_ACCOUNT_SID",
            # also from your twilio account
            auth_token="YOUR_AUTH_TOKEN",
            # a number associated with your twilio account
            twilio_number="YOUR_TWILIO_NUMBER"
    )

    # set serve_forever=False if you want to keep the server running
    s = agent.handle_channels([input_channel], 5004, serve_forever=False)
    # END DOC INCLUDE
    # the above marker marks the end of the code snipped included
    # in the docs
    assert s.started
    routes_list = utils.list_routes(s.application)
    assert routes_list.get("/webhooks/twilio/").startswith(
            'twilio_webhook.health')
    assert routes_list.get("/webhooks/twilio/webhook").startswith(
            'twilio_webhook.message')
    s.stop()


def test_slack_init_one_parameter():
    from rasa_core.channels.slack import SlackInput

    ch = SlackInput("xoxb-test")
    assert ch.slack_token == "xoxb-test"
    assert ch.slack_channel is None


def test_slack_init_two_parameters():
    from rasa_core.channels.slack import SlackInput

    ch = SlackInput("xoxb-test", "test")
    assert ch.slack_token == "xoxb-test"
    assert ch.slack_channel == "test"


def test_is_slack_message_none():
    from rasa_core.channels.slack import SlackInput

    payload = {}
    slack_message = json.loads(json.dumps(payload))
    assert SlackInput._is_user_message(slack_message) is None


def test_is_slack_message_true():
    from rasa_core.channels.slack import SlackInput

    event = {'type': 'message',
             'channel': 'C2147483705',
             'user': 'U2147483697',
             'text': 'Hello world',
             'ts': '1355517523'}
    payload = json.dumps({'event': event})
    slack_message = json.loads(payload)
    assert SlackInput._is_user_message(slack_message) is True


def test_is_slack_message_false():
    from rasa_core.channels.slack import SlackInput

    event = {'type': 'message',
             'channel': 'C2147483705',
             'user': 'U2147483697',
             'text': 'Hello world',
             'ts': '1355517523',
             'bot_id': '1355517523'}
    payload = json.dumps({'event': event})
    slack_message = json.loads(payload)
    assert SlackInput._is_user_message(slack_message) is False


def test_slackbot_init_one_parameter():
    from rasa_core.channels.slack import SlackBot

    ch = SlackBot("DummyToken")
    assert ch.token == "DummyToken"
    assert ch.slack_channel is None


def test_slackbot_init_two_parameter():
    from rasa_core.channels.slack import SlackBot

    bot = SlackBot("DummyToken", "General")
    assert bot.token == "DummyToken"
    assert bot.slack_channel == "General"


# Use monkeypatch for sending attachments, images and plain text.
def test_slackbot_send_attachment_only():
    from rasa_core.channels.slack import SlackBot

    httpretty.register_uri(httpretty.POST,
                           'https://slack.com/api/chat.postMessage',
                           body='{"ok":true,"purpose":"Testing bots"}')

    httpretty.enable()

    bot = SlackBot("DummyToken", "General")
    attachment = json.dumps([{"fallback": "Financial Advisor Summary",
                              "color": "#36a64f", "author_name": "ABE",
                              "title": "Financial Advisor Summary",
                              "title_link": "http://tenfactorialrocks.com",
                              "image_url": "https://r.com/cancel/r12",
                              "thumb_url": "https://r.com/cancel/r12",
                              "actions": [{"type": "button",
                                           "text": "\ud83d\udcc8 Dashboard",
                                           "url": "https://r.com/cancel/r12",
                                           "style": "primary"},
                                          {"type": "button",
                                           "text": "\ud83d\udccb Download XL",
                                           "url": "https://r.com/cancel/r12",
                                           "style": "danger"},
                                          {"type": "button",
                                           "text": "\ud83d\udce7 E-Mail",
                                           "url": "https://r.com/cancel/r12",
                                           "style": "danger"}],
                              "footer": "Powered by 1010rocks",
                              "ts": 1531889719}])
    bot.send_attachment("ID", attachment)

    httpretty.disable()

    r = httpretty.latest_requests[-1]

    assert r.parsed_body == {'channel': ['General'],
                             'as_user': ['True'],
                             'attachments': [attachment]}


def test_slackbot_send_attachment_withtext():
    from rasa_core.channels.slack import SlackBot

    httpretty.register_uri(httpretty.POST,
                           'https://slack.com/api/chat.postMessage',
                           body='{"ok":true,"purpose":"Testing bots"}')

    httpretty.enable()

    bot = SlackBot("DummyToken", "General")
    text = "Sample text"
    attachment = json.dumps([{"fallback": "Financial Advisor Summary",
                              "color": "#36a64f", "author_name": "ABE",
                              "title": "Financial Advisor Summary",
                              "title_link": "http://tenfactorialrocks.com",
                              "image_url": "https://r.com/cancel/r12",
                              "thumb_url": "https://r.com/cancel/r12",
                              "actions": [{"type": "button",
                                           "text": "\ud83d\udcc8 Dashboard",
                                           "url": "https://r.com/cancel/r12",
                                           "style": "primary"},
                                          {"type": "button",
                                           "text": "\ud83d\udccb XL",
                                           "url": "https://r.com/cancel/r12",
                                           "style": "danger"},
                                          {"type": "button",
                                           "text": "\ud83d\udce7 E-Mail",
                                           "url": "https://r.com/cancel/r123",
                                           "style": "danger"}],
                              "footer": "Powered by 1010rocks",
                              "ts": 1531889719}])

    bot.send_attachment("ID", attachment, text)

    httpretty.disable()

    r = httpretty.latest_requests[-1]

    assert r.parsed_body == {'channel': ['General'],
                             'as_user': ['True'],
                             'text': ['Sample text'],
                             'attachments': [attachment]}


def test_slackbot_send_image_url():
    from rasa_core.channels.slack import SlackBot

    httpretty.register_uri(httpretty.POST,
                           'https://slack.com/api/chat.postMessage',
                           body='{"ok":true,"purpose":"Testing bots"}')

    httpretty.enable()

    bot = SlackBot("DummyToken", "General")
    url = json.dumps([{"URL": "http://www.rasa.net"}])
    bot.send_image_url("ID", url)

    httpretty.disable()

    r = httpretty.latest_requests[-1]

    assert r.parsed_body['as_user'] == ['True']
    assert r.parsed_body['channel'] == ['General']
    assert len(r.parsed_body['attachments']) == 1
    assert '"text": ""' in r.parsed_body['attachments'][0]
    assert '"image_url": "[{\\"URL\\": \\"http://www.rasa.net\\"}]"' \
           in r.parsed_body['attachments'][0]


def test_slackbot_send_text():
    from rasa_core.channels.slack import SlackBot

    httpretty.register_uri(httpretty.POST,
                           'https://slack.com/api/chat.postMessage',
                           body='{"ok":true,"purpose":"Testing bots"}')

    httpretty.enable()

    bot = SlackBot("DummyToken", "General")
    bot.send_text_message("ID", "my message")
    httpretty.disable()

    r = httpretty.latest_requests[-1]

    assert r.parsed_body == {'as_user': ['True'],
                             'channel': ['General'],
                             'text': ['my message']}
