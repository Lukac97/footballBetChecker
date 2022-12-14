# FootballBetChecker
Tool used for checking result of football match betting tip/combination.
# How to use
Run football_bet_checker.py script with 2 arguments:
1. Link to footystats.com match screen (ex. https://footystats.org/international/serbia-national-team-vs-cameroon-national-team-h2h-stats#2315637)  
2. String containing betting combinations to be checked, separated by semicolons (ex. 1;g3+;x-1)  
  
In case arguments are not given to the script, the same information will be asked from user at the start of the script.
# Supported combinations
1, X, 2 - match outcome.  
P1, P2, PX, 2P1, 2P2, 2PX - halftime outcome.  
X-1, 1-2, NE 2-X, 1X-1, X2-X2 ... - halftime outcome and end outcome.  
1X, 2X, 12, P12, 2P1X, ... - double chance match outcome.  
g3+, g2-3, ... - total number of goals on match.  
Dg3+, G2-3, ... - host or guest total number of goals.  
P1g5+, P2Dg0-2, ... - First half/Second half total number of goals/host or guest total number of goals.  
GG, NG, GG1, GG2, NG1, NG2 - Goal-goal combinations.  

  
... as well as any variation of joined combinations (from the ones listed above) with | (or) and/or & (and).
