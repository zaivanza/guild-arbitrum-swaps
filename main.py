from web3 import Web3
import requests
from termcolor import cprint
import time
import json

RPC = {
        # '1': '',
        # '3': '',
        '10': 'https://mainnet.optimism.io',
        '56': 'https://bsc-dataseed.binance.org',
        '137': 'https://polygon-rpc.com',
        '42161': 'https://arb1.arbitrum.io/rpc', 
        # '43114': '',  # https://support.avax.network/en/articles/4626956-how-do-i-set-up-metamask-on-avalanche
    }

def check_status_transaction(tx, API_KEY):
    result = []
    link = f'https://api.arbiscan.io/api?module=transaction&action=gettxreceiptstatus&txhash={tx}&apikey={API_KEY}'
    response = requests.get(url=link)
    result.append(response.json())

    status = result[0]['result']['status']
    return status

tx_list = []

def inch_myc(privatekey, amount_to_swap, to_token_address, to_symbol):
    try:
        
        def intToDecimal(qty, decimal):
            return int(qty * int("".join(["1"] + ["0"]*decimal)))
        def decimalToInt(price, decimal):
            return price/ int("".join((["1"]+ ["0"]*decimal)))
        def get_api_call_data(url):
            try: 
                call_data = requests.get(url)
            except Exception as e:
                print(e)
                return get_api_call_data(url)
            try:
                api_data = call_data.json()
                return api_data
            except Exception as e: 
                print(call_data.text) 

        ChainUrl = "https://arb1.arbitrum.io/rpc"
        web3 = Web3(Web3.HTTPProvider(ChainUrl))
        account = web3.eth.account.privateKeyToAccount(privatekey)
        address_wallet = account.address

        fromTokenAddress = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE" # ETH
        withdrawAccount = address_wallet
        destReceiver = address_wallet
        slippage = 3
        gasLimit = 1000000
        amount = intToDecimal(amount_to_swap, 18) 
        gasPrice = intToDecimal(0.0000000001, 18)

        _1inchurl = f'https://api.1inch.exchange/v4.0/42161/swap?fromTokenAddress={fromTokenAddress}&toTokenAddress={to_token_address}&amount={amount}&fromAddress={withdrawAccount}&destReceiver={destReceiver}&slippage={slippage}&gasPrice={gasPrice}&gasLimit={gasLimit}'
        json_data = get_api_call_data(_1inchurl)

        nonce = web3.eth.getTransactionCount(withdrawAccount)
        tx = json_data['tx']
        tx['nonce'] = nonce
        tx['to'] = Web3.toChecksumAddress(tx['to'])
        tx['gasPrice'] = int(tx['gasPrice'])
        tx['value'] = int(tx['value'])
        signed_tx = web3.eth.account.signTransaction(tx, privatekey)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)

        token = {
            'address': to_token_address,
            'symbol': to_symbol,
            'amount': amount_to_swap,
            'tx_hash': web3.toHex(tx_hash)
        }

        tx_list.append(token)

        cprint(f'\n>>> swap {to_symbol} : https://arbiscan.io/tx/{web3.toHex(tx_hash)}', 'green')
    except Exception as error:
        cprint(f'\n>>> {address_wallet} | {to_symbol} | {error}', 'red')

def web_sushi_guild(privatekey, amount, to_token_address, to_symbol):
    try:

        RPC = "https://arb1.arbitrum.io/rpc"
        web3 = Web3(Web3.HTTPProvider(RPC))
        account = web3.eth.account.privateKeyToAccount(privatekey)
        address_wallet = account.address
        contractToken = Web3.toChecksumAddress('0x1b02da8cb0d097eb8d57a175b88c7d8b47997506')
        ABI = '[{"inputs":[{"internalType":"address","name":"_factory","type":"address"},{"internalType":"address","name":"_WETH","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"WETH","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"amountADesired","type":"uint256"},{"internalType":"uint256","name":"amountBDesired","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"amountTokenDesired","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"addLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"},{"internalType":"uint256","name":"liquidity","type":"uint256"}],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"factory","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountIn","outputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"reserveIn","type":"uint256"},{"internalType":"uint256","name":"reserveOut","type":"uint256"}],"name":"getAmountOut","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsIn","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"}],"name":"getAmountsOut","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"reserveA","type":"uint256"},{"internalType":"uint256","name":"reserveB","type":"uint256"}],"name":"quote","outputs":[{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidity","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETH","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"removeLiquidityETHSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermit","outputs":[{"internalType":"uint256","name":"amountToken","type":"uint256"},{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"token","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountTokenMin","type":"uint256"},{"internalType":"uint256","name":"amountETHMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityETHWithPermitSupportingFeeOnTransferTokens","outputs":[{"internalType":"uint256","name":"amountETH","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"tokenA","type":"address"},{"internalType":"address","name":"tokenB","type":"address"},{"internalType":"uint256","name":"liquidity","type":"uint256"},{"internalType":"uint256","name":"amountAMin","type":"uint256"},{"internalType":"uint256","name":"amountBMin","type":"uint256"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"bool","name":"approveMax","type":"bool"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"removeLiquidityWithPermit","outputs":[{"internalType":"uint256","name":"amountA","type":"uint256"},{"internalType":"uint256","name":"amountB","type":"uint256"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapETHForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactETHForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForETHSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokensSupportingFeeOnTransferTokens","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactETH","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"},{"internalType":"uint256","name":"amountInMax","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapTokensForExactTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]'
        contract = web3.eth.contract(address=contractToken, abi=ABI)
        spend = Web3.toChecksumAddress('0x82aF49447D8a07e3bd95BD0d56f35241523fBab1') # WETH

        def intToDecimal(qty, decimal):
            return int(qty * int("".join(["1"] + ["0"]*decimal)))

        gasLimit = 4000000
        gasPrice = intToDecimal(0.0000000001, 18)
        nonce = web3.eth.get_transaction_count(address_wallet)

        contract_txn = contract.functions.swapExactETHForTokens(
        0, # amountOutMin
        [spend, to_token_address], 
        address_wallet, # receiver
        (int(time.time()) + 10000) # deadline
        ).buildTransaction({
        'from': address_wallet,
        'value': web3.toWei(amount,'ether'), 
        'gas': gasLimit,
        'gasPrice': gasPrice,
        'nonce': nonce,
        })
            
        signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=privatekey)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        token = {
            'address': to_token_address,
            'symbol': to_symbol,
            'amount': amount_to_swap,
            'tx_hash': web3.toHex(tx_hash)
        }

        tx_list.append(token)

        cprint(f'\n>>> swap {to_symbol} : https://arbiscan.io/tx/{web3.toHex(tx_hash)}', 'green')
    except Exception as error:
        cprint(f'\n>>> {to_symbol} | {error}', 'red')


