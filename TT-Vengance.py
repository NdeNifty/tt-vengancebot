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
logging.info('Acccount balance is :' + account_balance.text)

#obtain parent window handle
parent = bot.window_handles[0]

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


# Analyse Statistics
# def analysis_algorithm():
#     logging.info('opened the analysis algorithm')
#     #statsdropdownxpath = "(//button[@class='c-events__toggle-statistics'])[2]"
#     #statslinkxpath = "(//span[@class='c-events-statistics__title'])[1]"
#     statsdropdown = bot.find_element(by=By.XPATH, value="(//button[@class='c-events__toggle-statistics'])[2]")
#     statslink = bot.find_element(by=By.XPATH, value="(//span[@class='c-events-statistics__title'])[1]")
#
#     statsdropdown.click()
#     statslink.click()
#     logging.info('Stats link opened')

# select Pro League
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
        # open_pro_league = bot.find_element(by=By.XPATH, value=proleaguelink)
        open_pro_league = WebDriverWait(bot, 5).until(ec.presence_of_element_located((By.XPATH, proleaguelink)))
        # open_pro_league = bot.find_element(by=By.XPATH, value="//a[@href='line/table-tennis/1197285-tt-cup']")
        open_pro_league.click()
    except:
        # open_pro_league = bot.find_element(by=By.XPATH, value=proleaguelink)
        open_pro_league = WebDriverWait(bot, 5).until(ec.presence_of_element_located((By.XPATH, proleaguelink)))
        # open_pro_league = bot.find_element(by=By.XPATH, value="//a[@href='line/table-tennis/1197285-tt-cup']")
        open_pro_league.click()
    logging.info('This Point')

    # Select First game
    first_pro_league_game = bot.find_element(by=By.XPATH, value="(//a[@data-liga='1691055'])[1]")
    # first_pro_league_game = bot.find_element(by=By.XPATH, value="(//a[@data-liga='1197285'])[1]")

    first_pro_league_game.click()
    logging.info('First Pro league game opened')

    # # Store iframe element
    # iframegameboard = bot.find_element(by=By.XPATH, value="//div[@class='st-integration']//iframe[1]")

    # # Go to iframe
    # bot.switch_to.frame(iframegameboard)

    league = bot.find_element(by=By.XPATH, value=leaguename)
    # team1 = WebDriverWait(bot, 3).until(ec.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[1]/div/div[2]")))

    # team1 = bot.find_element(by=By.XPATH, value="(//div[@class='team']//a)[1]")
    # team2 = bot.find_element(by=By.XPATH, value="(//div[@class='team'])[2]")
    # gametitle = team1.text + ' vs ' + team2.text
    # gametime = bot.find_element(by=By.XPATH, value="(//div[@class='time']//div)[2]")
    logging.info('League :' + league.text)

    team1odds = WebDriverWait(bot, 4).until(ec.visibility_of_element_located((By.XPATH, teamoneodds)))
    logging.info('Team 1 odds:' + team1odds.text)
    team2odds = WebDriverWait(bot, 2).until(ec.visibility_of_element_located((By.XPATH, teamtwoodds)))
    logging.info('Team 2 odds:' + team2odds.text)
    # team1odds = bot.find_element(by=By.XPATH, value="(//span[@class='koeff'])[1]")
    # team2odds = bot.find_element(by=By.XPATH, value="(//span[@class='koeff'])[2]")
    # logging.info('Team 1 odds:'+ team2odds.text)
    statsdropdown = bot.find_element(by=By.XPATH, value="(//button[@title='Statistics'])[1]")
    statslink = bot.find_element(by=By.XPATH, value="//button[@title='Statistics']//span[1]")

    try:
        clickmarket = bot.find_element(by=By.XPATH, value=market)
        if (float(team1odds.text) >= 1.28 and float(team2odds.text) >= 1.28):

            logging.info('Favorable bet found')
            # clickmarket.location_once_scrolled_into_view
            # bot.execute_script("return arguments[0].scrollIntoView();", clickmarket)

            statsdropdown.click()
            statslink.click()
            logging.info('Stats link clicked')
            # ObtainWindow handle for stats window
            statswindow = bot.window_handles[1]
            bot.switch_to.window(statswindow)
            print("Stats window opened")

            # Go to iframe
            #iframestatspage = bot.find_element(by=By.XPATH, value="//div[@class='st-integration st-integration--full-screen']//iframe[1]")
            WebDriverWait(bot, 15).until(ec.frame_to_be_available_and_switch_to_it((By.XPATH, "//div[@class='st-integration st-integration--full-screen']//iframe[1]")))
            print("Accessed iframe and ready to collect statistics")
            # Click head to head

            h2hlink = bot.find_element(by=By.XPATH, value="/html/body/div[1]/div/div/div/div[1]/div[2]/div[2]/a[2]/divx ")
            h2hlink.click()
            print("head to head opened")
            scores = bot.find_elements()

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


