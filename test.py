# main.py
from app.blockchain import Blockchain

def main():
    # Blockchain 생성자를 이용해 인스턴스를 생성하고, 필요한 인자를 전달합니다.
    bitcoin = Blockchain()

    # previous_block_hash = '519619156945694516'
    # current_block_data = [
    #     {
    #         'amount' : 10,
    #         'sender' : 'BAD48461AB6',
    #         'recipient' : 'ag4a6e4g9a4w5eg',
    #     },
    #     {
    #         'amount' : 30,
    #         "sender" : '15DSGA86G4AD46GAE',
    #         'recipient' : 'aega6we16ga1we65g1',
    #     },
    #     {
    #         'amount' : 100,
    #         "sender" : 'GAWEKGAWE66GA16W1E1661',
    #         'recipient' : 'a6w191a9be156b1a',
    #     },
    # ]
    # nonce = 100


    bc1 = {
    "chain": [
        {
        "index": 1,
        "timestamp": 1676535694659,
        "transactions": [],
        "nonce": 100,
        "hash": "0",
        "previousBlockHash": "0"
        },
        {
        "index": 2,
        "timestamp": 1676535705092,
        "transactions": [],
        "nonce": 18140,
        "hash": "0000b9135b054d1131392c9eb9d03b0111d4b516824a03c35639e12858912100",
        "previousBlockHash": "0"
        },
        {
        "index": 3,
        "timestamp": 1676535707065,
        "transactions": [
        {
        "sender": "00",
        "recipient": "ecd6c930add211eda7661d62fcb9f370",
        "transactionId": "f311c980add211eda7661d62fcb9f370"
        }
        ],
        "nonce": 5769,
        "hash": "00008381711a3d940cc5f6958796897d47a66c738f8eb1cda0ccd2d93df83b12",
        "previousBlockHash": "0000b9135b054d1131392c9eb9d03b0111d4b516824a03c35639e12858912100"
        },
        {
        "index": 4,
        "timestamp": 1676535708949,
        "transactions": [
        {
        "sender": "00",
        "recipient": "ecd6c930add211eda7661d62fcb9f370",
        "transactionId": "f43c3fc0add211eda7661d62fcb9f370"
        }
        ],
        "nonce": 5568,
        "hash": "0000a601a901cf2a8a5211c8e894b7cf52f2b3a22c0fdad58a68af8afac62764",
        "previousBlockHash": "00008381711a3d940cc5f6958796897d47a66c738f8eb1cda0ccd2d93df83b12"
        },
        {
        "index": 5,
        "timestamp": 1676535714075,
        "transactions": [
        {
        "sender": "00",
        "recipient": "ecd6c930add211eda7661d62fcb9f370",
        "transactionId": "f55bb980add211eda7661d62fcb9f370"
        }
        ],
        "nonce": 39289,
        "hash": "00006af5624886764b9cec3554fd40f7b882a76c3540a5ad5f901273b210f250",
        "previousBlockHash": "0000a601a901cf2a8a5211c8e894b7cf52f2b3a22c0fdad58a68af8afac62764"
        }
        ],
        "pendingTransactions": [
        {
        "sender": "00",
        "recipient": "ecd6c930add211eda7661d62fcb9f370",
        "transactionId": "f86a3200add211eda7661d62fcb9f370"
        }
        ],
        "currentUrl": "http://localhost:5001",
        "networkNodes": []
}

    

    print('VALID:', bitcoin.chain_is_valid(bc1['chain']))
    #print(bitcoin.hash_block(previous_block_hash,current_block_data,900))

if __name__ == "__main__":
    main()
