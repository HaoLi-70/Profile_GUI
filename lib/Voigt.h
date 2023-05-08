
#ifndef VOIGT_H
#define VOIGT_H

/*--------------------------------------------------------------------------------*/

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <complex.h>
#include "FADDEEVA.h"

/*--------------------------------------------------------------------------------*/

extern int profile(double *W, int num, double dnu, double a, double *H, double *L);

extern int profile2(double *W, int num, double dnu, double a, double *H, double *L);


extern int GAUSS_PROFILE(double *W, int num, double dnu, double *Y);

extern int LORENTZ_PROFILE(double *W, int num, double a, double *Y);

/*--------------------------------------------------------------------------------*/

#endif /* VOIGT_H */
