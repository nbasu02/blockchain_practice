## Credits

This project was created from this tutorial: https://hackernoon.com/learn-blockchains-by-building-one-117428612f46

## Running

After installing requirements, run `python app.py` to run application.

### Creating a transaction

Send a post request to `localhost:5000/transactions/new` with the parameters `sender`, `recipient`, and `amount` as json

### Mining a block

On your browser, go to `localhost:5000/mine` to hash all transactions into a new block, and add it to the blockchain

### Viewing the full chain

Send a GET request to `localhost:5000/chain`
