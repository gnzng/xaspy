import os
from tele_bot import run

# Main entrypoint
def main():

    try:
        with open('api.key') as f:
            bot_token = str(f.readline())
        f.close()
    except KeyError:
        print('The environment variable BOT_TOKEN is not defined')
        exit(1)

    run(bot_token)


if __name__ == "__main__":
    main()