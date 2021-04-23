# -*- coding: utf-8 -*-
"""
Created on Fri Mar 26 14:08:18 2021

@author: Boss
"""
import socket
import select
import errno
import sys

import game
import pickle
import time
from network import Network


nofw = 4
status = ""

user_ans = ""

def receivedRacks(myPlayer, n, myNumber):
    name = "Name: "
    Dice = "Dice: "
    Bought = "buying racks "
    Sold = "Sold: "
    get = "get"
    Iplayed = "Played"
    for tile in myPlayer.rack.get_temp_arr():  
        print(tile.letter, tile.score)
    print("Total value of your draw is: ", myPlayer.rack.get_temp_value())    
    if myPlayer.money >= myPlayer.rack.get_temp_value():
        print("You have:  $", myPlayer.money)
        user_ans = ""
        while user_ans.upper() != ("Y" or "N"):
            user_ans = input("Do you want to buy words? (Y-N)").upper()
            time.sleep(1)
            print(f" you entered {user_ans}")
            if user_ans == "Y":
                print("user wants to buy")
                try:
                    myGame = n.send(Bought)
                except:
                    continue 
                time.sleep(0.5)
                # myGame = n.send(Bought)
                # time.sleep(0.5)
            
                while True:
                    time.sleep(1)
                    serverMessage = myGame.getServerMessage()
                    print(f"serverMessage: {serverMessage} ")
                    if "Purchased" in serverMessage:
                        break
                    else:
                        try:
                            myGame = n.send(get)
                        except:
                            continue
                myPlayer = myGame.getPlayer(myNumber)
                print("you now have $", myPlayer.money)
                #for tile in player.get_rack_arr():
                 #   print(tile.letter)
                 
            else:
                break
        else:
            print("You have insufficient funds to purchase tiles")
            
        print("Your rack contains: ")
        for tile in myPlayer.get_rack_arr():
            print(tile.letter, tile.score)
      
        sell = input("Do you want to sell any words? Y/N ")
        if sell.upper() == "Y":
            attempt = 3
            while attempt >0:
                wordToSell = input("input word to sell: ")
                
                myPlayer.sell(wordToSell)
                  
                if myPlayer.sell_check:
                    Sold += wordToSell
                    myGame = n.send(Sold)
                    time.sleep(1)
                    # myGame = n.send(Sold)
                    # time.sleep(1)
                    while True:
                        myGame = n.send(get)
                        time.sleep(1)
                        serverMessage = myGame.getServerMessage()
                        print(f"serverMessage: {serverMessage} ")
                        if "SOLD" in serverMessage:
                            break
                    myPlayer = myGame.getPlayer(myNumber)
                    
                    print("You sold by $",myPlayer.wordvalue)
                    # myPlayer.addPlayerMessage(f" sold {wordToSell}")
                    break
                else:
                    attempt -=1
                    print("You failed to sell the word, ", attempt," attempts left" )
            print("You now have: $",myPlayer.money)
            # sending player object to game 
            myGame = n.send(Iplayed)
            return myGame