swaps = [
    {'address': '0xf97f4df75117a78c1A5a0DBb814Af92458539FB4',
    'symbol': 'LINK',
    'amount': 0.00001},

    {'address': '0x539bdE0d7Dbd336b79148AA742883198BBF60342',
    'symbol': 'MAGIC',
    'amount': 0.00001},

    {'address': '0xfc5A1A6EB076a2C7aD06eD22C90d7E710E35ad0a',
    'symbol': 'GMX',
    'amount': 0.00004},

    {'address': '0x6C2C06790b3E3E3c38e12Ee22F8183b37a13EE55',
    'symbol': 'DPX',
    'amount': 0.00003},

    {'address': '0x289ba1701C2F088cf0faf8B3705246331cB8A839',
    'symbol': 'LPT',
    'amount': 0.00001},

    {'address': '0x1622bF67e6e5747b81866fE0b85178a93C7F86e3',
    'symbol': 'UMAMI',
    'amount': 0.00002},

    {'address': '0x10393c20975cF177a3513071bC110f7962CD67da',
    'symbol': 'JONES',
    'amount': 0.00001},

    {'address': '0x5575552988A3A80504bBaeB1311674fCFd40aD4B',
    'symbol': 'SPA',
    'amount': 0.00001},

    {'address': '0x51318B7D00db7ACc4026C88c3952B66278B6A67F',
    'symbol': 'PLS',
    'amount': 0.00001},

    {'address': '0xa684cd057951541187f288294a1e1C2646aA2d24',
    'symbol': 'VSTA',
    'amount': 0.00001},

    {'address': '0x080F6AEd32Fc474DD5717105Dba5ea57268F46eb',
    'symbol': 'SYN',
    'amount': 0.00001},

    {'address': '0xd3f1Da62CAFB7E7BC6531FF1ceF6F414291F03D3',
    'symbol': 'DBL',
    'amount': 0.00001},

    {'address': '0xeEeEEb57642040bE42185f49C52F7E9B38f8eeeE',
    'symbol': 'ELK',
    'amount': 0.00001},
]


if __name__ == "__main__":
        
    cprint(f'\n============================================= hodlmod.eth =============================================', 'cyan')
    
    with open("private_keys.txt", "r") as f:
        keys_list = [row.strip() for row in f]

    for privatekey in keys_list:
        tx_list.clear()
        
        cprint(f'\n=============== start : {privatekey} ===============', 'white')

        fees = []
        for swap in swaps:
            amount_to_swap = swap['amount']
            to_token_address = swap['address']
            to_symbol = swap['symbol']
            fees.append(amount_to_swap)
            web_sushi_guild(privatekey, amount_to_swap, to_token_address, to_symbol)
            time.sleep(3)

        inch_myc(privatekey, 0.00001, '0xC74fE4c715510Ec2F8C61d70D397B32043F55Abe', 'MYC')

        with open("test.json", "w") as file:
            json.dump(tx_list, file, indent=4, ensure_ascii=False)

        for tx in tx_list:
            API_KEY = 'your_api_key'
            status = check_status_transaction(tx['tx_hash'], API_KEY)

            to_symbol = tx['symbol']
            to_token_address = tx['address']
            amount_to_swap = tx['amount']

            if status == '0':
                cprint(f"\nfail : {to_symbol} | {to_token_address} | {amount_to_swap}", 'red')
                if to_symbol == 'MYC':
                    inch_myc(privatekey, amount_to_swap, to_token_address, to_symbol)
                else:
                    web_sushi_guild(privatekey, amount_to_swap, to_token_address, to_symbol)

