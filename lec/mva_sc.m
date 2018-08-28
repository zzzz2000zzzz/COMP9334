function [R,X,nbar,Rzero,Xzero,U] = mva_sc(S,V,N,Z)

% MVA for closed single-class queueing networks 
%
% Inputs: 
%   S = service time per visit
%   V = visit ratio 
%   N = Number of terminals or number of users  
%   Z = thinking time
% 
% Outputs:
%   R = response time per visit (K-by-(N+1) matrix)
%   nbar = mean queue length (K-by-(N+1) matrix)
%   Rzero = system response time (1-by-(N+1) matrix)
%   Xzero = system throughput (1-by-(N+1) matrix)
%   U = utilisation (K-by-(N+1) matrix)
%
% Rzero(i) = System response time when there are (i-1) users
% Xzero(i) = System throughput when there are (i-1) users 

% Z = 0 by default
if (nargin < 3)
    Z = 0;
end   

% Initialisation
K = length(V);  % number of devices
% Make sure S and V are column vectors
S = S(:);
V = V(:); 

% Storage
nbar = zeros(K,N+1);
R = zeros(K,N+1);
X = zeros(K,N+1);
Rzero = zeros(1,N+1);
Xzero = zeros(1,N+1);
U = zeros(K,N+1);

for n = 1:N  % For each customers
    nindex = n+1;
        R(:,nindex) = S .* (1 + nbar(:,nindex-1));
        Rzero(nindex) = sum(V .* R(:,nindex));
        Xzero(nindex) = n / (Rzero(nindex) + Z);
        X(:,nindex) = Xzero(nindex) * V;
        U(:,nindex) = S .* X(:,nindex);
        nbar(:,nindex) = X(:,nindex) .* R(:,nindex);        
end    
