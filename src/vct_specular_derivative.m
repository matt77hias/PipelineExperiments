% Tangent space about perfect reflection vector

% The (normalized) surface normal expressed in tangent space.
nx = sym('nx');
assume(in(nx, 'real') & -1 <= nx & nx <= 1);
ny = sym('ny');
assume(in(ny, 'real') & -1 <= ny & ny <= 1);
nz = sym('nz');
assume(in(nz, 'real') & -1 <= nz & nz <= 1);
n = [nx, ny, nz];

% The (normalized) view (hit-to-eye) direction expressed in tangent space.
vx = sym('vx');
assume(in(vx, 'real') & -1 <= vx & vx <= 1);
vy = sym('vy');
assume(in(vy, 'real') & -1 <= vy & vy <= 1);
vz = sym('vz');
assume(in(vz, 'real') & -1 <= vz & vz <= 1);
v = [vx, vy, vz];

% The (normalized) view (hit-to-light) direction expressed in tangent space.
x = sym('x');
assume(in(x, 'real'));
y = sym('y');
assume(in(y, 'real'));
l = [x, y, sqrt(1-x^2-y^2)];

% Jacobian
% J = 1 / (sqrt(1-x^2-y^2) * sqrt(x^2+y^2));
% will be eliminated after multiplication by cos(theta) sin(theta)

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
assume(in(alpha, 'real') & 0 < alpha & alpha <= 1)
F0 = sym('F0');
assume(in(F0, 'real') & 0 <= F0 & F0 <= 1)

% BRDF (components)
V = simplify(2 / (n_dot_v*sqrt(alpha^2 + (1-alpha^2)*n_dot_l) ...
                + n_dot_l*sqrt(alpha^2 + (1-alpha^2)*n_dot_v)));
D = simplify(alpha^2 / (pi * (n_dot_h*(alpha^2-1) + 1)^2));
F = simplify(F0 + (1-F0)*(1-v_dot_h)^5);  
S = simplify((F * D * V) / 4);

Diff_xx = subs(subs(diff(log(S), x, 2), x, 0), y, 0);
Diff_yy = subs(subs(diff(log(S), y, 2), x, 0), y, 0);

Diff_xx = expand(Diff_xx);
Diff_xx = subs(Diff_xx, nx^2 + ny^2 + nz^2, 1);
Diff_xx = subs(Diff_xx, vx^2 + vy^2 + vz^2, 1);


function result = ses(arg)
    result = simplify(expand(simplify(arg)));
end