import asyncio
from asyncio import tasks
import discord
from discord.ext import tasks
import openai
from discord import FFmpegPCMAudio, app_commands
from discord.ext import commands
import random
import os
from dotenv import load_dotenv 
import time
from datetime import datetime, timedelta
from quote import quote
import csv
import randfacts
import math
import requests
import aiohttp
from dadjokes import Dadjoke
import ast

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
openai.api_key = os.getenv('API_KEY')


CHANNEL_ID = 947902507437391924
# client = commands.Bot(command_prefix="!", intents=discord.Intents.all()) 
# tree = app_commands.CommandTree(client)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all(), case_insensitive=True)

userSession = {}
huggingFaceToken = os.getenv("HUGGINGFACE_TOKEN")
HEADERS = {
    "Authorization": f"Bearer {huggingFaceToken}"
}
API = "https://api-inference.huggingface.co/google/flan-t5-base"
global secretWords
secretWords = ast.literal_eval(os.getenv("SECRET_WORD"))





@bot.event
async def on_ready():
    print("im ready")
    bigBenAUTO.start()
    quoteOfTheDay.start()
    await bot.tree.sync()
    channel = bot.get_channel(CHANNEL_ID)



# AUTO ADJECTIVE COMMAND / RANDOMBALL (8ball)

