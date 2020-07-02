import json
import os
import random
import time
from itertools import repeat

import hiveengine
import schedule
import steemengine
from beem import Steem
from beem.account import Account
from beem.nodelist import NodeList
from hiveengine.tokenobject import Token
from hiveengine.wallet import Wallet

# Settings
send_account = ""   # account to send the tokens from
token_to_check = "ARCHON" # Change to your token
type_to_check = "stake"  # "stake" or "balance"
token_to_send = "ARCHONM" 
minimum_balance = 25    # or minimum stake
amount_to_split = 50   # Amount in account to split up between holders. Because of rounding, allow for +/- 1% in your balance before sending
beem_unlock_pass = "" # your password to unlock beem




def drop():
    total = 0
    holders = Token(token_to_check)
    nodelist = NodeList()
    nodelist.update_nodes()
    nodes = nodelist.get_nodes(hive=False)
    nodes2 = nodelist.get_nodes(hive=True)
    hive = Steem(node=nodes2)
    wallet = Wallet(send_account, steem_instance=hive)
    holder = holders.get_holder()
    for h in holder:
        account = h["account"]
        balance = h[type_to_check]
        if float(balance) < 25:
            continue
        print(account + " with " + balance)
        total = total + float(balance)
    print(total)
    total_sent = 0
    for h in holder:
        account = h["account"]
        balance = h[type_to_check]
        if float(balance) < 25:
            continue
        share = float(balance) / total
        tosend = share * 50
        tosend = round(tosend, 6)
        print(account + " gets " + str(tosend) + token_to_send + " from " + str(balance) + " " + token_to_check)
        total_sent = total_sent + tosend
        memo = str(token_to_send + " airdrop based on your stake of " + str(balance) + token_to_check)
        hive.wallet.unlock(beem_unlock_pass)
        if account == send_account:
            print("Skipping send account (can't send to myself)")
            continue
        print(wallet.transfer(account, tosend, token_to_send, memo=memo))
        time.sleep(3)
    print(total_sent)


drop()
