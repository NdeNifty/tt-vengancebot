from selenium import webdriver
from csv import DictReader
import logging
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.select import Select
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from proleauge1 import Game, Proleague

# log file config
logging.basicConfig(filename="log.txt", filemode='w', format='%(asctime)s %(message)s')

profile = webdriver.FirefoxProfile()
profile.set_preference("dom.webnotifications.enabled", False)
profile.set_preference("dom.push.enabled", False)

options = Options()
options.headless = False

bot = webdriver.Firefox(options=options, firefox_profile=profile)

bot.get("https://1xbet.com/en")


def get_cookies_values(file):
    with open(file, encoding='utf-8-sig') as f:
        dict_reader = DictReader(f)
        list_of_dicts = list(dict_reader)
    return list_of_dicts


cookies = get_cookies_values("1xbet_cookies.csv")

for i in cookies:
    bot.add_cookie(i)

bot.refresh()
bot.maximize_window()

# Link Texts
sports = 'SPORTS'
tabletennis = 'Table Tennis'

# Class Names on Dom
balance = 'top-b-acc__amount'
searchfield = 'sport-search__input'

# Xpaths to various Leagues
proleaguelink = "//a[@href='line/table-tennis/1691055-pro-league']"
ttcuplink = "//a[@href='line/table-tennis/1197285-tt-cup']"
setkacuplink = "//a[@href='line/table-tennis/1733171-setka-cup']"

# Xpaths to betting variables and data
leaguename = "(//div[@id='line_breadcrumbs']//a)[3]"
teamoneodds = "(//span[@class='koeff'])[1]"
teamtwoodds = "(//span[@class='koeff'])[2]"
market = "//span[text()[normalize-space()='Total Sets Over 3.5']]"
# setamount = "//input[@class='c-spinner__input bet_sum_input']"
setamount = "(//label[text()='Set bet slip stake to change by']/following::input)[2]"
punterharmmer = "//button[text()[normalize-space()='place a bet']]"

# Get account balance
account_balance = bot.find_element(by=By.CLASS_NAME, value=balance)
logging.info('Account balance is :' + account_balance.text)

#obtain parent window handle
parent = bot.window_handles[0]

# Dictionary to store games details
GamesList = []
# The betting function
def placebet():
    betbutton = bot.find_element(by=By.XPATH, value="//button[text()[normalize-space()='place a bet']]")
    logging.info("Input field found")
    realbalance = bot.find_element(by=By.CLASS_NAME, value="top-b-acc__amount")
    actualbalance = float(realbalance.text)
    logging.info("Balance gotten")
    stake = 0
    if 90 < actualbalance <= 499:
        stake = account_balance
        logging.info('Stake amount : ' + str(stake) + ' CFA')
    elif 500 < actualbalance <= 10000:
        stake = 100
        # stake = 25%balance
        logging.info('Stake amount : ' + str(stake) + ' CFA')
    elif 10000 < actualbalance <= 25000:
        stake = 5000
        logging.info('Stake amount : ' + str(stake) + ' CFA')
    elif 25000 < actualbalance <= 50000:
        stake = 8000
        logging.info('Stake amount : ' + str(stake) + ' CFA')
    elif actualbalance >= 50000:
        stake = 10000
        logging.info('Stake amount : ' + str(stake) + ' CFA')
    amountinput = bot.find_element(by=By.XPATH,
                                   value="(//label[text()='Set bet slip stake to change by']/following::input)[2]")
    amountinput.clear()
    amountinput.send_keys(stake)
    betbutton.click()
    stakestake = str(stake)
    logging.info('Bet placed succesfully with stake: ' + stakestake + ' CFA')



