% COMP9334 
% Week 4, Database server example
% After working out the balance equation, we need to solve
% the set of linear equations
% 
% I have chosen to use the first 5 equations on page 28 together
% with sum( probabilities ) = 1 
% 
% In principle, you can choose any of the 5 equations together
% with sum( probabilities ) = 1 
%
% We put the linear equations in standard form A x = b
% where x is the unknown vector  
% 
A = [ 5 0 -2.5 0 0 0 0 0 0 0 0 0 
      0 7.5 -2.5 0 -2.5 0 0 0 0 0 0 0
      -5 -2.5 10 0 0 -2.5 0 0 0 0 0 0 
      0 0 0 7.5 -2.5 0 -5 0 0 0 0 0 
      0 -5 0 -2.5 12.5 -2.5 0 -2.5 0 0 0 0 
      0 0 -5 0 -2.5 10 0 0 -2.5 0 0 0 
      0 0 0 -5 0 0 12.5 -2.5 0 -5 0 0 
      0 0 0 0 -5 0 -2.5 12.5 -2.5 0 -2.5 0 
      0 0 0 0 0 -5 0 -2.5 10 0 0 -2.5 
      0 0 0 0 0 0 -5 0 0 7.5 -2.5 0 
      0 0 0 0 0 0 0 -5 0 -2.5 7.5 -2.5
      1 1 1 1 1 1 1 1 1 1 1 1];
b = [0 0 0 0 0 0 0 0 0 0 0 1]';
x = A\b