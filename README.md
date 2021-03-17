# Team 21 - Backstreet Brogrammers

## Efficient Backtesting framework using python modules and AWS framework

* Custom bundle pricing data (minutely and daily) ingestion from AWS S3 using [feather file](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_feather.html) format which is able to handle big price data most [efficiently](https://towardsdatascience.com/the-best-format-to-save-pandas-data-414dca023e0d)
* By default - feather file read uses multiple threads to load the data into pandas dataframe in the most efficient way 
* Example strategies implemented - Simple Moving Averages, Contrarian, Bollinger Bands and daily portfolio rebalancing

### Setup
* Checkout the project (using git clone) to local
* Build the docker image : ./scripts/build_bolt.sh

### Run
* Execute : ./scripts/start_bolt.sh
* Copy the jupyter notebook token from : ./logs/backtest_bolt_<container_id>.log
* Launch browser and link: http://localhost:8802/tree
* Paste the token and launch jupyter
* All example strategies are given which can be opened and run
* Once done, can logout from jupyter notebook
* Stop the docker container : ./scripts/stop_bolt.sh

### Ingest the custom bundle
* Prepare the daily or minutely ticker OHCLV data file as a [binary feather file](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_feather.html) and store it in AWS S3 - it can hold big data
* Framework will automatically fetch the stock data from AWS S3 where it is stored as binary feather file format while running the backtesting strategies