# Pro League First Game function
def proleague():
    # Click on sports link
    open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
    open_sports.click()
    logging.info('Clicked Sports')

    # click on table tennis
    open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
    open_tt.click()
    logging.info('Clicked Table Tennis')

    # go to search to quit dropdown
    go_to_search = bot.find_element(by=By.CLASS_NAME, value=searchfield)
    go_to_search.click()
    logging.info('Clicked Search')

    try:
        # open Pro League Tournament
        open_pro_league = WebDriverWait(bot, 30).until(ec.presence_of_element_located((By.XPATH, proleaguelink)))
        open_pro_league.click()
        logging.info('Pro League Found and Opened')
    except:
        logging.info("Pro League Tournament not found !!!!!!")
        logging.info("Skipping to TT Cup..........................")
        print("Pro League Tournament not found !!!!!!")
        print("Skipping to TT Cup..........................")
        ttcup()


    # Select First game
    first_pro_league_gamexPath = "(//a[@data-liga='1691055'])[1]"
    first_pro_league_game = WebDriverWait(bot, 30).until(ec.presence_of_element_located((By.XPATH, first_pro_league_gamexPath)))

    first_pro_league_game.click()
    logging.info('First Pro league game opened')
    print('First Pro league game opened')

    league = bot.find_element(by=By.XPATH, value=leaguename)

    team1Xpath = "(//div[@class='team']//a)[1]"
    team2Xpath = "(//div[@class='team'])[2]"
    gametimeXpath = "(//div[@class='time']//div)[2]"
    team1 = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, team1Xpath)))
    team2 = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, team2Xpath)))
    gametime = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, gametimeXpath)))


    # Dictionary to hold game details
    gamedetails ={ }
    gamedetails["team1"] = team1
    gamedetails["team2"] = team2
    gamedetails["gametime"] = gametime

    # Check GameList if the game has been analysed before
    if gamedetails in GamesList:
        # Go to next game
        logging.info("This game has been analysed already!!!!!")
        logging.info("Skipping to the next Pro league game..............")
        print("This game has been analysed already !!!!!")
        print("Skipping to the next Pro league game..............")
        # Click on sports link
        open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
        open_sports.click()
        logging.info('Clicked Sports')

        # click on table tennis
        open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
        open_tt.click()
        logging.info('Clicked Table Tennis')
        proleague2()
    else:
        # Add Game details to the Bet list
        GamesList.append(gamedetails)
        logging.info("The game details have been added to the Analysed List")
        print("The game details have been added to the analysed list")




    logging.info('League :' + league.text)

    team1odds = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, teamoneodds)))
    logging.info('Team 1 odds:' + team1odds.text)
    team2odds = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, teamtwoodds)))
    logging.info('Team 2 odds:' + team2odds.text)

    statsdropdown = bot.find_element(by=By.XPATH, value="(//button[@title='Statistics'])[1]")
    statslink = bot.find_element(by=By.XPATH, value="//button[@title='Statistics']//span[1]")



    try:
        clickmarket = bot.find_element(by=By.XPATH, value=market)
        if (float(team1odds.text) >= 1.28 and float(team2odds.text) >= 1.28):

            logging.info('Favorable bet found')

            statsdropdown.click()
            statslink.click()
            logging.info('Stats link clicked')
            # ObtainWindow handle for stats window
            statswindow = bot.window_handles[1]
            bot.switch_to.window(statswindow)
            print("Stats window opened")

            WebDriverWait(bot, 20).until(ec.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@class,'st-portal st-integration__portal')]")))
            h2hclick1 = WebDriverWait(bot, 30).until(ec.element_to_be_clickable((By.XPATH, "(//div[@class='st-switch__text'])[2]")))

            print("Accessed iframe and ready to collect statistics")
            # Click head to head
            get_title = bot.title
            print("The title is : " + get_title)

            h2hlink = bot.find_element(by=By.XPATH, value="/html/body/div/div/div/div/div[1]/div[2]/div[2]/a[2]")

            try:
                WebDriverWait(bot, 30).until(ec.element_to_be_clickable((By.XPATH, "(//div[@class='st-switch__text'])[2]")))
                h2hclick1.click()
                someclick = WebDriverWait(bot, 30).until(ec.element_to_be_clickable((By.XPATH, "(//div[@class='st-switch__text'])[2]")))
                someclick.click()
                # Double click if the first click did not respond
                action = ActionChains(bot)
                action.double_click(h2hlink).perform()
                h2hlink.click()
            except:
                h2hclick1.click()
                h2hlink.click()
                print("h2h link clicked twice")

            print("toogle head to head opened")

            scoresList =[]
            scores = WebDriverWait(bot, 20).until(ec.presence_of_all_elements_located((By.CLASS_NAME, "st-score__value")))
            # scores = bot.find_elements(by=By.CLASS_NAME, value="st-score__value")
            for score in scores:
                print("Score: " + score.text)
                scoresList.append(score.text)
            print("The scorelist is :")
            print(scoresList)
            logging.info(scoresList)

            # Bet Analysis Variables
            totalscores = len(scoresList)
            zeros = scoresList.count('0')
            zerostreshold = 100 * zeros/totalscores

            if totalscores < 3:
                print("Not enough statistics for analysis. The bot will proceed to the next league")
                scoresList.clear()
                bot.close()
                bot.switch_to.window(parent)
                logging.info('odds not favorable')
                logging.info('Going to the next game')
                print('odds not favorable')
                print('Going to the next game')
                # Click on sports link
                open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
                open_sports.click()
                logging.info('Clicked Sports')

                # click on table tennis
                open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
                open_tt.click()
                logging.info('Clicked Table Tennis')
                proleague2()

            elif 2.9 < totalscores and zerostreshold < 25 :
                scoresList.clear()
                bot.close()
                bot.switch_to.window(parent)
                # bot.switch_to.default_content()


            # Scroll market to center of page
            desired_y = (clickmarket.size['height'] / 2) + clickmarket.location['y']
            current_y = (bot.execute_script('return window.innerHeight') / 2) + bot.execute_script(
                'return window.pageYOffset')
            scroll_y_by = desired_y - current_y
            bot.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
            scroll = ActionChains(bot)
            scroll.move_to_element(clickmarket).perform()
            # clickmarket.click()
            # logging.info('Market added to betslip')
            # Go to place bet function
            # placebet()

            logging.info('Pro league Bet placed.......................!')
            bot.refresh()
            logging.info("Page refreshed")
            # Click on sports link
            open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
            open_sports.click()
            logging.info('Clicked Sports')

            # click on table tennis
            open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
            open_tt.click()
            logging.info('Clicked Table Tennis')
            proleague2()
        else:

            logging.info('odds not favorable')
            logging.info('Going to the next game')
            # Click on sports link
            open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
            open_sports.click()
            logging.info('Clicked Sports')

            # click on table tennis
            open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
            open_tt.click()
            logging.info('Clicked Table Tennis')
            proleague2()
    except NoSuchElementException:
        logging.info('Over 3.5 Market not found. Going to next game')
        # Click on sports link
        open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
        open_sports.click()
        logging.info('Clicked Sports')

        # click on table tennis
        open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
        open_tt.click()
        logging.info('Clicked Table Tennis')
        proleague2()


