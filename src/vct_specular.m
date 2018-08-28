% The (normalized) surface normal expressed in tangent space.
% (theta, phi) = (0,_)
n = [0, 0, 1];
n_norm = norm(n);

% The (normalized) view (hit-to-eye) direction expressed in tangent space.
% (theta, phi) = (xi,0)
xi = sym('xi');
assume(in(xi, 'real') & 0 <= xi & xi <= pi/2) 
v = [sin(xi), 0, cos(xi)];
v_norm = simplify(norm(v));

% The (normalized) light (hit-to-light) direction expressed in tangent space.
theta = sym('theta');
assume(in(theta, 'real') & 0 <= theta & theta <= pi/2) 
phi = sym('phi');
assume(in(phi, 'real') & 0 <= phi & phi <= 2*pi) 
l = [cos(phi)*sin(theta), sin(phi)*sin(theta), cos(theta)];
l_norm = simplify(norm(l));

% The (normalized) half direction expressed in tangent space.
vl_norm = ses(norm(v + l));
h = simplify((v + l) / vl_norm);
h_norm = simplify(norm(h));

% Dot products
n_dot_v = simplify(dot(n, v));
n_dot_l = simplify(dot(n, l));
n_dot_h = simplify(dot(n, h));
v_dot_h = simplify(dot(v, h));

% Material constants
alpha = sym('alpha');
assume(in(alpha, 'real') & 0 <= alpha & alpha <= 1)
F0 = sym('F0');
assume(in(F0, 'real') & 0 <= F0 & F0 <= 1)

% BRDF components
V = simplify(2 / (n_dot_v*sqrt(alpha^2 + (1-alpha^2)*n_dot_l) ...
                + n_dot_l*sqrt(alpha^2 + (1-alpha^2)*n_dot_v)));
D = simplify(alpha^2 / (pi * (n_dot_h*(alpha^2-1) + 1)^2));
F = simplify(F0 + (1-F0)*(1-v_dot_h)^5);  
S = simplify((F * D * V) / 4);

% Check whether NDF is normalized.
integrand_D = ses(D * cos(theta));
integral_D1 = ses(int(integrand_D, phi,   0, 2*pi));
integral_D2 = ses(int(integral_D1, theta, 0, pi/2));
% Compute 1st Moment.
integrand_S = ses(S * cos(theta));
integral_S1 = ses(int(integrand_S, phi,   0, 2*pi));
integral_S2 = ses(int(integral_S1, theta, 0, pi/2));
% Compute 2nd Moment.
integrand_T = ses(S * cos(theta)^2);
integral_T1 = ses(int(integrand_T, phi,   0, 2*pi));
integral_T2 = ses(int(integral_T1, theta, 0, pi/2));

function y = ses(x)
    y = simplify(expand(simplify(x)));
end