# TT-Cup function 
def ttcup():
    # go to search to quit dropdown
    go_to_search = bot.find_element(by=By.CLASS_NAME, value=searchfield)
    go_to_search.click()
    logging.info('Clicked Search')
    try:
        # select Pro TT-Cup
        # open_tt_cup = bot.find_element(by=By.XPATH, value=ttcuplink)
        open_tt_cup = WebDriverWait(bot, 8).until(ec.presence_of_element_located((By.XPATH, ttcuplink)))
    # open_pro_league = bot.find_element(by=By.XPATH, value="//a[@href='line/table-tennis/1197285-tt-cup']")
    except:
        try:
            open_tt_cup = WebDriverWait(bot, 8).until(ec.presence_of_element_located((By.XPATH, ttcuplink)))
            open_tt_cup.click()
        except:
            setkacup()
    logging.info('This Point')

    # Select First game
    first_tt_cup = bot.find_element(by=By.XPATH, value="(//a[@data-liga='1197285'])[1]")
    # first_pro_league_game = bot.find_element(by=By.XPATH, value="(//a[@data-liga='1197285'])[1]")

    first_tt_cup.click()
    logging.info('First TT- Cup game opened')

    # # Store iframe element
    # iframegameboard = bot.find_element(by=By.XPATH, value="//div[@class='st-integration']//iframe[1]")

    # # Go to iframe
    # bot.switch_to.frame(iframegameboard)

    league = bot.find_element(by=By.XPATH, value=leaguename)
    # team1 = WebDriverWait(bot, 3).until(ec.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[1]/div/div[2]")))

    # team1 = bot.find_element(by=By.XPATH, value="(//div[@class='team']//a)[1]")
    # team2 = bot.find_element(by=By.XPATH, value="(//div[@class='team'])[2]")
    # gametitle = team1.text + ' vs ' + team2.text
    # gametime = bot.find_element(by=By.XPATH, value="(//div[@class='time']//div)[2]")
    logging.info('League :' + league.text)
    # logging.info('Game : ' + team1.text + ' - ' + team2.text)
    # logging.info('Game Time : ' + gametime.text)

    team1odds = WebDriverWait(bot, 2).until(ec.visibility_of_element_located((By.XPATH, teamoneodds)))
    logging.info('Team 1 odds:' + team1odds.text)
    team2odds = WebDriverWait(bot, 1).until(ec.visibility_of_element_located((By.XPATH, teamtwoodds)))
    logging.info('Team 2 odds:' + team2odds.text)
    # team1odds = bot.find_element(by=By.XPATH, value="(//span[@class='koeff'])[1]")
    # team2odds = bot.find_element(by=By.XPATH, value="(//span[@class='koeff'])[2]")
    # logging.info('Team 1 odds:'+ team2odds.text)
    statsdropdown = bot.find_element(by=By.XPATH, value="(//button[@title='Statistics'])[1]")
    statslink = bot.find_element(by=By.XPATH, value="//button[@title='Statistics']//span[1]")

    try:
        clickmarket = bot.find_element(by=By.XPATH, value=market)
        if float(team1odds.text) >= 1.28 and float(team2odds.text) >= 1.28:
            logging.info('Favorable bet found')
            # clickmarket.location_once_scrolled_into_view
            # bot.execute_script("return arguments[0].scrollIntoView();", clickmarket)
            statsdropdown.click()
            statslink.click()
            logging.info('Stats link clicked')
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
            # placebet()

            logging.info('TT Cup Bet placed.......................!')
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
        logging.info('Over 3.5 Market not found. Going to next game -')
        # Click on sports link
        open_sports = bot.find_element(by=By.LINK_TEXT, value=sports)
        open_sports.click()
        logging.info('Clicked Sports')

        # click on table tennis
        open_tt = bot.find_element(by=By.LINK_TEXT, value=tabletennis)
        open_tt.click()
        logging.info('Clicked Table Tennis')
        setkacup()
        logging.info('Clicked Table Tennis')