# Pro League second Game function
def proleague2():
    # Click on sports link
    open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
    open_sports.click()
    logging.info('Clicked Sports')

    # click on table tennis
    open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
    open_tt.click()
    logging.info('Clicked Table Tennis')

    # go to search to quit dropdown
    go_to_search = bot.find_element(by=By.CLASS_NAME, value=searchfield)
    go_to_search.click()
    logging.info('Clicked Search')

    try:
        # open Pro League Tournament
        open_pro_league = WebDriverWait(bot, 30).until(ec.presence_of_element_located((By.XPATH, proleaguelink)))
        open_pro_league.click()
    except:
        logging.info("Pro League Tournament not found !!!!!!")
        logging.info("Skipping to TT Cup..........................")
        print("Pro League Tournament not found !!!!!!")
        print("Skipping to TT Cup..........................")
        ttcup()
    logging.info('This Point')

    # Select Second game
    second_pro_league_gamexPath = "(//a[@data-liga='1691055'])[2]"
    second_pro_league_game = WebDriverWait(bot, 30).until(
        ec.presence_of_element_located((By.XPATH, second_pro_league_gamexPath)))

    second_pro_league_game.click()
    logging.info('Second Pro league game opened')
    print('Second Pro league game opened')

    league = bot.find_element(by=By.XPATH, value=leaguename)

    team1Xpath = "(//div[@class='team']//a)[1]"
    team2Xpath = "(//div[@class='team'])[2]"
    gametimeXpath = "(//div[@class='time']//div)[2]"
    team1 = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, team1Xpath)))
    team2 = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, team2Xpath)))
    gametime = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, gametimeXpath)))

    # Dictionary to hold game details
    gamedetails = {}
    gamedetails["team1"] = team1
    gamedetails["team2"] = team2
    gamedetails["gametime"] = gametime

    # Check GameList if the game has been analysed before
    if gamedetails in GamesList:
        # Go to next game
        logging.info("This game has been analysed already!!!!!")
        logging.info("Skipping to the next game..............")
        print("This game has been analysed already !!!!!")
        print("Skipping to the next game..............")
        # Click on sports link
        open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
        open_sports.click()
        logging.info('Clicked Sports')

        # click on table tennis
        open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
        open_tt.click()
        logging.info('Clicked Table Tennis')
        ttcup()
    else:
        # Add Game details to the Bet list
        GamesList.append(gamedetails)
        logging.info("The game details have been added to the Analysed List")
        print("The game details have been added to the analysed list")

    logging.info('League :' + league.text)

    team1odds = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, teamoneodds)))
    logging.info('Team 1 odds:' + team1odds.text)
    team2odds = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, teamtwoodds)))
    logging.info('Team 2 odds:' + team2odds.text)

    statsdropdown = bot.find_element(by=By.XPATH, value="(//button[@title='Statistics'])[1]")
    statslink = bot.find_element(by=By.XPATH, value="//button[@title='Statistics']//span[1]")

    try:
        clickmarket = bot.find_element(by=By.XPATH, value=market)
        if (float(team1odds.text) >= 1.28 and float(team2odds.text) >= 1.28):

            logging.info('Favorable bet found')

            statsdropdown.click()
            statslink.click()
            logging.info('Stats link clicked')
            # ObtainWindow handle for stats window
            statswindow = bot.window_handles[1]
            bot.switch_to.window(statswindow)
            print("Stats window opened")

            WebDriverWait(bot, 20).until(ec.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[contains(@class,'st-portal st-integration__portal')]")))
            h2hclick1 = WebDriverWait(bot, 20).until(
                ec.element_to_be_clickable((By.XPATH, "(//div[@class='st-switch__text'])[2]")))

            print("Accessed iframe and ready to collect statistics")
            # Click head to head
            get_title = bot.title
            print("The title is : " + get_title)

            h2hlink = bot.find_element(by=By.XPATH, value="/html/body/div/div/div/div/div[1]/div[2]/div[2]/a[2]")

            try:
                WebDriverWait(bot, 20).until(
                    ec.element_to_be_clickable((By.XPATH, "(//div[@class='st-switch__text'])[2]")))
                h2hclick1.click()
                # Double click if the first click did not respond
                action = ActionChains(bot)
                action.double_click(h2hlink).perform()
                h2hlink.click()
            except:
                h2hclick1.click()
                h2hlink.click()
                print("h2h link clicked twice")

            print("toogle head to head opened")

            scoresList = []
            scores = WebDriverWait(bot, 20).until(
                ec.presence_of_all_elements_located((By.CLASS_NAME, "st-score__value")))
            # scores = bot.find_elements(by=By.CLASS_NAME, value="st-score__value")
            for score in scores:
                print("Score: " + score.text)
                scoresList.append(score.text)
            print("The scorelist is :")
            print(scoresList)
            logging.info(scoresList)

            # Bet Analysis Variables
            totalscores = len(scoresList)
            zeros = scoresList.count('0')
            zerostreshold = 100 * zeros / totalscores

            if totalscores < 3:
                print("Not enough statistics for analysis. The bot will proceed to the next league")
                scoresList.clear()
                bot.close()
                bot.switch_to.window(parent)
                logging.info('odds not favorable')
                logging.info('Going to the next game')
                print('odds not favorable')
                print('Going to the next game')
                # Click on sports link
                open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
                open_sports.click()
                logging.info('Clicked Sports')

                # click on table tennis
                open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
                open_tt.click()
                logging.info('Clicked Table Tennis')
                ttcup()

            elif 2.9 < totalscores and zerostreshold < 25:
                scoresList.clear()
                bot.close()
                bot.switch_to.window(parent)
                # bot.switch_to.default_content()

            # Scroll market to center of page
            desired_y = (clickmarket.size['height'] / 2) + clickmarket.location['y']
            current_y = (bot.execute_script('return window.innerHeight') / 2) + bot.execute_script(
                'return window.pageYOffset')
            scroll_y_by = desired_y - current_y
            bot.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
            scroll = ActionChains(bot)
            scroll.move_to_element(clickmarket).perform()
            # clickmarket.click()
            # logging.info('Market added to betslip')
            # Go to place bet function
            # placebet()

            logging.info('Pro league Bet placed.......................!')
            bot.refresh()
            logging.info("Page refreshed")
            # Click on sports link
            open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
            open_sports.click()
            logging.info('Clicked Sports')

            # click on table tennis
            open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
            open_tt.click()
            logging.info('Clicked Table Tennis')
            ttcup()
        else:

            logging.info('odds not favorable')
            logging.info('Going to the next game')
            # Click on sports link
            open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
            open_sports.click()
            logging.info('Clicked Sports')

            # click on table tennis
            open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
            open_tt.click()
            logging.info('Clicked Table Tennis')
            ttcup()
    except NoSuchElementException:
        logging.info('Over 3.5 Market not found. Going to next game')
        # Click on sports link
        open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
        open_sports.click()
        logging.info('Clicked Sports')

        # click on table tennis
        open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
        open_tt.click()
        logging.info('Clicked Table Tennis')
        ttcup()

# TT-Cup First Game function
def ttcup():
    # Click on sports link
    open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
    open_sports.click()
    logging.info('Clicked Sports')

    # click on table tennis
    open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
    open_tt.click()
    logging.info('Clicked Table Tennis')

    # go to search to quit dropdown
    go_to_search = bot.find_element(by=By.CLASS_NAME, value=searchfield)
    go_to_search.click()
    logging.info('Clicked Search')

    try:
        # open Pro League Tournament
        open_tt_cup = WebDriverWait(bot, 30).until(ec.presence_of_element_located((By.XPATH, ttcuplink)))
        open_tt_cup.click()
    except:
        logging.info("TT-Cup Tournament not found !!!!!!")
        logging.info("Skipping to Setka Cup..........................")
        print("TT-Cup Tournament not found !!!!!!")
        print("Skipping to Setka Cup..........................")
        setkacup()

    # Select First game
    first_tt_cup_gamexPath = "(//a[@data-liga='1197285'])[1]"
    first_tt_cup_game = WebDriverWait(bot, 30).until(ec.presence_of_element_located((By.XPATH, first_tt_cup_gamexPath)))

    first_tt_cup_game.click()
    logging.info('First Pro league game opened')
    print('First Pro league game opened')

    league = bot.find_element(by=By.XPATH, value=leaguename)

    team1Xpath = "(//div[@class='team']//a)[1]"
    team2Xpath = "(//div[@class='team'])[2]"
    gametimeXpath = "(//div[@class='time']//div)[2]"
    team1 = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, team1Xpath)))
    team2 = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, team2Xpath)))
    gametime = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, gametimeXpath)))

    # Dictionary to hold game details
    gamedetails = {}
    gamedetails["team1"] = team1
    gamedetails["team2"] = team2
    gamedetails["gametime"] = gametime

    # Check GameList if the game has been analysed before
    if gamedetails in GamesList:
        # Go to next game
        logging.info("This game has been analysed already!!!!!")
        logging.info("Skipping to the next TT Cup game..............")
        print("This game has been analysed already !!!!!")
        print("Skipping to the next TT Cup game..............")
        # Click on sports link
        open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
        open_sports.click()
        logging.info('Clicked Sports')

        # click on table tennis
        open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
        open_tt.click()
        logging.info('Clicked Table Tennis')
        ttcup2()
    else:
        # Add Game details to the Bet list
        GamesList.append(gamedetails)
        logging.info("The game details have been added to the Analysed List")
        print("The game details have been added to the analysed list")

    logging.info('League :' + league.text)

    team1odds = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, teamoneodds)))
    logging.info('Team 1 odds:' + team1odds.text)
    team2odds = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, teamtwoodds)))
    logging.info('Team 2 odds:' + team2odds.text)

    statsdropdown = bot.find_element(by=By.XPATH, value="(//button[@title='Statistics'])[1]")
    statslink = bot.find_element(by=By.XPATH, value="//button[@title='Statistics']//span[1]")

    try:
        clickmarket = bot.find_element(by=By.XPATH, value=market)
        if (float(team1odds.text) >= 1.28 and float(team2odds.text) >= 1.28):

            logging.info('Favorable bet found')

            statsdropdown.click()
            statslink.click()
            logging.info('Stats link clicked')
            # ObtainWindow handle for stats window
            statswindow = bot.window_handles[1]
            bot.switch_to.window(statswindow)
            print("Stats window opened")

            WebDriverWait(bot, 20).until(ec.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[contains(@class,'st-portal st-integration__portal')]")))
            h2hclick1 = WebDriverWait(bot, 20).until(
                ec.element_to_be_clickable((By.XPATH, "(//div[@class='st-switch__text'])[2]")))

            print("Accessed iframe and ready to collect statistics")
            # Click head to head
            get_title = bot.title
            print("The title is : " + get_title)

            h2hlink = bot.find_element(by=By.XPATH, value="/html/body/div/div/div/div/div[1]/div[2]/div[2]/a[2]")

            try:
                WebDriverWait(bot, 20).until(ec.element_to_be_clickable((By.XPATH, "(//div[@class='st-switch__text'])[2]")))
                h2hclick1.click()
                # Double click if the first click did not respond
                action = ActionChains(bot)
                action.double_click(h2hlink).perform()
                h2hlink.click()
            except:
                h2hclick1.click()
                h2hlink.click()
                print("h2h link clicked twice")

            print("toogle head to head opened")

            scoresList = []
            scores = WebDriverWait(bot, 20).until(ec.presence_of_all_elements_located((By.CLASS_NAME, "st-score__value")))
            # scores = bot.find_elements(by=By.CLASS_NAME, value="st-score__value")
            for score in scores:
                print("Score: " + score.text)
                scoresList.append(score.text)
            print("The scorelist is :")
            print(scoresList)
            logging.info(scoresList)

            # Bet Analysis Variables
            totalscores = len(scoresList)
            zeros = scoresList.count('0')
            zerostreshold = 100 * zeros / totalscores

            if totalscores < 3:
                print("Not enough statistics for analysis. The bot will proceed to the next league")
                scoresList.clear()
                bot.close()
                bot.switch_to.window(parent)
                logging.info('odds not favorable')
                logging.info('Going to the next game')
                print('odds not favorable')
                print('Going to the next game')
                # Click on sports link
                open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
                open_sports.click()
                logging.info('Clicked Sports')

                # click on table tennis
                open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
                open_tt.click()
                logging.info('Clicked Table Tennis')
                ttcup2()

            elif 2.9 < totalscores and zerostreshold < 25:
                scoresList.clear()
                bot.close()
                bot.switch_to.window(parent)
                # bot.switch_to.default_content()

            # Scroll market to center of page
            desired_y = (clickmarket.size['height'] / 2) + clickmarket.location['y']
            current_y = (bot.execute_script('return window.innerHeight') / 2) + bot.execute_script(
                'return window.pageYOffset')
            scroll_y_by = desired_y - current_y
            bot.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
            scroll = ActionChains(bot)
            scroll.move_to_element(clickmarket).perform()
            # clickmarket.click()
            # logging.info('Market added to betslip')
            # Go to place bet function
            # placebet()

            logging.info('Pro league Bet placed.......................!')
            bot.refresh()
            logging.info("Page refreshed")
            # Click on sports link
            open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
            open_sports.click()
            logging.info('Clicked Sports')

            # click on table tennis
            open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
            open_tt.click()
            logging.info('Clicked Table Tennis')
            ttcup2()
        else:

            logging.info('odds not favorable')
            logging.info('Going to the next game')
            # Click on sports link
            open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
            open_sports.click()
            logging.info('Clicked Sports')

            # click on table tennis
            open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
            open_tt.click()
            logging.info('Clicked Table Tennis')
            ttcup2()
    except NoSuchElementException:
        logging.info('Over 3.5 Market not found. Going to next game')
        # Click on sports link
        open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
        open_sports.click()
        logging.info('Clicked Sports')

        # click on table tennis
        open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
        open_tt.click()
        logging.info('Clicked Table Tennis')
        ttcup2()

# TT-Cup Second Game function
def ttcup2():
    # Click on sports link
    open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
    open_sports.click()
    logging.info('Clicked Sports')

    # click on table tennis
    open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
    open_tt.click()
    logging.info('Clicked Table Tennis')

    # go to search to quit dropdown
    go_to_search = bot.find_element(by=By.CLASS_NAME, value=searchfield)
    go_to_search.click()
    logging.info('Clicked Search')

    try:
        # open Pro League Tournament
        open_pro_league = WebDriverWait(bot, 30).until(ec.presence_of_element_located((By.XPATH, proleaguelink)))
        open_pro_league.click()
    except:
        logging.info("TT-Cup Tournament not found !!!!!!")
        logging.info("Skipping to Setka Cup..........................")
        print("TT-Cup Tournament not found !!!!!!")
        print("Skipping to Setka Cup..........................")
        setkacup()
    logging.info('This Point')

    # Select Second game
    second_tt_cup_gamexPath = "(//a[@data-liga='1197285'])[2]"
    second_tt_cup_game = WebDriverWait(bot, 30).until(ec.presence_of_element_located((By.XPATH, second_tt_cup_gamexPath)))

    second_tt_cup_game.click()
    logging.info('Second TT-Cup Cup game opened')
    print('Second TT-Cup Cup game opened')

    league = bot.find_element(by=By.XPATH, value=leaguename)

    team1Xpath = "(//div[@class='team']//a)[1]"
    team2Xpath = "(//div[@class='team'])[2]"
    gametimeXpath = "(//div[@class='time']//div)[2]"
    team1 = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, team1Xpath)))
    team2 = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, team2Xpath)))
    gametime = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, gametimeXpath)))

    # Dictionary to hold game details
    gamedetails = {}
    gamedetails["team1"] = team1
    gamedetails["team2"] = team2
    gamedetails["gametime"] = gametime

    # Check GameList if the game has been analysed before
    if gamedetails in GamesList:
        # Go to next game
        logging.info("This game has been analysed already!!!!!")
        logging.info("Skipping to the next game..............")
        print("This game has been analysed already !!!!!")
        print("Skipping to the next game..............")
        # Click on sports link
        open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
        open_sports.click()
        logging.info('Clicked Sports')

        # click on table tennis
        open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
        open_tt.click()
        logging.info('Clicked Table Tennis')
        setkacup()
    else:
        # Add Game details to the Bet list
        GamesList.append(gamedetails)
        logging.info("The game details have been added to the Analysed List")
        print("The game details have been added to the analysed list")

    logging.info('League :' + league.text)

    team1odds = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, teamoneodds)))
    logging.info('Team 1 odds:' + team1odds.text)
    team2odds = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, teamtwoodds)))
    logging.info('Team 2 odds:' + team2odds.text)

    statsdropdown = bot.find_element(by=By.XPATH, value="(//button[@title='Statistics'])[1]")
    statslink = bot.find_element(by=By.XPATH, value="//button[@title='Statistics']//span[1]")

    try:
        clickmarket = bot.find_element(by=By.XPATH, value=market)
        if (float(team1odds.text) >= 1.28 and float(team2odds.text) >= 1.28):

            logging.info('Favorable bet found')

            statsdropdown.click()
            statslink.click()
            logging.info('Stats link clicked')
            # ObtainWindow handle for stats window
            statswindow = bot.window_handles[1]
            bot.switch_to.window(statswindow)
            print("Stats window opened")

            WebDriverWait(bot, 20).until(ec.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[contains(@class,'st-portal st-integration__portal')]")))
            h2hclick1 = WebDriverWait(bot, 20).until(
                ec.element_to_be_clickable((By.XPATH, "(//div[@class='st-switch__text'])[2]")))

            print("Accessed iframe and ready to collect statistics")
            # Click head to head
            get_title = bot.title
            print("The title is : " + get_title)

            h2hlink = bot.find_element(by=By.XPATH, value="/html/body/div/div/div/div/div[1]/div[2]/div[2]/a[2]")

            try:
                WebDriverWait(bot, 20).until(
                    ec.element_to_be_clickable((By.XPATH, "(//div[@class='st-switch__text'])[2]")))
                h2hclick1.click()
                # Double click if the first click did not respond
                action = ActionChains(bot)
                action.double_click(h2hlink).perform()
                h2hlink.click()
            except:
                h2hclick1.click()
                h2hlink.click()
                print("h2h link clicked twice")

            print("toogle head to head opened")

            scoresList = []
            scores = WebDriverWait(bot, 20).until(
                ec.presence_of_all_elements_located((By.CLASS_NAME, "st-score__value")))
            # scores = bot.find_elements(by=By.CLASS_NAME, value="st-score__value")
            for score in scores:
                print("Score: " + score.text)
                scoresList.append(score.text)
            print("The scorelist is :")
            print(scoresList)
            logging.info(scoresList)

            # Bet Analysis Variables
            totalscores = len(scoresList)
            zeros = scoresList.count('0')
            zerostreshold = 100 * zeros / totalscores

            if totalscores < 3:
                print("Not enough statistics for analysis. The bot will proceed to the next league")
                scoresList.clear()
                bot.close()
                bot.switch_to.window(parent)
                logging.info('odds not favorable')
                logging.info('Going to the next game')
                print('odds not favorable')
                print('Going to the next game')
                # Click on sports link
                open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
                open_sports.click()
                logging.info('Clicked Sports')

                # click on table tennis
                open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
                open_tt.click()
                logging.info('Clicked Table Tennis')
                setkacup()

            elif 2.9 < totalscores and zerostreshold < 25:
                scoresList.clear()
                bot.close()
                bot.switch_to.window(parent)
                # bot.switch_to.default_content()

            # Scroll market to center of page
            desired_y = (clickmarket.size['height'] / 2) + clickmarket.location['y']
            current_y = (bot.execute_script('return window.innerHeight') / 2) + bot.execute_script(
                'return window.pageYOffset')
            scroll_y_by = desired_y - current_y
            bot.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
            scroll = ActionChains(bot)
            scroll.move_to_element(clickmarket).perform()
            # clickmarket.click()
            # logging.info('Market added to betslip')
            # Go to place bet function
            # placebet()

            logging.info('Pro league Bet placed.......................!')
            bot.refresh()
            logging.info("Page refreshed")
            # Click on sports link
            open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
            open_sports.click()
            logging.info('Clicked Sports')

            # click on table tennis
            open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
            open_tt.click()
            logging.info('Clicked Table Tennis')
            setkacup()
        else:

            logging.info('odds not favorable')
            logging.info('Going to the next game')
            # Click on sports link
            open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
            open_sports.click()
            logging.info('Clicked Sports')

            # click on table tennis
            open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
            open_tt.click()
            logging.info('Clicked Table Tennis')
            setkacup()
    except NoSuchElementException:
        logging.info('Over 3.5 Market not found. Going to next game')
        # Click on sports link
        open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
        open_sports.click()
        logging.info('Clicked Sports')

        # click on table tennis
        open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
        open_tt.click()
        logging.info('Clicked Table Tennis')
        setkacup()

# Setka Cup First Game function
def setkacup():
    # Click on sports link
    open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
    open_sports.click()
    logging.info('Clicked Sports')

    # click on table tennis
    open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
    open_tt.click()
    logging.info('Clicked Table Tennis')

    # go to search to quit dropdown
    go_to_search = bot.find_element(by=By.CLASS_NAME, value=searchfield)
    go_to_search.click()
    logging.info('Clicked Search')

    try:
        # open Pro League Tournament
        open_setka_cup = WebDriverWait(bot, 30).until(ec.presence_of_element_located((By.XPATH, setkacuplink)))
        open_setka_cup.click()
    except:
        logging.info("Setka Cup Tournament not found !!!!!!")
        logging.info("Skipping to Pro League ..........................")
        print("Setka Cup Tournament not found !!!!!!")
        print("Skipping to Pro League..........................")
        proleague()
    logging.info('This Point')

    # Select Second game
    first_setka_cup_gamexPath = "(//a[@data-liga='1733171'])[1]"
    first_setka_cup_game = WebDriverWait(bot, 30).until(ec.presence_of_element_located((By.XPATH, first_setka_cup_gamexPath)))

    first_setka_cup_game.click()
    logging.info('First Setka cup game opened')
    print('First Setka cup game opened')

    # league = bot.find_element(by=By.XPATH, value=leaguename)
    league = WebDriverWait(bot, 30).until(ec.presence_of_element_located((By.XPATH, leaguename)))

    team1Xpath = "(//div[@class='team']//a)[1]"
    team2Xpath = "(//div[@class='team'])[2]"
    gametimeXpath = "(//div[@class='time']//div)[2]"
    team1 = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, team1Xpath)))
    team2 = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, team2Xpath)))
    gametime = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, gametimeXpath)))

    # Dictionary to hold game details
    gamedetails = {}
    gamedetails["team1"] = team1
    gamedetails["team2"] = team2
    gamedetails["gametime"] = gametime

    # Check GameList if the game has been analysed before
    if gamedetails in GamesList:
        # Go to next game
        logging.info("This game has been analysed already!!!!!")
        logging.info("Skipping to the next game..............")
        print("This game has been analysed already !!!!!")
        print("Skipping to the next game..............")
        # Click on sports link
        open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
        open_sports.click()
        logging.info('Clicked Sports')

        # click on table tennis
        open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
        open_tt.click()
        logging.info('Clicked Table Tennis')
        setkacup2()
    else:
        # Add Game details to the Bet list
        GamesList.append(gamedetails)
        logging.info("The game details have been added to the Analysed List")
        print("The game details have been added to the analysed list")

    logging.info('League :' + league.text)

    team1odds = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, teamoneodds)))
    logging.info('Team 1 odds:' + team1odds.text)
    team2odds = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, teamtwoodds)))
    logging.info('Team 2 odds:' + team2odds.text)

    statsdropdown = bot.find_element(by=By.XPATH, value="(//button[@title='Statistics'])[1]")
    statslink = bot.find_element(by=By.XPATH, value="//button[@title='Statistics']//span[1]")

    try:
        clickmarket = bot.find_element(by=By.XPATH, value=market)
        if (float(team1odds.text) >= 1.28 and float(team2odds.text) >= 1.28):

            logging.info('Favorable bet found')

            statsdropdown.click()
            statslink.click()
            logging.info('Stats link clicked')
            # ObtainWindow handle for stats window
            statswindow = bot.window_handles[1]
            bot.switch_to.window(statswindow)
            print("Stats window opened")

            WebDriverWait(bot, 20).until(ec.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[contains(@class,'st-portal st-integration__portal')]")))
            h2hclick1 = WebDriverWait(bot, 20).until(
                ec.element_to_be_clickable((By.XPATH, "(//div[@class='st-switch__text'])[2]")))

            print("Accessed iframe and ready to collect statistics")
            # Click head to head
            get_title = bot.title
            print("The title is : " + get_title)

            h2hlink = bot.find_element(by=By.XPATH, value="/html/body/div/div/div/div/div[1]/div[2]/div[2]/a[2]")

            try:
                WebDriverWait(bot, 20).until(
                    ec.element_to_be_clickable((By.XPATH, "(//div[@class='st-switch__text'])[2]")))
                h2hclick1.click()
                # Double click if the first click did not respond
                action = ActionChains(bot)
                action.double_click(h2hlink).perform()
                h2hlink.click()
            except:
                h2hclick1.click()
                h2hlink.click()
                print("h2h link clicked twice")

            print("toogle head to head opened")

            scoresList = []
            scores = WebDriverWait(bot, 20).until(
                ec.presence_of_all_elements_located((By.CLASS_NAME, "st-score__value")))
            # scores = bot.find_elements(by=By.CLASS_NAME, value="st-score__value")
            for score in scores:
                print("Score: " + score.text)
                scoresList.append(score.text)
            print("The scorelist is :")
            print(scoresList)
            logging.info(scoresList)

            # Bet Analysis Variables
            totalscores = len(scoresList)
            zeros = scoresList.count('0')
            zerostreshold = 100 * zeros / totalscores

            if totalscores < 3:
                print("Not enough statistics for analysis. The bot will proceed to the next league")
                scoresList.clear()
                bot.close()
                bot.switch_to.window(parent)
                logging.info('odds not favorable')
                logging.info('Going to the next game')
                print('odds not favorable')
                print('Going to the next game..')
                # Click on sports link
                open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
                open_sports.click()
                logging.info('Clicked Sports')

                # click on table tennis
                open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
                open_tt.click()
                logging.info('Clicked Table Tennis')
                setkacup2()

            elif 2.9 < totalscores and zerostreshold < 25:
                scoresList.clear()
                bot.close()
                bot.switch_to.window(parent)
                # bot.switch_to.default_content()

            # Scroll market to center of page
            desired_y = (clickmarket.size['height'] / 2) + clickmarket.location['y']
            current_y = (bot.execute_script('return window.innerHeight') / 2) + bot.execute_script(
                'return window.pageYOffset')
            scroll_y_by = desired_y - current_y
            bot.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
            scroll = ActionChains(bot)
            scroll.move_to_element(clickmarket).perform()
            # clickmarket.click()
            # logging.info('Market added to betslip')
            # Go to place bet function
            # placebet()

            logging.info('Pro league Bet placed.......................!')
            bot.refresh()
            logging.info("Page refreshed")
            # Click on sports link
            open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
            open_sports.click()
            logging.info('Clicked Sports')

            # click on table tennis
            open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
            open_tt.click()
            logging.info('Clicked Table Tennis')
            setkacup2()
        else:

            logging.info('odds not favorable')
            logging.info('Going to the next game')
            # Click on sports link
            open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
            open_sports.click()
            logging.info('Clicked Sports')

            # click on table tennis
            open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
            open_tt.click()
            logging.info('Clicked Table Tennis')
            setkacup2
    except NoSuchElementException:
        logging.info('Over 3.5 Market not found. Going to next game')
        # Click on sports link
        open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
        open_sports.click()
        logging.info('Clicked Sports')

        # click on table tennis
        open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
        open_tt.click()
        logging.info('Clicked Table Tennis')
        setkacup2()

def setkacup2():
    # Click on sports link
    open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
    open_sports.click()
    logging.info('Clicked Sports')

    # click on table tennis
    open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
    open_tt.click()
    logging.info('Clicked Table Tennis')

    # go to search to quit dropdown
    go_to_search = bot.find_element(by=By.CLASS_NAME, value=searchfield)
    go_to_search.click()
    logging.info('Clicked Search')

    try:
        # open Pro League Tournament
        open_setkacup2 = WebDriverWait(bot, 30).until(ec.presence_of_element_located((By.XPATH, setkacuplink)))
        open_setkacup2.click()
    except:
        logging.info("Setka Cup Tournament not found !!!!!!")
        logging.info("Skipping to Pro League..........................")
        print("Setka Cup League Tournament not found !!!!!!")
        print("Skipping to Pro League ..........................")
        proleague()
    logging.info('This Point')

    # Select Second game
    second_setka_cup_gamexPath = "(//a[@data-liga='1733171'])[2]"
    second_setka_cup_game = WebDriverWait(bot, 30).until(ec.presence_of_element_located((By.XPATH, second_setka_cup_gamexPath)))

    second_setka_cup_game.click()
    logging.info('Second Pro league game opened')
    print('Second Pro league game opened')

    league = bot.find_element(by=By.XPATH, value=leaguename)

    team1Xpath = "(//div[@class='team']//a)[1]"
    team2Xpath = "(//div[@class='team'])[2]"
    gametimeXpath = "(//div[@class='time']//div)[2]"
    team1 = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, team1Xpath)))
    team2 = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, team2Xpath)))
    gametime = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, gametimeXpath)))

    # Dictionary to hold game details
    gamedetails = {}
    gamedetails["team1"] = team1
    gamedetails["team2"] = team2
    gamedetails["gametime"] = gametime

    # Check GameList if the game has been analysed before
    if gamedetails in GamesList:
        # Go to next game
        logging.info("This game has been analysed already!!!!!")
        logging.info("Skipping to the next game..............")
        print("This game has been analysed already !!!!!")
        print("Skipping to the next game..............")
        # Click on sports link
        open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
        open_sports.click()
        logging.info('Clicked Sports')

        # click on table tennis
        open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
        open_tt.click()
        logging.info('Clicked Table Tennis')
        proleague()
    else:
        # Add Game details to the Bet list
        GamesList.append(gamedetails)
        logging.info("The game details have been added to the Analysed List")
        print("The game details have been added to the analysed list")

    logging.info('League :' + league.text)

    team1odds = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, teamoneodds)))
    logging.info('Team 1 odds:' + team1odds.text)
    team2odds = WebDriverWait(bot, 10).until(ec.visibility_of_element_located((By.XPATH, teamtwoodds)))
    logging.info('Team 2 odds:' + team2odds.text)

    statsdropdown = bot.find_element(by=By.XPATH, value="(//button[@title='Statistics'])[1]")
    statslink = bot.find_element(by=By.XPATH, value="//button[@title='Statistics']//span[1]")

    try:
        clickmarket = bot.find_element(by=By.XPATH, value=market)
        if (float(team1odds.text) >= 1.28 and float(team2odds.text) >= 1.28):

            logging.info('Favorable bet found')

            statsdropdown.click()
            statslink.click()
            logging.info('Stats link clicked')
            # ObtainWindow handle for stats window
            statswindow = bot.window_handles[1]
            bot.switch_to.window(statswindow)
            print("Stats window opened")

            WebDriverWait(bot, 20).until(ec.frame_to_be_available_and_switch_to_it(
                (By.XPATH, "//iframe[contains(@class,'st-portal st-integration__portal')]")))
            h2hclick1 = WebDriverWait(bot, 20).until(
                ec.element_to_be_clickable((By.XPATH, "(//div[@class='st-switch__text'])[2]")))

            print("Accessed iframe and ready to collect statistics")
            # Click head to head
            get_title = bot.title
            print("The title is : " + get_title)

            h2hlink = bot.find_element(by=By.XPATH, value="/html/body/div/div/div/div/div[1]/div[2]/div[2]/a[2]")

            try:
                WebDriverWait(bot, 20).until(
                    ec.element_to_be_clickable((By.XPATH, "(//div[@class='st-switch__text'])[2]")))
                h2hclick1.click()
                # Double click if the first click did not respond
                action = ActionChains(bot)
                action.double_click(h2hlink).perform()
                h2hlink.click()
            except:
                h2hclick1.click()
                h2hlink.click()
                print("h2h link clicked twice")

            print("toogle head to head opened")

            scoresList = []
            scores = WebDriverWait(bot, 20).until(
                ec.presence_of_all_elements_located((By.CLASS_NAME, "st-score__value")))
            # scores = bot.find_elements(by=By.CLASS_NAME, value="st-score__value")
            for score in scores:
                print("Score: " + score.text)
                scoresList.append(score.text)
            print("The scorelist is :")
            print(scoresList)
            logging.info(scoresList)

            # Bet Analysis Variables
            totalscores = len(scoresList)
            zeros = scoresList.count('0')
            zerostreshold = 100 * zeros / totalscores

            if totalscores < 3:
                print("Not enough statistics for analysis. The bot will proceed to the next league")
                scoresList.clear()
                bot.close()
                bot.switch_to.window(parent)
                logging.info('odds not favorable')
                logging.info('Going to the next game')
                print('odds not favorable')
                print('Going to the next game')
                # Click on sports link
                open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
                open_sports.click()
                logging.info('Clicked Sports')

                # click on table tennis
                open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
                open_tt.click()
                logging.info('Clicked Table Tennis')
                proleague()

            elif 2.9 < totalscores and zerostreshold < 25:
                scoresList.clear()
                bot.close()
                bot.switch_to.window(parent)
                # bot.switch_to.default_content()

            # Scroll market to center of page
            desired_y = (clickmarket.size['height'] / 2) + clickmarket.location['y']
            current_y = (bot.execute_script('return window.innerHeight') / 2) + bot.execute_script('return window.pageYOffset')
            scroll_y_by = desired_y - current_y
            bot.execute_script("window.scrollBy(0, arguments[0]);", scroll_y_by)
            scroll = ActionChains(bot)
            scroll.move_to_element(clickmarket).perform()
            # clickmarket.click()
            # logging.info('Market added to betslip')
            # Go to place bet function
            # placebet()

            logging.info('Pro league Bet placed.......................!')
            bot.refresh()
            logging.info("Page refreshed")
            # Click on sports link
            open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
            open_sports.click()
            logging.info('Clicked Sports')

            # click on table tennis
            open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
            open_tt.click()
            logging.info('Clicked Table Tennis')
            proleague()
        else:

            logging.info('odds not favorable')
            logging.info('Going to the next game')
            # Click on sports link
            open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
            open_sports.click()
            logging.info('Clicked Sports')

            # click on table tennis
            open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
            open_tt.click()
            logging.info('Clicked Table Tennis')
            proleague()
    except NoSuchElementException:
        logging.info('Over 3.5 Market not found. Going to next game')
        # Click on sports link
        open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
        open_sports.click()
        logging.info('Clicked Sports')

        # click on table tennis
        open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
        open_tt.click()
        logging.info('Clicked Table Tennis')
        proleague()


# Start pro league
proleague()

# scroll = ActionChains(bot)
# scroll.move_to_element(open_pro_league).perform()
# open_pro_league.click()
# logging.info('Opened Pro League')


# driver.quit()
