from web3 import Web3
import argparse
import json

abi = json.loads('[{"inputs": [], "stateMutability": "nonpayable", "type": "constructor"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": true, "internalType": "address", "name": "spender", "type": "address"}, {"indexed": false, "internalType": "uint256", "name": "value", "type": "uint256"}], "name": "Approval", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "sender", "type": "address"}, {"indexed": true, "internalType": "uint256", "name": "coins", "type": "uint256"}], "name": "Deposit", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "uint256", "name": "stake", "type": "uint256"}, {"indexed": true, "internalType": "uint256", "name": "rewards", "type": "uint256"}], "name": "StakeInfo", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "uint256", "name": "access", "type": "uint256"}, {"indexed": true, "internalType": "uint256", "name": "withdraw", "type": "uint256"}], "name": "TimeInfo", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "from", "type": "address"}, {"indexed": true, "internalType": "address", "name": "to", "type": "address"}, {"indexed": false, "internalType": "uint256", "name": "value", "type": "uint256"}], "name": "Transfer", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "sender", "type": "address"}, {"indexed": true, "internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "Withdraw", "type": "event"}, {"anonymous": false, "inputs": [{"indexed": true, "internalType": "address", "name": "sender", "type": "address"}, {"indexed": true, "internalType": "uint256", "name": "totalCoins", "type": "uint256"}], "name": "WithdrawAll", "type": "event"}, {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "burn", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "account", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "burnFrom", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"}], "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "addedValue", "type": "uint256"}], "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"}, {"inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"}, {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transferFrom", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_coins", "type": "uint256"}], "name": "depositStaking", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "address", "name": "_user", "type": "address"}], "name": "getStakeInfo", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [{"internalType": "uint256", "name": "_amount", "type": "uint256"}], "name": "withdrawRewards", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "name": "withdrawAll", "outputs": [], "stateMutability": "nonpayable", "type": "function"}, {"inputs": [], "name": "getTimeAccessInfo", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}, {"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "nonpayable", "type": "function"}]')
def front(priv_key,contract_address):
    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    if not w3.isConnected():
        print("cannot connect to json rpc")
        return
    print("[+] complete connect to http json rpc")

    c = w3.eth.contract(address=Web3.toChecksumAddress(contract_address),abi=abi)
    sender = w3.eth.account.from_key(priv_key).address
    while True:
        print("""
[*]
    1: depositStaking(uint256 _coins)
    2: getStakeInfo(address owner)
    3: withdrawRewards(uint256 _amount)
    4: balanceOf(address owner) returns(uint256)
    5: getTimeAccessInfo() public
    6: withdrawAll()
    q: quit from program
    Enter action:      
""",end="")
        try:
            choose = input().strip().rstrip()
            if choose == "1":
                _coins = int(input("enter uint256 _coins:").strip().rstrip())
                tx = c.functions.depositStaking(_coins).buildTransaction({
                    "from":sender,
                    "nonce":w3.eth.get_transaction_count(sender),
                    "gasPrice": w3.eth.gas_price,
                    "gas": 150000,
                })
                tx_sign = w3.eth.account.sign_transaction(tx, priv_key)
                tx_hash = w3.eth.send_raw_transaction(tx_sign.rawTransaction)
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                Deposit = c.events.Deposit()
                Deposit = Deposit.processReceipt(tx_receipt)
                sender = Deposit[0]['args']["sender"]
                coins = Deposit[0]['args']["coins"]
                print("sender: %s, coins: %d" % (sender,coins))
                print("[+] tx hash",tx_receipt['transactionHash'].hex())

            elif choose == "2":
                owner = input("address owner:").rstrip().strip()
                tx = c.functions.getStakeInfo(owner).buildTransaction({
                    "from":sender,
                    "nonce":w3.eth.get_transaction_count(sender),
                    "gasPrice": w3.eth.gas_price,
                    "gas": 150000,
                })
                tx_sign = w3.eth.account.sign_transaction(tx, priv_key)
                tx_hash = w3.eth.send_raw_transaction(tx_sign.rawTransaction)
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                StakeInfo = c.events.StakeInfo()
                StakeInfo = StakeInfo.processReceipt(tx_receipt)
                s = StakeInfo[0]['args']["stake"]
                r = StakeInfo[0]['args']["rewards"]
                print("stake: %s, rewards: %s" % (s,r))
                print("[+] tx hash",tx_receipt['transactionHash'].hex())

            elif choose == "3":
                _amount = int(input("enter uint256 _amount:").strip().rstrip())
                tx = c.functions.withdrawRewards(_amount).buildTransaction({
                    "from":sender,
                    "nonce":w3.eth.get_transaction_count(sender),
                    "gasPrice": w3.eth.gas_price,
                    "gas": 150000,
                })
                tx_sign = w3.eth.account.sign_transaction(tx, priv_key)
                tx_hash = w3.eth.send_raw_transaction(tx_sign.rawTransaction)
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                Withdraw = c.events.Withdraw()
                Withdraw = Withdraw.processReceipt(tx_receipt)
                sender = Withdraw[0]['args']["sender"]
                amount = Withdraw[0]['args']["amount"]
                print("sender: %s, amount: %d" % (sender,amount))
                print("[+] tx hash",tx_receipt['transactionHash'].hex())
            elif choose == "4":
                owner = input("address owner:").strip().rstrip()
                balance = c.functions.balanceOf(w3.toChecksumAddress(owner)).call()
                print("balance:",balance)
            elif choose == "5":
                tx = c.functions.getTimeAccessInfo().buildTransaction({
                    "from":sender,
                    "nonce":w3.eth.get_transaction_count(sender),
                    "gasPrice": w3.eth.gas_price,
                    "gas": 150000,
                })
                tx_sign = w3.eth.account.sign_transaction(tx, priv_key)
                tx_hash = w3.eth.send_raw_transaction(tx_sign.rawTransaction)
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                TimeInfo = c.events.TimeInfo()
                TimeInfo = TimeInfo.processReceipt(tx_receipt)
                access = TimeInfo[0]['args']["access"]
                withdraw = TimeInfo[0]['args']["withdraw"]
                print("[+] tx hash",tx_receipt['transactionHash'].hex())
                print("access: %d seconds, withdraw: %d seconds" % (access,withdraw))
            elif choose == "6":
                tx = c.functions.withdrawAll().buildTransaction({
                    "from":sender,
                    "nonce":w3.eth.get_transaction_count(sender),
                    "gasPrice": w3.eth.gas_price,
                    "gas": 150000,
                })
                tx_sign = w3.eth.account.sign_transaction(tx, priv_key)
                tx_hash = w3.eth.send_raw_transaction(tx_sign.rawTransaction)
                tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
                WithdrawAll = c.events.WithdrawAll()
                WithdrawAll = WithdrawAll.processReceipt(tx_receipt)
                sender = WithdrawAll[0]['args']["sender"]
                totalcoins = WithdrawAll[0]['args']["totalCoins"]
                print("[+] tx hash",tx_receipt['transactionHash'].hex())
                print("sender: %s, totalcoins: %d" % (sender,totalcoins))
            elif choose == "q":
                exit(0)
            else:
                print("invalid input")
                continue
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = 'front for StakingCoin')
    parser.add_argument('contract_address', type=str,
                    help='contract address StakingCoin')
    parser.add_argument('priv_key', type=str,
                    help='priv key user, in this case it is owner priv key')
    args = parser.parse_args()
    front(args.priv_key,args.contract_address)