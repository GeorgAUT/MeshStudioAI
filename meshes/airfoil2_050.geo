// -------------------------------
// Channel with NACA 4412 airfoil cutout (.geo)
// Chord = 0.42 (3x bigger than 0.14), shifted 5% chord to the right
// Fix: ensure the airfoil curve loop is truly closed by reusing TE/LE points
// -------------------------------

// far field resolution
dx1 = 0.015;
// resolution at airfoil
dx2 = 0.010;

// -------------------------------
// Outer rectangle (channel)
// -------------------------------
Point(1) = {0,   0,    0, dx1};
Point(2) = {2.2, 0,    0, dx1};
Point(3) = {0,   0.41, 0, dx1};
Point(4) = {2.2, 0.41, 0, dx1};

Line(1) = {3, 4};  // top
Line(2) = {4, 2};  // right (outflow)
Line(3) = {2, 1};  // bottom
Line(4) = {1, 3};  // left (inflow)

Line Loop(11) = {1, 2, 3, 4};

// -------------------------------
// NACA 4412 parameters + placement
// -------------------------------
// NACA 4412 => m=0.04, p=0.4, t=0.12
centerX = 0.3;   // 0.2 + 0.05*c = 0.2 + 0.021
centerY = 0.2;

c     = 0.42;   // 3x larger chord
t     = 0.12;
m     = 0.04;
p     = 0.40;
alpha = 0.0;    // radians

nPts = 120;     // points per side (increase if you want smoother)

upper[] = {};
lower[] = {};

// ---- build upper surface points from TE -> LE (includes both endpoints)
For i In {0:nPts}
  x  = c * (nPts - i) / nPts; // c -> 0
  xc = x / c;

  yt = 5 * t * c * (0.2969*Sqrt(xc)
                  - 0.1260*xc
                  - 0.3516*xc*xc
                  + 0.2843*xc*xc*xc
                  - 0.1015*xc*xc*xc*xc);

  If (xc < p)
    yc    = m * c * ((2*p*xc) - xc*xc)/(p*p);
    dycdx = 2*m*(p-xc)/(p*p);
  Else
    yc    = m * c * ((1-2*p) + 2*p*xc - xc*xc)/((1-p)*(1-p));
    dycdx = 2*m*(p-xc)/((1-p)*(1-p));
  EndIf

  theta = Atan(dycdx);

  xu = x - yt*Sin(theta);
  yu = yc + yt*Cos(theta);

  // shift to mid-chord at origin
  x0 = xu - c/2;
  y0 = yu;

  // rotate + translate
  xr =  x0*Cos(alpha) - y0*Sin(alpha);
  yr =  x0*Sin(alpha) + y0*Cos(alpha);

  pt = newp;
  Point(pt) = {centerX + xr, centerY + yr, 0, dx2};
  upper[] += {pt};
EndFor

// Grab the actual point tags for TE and LE from the upper list
pTE = upper[0];        // first upper point = TE
pLE = upper[#upper[]-1]; // last upper point  = LE

// ---- build lower surface points from LE -> TE
// Reuse LE and TE point tags, and only create interior lower points
lower[] += {pLE};

For i In {1:nPts-1}
  x  = c * i / nPts;  // (0,c) excluding endpoints
  xc = x / c;

  yt = 5 * t * c * (0.2969*Sqrt(xc)
                  - 0.1260*xc
                  - 0.3516*xc*xc
                  + 0.2843*xc*xc*xc
                  - 0.1015*xc*xc*xc*xc);

  If (xc < p)
    yc    = m * c * ((2*p*xc) - xc*xc)/(p*p);
    dycdx = 2*m*(p-xc)/(p*p);
  Else
    yc    = m * c * ((1-2*p) + 2*p*xc - xc*xc)/((1-p)*(1-p));
    dycdx = 2*m*(p-xc)/((1-p)*(1-p));
  EndIf

  theta = Atan(dycdx);

  xl = x + yt*Sin(theta);
  yl = yc - yt*Cos(theta);

  x0 = xl - c/2;
  y0 = yl;

  xr =  x0*Cos(alpha) - y0*Sin(alpha);
  yr =  x0*Sin(alpha) + y0*Cos(alpha);

  pt = newp;
  Point(pt) = {centerX + xr, centerY + yr, 0, dx2};
  lower[] += {pt};
EndFor

lower[] += {pTE};

// ---- splines and loop
sUpper = newl;
Spline(sUpper) = {upper[]};   // TE -> LE

sLower = newl;
Spline(sLower) = {lower[]};   // LE -> TE

Line Loop(12) = {sUpper, sLower};

// -------------------------------
// Fluid domain: rectangle with airfoil hole
// (using -12 is fine too; keeping +12 works since loop is now correct)
// -------------------------------
Plane Surface(15) = {11, 12};

// -------------------------------
// Physical groups
// -------------------------------
Physical Line(1) = {1, 3};            // top & bottom
Physical Line(2) = {4};               // inflow
Physical Line(3) = {2};               // outflow
Physical Line(4) = {sUpper, sLower};  // airfoil boundary
Physical Surface(15) = {15};          // fluid domain