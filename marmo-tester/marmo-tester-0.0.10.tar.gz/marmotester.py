from curses import wrapper, curs_set

from marmopy import Wallet, DefaultConf, Intent, Contract, from_bytes, to_bytes, Provider
import csv

import os, time,sys, csv

# Looks
space_top = 11
margin_left = 1

# Test settings
node = "https://ropsten.node.rcn.loans:8545/"
timeout = 640

if len(sys.argv) <= 1:
    print("Marmo relayer not provided")
    exit()

relayer = sys.argv[1]

if relayer.replace('-', '').lower() == "help":
    print("INPUTS: [RELAYER] [ETH_NODE (Optional)] [TIMEOUT (Optional)]")
    exit()

if len(sys.argv) == 3:
    node = sys.argv[2]

if len(sys.argv) == 4:
    timeout = int(sys.argv[3])

# Test dest
minter_contract = "0x2cf163d65eac738debdb0a78bb997268f7982feb"
mint_to = "0x06779a9848e5Df60ce0F5f63F88c5310C4c7289C"

# Abi
abi = '''
[
	{
		"constant": false,
		"inputs": [
			{
				"name": "_to",
				"type": "address"
			}
		],
		"name": "mint",
		"outputs": [
			{
				"name": "value",
				"type": "uint256"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"name": "_token",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"payable": true,
		"stateMutability": "payable",
		"type": "fallback"
	},
	{
		"constant": true,
		"inputs": [],
		"name": "token",
		"outputs": [
			{
				"name": "",
				"type": "address"
			}
		],
		"payable": false,
		"stateMutability": "view",
		"type": "function"
	}
]
'''

Minter = Contract(abi)
minter = Minter(minter_contract)

# based on https://stackoverflow.com/a/2785908/1056345                                                                                                                                                                                                                                                                         
def wait_until(somepredicate, timeout, period=1, times=1, pingback = lambda *args: None, *args, **kwargs):
    must_end = time.time() + timeout
    while time.time() < must_end:
        try:
            if somepredicate(*args, **kwargs):
                return True
        except:
            pass

        for i in range(0, times):
            time.sleep(period / times)
            pingback()

    return False

def norm_string(s, size):
    if len(s) > size:
        return s

    return (size - len(s)) * " " + s

def run(stdscr):
    import os
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # State
    total_tested = 0
    total_error = 0
    total_error_post = 0
    total_error_confirm = 0
    total_intent_time = 0

    all_intents = dict()

    # Setup marmo
    DefaultConf.ROPSTEN.as_default()
    Provider(node, relayer).as_default()

    # Clear screen
    stdscr.clear()
    curs_set(0)

    wallet = Wallet(from_bytes(os.urandom(32)))

    intent_action = minter.mint(mint_to)

    with open('logs/{}.csv'.format(wallet.address), mode='a') as log:
        log = csv.writer(log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        log.writerow([relayer, node, timeout, wallet.signer, wallet.address])
        log.writerow([' '])

    def render_intents():
        line = 0
        # `[`ˆstdscr.chgat(space_top, 0)
        # stdscr.clrtobot()
        for i in range(total_tested, -1, -1):
            try:
                intent = all_intents[i]
                if intent.has_key('tx'):
                    stdscr.addstr(
                        line + space_top,
                        margin_left,
                        '{} Timestamp: {} ID: {} TX: {} Delta: {}ms Posted: {} Completed: {}'.format(
                            norm_string(str(i), 6),
                            int(intent['time']),
                            intent['id'],
                            intent['tx'],
                            norm_string(str(int((intent['ended'] - intent['started']) * 1000)), 9),
                            intent['posted'],
                            intent['completed']
                        )
                    )
                else:
                    stdscr.addstr(
                        line + space_top,
                        margin_left,
                        '{} Timestamp: {} ID: {} Delta: {}ms'.format(
                            norm_string(str(i), 6),
                            int(intent['time']),
                            intent['id'],
                            int((time.time() - intent['started']) * 1000),
                        )
                    )

                line = line + 1
            except:
                pass

        stdscr.refresh()

    while True:
        # Print
        stdscr.addstr(1, margin_left, 'Welcome to Marmo testing-land!')
        stdscr.addstr(3, margin_left, 'Testing relayer {}'.format(relayer))
        stdscr.addstr(4, margin_left, 'Marmo wallet {}'.format(wallet.address))
        stdscr.addstr(6, margin_left, 'Current run:')
        stdscr.addstr(7, margin_left + 1, 'Total tested {}'.format(total_tested))
        stdscr.addstr(8, margin_left + 1, 'Intent success {}'.format(total_tested - total_error))
        stdscr.addstr(9, margin_left + 1, 'Intent error {} (P: {} C: {})'.format(total_error, total_error_post, total_error_confirm))

        if total_tested - total_error != 0:
            avg_time = total_intent_time * 1000 / float(total_tested - total_error)
        else:
            avg_time = '--'

        stdscr.addstr(10, margin_left + 1, 'Average Intent time {}ms'.format(avg_time))

        stdscr.refresh()

        intent_internal_id = total_tested

        intent = Intent(
            intent_action=intent_action,
            salt=hex(intent_internal_id),
            expiration=32382750600
        )

        signed_intent = wallet.sign(intent)
        started_time = time.time()

        all_intents[intent_internal_id] = {
            'time': time.time(),
            'id': signed_intent.id,
            'started': started_time,
        }

        response = signed_intent.relay()
        posted = response.status_code == 200 or response.status_code == 201

        if posted:
            completed = wait_until(lambda: signed_intent.status()["code"] == "completed", timeout, pingback=lambda: render_intents(), times=10)
        else:
            completed = False

        total_tested = total_tested + 1

        ended = time.time()
        duration = ended - started_time

        if completed and posted:
            total_intent_time = total_intent_time + duration

            try:
                tx = signed_intent.status()["receipt"]["tx_hash"]
            except:
                tx = "Error retrieving tx hash"

        else:
            total_error = total_error + 1
            tx = '--'
            if not posted:
                total_error_post = total_error_post + 1
            elif not completed:
                total_error_confirm = total_error_confirm + 1

        all_intents[intent_internal_id] = {
            'time': all_intents[intent_internal_id]['time'],
            'id': signed_intent.id,
            'tx': tx,
            'started': started_time,
            'ended': ended,
            'posted': posted,
            'completed': completed
        }

        render_intents()

        # Dump to CSV
        with open('logs/{}.csv'.format(wallet.address), mode='a') as log:
            log = csv.writer(log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            log.writerow([
                all_intents[intent_internal_id]['time'],
                signed_intent.id,
                tx,
                started_time,
                ended,
                posted,
                completed
            ])

        stdscr.refresh()


def main():
    wrapper(run)

if __name__ == '__main__':
    main()
