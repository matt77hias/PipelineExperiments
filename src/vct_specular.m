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
n_dot_h = ses(subs(n_dot_h, sin(theta), sqrt(1-cos(theta)^2)));
v_dot_h = simplify(dot(v, h));
v_dot_h = ses(subs(v_dot_h, sin(theta), sqrt(1-cos(theta)^2)));

% Material constants
alpha = sym('alpha');
assume(in(alpha, 'real') & 0 < alpha & alpha <= 1)
F0 = sym('F0');
assume(in(F0, 'real') & 0 <= F0 & F0 <= 1)

% BRDF (components)
V = simplify(2 / (n_dot_v*sqrt(alpha^2 + (1-alpha^2)*n_dot_l) ...
                + n_dot_l*sqrt(alpha^2 + (1-alpha^2)*n_dot_v)));
D = simplify(alpha^2 / (pi * (n_dot_h*(alpha^2-1) + 1)^2));
F = simplify(F0 + (1-F0)*(1-v_dot_h)^5);  
S = simplify((F * D * V) / 4);

% Integrands
% d_omega      =  sin(theta) d_theta d_phi | theta=(0,pi/2)   phi=(0,2*pi) 
% d_cos(theta) = -sin(theta) d_theta       | cos(theta)=(1,0) 
% d_omega      = -d_cos(theta)       d_phi | cos(theta)=(1,0) phi=(0,2*pi)
% d_omega      =  d_cos(theta)       d_phi | cos(theta)=(0,1) phi=(0,2*pi)
% d_omega      =  d_x                d_phi | x         =(0,1) phi=(0,2*pi)
x = sym('x');
assume(in(x, 'real') & 0 <= x & x <= 1);

integrand_D  = ses(D * n_dot_l);
integrand_D  = ses(subs(integrand_D,  cos(theta), x));

integrand_M1 = ses(S * n_dot_l);
integrand_M1 = ses(subs(integrand_M1, cos(theta), x));

integrand_M2 = ses(S * n_dot_l^2);
integrand_M2 = ses(subs(integrand_M2, cos(theta), x));

% Integrals
%integral_D1  = ses(int(integrand_D,  phi, 0, 2*pi));
%integral_D2  = ses(int(integral_D1,  x,   0, 1));

%integral_M11 = ses(int(integrand_M1, phi, 0, 2*pi));
%integral_M12 = ses(int(integral_M11, x,   0, 1));

%integral_M21 = ses(int(integrand_M2, phi, 0, 2*pi));
%integral_M22 = ses(int(integral_M21, x,   0, 1));

function result = ses(arg)
    result = simplify(expand(simplify(arg)));
end