from app import app
from two1.commands import buy
from two1.commands.config import Config
from two1 import TWO1_WWW_HOST
from two1.bitrequests import BitTransferRequests
from two1.bitrequests import OnChainRequests
import two1.commands.util.uxstring as uxstring
import re

FEE_PER_KB = 10000  # Satoshis

# Each txn input is ~150 bytes:
# outpoint: 32 bytes
# outpoint index: 4 bytes
# signature: 77-78 bytes
# compressed public key: 33 bytes
# sequence num: 4 bytes
DEFAULT_INPUT_FEE = int(0.15 * FEE_PER_KB)

# Each txn output is ~40 bytes, thus 0.04
DEFAULT_OUTPUT_FEE = int(0.04 * FEE_PER_KB)

# Two UTXO with one Output
DEFAULT_ONCHAIN_BUY_FEE = (DEFAULT_INPUT_FEE * 2) + DEFAULT_OUTPUT_FEE

MARKETPLACE_API = app.config['MARKETPLACE_API']

conf = Config()

URL_REGEXP = re.compile(
    r'^(?:http)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

DEMOS = {
    "search": {"path": "/search/bing"}
}

class two1lib(object):

    @staticmethod
    def buy(config, resource, data, method, data_file, output_file,
         payment_method, max_price, info_only):
        """Buy from any machine payable endpoint

           Note: The two1lib _buy function does not support simply returning an object,
                 until then, include a local copy here
        """
        # If resource is a URL string, then bypass seller search
        if URL_REGEXP.match(resource):
            target_url = resource
            seller = target_url
        elif resource in DEMOS:
            target_url = TWO1_WWW_HOST + DEMOS[resource]["path"]
            data = json.dumps(data)
        else:
            raise NotImplementedError('Endpoint search is not implemented!')
        
        # Change default HTTP method from "GET" to "POST", if we have data
        if method == "GET" and (data or data_file):
            method = "POST"
        
        # Set default headers for making bitrequests with JSON-like data
        headers = {'Content-Type': 'application/json'}

        try:
        # Find the correct payment method
            if payment_method == 'offchain':
                bit_req = BitTransferRequests(config.machine_auth, config.username)
            elif payment_method == 'onchain':
                bit_req = OnChainRequests(config.wallet)
                    
            else:
                raise Exception('Payment method does not exist.')
                    
            # Make the request
            if info_only:
                res = bit_req.get_402_info(target_url)
            else:
                res = bit_req.request(
                    method.lower(), target_url, max_price=max_price,
                    data=data or data_file, headers=headers)
        except ResourcePriceGreaterThanMaxPriceError as e:
            config.log(uxstring.Error.resource_price_greater_than_max_price.format(e))
            return
        except Exception as e:
            if 'Insufficient funds.' in str(e):
                config.log(uxstring.Error.insufficient_funds_mine_more.format(
                    DEFAULT_ONCHAIN_BUY_FEE
                ))
            else:
                config.log(str(e), fg="red")
            return

        # Output results to user
        if output_file:
            # Write response output file
            output_file.write(res.content)
        elif info_only:
            # Print headers that are related to 402 payment required
            for key, val in res.items():
                config.log('{}: {}'.format(key, val))
        elif resource in DEMOS:
            config.log(DEMOS[resource]["formatter"](res))
        else:
            response = res.json()
            # Clean up names            
            for index, elem in enumerate(response):
                if elem['name'] is None:
                    response[index]['name'] = 'Please name me'
                elif len(elem['name']) == 0:
                    response[index]['name'] = 'Please name me'
                else:
                    response[index]['name'] = response[index]['name'].title()
                print(elem['description'])
                if elem['description'] is None:
                    try: 
                        response[index]['description'] = elem['owner'].title() + ' is a bad endpoint operator and forgot to place a description'
                    except:
                        response[index]['description'] = 'Anonymous is a bad endpoint operator and forgot to place a description'                        
                # Any description greater than 66 characters causes the text to overflow, this enforces a limit
                elif len(elem['description']) > 63:
                    response[index]['description'] = response[index]['description'][:63] + '...'
                    
            # Write response to console
            return response

        # Write the amount paid out if something was truly paid
        if not info_only and hasattr(res, 'amount_paid'):
            client = rest_client.TwentyOneRestClient(TWO1_HOST,
                                                     config.machine_auth,
                                                     config.username)
            user_balances = _get_balances(config, client)
            if payment_method == 'offchain':
                balance_amount = user_balances.twentyone
                balance_type = '21.co'
            elif payment_method == 'onchain':
                balance_amount = user_balances.onchain
                balance_type = 'blockchain'

        # Record the transaction if it was a payable request
        if hasattr(res, 'paid_amount'):
            config.log_purchase(s=seller,
                                r=resource,
                                p=res.paid_amount,
                                d=str(datetime.datetime.today()))
            
    @staticmethod
    def get_quote():
        """Get list of active endpoints on the 21 marketplace
    
       Github Repo: https://github.com/weex/up
       
       Parameters: None
       Returns: Array containing marketplace endpoint data

        """

        url = MARKETPLACE_API
        price = 1000

        try: 
          marketplaceInfo = two1lib.buy(conf, url, None, 'GET', None, None, 'offchain', price, False)
        except:
          return {}
        return marketplaceInfo


