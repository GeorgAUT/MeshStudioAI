// -------------------------------
// Channel with airfoil cutout (.geo)
// Same outer rectangle as your file, but the circular cutout is replaced by an airfoil
// -------------------------------

// far field resolution
dx1 = 0.015;
// resolution at airfoil
dx2 = 0.015;

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

Line Loop(11) = {1, 2, 3, 4}; // outer boundary loop

// -------------------------------
// Airfoil cutout: symmetric NACA 00xx (default: NACA 0012)
// Placed where your cylinder was: center at (0.2, 0.2)
// Chord chosen to match cylinder diameter (~0.1)
// -------------------------------
centerX = 0.2;
centerY = 0.2;

c     = 0.10;   // chord length
t     = 0.12;   // thickness ratio (0.12 => NACA 0012)
alpha = 0.0;    // angle of attack (radians). Example: 5 deg -> 5*Pi/180

nPts = 60; // points per side (upper and lower). Increase for smoother airfoil.

// arrays holding point tags
upper[] = {};
lower[] = {};

// ---- upper surface points: from TE (x=c) to LE (x=0)
For i In {0:nPts}
  x = c * (nPts - i) / nPts; // goes c -> 0
  xcLoc = x / c;

  // NACA 00xx thickness distribution
  yt = 5 * t * c * (0.2969*Sqrt(xcLoc)
                  - 0.1260*xcLoc
                  - 0.3516*xcLoc*xcLoc
                  + 0.2843*xcLoc*xcLoc*xcLoc
                  - 0.1015*xcLoc*xcLoc*xcLoc*xcLoc);

  // shift so mid-chord is at (0,0) before rotation/translation
  x0 = x - c/2;
  y0 = yt;

  // rotate by alpha and translate to (centerX, centerY)
  xr =  x0*Cos(alpha) - y0*Sin(alpha);
  yr =  x0*Sin(alpha) + y0*Cos(alpha);

  p = newp;
  Point(p) = {centerX + xr, centerY + yr, 0, dx2};
  upper[] += {p};
EndFor

// ---- lower surface points: from LE (x=0) back to TE (x=c)
For i In {0:nPts}
  x = c * i / nPts; // goes 0 -> c
  xcLoc = x / c;

  yt = 5 * t * c * (0.2969*Sqrt(xcLoc)
                  - 0.1260*xcLoc
                  - 0.3516*xcLoc*xcLoc
                  + 0.2843*xcLoc*xcLoc*xcLoc
                  - 0.1015*xcLoc*xcLoc*xcLoc*xcLoc);

  x0 = x - c/2;
  y0 = -yt;

  xr =  x0*Cos(alpha) - y0*Sin(alpha);
  yr =  x0*Sin(alpha) + y0*Cos(alpha);

  p = newp;
  Point(p) = {centerX + xr, centerY + yr, 0, dx2};
  lower[] += {p};
EndFor

// Splines to close the airfoil boundary
sUpper = newl;
Spline(sUpper) = {upper[]};

sLower = newl;
Spline(sLower) = {lower[]};

// Airfoil loop (a closed cutout)
Line Loop(12) = {sUpper, sLower};

// -------------------------------
// Fluid domain: rectangle with airfoil hole
// -------------------------------
Plane Surface(15) = {11, 12};

// -------------------------------
// Physical groups (same meaning as your original file)
// -------------------------------

// Top (Line 1) and bottom (Line 3)
Physical Line(1) = {1, 3};
// Inflow (left)
Physical Line(2) = {4};
// Outflow (right)
Physical Line(3) = {2};
// Airfoil boundary
Physical Line(4) = {sUpper, sLower};

// Whole domain ID
Physical Surface(15) = {15};