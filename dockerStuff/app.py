import time
import json
from playsound import playsound
import colorama
from colorama import Back, Fore, Style
from pathlib import Path
import os
import sys

colorama.init(autoreset=True)

s = {"time_unit": 0, "time_unit_string": "seconds", "study_length": 0, "break_length": 0}
settings_path = Path("Settings.json")

def ask_import():
    while True:
        print(Fore.YELLOW + "Would you like to import settings from a file? ([y]/n)")
        import_settings = input(">>> ")
        if (import_settings.capitalize() != 'Y' and import_settings.capitalize() != 'N' and import_settings != ''):
            print(Fore.RED + "Please give either an empty answer, y, or n")
            continue
        break
    return import_settings

def import_settings():
    while True:
        import_settings = ask_import()

        if (import_settings.capitalize() == 'Y' or import_settings == ''):
            try:
                with open('Settings.json', 'r') as file:
                    settings = json.load(file)
                    s["time_unit"] = settings["time_unit"]
                    s["time_unit_string"] = settings["time_unit_string"]
                    s["study_length"] = settings["study_length"]
                    s["break_length"] = settings["break_length"]
                    print(Fore.YELLOW + "successfully loaded with time unit as {}, study time as {}, and break time as {}!".format(s["time_unit_string"], s["study_length"], s["break_length"]))
                    return True
            except:
                print(Fore.RED + "There either is no settings file, it's empty, or it doesn't have all the required fields")
                print(Fore.RED + "(I would suggest inputting the values here the first time around)")
                continue
        return False

def ask_time_unit():
    while True:
        print(Fore.YELLOW + "Which time unit would you like to use? (0 = Seconds, [1 = Minutes], 2 = Hours)")
        s["time_unit"] = input(">>> ")
        if (s["time_unit"] == ''):
            s["time_unit_string"] = "minutes"
            break
        else:
            s["time_unit"] = int(s["time_unit"])
            if s["time_unit"] == 0:
                s["time_unit_string"] = "seconds"
                break
            elif s["time_unit"] == 1:
                s["time_unit_string"] = "minutes"
                break
            elif s["time_unit"] == 2:
                s["time_unit_string"] = "hours"
                break
            else:
                print(Fore.RED + "Please provide one of the listed numbers (or an empty answer)")
                continue

def ask_study_period():
    while True:
        print(Fore.YELLOW + "How long would you like the study period to be?")
        s["study_length"] = int(input(">>> "))
        if (s["study_length"] < 0 or s["study_length"] >= 60):
            print(Fore.RED + "Study length cannot be 0 or negative, and can be at most 60")
            continue
        break

def ask_full_hour():
    while True:
        print(Fore.YELLOW + "Would you like the study-break period to be a full 60 units? ([y]/n)")
        hour_full = input(">>> ")
        if (hour_full.capitalize() != 'Y' and hour_full.capitalize() != 'N' and hour_full != ''):
            print(Fore.RED + "Please give either an empty answer, y, or n")
            continue
        elif (hour_full.capitalize() == 'Y' or hour_full == ''):
            return True
        else:
            return False

def ask_break_period(full_hour):
    if (full_hour):
        s["break_length"] = 60 - s["study_length"]
    else:
        while True:
            print(Fore.YELLOW + "How long would you like the break period to be? (Also in the same time unit)")
            s["break_length"] = int(input(">>> "))
            if (s["break_length"] < 0 or s["break_length"] >= 60):
                print(Fore.RED + "Break length cannot be 0 or negative, and can be at most 60")
                continue
            break

def ask_save():
    while True:
        print(Fore.YELLOW + "Would you like to save your settings for future use? ([y]/n)")
        save_settings = input(">>> ")
        if (save_settings.capitalize() != 'Y' and save_settings.capitalize() != 'N' and save_settings != ''):
            print(Fore.RED + "Please give either an empty answer, y, or n")
            continue
        elif (save_settings.capitalize() == 'Y' or save_settings == ''):
            if settings_path.is_file():
                settings_path.unlink()
            with open('Settings.json', 'a') as file:
                json.dump(s, file)
        break



def ask_settings():
    if (import_settings() == False):


        
        ask_time_unit()

        ask_study_period()
        
        FULL_HOUR = ask_full_hour()

        ask_break_period(FULL_HOUR)

        ask_save()



def main():
    ask_settings()
    os.system("cls")
    
    study_message = Back.RED + Fore.BLACK + "Time to study!"

    break_message1 =                Back.RED + "     " + Back.YELLOW + "  " + Back.GREEN + "  " + Back.CYAN + "  " + Back.BLUE + "  " + Back.MAGENTA + "     \n"
    break_message2 = Fore.WHITE +   Back.RED + "   BR" + Back.YELLOW + "EA" + Back.GREEN + "K " + Back.CYAN + "TI" + Back.BLUE + "ME" + Back.MAGENTA + "!!   \n"
    break_message3 =                Back.RED + "     " + Back.YELLOW + "  " + Back.GREEN + "  " + Back.CYAN + "  " + Back.BLUE + "  " + Back.MAGENTA + "     "
    break_message = break_message1 + break_message2 + break_message3
    
    if (s["time_unit"] == 2):
        s["time_unit"] = 3600
    elif (s["time_unit"] == '' or s["time_unit"] == 1):
        s["time_unit"] = 60
    elif (s["time_unit"] == 0):
        s["time_unit"] = 1

    study_length = s["study_length"] * int(s["time_unit"])
    break_length = s["break_length"] * int(s["time_unit"])

    if (len(sys.argv) > 1):
        if (sys.argv[1] == 'hihi'):
            while True:
                timer(break_message, 'yippee.mp3', break_length, Fore.GREEN)
                timer(study_message, 'naurr.mp3', study_length, Fore.RED)
    while True:
        timer(study_message, 'naurr.mp3', study_length, Fore.RED)
        timer(break_message, 'yippee.mp3', break_length, Fore.GREEN)

def timer(message, sound, length, clock_color):
        print(message)
        playsound(sound)
        print("")

        for i in range(length, 0, -1):
            seconds = i % 60
            minutes = int(i / 60) % 60
            hours = int(i / 3600)
            clock = f"{hours:02}:{minutes:02}:{seconds:02}"

            print(clock_color + clock, end = '\r')
            time.sleep(1)
        os.system("cls")

if __name__ == "__main__":
    main()
