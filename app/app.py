from flask import Flask, request, jsonify, render_template, send_from_directory

from blockchain import Blockchain
from uuid import uuid4
import requests
import sys

app = Flask(__name__)
bitcoin = Blockchain()

node_address = str(uuid4()).replace('-', '')


@app.route('/blockchain', methods=['GET']) #전체 블록을 보여줌
def get_blockchain():
    return jsonify(bitcoin.__dict__)


@app.route('/transaction', methods=['POST']) # pending_transactions에 transaction 추가
def create_transaction():
    new_transaction = request.get_json()
    block_index = bitcoin.add_transaction_to_pending_transactions(new_transaction)
    return jsonify({'note': f'Transaction will be added in block {block_index}.'})




@app.route('/mine', methods=['GET']) # 작업증명
def mine():
    last_block = bitcoin.get_last_block()
    previous_block_hash = last_block['hash']
    current_block_data = {
        'transactions': bitcoin.pending_transactions,
        'index': last_block['index'] + 1
    }
    bitcoin.create_new_transaction(12.5, "00", node_address)
    nonce = bitcoin.proof_of_work(previous_block_hash, current_block_data)
    block_hash = bitcoin.hash_block(previous_block_hash, current_block_data, nonce)
    new_block = bitcoin.create_new_block(nonce, previous_block_hash, block_hash)

    request_promises = []

    for network_node_url in bitcoin.network_nodes:
        request_options = {
            'newBlock': new_block
        }
        res = requests.post(network_node_url + '/receive-new-block', json=request_options)
        request_promises.append(res)

    responses = [rp.json() for rp in request_promises]

    request_options = {
        'amount': 12.5,
        'sender': "00",
        'recipient': node_address
    }
    requests.post(bitcoin.current_node_url + '/transaction/broadcast', json=request_options)

    return jsonify({
        'note': "New block mined successfully",
        'block': new_block
    })

@app.route('/register-and-broadcast-node', methods=['POST'])
def register_and_broadcast_node():
    new_node_url = request.json['newNodeUrl']
    if new_node_url not in bitcoin.network_nodes:
        bitcoin.network_nodes.append(new_node_url)

    reg_nodes_promises = []
    for network_node_url in bitcoin.network_nodes:
        response = requests.post(f"{network_node_url}/register-node", json={'newNodeUrl': new_node_url}) # 새로운 노드를 연결하는 요청 받은 노드가 원래 연결되어 있던 노드에게 새로운 노드를 등록하는 요청 보내는 API 호출 
        reg_nodes_promises.append(response)

    for response in reg_nodes_promises:
        if response.status_code == 200:
            requests.post(f"{new_node_url}/register-nodes-bulk", json={'allNetworkNodes': bitcoin.network_nodes + [bitcoin.current_node_url]}) # 새로운 노드를 추가한 뒤 전체 노드 정보를 새로 연결되는 노드에게 주는 API 호출

    return jsonify({'note': 'New node registered with network successfully.'})


@app.route('/register-node', methods=['POST']) # 새로운 노드를 연결하는 요청 받은 노드가 원래 연결되어 있던 노드에게 새로운 노드를 등록하는 요청 보내는 API
def register_node():
    new_node_url = request.json['newNodeUrl']
    node_not_already_present = new_node_url not in bitcoin.network_nodes
    not_current_node = bitcoin.current_node_url != new_node_url
    #node_not_already_present = #채우시오 : new_node_url이 network_noeds에 없으면 true (type boolean)
    #not_current_node = #채우시오 : current_node_url이 new_node_url이 아니면 true(type boolean)
    if node_not_already_present and not_current_node:#두 가지 조건을 모두 만족하면 실행
        #새로운 노드 network_node에 추가
        bitcoin.network_nodes.append(new_node_url)
    return jsonify({'note': 'New node registered successfully.'})


@app.route('/register-nodes-bulk', methods=['POST']) # 새로운 노드를 추가한 뒤 전체 노드 정보를 새로 연결되는 노드에게 주는 API
def register_nodes_bulk():
    all_network_nodes = request.json['allNetworkNodes']
    for network_node_url in all_network_nodes:
        node_not_already_present = network_node_url not in bitcoin.network_nodes
        not_current_node = bitcoin.current_node_url != network_node_url
        #node_not_already_present = #채우시오 : new_node_url이 network_noeds에 없으면 true (type boolean)
        #not_current_node = #채우시오 : current_node_url이 new_node_url이 아니면 true(type boolean)
        if node_not_already_present and not_current_node: #두 가지 조건을 모두 만족하면 실행
            #새로운 노드 network_node에 추가
            bitcoin.network_nodes.append(network_node_url)

    return jsonify({'note': 'Bulk registration successful.'}) 

@app.route('/transaction/broadcast', methods=['POST'])
def broadcast_transaction():
    new_transaction = bitcoin.create_new_transaction(
        request.json['amount'],
        request.json['sender'],
        request.json['recipient']
    )
    bitcoin.add_transaction_to_pending_transactions(new_transaction)

    request_promises = []
    for network_node_url in bitcoin.network_nodes:
        request_options = {
            'url': network_node_url + '/transaction',
            'json': new_transaction
        }
        request_promises.append(requests.post(**request_options))

    for response in request_promises:
        response.raise_for_status()

    return jsonify({'note': 'Transaction created and broadcast successfully.'})

@app.route('/receive-new-block', methods=['POST'])
def receive_new_block():
    new_block = request.json['newBlock']
    last_block = bitcoin.get_last_block()
    correct_hash = last_block['hash'] == new_block['previous_block_hash']
    correct_index = last_block['index'] + 1 == new_block['index']

    if correct_hash and correct_index:
        bitcoin.chain.append(new_block)
        bitcoin.pending_transactions = []
        return jsonify({
            'note': 'New block received and accepted',
            'newBlock': new_block
        })
    else:
        return jsonify({
            'note': 'New block rejected.',
            'newBlock': new_block
        })


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000  # 기본 포트 번호를 설정하십시오.
    
    if len(sys.argv) > 2:
        current_node_url = sys.argv[2]
    else:
        current_node_url = f"http://3.82.25.140:{port}"
    
    bitcoin = Blockchain(current_node_url)  # 현재 노드 URL 전달
    app.run(host="0.0.0.0", port=port)