def main():
    name = "Name: "
    Dice = "Dice: "
    Bought = "buying racks "
    Sold = "Sold: "
    get = "get"
    firstRun = True
    i = 0
    print("lets send network")
    try:
        n = Network()
        print("we connected to network")
        print(n.p)
        myNumber = n.p 
    except Exception as e:
        print(e)
        print("couldnt connect")
        
        time.sleep(2)
        
    run = True
    # firstRun = True
    inLobby = True
    print(f" I am player number {myNumber}")
    while run:
        if firstRun:
            print("welcome to buyGame")
            firstRun = False
        else:
            print(f"round {i}")
        # if firstRun:
        try:
            #print("fetching game")
            myGame = n.send("get")
        except:
            # run = False
            print("cant get game")
            break
            # firstRun = False
        
        time.sleep(1)
        
        # backupGame = myGame
        user_ans = ""
        
        if myGame != False:
            
            myPlayer = myGame.getPlayer(myNumber)
            #print("number success")
        # 
        while inLobby:
            user_ans = input("enter name to change name, or 1 to begin game ")
            print(user_ans)
            if user_ans == "name":
                myName = "Name: " + str(input("enter your name: "))
                name += myName
                print(f"you entered: {myName} is this Correct?")
                input("Enter")
                
                try:
                    myGame = n.send(myName)
                    time.sleep(2)
                except Exception as e:
                    print(e)
                time.sleep(1)
            elif user_ans == "1":
                try:  
                    myGame = n.send("start")
                    time.sleep(1)
                except Exception as e:
                    print(e)
                if myGame == False:
                    print("not my game!")
                    break
            # if myGame == False:
            #     myGame = n.send("get")
            #     time.sleep(1)
            if myGame.leader == myNumber:
                # i am the leader 
                # print(myGame.leader)
                # print("Leader^ me v")
                # print(myNumber)
                print("You are the leader you begin")
                inLobby = False
            elif myGame.ready:
                print("game state is ready ")
                inLobby = False
                        
        # outside lobby now it is the game 
        time.sleep(1)
        try:
            # myGame = n.send(get)
            # myGame = n.send(get)
            # myGame = n.send(get)
            myGame = n.send(get)
            time.sleep(1)
        except Exception as e:
            print(e)
        if myNumber == myGame.currentPlayer:
            print("it is your turn to roll")
            input("Press enter to roll dice:")
            diceValue = str(game.dice_roll())
            diceMessage = Dice + diceValue
            try:
                myGame = n.send(diceMessage)
                serverMessage = myGame.getServerMessage()
                print(f"serverMessage: {serverMessage} ")
                # time.sleep(0.5)
                # myGame = n.send(diceMessage)
            except Exception as e:
                print(e)
            try:
                myGame = n.send(get)
            
                time.sleep(1)
            except Exception as e:
                print(e)
        myPlayer = myGame.getPlayer(myNumber)
        serverMessage = myGame.getServerMessage()
        if "Racks" in serverMessage:
            try:
                myGame = receivedRacks(myPlayer, n, myNumber )
            except Exception as e:
                print(e)
            # myPlayer = myGame.getPlayer(myNumber)
            # serverMessage = myGame.getServerMessage()
            # print(f"serverMessage: {serverMessage} ")
            # while True:
            #     serverMessage = myGame.getServerMessage()
            #     print(f"serverMessage: {serverMessage} ")
            #     if "Racks" in serverMessage:
                    
            #         myPlayer = myGame.getPlayer(myNumber)
            #         for tile in myPlayer.rack.get_temp_arr():  
            #             print(tile.letter, tile.score)
            #         break
            #     else:
            #         print("no racks ")
            #         try:
            #             myGame = n.send(get)
            #         except:
            #             continue
            #         time.sleep(2)
            #         continue
            # print("Total value of your draw is: ", myPlayer.rack.get_temp_value())    
            # if myPlayer.money >= myPlayer.rack.get_temp_value():
            #     print("You have:  $", myPlayer.money)
            #     user_ans = ""
            #     while user_ans.upper() != ("Y" or "N"):
            #       user_ans = input("Do you want to buy words? (Y-N)").upper()
            #       time.sleep(1)
            #       print(f" you entered {user_ans}")
            #       if user_ans == "Y":
            #           print("user wants  to buy")
            #           try:
            #               myGame = n.send(Bought)
            #           except:
            #               continue 
            #           time.sleep(0.5)
            #           # myGame = n.send(Bought)
            #           # time.sleep(0.5)
                      
            #           while True:
                          
            #               time.sleep(1)
            #               serverMessage = myGame.getServerMessage()
            #               print(f"serverMessage: {serverMessage} ")
            #               if "Purchased" in serverMessage:
            #                   break
            #               else:
            #                   try:
            #                       myGame = n.send(get)
            #                   except:
            #                       continue
            #           myPlayer = myGame.getPlayer(myNumber)
            #           print("you now have $", myPlayer.money)
            #           #for tile in player.get_rack_arr():
            #            #   print(tile.letter)
                       
            #       else:
            #           break
            # else:
            #     print("You have insufficient funds to purchase tiles")
                
            # print("Your rack contains: ")
            # for tile in myPlayer.get_rack_arr():
            #     print(tile.letter, tile.score)
          
            # sell = input("Do you want to sell any words? Y/N ")
            # if sell.upper() == "Y":
            #     attempt = 3
            #     while attempt >0:
            #         wordToSell = input("input word to sell: ")
                    
            #         myPlayer.sell(wordToSell)
                      
            #         if myPlayer.sell_check:
            #             Sold += wordToSell
            #             myGame = n.send(Sold)
            #             time.sleep(1)
            #             # myGame = n.send(Sold)
            #             # time.sleep(1)
            #             while True:
            #                 myGame = n.send(get)
            #                 time.sleep(1)
            #                 serverMessage = myGame.getServerMessage()
            #                 print(f"serverMessage: {serverMessage} ")
            #                 if "SOLD" in serverMessage:
            #                     break
            #             myPlayer = myGame.getPlayer(myNumber)
                        
            #             print("You sold by $",myPlayer.wordvalue)
            #             # myPlayer.addPlayerMessage(f" sold {wordToSell}")
            #             break
            #         else:
            #             attempt -=1
            #             print("You failed to sell the word, ", attempt," attempts left" )
            #     print("You now have: $",myPlayer.money)
            #     # sending player object to game 
            if myGame.leader == myNumber:
                myGame = n.send("Done")
            
        else:
            print(f"Player {myGame.currentPlayer} is currently playing")
        try:
            myGame = n.send(get)
            sData = myGame.getServerMessage()
            if  sData == "Done":
                print(f"round {i} done, time for next round ")
                i += 1
            # elif "Racks" in sData:
            #     myPlayer = myGame.getPlayer(myNumber)
            #     print("Your rack contains ")
            #     for tile in myPlayer.rack.get_temp_arr():
            #         print(tile.letter, tile.score)
                
                    
                time.sleep(3)
        except Exception as e:
            print(e)
        
          # done selling        
if __name__ == '__main__':
    main()
                
