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

% Dot products
n_dot_v = simplify(dot(n, v));
n_dot_l = simplify(dot(n, l));
v_dot_l = simplify(dot(v, l));
n_dot_h = (n_dot_v + n_dot_l) / sqrt(2 + 2*v_dot_l);

Diff_xx = diff(n_dot_h, x, 2);
Diff_yy = diff(n_dot_h, y, 2);
Diff_xy = diff(diff(n_dot_h, x), y);
Diff_yx = diff(diff(n_dot_h, y), x);

n_dot_h_00 = subs(subs(n_dot_h, x, 0), y, 0);
Diff_xx_00 = subs(subs(Diff_xx, x, 0), y, 0);
Diff_yy_00 = subs(subs(Diff_yy, x, 0), y, 0);
Diff_xy_00 = subs(subs(Diff_xy, x, 0), y, 0);
Diff_yx_00 = subs(subs(Diff_yx, x, 0), y, 0);

function result = ses(arg)
    result = simplify(expand(simplify(arg)));
end