# Setka Cup function
def setkacup():
    # go to search to quit dropdown
    go_to_search = bot.find_element(by=By.CLASS_NAME, value=searchfield)
    go_to_search.click()
    logging.info('Setka Cup Function')

    # select Pro League
    try:
        # open_setkacup = bot.find_element(by=By.XPATH, value=setkacuplink)
        open_setkacup = WebDriverWait(bot, 10).until(ec.presence_of_element_located((By.XPATH, setkacuplink)))
    # open_pro_league = bot.find_element(by=By.XPATH, value="//a[@href='line/table-tennis/1197285-tt-cup']")
    except:
        open_setkacup = WebDriverWait(bot, 10).until(ec.presence_of_element_located((By.XPATH, setkacuplink)))
    open_setkacup.click()
    logging.info('This point: Setka Cup games')

    # Select First game
    first_setkacup = bot.find_element(by=By.XPATH, value="(//a[@data-liga='1733171'])[1]")
    # first_pro_league_game = bot.find_element(by=By.XPATH, value="(//a[@data-liga='1197285'])[1]")

    first_setkacup.click()
    logging.info('First Pro league game opened')

    league = bot.find_element(by=By.XPATH, value=leaguename)
    # team1 = WebDriverWait(bot, 3).until(ec.visibility_of_element_located((By.XPATH, "/html/body/div[3]/div[1]/div[2]/div/div/div[3]/div/div/div/div[1]/div/div/div[1]/div/div/div[2]/div/div[1]/div/div[2]")))

    # team1 = bot.find_element(by=By.XPATH, value="(//div[@class='team']//a)[1]")
    # team2 = bot.find_element(by=By.XPATH, value="(//div[@class='team'])[2]")
    # gametitle = team1.text + ' vs ' + team2.text
    # gametime = bot.find_element(by=By.XPATH, value="(//div[@class='time']//div)[2]")
    logging.info('League :' + league.text)
    # logging.info('Game : ' + team1.text + ' - ' + team2.text)
    # logging.info('Game Time : ' + gametime.text)

    team1odds = WebDriverWait(bot, 2).until(ec.visibility_of_element_located((By.XPATH, teamoneodds)))
    logging.info('Team 1 odds:' + team1odds.text)
    team2odds = WebDriverWait(bot, 1).until(ec.visibility_of_element_located((By.XPATH, teamtwoodds)))
    logging.info('Team 2 odds:' + team2odds.text)
    # team1odds = bot.find_element(by=By.XPATH, value="(//span[@class='koeff'])[1]")
    # team2odds = bot.find_element(by=By.XPATH, value="(//span[@class='koeff'])[2]")
    # logging.info('Team 1 odds:'+ team2odds.text)

    statsdropdown = bot.find_element(by=By.XPATH, value="(//button[@title='Statistics'])[1]")
    statslink = bot.find_element(by=By.XPATH, value="//button[@title='Statistics']//span[1]")

    try:
        clickmarket = bot.find_element(by=By.XPATH, value=market)
        if (float(team1odds.text) >= 1.28 and float(team2odds.text) >= 1.28):
            logging.info('Favorable bet found')
            statsdropdown.click()
            statslink.click()

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
            # placebet()

            logging.info('Setka cup Bet placed.......................!')
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
        logging.info('Clicked Table Tennis')


# Start pro league
proleague()

# scroll = ActionChains(bot)
# scroll.move_to_element(open_pro_league).perform()
# open_pro_league.click()
# logging.info('Opened Pro League')


# driver.quit()
