# ms-test-optimizer
Morgan Stanley Delta One Team - Coding Test

### Coding Test

Requirements: Finish independently, internet/google/stackoverflow etc. available. No cooperation, no
copy & paste.

#### Project:
Use python to write an optimizer.

#### Requirements:
1. Suppose we initially have a basket of $10 million CSI300 underlying stocks, with equal weights.
2. Use Markowitz optimization to build a portfolio, maximize future return and minimize risk.
3. For risk calculation, you can either use Barra Data (if you have), or past 5 years daily data to
calculate Cov matrix.
4. Each component weight should deviate from CSI300 weight less than 3%.
5. Turnover rate should be less than 15%.
6. For alpha, you can generate random number, alpha itself is not important.

#### Result:
1. Please make sure your script can run without error.
2. Please hand in the full code as well as outputs.
3. Please save Input/Output as csv, and code as txt file.


### Solution 

#### Input data
All data was cached from Bloomberg terminal
1. `input/SHSZ300 Index.csv`: CSI 300 index member weights history
2. `input/SHSZ300 Index last_price.csv`: CSI 300 index daily close levels history
3. `input/SHSZ300 Index member_last_price.csv`: CSI 300 index members close price history

#### Optimizer
1. `optimizer/blp.py`: bloomberg pipeline, contains APIs to download and retrieve input data
2. `optimizer/alpha.py`: fake alpha, using daily returns to generate momentum factor
3. `optimizer/risk.py`: 5 years daily return to calculate covariance matrix and construct risk model
4. `optimizer/opt.py`: index-tracking markowitz optimization policy, maximize expected returns and minimize risk, with deviation limit

#### Output data
1. `output/port_holdings.csv`: portfolio daily holdings history
2. `output/port_returns.html`: portfolio daily returns chart
3. `output/port_value.html`: portfolio value chart
4. `output/example.html`: jupyter notebook export form example.ipynb

#### Examples
1. `sim_example.py`: simulation example with designated output generation
2. `example.ipynb`: simulation example with performance analytics

#### Dependency
1. `xbbg`: Bloomberg API to download history of index members, index levels and components prices
2. `cvxportfolio` \& `cvxpy`: open source Python-embedded modeling language for convex optimization problems. It lets 
me express problem in a natural way that follows the math required by solvers. 

#### Requirements explanation:
1. Initial basket of $10 million CSI300 underlying stocks, with equal weights: implemented in `init_port` in examples
2. Markowitz optimization: implemented in `opt.py`
3. Risk calculation: used past 5 years daily data to calculate Cov matrix, implemented in `risk.py`
4. Each component weight should deviate from CSI300 weight less than 3%: implemented argument `tracking_error` in `opt.py`
5. Turnover rate should be less than 15%: two solutions -
   1. preferably, controlled via transaction cost model (implemented as `tcost_model` in examples)
   2. optionally, can enable `turnover_limit` in `opt.py`, but this is a hard constraint to restrict daily turnover < 15% 
6. For alpha, you can generate random number: implemented momentum in `alpha.py`