import calendar
import datetime
import hashlib
import json

class Blockchain(list):
    def __init__(self):
        self.transactions = []
        self.add_block(proof=100, previous_hash='abc123')

    def add_block(self, proof, previous_hash=None):
        previous_hash = previous_hash or Block.hash(self.last_block)

        block = Block(
            index=len(self),
            proof=proof,
            transactions=self.transactions,
            previous_hash=previous_hash
            )
        self.append(block)
        self.transactions = []
        return block

    def add_transaction(self, sender, recipient, amount):
        transaction = Transaction(sender, recipient, amount)
        self.transactions.append(transaction)
        return self.last_block['index'] + 1 # or len(self)?

    @property
    def last_block(self):
        if self:
            return self[-1]

    def proof_of_work(self):
        last_proof = self.last_block['proof']

        proof = 0
        while not Blockchain.valid_proof(last_proof, proof):
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Shamelessly pulled from the tutorial

        Validates the Proof: Does hash(last_proof, proof) contain 4 leading zeroes?
        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = str(last_proof + proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

class Block(dict):
    def __init__(self, index, transactions, proof, previous_hash):
        default_block = {
            'index': index, # in the tutorial, but necessary?
            'timestamp': calendar.timegm(datetime.datetime.utcnow().timetuple()),
            'transactions': transactions,
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.update(default_block)

    def add_transaction(self, transaction):
        if not isinstance(transaction, Transaction):
            raise TypeError('Requires a Transaction item')
        self['transactions'].append(transaction)

    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        :param block: <dict> Block
        :return: <str>
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Transaction(dict):
    def __init__(self, sender, recipient, amount):
        self['sender'] = sender
        self['recipient'] = recipient
        self['amount'] = amount