adjectives = ["attractive", "bald", "beautiful", "chubby", "clean", "dazzling", "drab", "elegant", "fancy", "fit", "fat", "flabby", "glamorous", "gorgeous", "handsome", "magnificent", "muscular", "skinny", "plain", "plump", "scruffy", "rizzy", "stocky", "unkempt", "unsightly", "agreeable", "ambitious", "brave", "calm", "delightful", "eager", "faithful", "gentle", "happy","angry", "sad", "lively", "nice", "mean", "witty", "fuckin stupid", "clumsy", "fierce", "grumpy", "helpless", "itchy", "stroking", "lubed up", "big", "colossal", "gigantic", "great", "huge", "immense", "large", "little", "mammoth", "tiny", "gay", "straight", "gang", "on gang this is", "on my mother", "im so zesty... also", "i wanna fuck", "is this", "was this", "salad bacon cheese oh my god", "flumpy", "plumpy", "fraser reminds me of", "raph reminds me of", "donald reminds me of", "clunie reminds me of", "cookies", "i really want cookies but i just wanna say that", "yummers", "3.1415926535897932", "women are kinda like", "men are kinda like", "women", "r", "maybe", "i do not know the answer to your question however i do have to say", "eh", "meh", "neh", "nah", "yea", "duh", "mmmmmeh", "huh? i thought", "huh?", "huh", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"]

effect = False
question = False
question_user_id = None
measure = False
suffixOn = False
timerOn = False
guessTheNumOn = False
gptQuestion = False
rouletteOn = False
rpsOn = False
dice = False
busOn = False
colourGuess = False
valueGuess = False
rangeGuess = False
suitGuess = False
cardsCalled = []
aiOn = False
totalCount = 0
guessTheNumTarget = None  # Store the target number for the guessing game

def startBus():
    global colourGuess, valueGuess, rangeGuess, suitGuess, cardsCalled
    colourGuess = True
    valueGuess = False
    rangeGuess = False
    suitGuess = False
    cardsCalled = []
answers = ['yes', 'no', 'ask your mother', 'definitely', 'that is absolutely true', 'very no', 'absolutely not', 'not at all true', 'that is false', 'I do not care', 'this is not my business', 'and why is that my problem?', 'get raph to answer this idk', 'just because im an 8ball doesnt mean i can fix all of your problems', 'why?', 'who?', 'how?', 'how does society accept this at all?', 'elon musk might have something to say about that', 'come out already', 'this is so not right', 'nuh uh', 'yuh huh', 'perchance...']
## ON MESSAGE ###

@bot.event
async def on_message(message):
    global effect, question, question_user_id, measure, suffixOn, timerOn, guessTheNumOn, gptQuestion, messages, rpsOn, diceNumbers, dice, rouletteOn, busOn, colourGuess, valueGuess, rangeGuess, suitGuess, cardsCalled, aiOn, totalCount

    if message.author.bot:
        return
    
    if message.author.id != bot.user.id:
        words = message.content.split()
        if secretWords:
            secretWordList = [w.strip().lower() for w in secretWords]
            for word in words:
                if word.lower() in secretWordList:
                    print(f"Secret word '{word}' found!")
                    fieldNamesWord = ['Name', 'TotalCount']
                    usernameWord = message.author.name
                    updatedWord = False
                    if os.path.exists('word.csv'):
                        with open('word.csv', 'r', newline='') as csvfile:
                            reader = csv.DictReader(csvfile, fieldnames=fieldNamesWord)
                            data = list(reader)
                    else:
                        data = []

                    for row in data:
                        if row['Name'] == usernameWord:
                            row['TotalCount'] = str(int(row['TotalCount']) + 1)
                            updatedWord = True
                            totalCount = int(row['TotalCount'])
                            break

                    if not updatedWord:
                        totalCount = 1
                        data.append({'Name': usernameWord, 'TotalCount': str(totalCount)})

                    with open('word.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldNamesWord)
                        writer.writerows(data)

                    print(f'Count for {usernameWord}: {totalCount}')

    #lewisEffect
    if effect and message.author.id != bot.user.id:
        await message.channel.send(random.choice(adjectives) + " " + message.content)

    #randomBall
    if question and message.author.id == question_user_id and message.author.id != bot.user.id:
        await message.channel.send("You asked: "+ message.content + "\nAnswer: " + random.choice(answers))
        question = False
        question_user_id = None
    

    #Ruler
    if measure and message.author.id != bot.user.id:
        await message.channel.send('The length of ' + message.content + ' is ' + str(random.randint(0, 5000)) + ' ' + random.choice(measurements))
        measure = False

    #Inger
    if suffixOn and message.author.id != bot.user.id:

        words = message.content.split()
        suffixed = [word + random.choice(suffix) for word in words]
        suffixed = ' '.join(suffixed)
        await message.channel.send(suffixed)

    if guessTheNumOn and message.author.id != bot.user.id:
        
        global guessTheNumTarget, timerOn

        
        if guessTheNumTarget is None:
            guessTheNumTarget = random.randint(1, 40)
            print(f"Target number for guessing game: {guessTheNumTarget}")

            async def guess_timer(channel):
                global timerOn, guessTheNumOn, guessTheNumTarget
                await asyncio.sleep(20)
                if guessTheNumOn:
                    await channel.send(f'You lose! The number was {guessTheNumTarget}')
                    guessTheNumOn = False
                    timerOn = False
                    guessTheNumTarget = None

            if not timerOn:
                timerOn = True
                bot.loop.create_task(guess_timer(message.channel))

        try:
            userGuess = int(message.content.strip())
        except ValueError:
            await message.channel.send('Please enter a valid number!')
            return

        if timerOn and guessTheNumOn:
            if userGuess == guessTheNumTarget:
                await message.channel.send('Congrats, you win!')
                guessTheNumOn = False
                timerOn = False
                guessTheNumTarget = None
            else:
                await message.channel.send('Wrong guess, try again!')

    if rpsOn and message.author.id != bot.user.id:
        userRpsGuess = message.content.lower()
        rpsChoices = ['rock', 'paper', 'scissors']

        if userRpsGuess in rpsChoices:
            botChoice = random.choice(rpsChoices)
            await message.channel.send(botChoice)

            if userRpsGuess == rpsChoices[0] and botChoice == rpsChoices[1] or userRpsGuess == rpsChoices[2] and botChoice == rpsChoices[0] or userRpsGuess == rpsChoices[1] and botChoice == rpsChoices[2]:
                await message.channel.send('I won!')
                rpsOn = False
            
            elif userRpsGuess == rpsChoices[0] and botChoice == rpsChoices[2] or userRpsGuess == rpsChoices[2] and botChoice == rpsChoices[1] or userRpsGuess == rpsChoices[1] and botChoice == rpsChoices[0]:
                await message.channel.send('I lost!')
                rpsOn = False

            else:
                await message.channel.send('Tie!')
                rpsOn = False
        
        else:
            await message.channel.send('Put in a choice (rock, paper, scissor)')


    if dice == True and message.author.id != bot.user.id:
        if message.content.isdigit():
            userDiceNum = int(message.content)
            diceNumber = random.randint(1, 6)

            if userDiceNum != diceNumber:
                await message.channel.send(f'nuh uh WRRRROOOOOOOOOOOOOOOOONG it was {diceNumber}')
                dice = False
            else:
                await message.channel.send('You got it!!!! HAAA!')
                dice = False

        else:
            await message.channel.send('NUMBER IDIOTTTTTTTTTTAAAAAA SHHHHHHHHH!!!')
            dice = False


    if rouletteOn and message.author.id != bot.user.id:



        #user variables
        global username
        username = message.author.name
        global fieldNames
        fieldNames = ['Name', 'Tokens']
        global userTokens
        userTokens = 0
        global nameFound
        nameFound = False
        
        #bet variables
        global betOn
        betOn = False
        global to12
        to12 = False
        global to24
        to24 = False
        global to36
        to36 = False
        global userRouletteGuessBool
        userRouletteGuessBool = False
        global userRouletteNumBool
        userRouletteNumBool = False
        global updated
        updated = False

        
        #user tokens init / find

        with open('stats.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldNames)
            data = list(reader)


        for row in data:
            if row['Name'] == username:
                userRow = row['Tokens'] = str(int(row['Tokens']))
                updated = True
                break

        if not updated:
            data.append({'Name': username, 'Tokens': str(userTokens)})

        
        global betAmount
        betAmount = int(userRow) / 10


    #check message


        if message.content.lower() == "1st 12" and message.author.id != bot.user.id:
            to12 = True
            betOn = True
        
        elif message.content.lower() == "2nd 12" and message.author.id != bot.user.id:
            to24 = True
            betOn = True
        
        elif message.content.lower() == "3rd 12" and message.author.id != bot.user.id:
            to36 = True
            betOn = True
        
        elif message.content.isdigit() and message.author.id != bot.user.id:
            userRouletteNum = int(message.content)
            userRouletteNumBool = True
            betOn = True
        
        else:
            userRouletteGuess = message.content.lower()
            userRouletteGuessBool = True
            betOn = True

    #set colours and random nums
    
        colours = ['Black', 'Red']
        finalColour = random.choice(colours)

        if finalColour == 'Black':
            blackNums = [0, 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
            finalNum = random.choice(blackNums)
            if finalNum == 0:
                finalColour = 'Green'

        if finalColour == 'Red':
            redNums = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
            finalNum = random.choice(redNums)


    #odd/even
    
        if userRouletteGuessBool:
            if userRouletteGuess == 'odd':
                if finalNum % 2 == 1:
                    await message.channel.send(f'{finalColour} {finalNum} - You win!')
                    userTokens = betAmount
                    userRouletteGuessBool = False
                    rouletteOn = False

                else:
                    await message.channel.send(f'{finalColour} {finalNum} - You lose!')
                    userTokens = userTokens - betAmount
                    userRouletteGuessBool = False
                    rouletteOn = False


            elif userRouletteGuess == 'even':
                if finalNum % 2 == 0:
                    if finalNum != 0:
                        await message.channel.send(f'{finalColour} {finalNum} - You win!')
                        userTokens = betAmount
                        userRouletteGuessBool = False
                        rouletteOn = False

                    else:
                        await message.channel.send(f'{finalColour} {finalNum} - You lose!')
                        userTokens = userTokens - betAmount
                        userRouletteGuessBool = False
                        rouletteOn = False

                else:
                    await message.channel.send(f'{finalColour} {finalNum} - You lose!')
                    userTokens = userTokens - betAmount
                    userRouletteGuessBool = False
                    rouletteOn = False


    #colours

            if userRouletteGuess == 'black':
                if finalColour == 'Black':
                    await message.channel.send(f'{finalColour} {finalNum} - You win!')
                    userTokens = betAmount
                    userRouletteGuessBool = False
                    rouletteOn = False

                else:
                    await message.channel.send(f'{finalColour} {finalNum} - You lose!')
                    userTokens = userTokens - betAmount
                    userRouletteGuessBool = False
                    rouletteOn = False

            
            if userRouletteGuess == 'red':
                if finalColour == 'Red':
                    await message.channel.send(f'{finalColour} {finalNum} - You win!')
                    userTokens = betAmount
                    userRouletteGuessBool = False
                    rouletteOn = False

                else:
                    await message.channel.send(f'{finalColour} {finalNum} - You lose!')
                    userTokens = userTokens - betAmount
                    userRouletteGuessBool = False
                    rouletteOn = False


    #numbet

        if userRouletteNumBool:
            if userRouletteNum == finalNum:
                await message.channel.send(f'{finalColour} {finalNum} - You win!')
                userTokens = betAmount * 34
                userRouletteNumBool = False
                rouletteOn = False
            else:
                await message.channel.send(f'{finalColour} {finalNum} - You lose!')
                userTokens = userTokens - betAmount
                userRouletteNumBool = False
                rouletteOn = False


    #to12

        if to12:
            if finalNum <= 12:
                await message.channel.send(f'{finalColour} {finalNum} - You win!')
                userTokens = betAmount * 2
                to12 = False
                rouletteOn = False
            else:
                await message.channel.send(f'{finalColour} {finalNum} - You lose!')
                userTokens = userTokens - betAmount
                to12 = False
                rouletteOn = False

    #to24

        if to24:
            if finalNum > 12 and finalNum <= 24:
                await message.channel.send(f'{finalColour} {finalNum} - You win!')
                userTokens = betAmount * 2
                to24 = False
                rouletteOn = False
            else:
                await message.channel.send(f'{finalColour} {finalNum} - You lose!')
                userTokens = userTokens - betAmount
                to24 = False
                rouletteOn = False

    #to36

        if to36:
            if finalNum > 24 and finalNum <= 36:
                await message.channel.send(f'{finalColour} {finalNum} - You win!')
                userTokens = betAmount * 2
                to36 = False
                rouletteOn = False
            else:
                await message.channel.send(f'{finalColour} {finalNum} - You lose!')
                userTokens = userTokens - betAmount
                to36 = False
                rouletteOn = False

        finalUserTokens = round(userTokens)
        
        for row in data:
            if row['Name'] == username:
                userRow = row['Tokens'] = str(int(row['Tokens']) + finalUserTokens)
                updated = True
                break

        if not updated:
            data.append({'Name': username, 'Tokens': str(finalUserTokens)})


        #CSV STUFF#
        
        with open('stats.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
            writer.writerows(data)
        
    await bot.process_commands(message)



    #ridethebus
    if busOn and message.author.id != bot.user.id:

        startBus()


        username = message.author.name
        fieldNames = ['Name', 'Tokens']
        userTokens = 0
        nameFound = False

        with open('stats.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldNames)
            data = list(reader)


        for row in data:
            if row['Name'] == username:
                userRow = row['Tokens'] = str(int(row['Tokens']))
                updated = True
                break

        if not updated:
            data.append({'Name': username, 'Tokens': str(userTokens)})

        betAmount = int(userRow) / 10


        #MAIN
        def busCards():
            colours = ['black', 'red']
            global busColour
            busColour = random.choice(colours)

            nums = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
            global busNum
            busNum = random.choice(nums)

        if colourGuess:
            userColourGuess = message.content.lower()
            busCards()
            actualColour = busColour
            actualNum = busNum
            cardsCalled.append(actualNum)
            if userColourGuess == actualColour:
                await message.channel.send(f'{actualColour} {actualNum} - Correct!')
                await message.channel.send('Higher or lower?')
                colourGuess = False
                valueGuess = True
            else:
                await message.channel.send(f'{actualColour} {actualNum} - Incorrect!')
                busOn = False

        def checkVal(msg):
            return msg.author.id == message.author.id and msg.channel.id == message.channel.id and msg.content.lower() in ['higher', 'lower']
        if valueGuess:
            userValueGuess = await bot.wait_for('message', check=checkVal, timeout=60.0)
            firstCard = cardsCalled[0]
            busCards()
            secondNum = busNum
            secondColour = busColour

            print(f'first = {firstCard}, second = {secondNum}, guess = {userValueGuess}')

            if userValueGuess == 'higher':
                print(userValueGuess)
                if secondNum > firstCard:
                    await message.channel.send(f'{secondColour} {secondNum} - Correct!')
                    await message.channel.send('Between these values or outwith these values?')
                    cardsCalled.append(secondNum)
                    valueGuess = False
                    rangeGuess = True
                else:
                    await message.channel.send(f'{secondColour} {secondNum} - Incorrect!')
                    print(userValueGuess)
                    busOn = False
            elif userValueGuess == 'lower':
                print(userValueGuess)
                if secondNum < firstCard:
                    await message.channel.send(f'{secondColour} {secondNum} - Correct!')
                    await message.channel.send('Between these values or outwith these values?')
                    cardsCalled.append(secondNum)
                    valueGuess = False
                    rangeGuess = True
                else:
                    await message.channel.send(f'{secondColour} {secondNum} - Incorrect!')
                    print(userValueGuess)
                    busOn = False
            else:
                await message.channel.send("Invalid input! Please respond with 'higher' or 'lower'.")
                busOn = False

        else:
            await message.channel.send("Invalid input! Please respond with 'higher' or 'lower'.")
            busOn = False

        if rangeGuess:
            userRangeGuess = message.content.lower()
            firstCard = cardsCalled[0]
            secondCard = cardsCalled[1]
            busCards()
            thirdNum = busNum
            if userRangeGuess == 'between':
                if thirdNum > firstCard and thirdNum < secondCard:
                    await message.channel.send(f'{busColour} {busNum} - Correct!')
                    await message.channel.send('What will the suit be?')
                    cardsCalled.append(busNum)
                    suitGuess = True
                else:
                    await message.channel.send(f'{busColour} {busNum} - Incorrect!')
                    busOn = False

            if userRangeGuess == 'outwith' or userRangeGuess == 'out':
                if thirdNum < firstCard and thirdNum > secondCard:
                    await message.channel.send(f'{busColour} {busNum} - Correct!')
                    await message.channel.send('What will the suit be?')
                    cardsCalled.append(busNum)
                    suitGuess = True
                else:
                    await message.channel.send(f'{busColour} {busNum} - Incorrect!')
                    busOn = False



    #AIChat

    if aiOn and message.author.id != bot.user.id:

        if aiOn and message.author.id in userSession:
            aiUserID = message.author.id

            userSession[aiUserID].append({"role": "user", "content": message.content})

            history = ""
            for msg in userSession[aiUserID]:
                history += f"{msg['role']}: {msg['content']}\n"

            try:
                resp = requests.post(
                    API,
                    headers=HEADERS,
                    json={"inputs": history}
                )
                resp.raise_for_status()
                data = resp.json()

                if isinstance(data, dict) and "generated_text" in data:
                    reply = data["generated_text"]
                elif isinstance(data, list) and "generated_text" in data[0]:
                    reply = data[0]["generated_text"]
                else:
                    reply = "Sorry, I couldn't understand the response."
            except requests.exceptions.RequestException as e:
                reply = "There was an error connecting to the AI service."
                print(f"Request error: {e}")
            except Exception as e:
                reply = "An unexpected error occurred."
                print(f"Unexpected error: {e}")

                userSession[aiUserID].append({"role": "assistant", "content": reply})
                await message.channel.send(reply)

            except Exception as e:
                await message.channel.send("Something went wrong.")
                print(e)




#lewisEffectOn
@bot.tree.command(name='lewis-effect-on', description='Adds random words onto what you just said')
async def lewisEffectOn(interaction: discord.Interaction):
    global effect
    effect = True
    await interaction.response.send_message("Lewis effect is enabled.")


#lewisEffectOff
@bot.tree.command(name='lewis-effect-off', description='Toggles Lewis Effect off')
async def lewisEffectOff(interaction: discord.Interaction):
    global effect
    effect = False
    await interaction.response.send_message("Lewis effect is disabled.")


#randomBall
@bot.tree.command(name='8ball')
async def randomBall(interaction: discord.Interaction):
    global question, question_user_id
    question = True
    question_user_id = interaction.user.id
    await interaction.response.send_message(f'{interaction.user.name}, Ask me a question!')


#imageTest
@bot.tree.command(name='image', description='Test image to see if bot is running')
async def image(interaction: discord.Interaction):
    await interaction.response.defer()
    await interaction.followup.send(file=discord.File(r'C:/Users/lewis/Downloads/IMG_6847.jpg')) 



@bot.tree.command(name='slashtest', description='yupyupyupy')
async def slashTest(interaction: discord.Interaction):
    await interaction.response.send_message('yup it works')


#Blackjack


cards = {'Ace' : 1, '2' : 2, '3' : 3, '4' : 4, '5': 5, '6' : 6, '7' : 7, '8' : 8, '9' : 9, '10' : 10, 'Jack' : 10, 'Queen' : 10, 'King' : 10}
deck = list(cards.keys()) * 4
random.shuffle(deck)

def deal_card(deck):
    return deck.pop()


player_hand = []
dealer_hand = []

player_hand.append(deal_card(deck))
player_hand.append(deal_card(deck))


dealer_hand.append(deal_card(deck))
dealer_hand.append(deal_card(deck))


def display_hands(player_hand, dealer_hand, reveal_dealer = False):
    player_display = ', '.join(player_hand)
    player_total = calculate_hand(player_hand)
    dealer_total = calculate_hand(dealer_hand)

    if reveal_dealer:
        dealer_display = ', '.join(dealer_hand)
        return (f'Players hand: {player_display} (Total: {player_total})\n'
                f'Dealers hand: {dealer_display} (Total: {dealer_total})\n')
    else:
        dealer_display = dealer_hand[0] + ', [Hidden]'
    return (f'Players hand: {player_display} (Total: {player_total})\n'
            f'Dealers hand: {dealer_display}')

def calculate_hand(hand):
    value = 0
    aces = 0

    for card in hand:
        value += cards[card]
        if card == 'Ace':
            aces += 1

    while value <= 11 and aces > 0:
        value += 10
        aces -= 1

    return value


@bot.tree.command(name='blackjack', description='Play a game of blackjack with me! (prone to bugs)')
async def blackJack(interaction: discord.Interaction):
    player_hand = []
    dealer_hand = []
    blackJackTokens = 0
    fieldNames = ['Name', 'Tokens']
    username = interaction.user.name
    updated = False

    with open('stats.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldNames)
        data = list(reader)


    for row in data:
        if row['Name'] == username:
            userRow = row['Tokens'] = str(int(row['Tokens']))
            updated = True
            break

    if not updated:
        data.append({'Name': username, 'Tokens': str(blackJackTokens)})

    global betAmountJack
    betAmountJack = int(userRow) / 10

    # Initial deal
    player_hand.append(deal_card(deck))
    player_hand.append(deal_card(deck))

    dealer_hand.append(deal_card(deck))
    dealer_hand.append(deal_card(deck))

    await interaction.response.send_message(display_hands(player_hand, dealer_hand))

    
    def check(msg):
        return msg.author.id == interaction.user.id and msg.channel == interaction.channel and msg.content.lower() in ['hit', 'stand']

    
    while True:
        await interaction.followup.send(f'Hit or Stand?\nBet: {round(betAmountJack)}')
        try:
            msg = await bot.wait_for('message', check=check, timeout=60.0)
        except asyncio.TimeoutError:
            await interaction.followup.send("Timeout!")
            return

        if msg.content.lower() == 'hit':
            player_hand.append(deal_card(deck))
            await interaction.followup.send(display_hands(player_hand, dealer_hand))

            if calculate_hand(player_hand) > 21:
                await interaction.followup.send('You bussssed! losaaaah')
                blackJackTokens = blackJackTokens - betAmountJack
                return

        elif msg.content.lower() == 'stand':
            break 

    
    while calculate_hand(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
#devil
    await interaction.followup.send(display_hands(player_hand, dealer_hand, reveal_dealer=True))

    
    player_total = calculate_hand(player_hand)
    dealer_total = calculate_hand(dealer_hand)

    if dealer_total > 21:
        await interaction.followup.send('you won :(')
        blackJackTokens = betAmountJack
    elif player_total > dealer_total:
        await interaction.followup.send('you won :(')
        blackJackTokens = betAmountJack
    elif player_total < dealer_total:
        await interaction.followup.send('I WON AHHAHAHAHAHA')
        blackJackTokens = blackJackTokens - betAmountJack
    else:
        await interaction.followup.send('its a.. tie? idk get ur money back')

    finalUserTokens = round(blackJackTokens)


    for row in data:
        if row['Name'] == username:
            userRow = row['Tokens'] = str(int(row['Tokens']) + finalUserTokens)
            updated = True
            break

    if not updated:
        data.append({'Name': username, 'Tokens': str(finalUserTokens)})


    #CSV STUFF#
    
    with open('stats.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldNames)
        writer.writerows(data)




measurements = ['kilometres', 'miles', 'hamburgers', 'crocodiles', 'bald eagles', 'centimetres', 'millimetres', 'metres', 'megametres', 'AU', 'lightyears', 'nanometres', 'feet', 'yards', 'toes', 'seconds', 'minutes', 'years', 'tomorrows']

@bot.tree.command(name='ruler', description='Tell me something to measure!')
async def ruler(interaction: discord.Interaction):
    await interaction.response.send_message('What would you like to measure?')
    global measure
    measure = True




suffix = ['ing', 'nd' 'st', 'rd', 'th', 'ed', 'ily', 's', 'ist' 'ance', 'ible', 'ous', 'some', 'ery', 'ess', 'ish']

@bot.tree.command(name='inger-on', description='adds random things onto the end of every message (eg ing)')
async def inger(interaction: discord.Interaction):
    await interaction.response.send_message('I will now take every single message and add something to the end yk')



@bot.tree.command(name='guess-the-num', description='Guess the number! (BROKEN)')
async def guessTheNum(interaction: discord.Interaction):
    global guessTheNumOn, timerOn, guessTheNumTarget
    guessTheNumOn = True
    guessTheNumTarget = None
    await interaction.response.send_message(
        'RULES: \nThe player will have 20 seconds to guess the right number (between 1 - 40)\nYour time begins in 3 seconds'
    )
    await asyncio.sleep(3)
    timerOn = True
    await interaction.followup.send('go go go!')

    async def timer(channel):
        global timerOn, guessTheNumOn, guessTheNumTarget
        await asyncio.sleep(20)
        if guessTheNumOn:
            await channel.send(f'Time is up! The number was {guessTheNumTarget}')
            guessTheNumOn = False
            timerOn = False
            guessTheNumTarget = None


    bot.loop.create_task(timer(interaction.channel))


#AUTO big ben
@tasks.loop(seconds=1)
async def bigBenAUTO():
    time_now = datetime.now().strftime("%H:%M:%S")

    if time_now in ["00:00:00", "01:00:00", "02:00:00", "03:00:00", "04:00:00", "05:00:00", "06:00:00", "07:00:00", "08:00:00", "09:00:00", "10:00:00", "11:00:00", "12:00:00", "13:00:00", "14:00:00", "15:00:00", "16:00:00", "17:00:00", "18:00:00", "19:00:00", "20:00:00", "21:00:00", "22:00:00", "23:00:00"]: 

        for guild in bot.guilds:
            if guild.id != 837266679443619860:
                continue

            print(f'Checking guild: {guild.name}')

            for vc in guild.voice_channels:
                print(f'VC: {vc.name}, Members: {len(vc.members)}')

            channel_check = [vc for vc in guild.voice_channels if len(vc.members) > 0]

            if not channel_check:
                print('VC is empty')
                return
        
        channel = max(channel_check, key=lambda vc: len(vc.members))

        if guild.voice_client is None:
            print(f'Connecting to voice channel: {channel.name}')
            voice_client = await channel.connect()

            try:
                source = FFmpegPCMAudio('C:/Users/lewis/Downloads/bigbenny.mp3')
                voice_client.play(source, after=lambda e: print(f'Playback finished: {e}' if e else 'Playback finished.'))
                
                while voice_client.is_playing():
                    await asyncio.sleep(1) 
                
                await voice_client.disconnect()

            except Exception as e:
                print(f'Error: {e}')
                if voice_client.is_connected():
                    await voice_client.disconnect()

@bot.tree.command(name='set-birthday', description='add your birthday and I will remind you when it is')
async def birthday(interaction: discord.Interaction, *, prompt: str):

    fieldnames = ['Name', 'Birthday']
    username = interaction.user.name
    birthday_str = prompt.strip()
    updated = False


    if os.path.exists('birthdays.csv'):
        with open('birthdays.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            data = list(reader)
    else:
        data = []

    for row in data:
        if row['Name'] == username:
            row['Birthday'] = birthday_str
            updated = True
            break

    if not updated:
        data.append({'Name': username, 'Birthday': birthday_str})

    # Write back to file
    with open('birthdays.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerows(data)

    await interaction.response.send_message(f"Birthday for {username} set to {birthday_str}!")

@tasks.loop(hours=1)
async def birthdayCheck():

    channel_id = 947902507437391924
    channel = bot.get_channel(channel_id)
    if channel is None:
        print("Birthday channel not found.")
        return

    today = datetime.now().strftime("%d/%m")
    fieldnames = ['Name', 'Birthday']

    if os.path.exists('birthdays.csv'):
        with open('birthdays.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldnames)
            for row in reader:
                username = row['Name']
                birthday_str = row['Birthday'].strip()
                if birthday_str[:5] == today:
                    for guild in bot.guilds:
                        member = discord.utils.get(guild.members, name=username)
                        if member:
                            await channel.send(f"Happy Birthday {member.mention}! 🎉")
                            break
                    else:
                        await channel.send(f"Happy Birthday {username}! 🎉")

@bot.tree.command(name='birthday-dates', description='List of all saved birthdays')
async def birthday_dates(interaction: discord.Interaction):
    fieldnames = ['Name', 'Birthday']
    if not os.path.exists('birthdays.csv'):
        await interaction.response.send_message("No birthdays found.")
        return

    with open('birthdays.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        birthdays = [f"{row['Name']}: {row['Birthday']}" for row in reader if row['Name'] and row['Birthday']]

    if birthdays:
        birthdayList = "Saved birthdays:\n" + "\n".join(birthdays)
    else:
        birthdayList = "No birthdays found NOOOOOOOOOOOO"
    await interaction.response.send_message(birthdayList)

#MANUAL big ben
@bot.tree.command(name='big-ben', description='Big Ben.')
async def bigBen(interaction: discord.Interaction):
    if interaction.user.voice:
        voice_channel = interaction.user.voice.channel
        voice_client = await voice_channel.connect()

        try:
            source = FFmpegPCMAudio('C:/Users/lewis/Downloads/bigbenny.mp3')
            voice_client.play(source, after=lambda e: print(f'Playback finished: {e}' if e else 'Playback finished.'))
            
            while voice_client.is_playing():
                await asyncio.sleep(1) 
            
            await voice_client.disconnect()
        except Exception as e:
                print(f'Error: {e}')
                await voice_client.disconnect()
        else:
            await interaction.response.send_message('You are not connected to a voice channel.')



#espressooooooooooo
@bot.tree.command(name='sabrina', description='Joins VC to play sabriner!')
async def espresso(interaction: discord.Interaction):
    if interaction.user.voice:
        voice_channel = interaction.user.voice.channel
        voice_client = await voice_channel.connect()

        try:
            songs = ['C:/Users/lewis/Downloads/espresso.mp3', 'C:/Users/Lewis/Downloads/pleasepleaseplease.mp3', 'C:/Users/Lewis/Downloads/taste.mp3', 'C:/Users/Lewis/Downloads/feather.mp3']
            voiceSong = random.choice(songs)
            source = FFmpegPCMAudio(voiceSong)
            voice_client.play(source, after=lambda e: print(f'Playback finished: {e}' if e else 'Playback finished.'))

            while voice_client.is_playing():
                await asyncio.sleep(1)

            await voice_client.disconnect()
        except Exception as e:
            print(f'Error: {e}')
            await voice_client.disconnect()
        else:
            await interaction.response.send_message('lemesso')



@bot.tree.command(name='random-quote')
async def randomQuote(interaction: discord.Interaction):

    searchArray = ['love', 'happiness', 'success', 'friendship', 'wisdom', 'life', 'strength', 'dreams', 'courage', 'nature']
    search = random.choice(searchArray)
    quotes = quote(search, limit=10)

    if quotes:
        selectedQuote = random.choice(quotes)
        quoteText = f'"{selectedQuote['quote']}" - {selectedQuote['author']}'
    else:
        quoteText = 'No quoties found matey!'

    await interaction.response.send_message(quoteText)


@tasks.loop(seconds=1)
async def quoteOfTheDay():
    
    
    time_now = datetime.now().strftime("%H:%M:%S")
    targetTime = ['09:00:00', '12:00:00', '17:00:00', '20:30:00']

    if time_now in targetTime:
        quoteChannel = bot.get_channel(1201260512160256050)
        searchArray = ['love', 'happiness', 'success', 'friendship', 'wisdom', 'life', 'strength', 'dreams', 'courage', 'nature']
        search = random.choice(searchArray)
        quotes = quote(search, limit=10)

        if quotes:
            selectedQuote = random.choice(quotes)
            quoteText = f'"{selectedQuote['quote']} - {selectedQuote['author']}'
        else:
            quoteText = 'No quoties found matey!'

        print(quoteText)
        await quoteChannel.send(quoteText)


@bot.tree.command(name='rock-paper-scissors', description='Play Rock Paper Scissors with me!')
async def rps(interaction: discord.Interaction):
    await interaction.response.send_message('Rock paper scissors! Lets play! (I will pick my choice randomly after youve done yours so its not rigged )')
    global rpsOn
    rpsOn = True


@bot.tree.command(name='dice')
async def dice(interaction: discord.Interaction):
    await interaction.response.send_message('Ill roll a 6 sided die. Guess the correct number or you get timed out.')
    global dice
    dice = True


@bot.tree.command(name='pregnant-man-aerodynamics')
async def aero(interaction: discord.Interaction):
    await interaction.response.send_message('Here are the aerodynamics of a pregnant man.')
    await interaction.followup.send(file=discord.File(r'C:/Users/lewis/Downloads/pregnantaero.png')) 


@bot.tree.command(name='roulette')
async def roulette(interaction: discord.Interaction):
    global rouletteOn
    rouletteOn = True
    await interaction.response.send_message(file=discord.File(r'C:/Users/lewis/Downloads/rouletteboard.jpg'))
    await interaction.followup.send('Bet on: \n| 0 - 36 |\n| 1st 12 | 2nd 12 | 3rd 12 |\n| EVEN | ODD |\n| 🟥 | ⬛ |\n(bet is 10 percent of your total tokens, use /tokens to see your tokens.)')

@bot.tree.command(name='ride-the-bus')
async def bus(interaction: discord.Interaction):
    global busOn
    busOn = True
    await interaction.response.send_message('Ride the Bus \n\nThere will be a total of 4 rounds in which for each round you bet on properties of the upcoming card\nThese bets consist of:\n\n+Colour (🟥,⬛)\n+Higher / lower than previous card value\nBetween or outwith of the previous 2 cards values (eg 10 and 4)\nCard suit (club, diamond, heart, spade)\n\nThere is a multiplier on your bet the further you can make it.')
    await interaction.followup.send('Colour? (🟥, ⬛)')


@bot.tree.command(name='tokens')
async def roulette(interaction: discord.Interaction):
    fieldNames = ['Name', 'Tokens']
    nameFound = False
    username = interaction.user.name
    with open('stats.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=fieldNames)
            data = list(reader)

    for row in data:
        if row['Name'] == username:
            nameFound = True
            break

    if nameFound:
        await interaction.response.send_message(f'{interaction.user.name}, you have {str(row['Tokens'])} Tokens.')
    else:
        await interaction.followup.send('You dont have any tokens! Play something to get some!')

@bot.tree.command(name='secret-word-count')
async def secretWordCount(interaction: discord.Interaction):
    with open('word.csv', 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        wordMessage = ''
        for row in csv_reader:
            wordMessage += f' has said one of {str(secretWords)} '.join(row) + ' times.' + '\n'
        if wordMessage:
            await interaction.response.send_message(wordMessage)


@bot.tree.command(name='random-fact')
async def randomFact(interaction: discord.Interaction):
    randomFactFinal = randfacts.get_fact()
    await interaction.response.send_message(randomFactFinal)

@bot.tree.command(name='dad-joke')
async def dadJoke(interaction: discord.Interaction):
    dadJokeFinal = Dadjoke()
    await interaction.response.send_message(dadJokeFinal.joke)



@bot.tree.command(name='open-chat')
async def aiChat(interaction: discord.Interaction, *, prompt: str):
    global aiOn
    aiUserID = interaction.user.id
    aiOn = True


    userSession[aiUserID] = prompt

    try:
        response = requests.post(API, headers=HEADERS, json={"inputs": prompt})

        if response.status_code != 200:
            raise Exception(f"API error: {response.text}")

        data = response.json()
        if isinstance(data, dict) and "generated_text" in data:
            reply = data["generated_text"]
        elif isinstance(data, list) and "generated_text" in data[0]:
            reply = data[0]["generated_text"]
        else:
            reply = "Sorry, I couldn't understand the response."

        await interaction.response.send_message(f"Chat started.\n{reply}")

    except Exception as e:
        await interaction.response.send_message('Whoops! Error!')
        print(e)

@bot.tree.command(name='close-chat')
async def closeAI(interaction: discord.Interaction):
    global aiOn
    aiOn = False
    await interaction.response.send_message('AI has been turned off. :(')


bot.run(TOKEN)

# to run type "python bot.py"