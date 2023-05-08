
#ifndef FADDEEVA_H
#define FADDEEVA_H

/*--------------------------------------------------------------------------------*/

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <complex.h>

//Pi Ratio of circumference to diameter 3.1415926535897932384626433832795028841971
#define Par_Pi 3.14159265359
//square root of Pi
#define Par_SqrtPi 1.7724538509

#define Par_Sqrt2Pi 2.5066283//sqrt(2Pi)

// Lightspeed[10^9 m s^-1]
#define Par_C 2.99792458e-1

/*--------------------------------------------------------------------------------*/

extern int Faddeeva(double Nu, double y, double *H, double *L, int digits);

extern int Faddeeva916(double Nu, double y, double *H, double *L, int digits);

/*--------------------------------------------------------------------------------*/

#endif /* FADDEEVA_H */
