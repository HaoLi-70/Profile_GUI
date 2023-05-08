#include "Voigt.h"

/*--------------------------------------------------------------------------------*/

    /*######################################################################
     
      revision log:
     
     ######################################################################*/

/*--------------------------------------------------------------------------------*/

extern int profile(double *W, int num, double dnu, double a, double *H, double *L){

  int i;
  double an=a/dnu;
  for(i=0;i<num;i++){
    Faddeeva(W[i]/dnu, an, H+i, L+i, 6);
    H[i] /= Par_SqrtPi*dnu;
    L[i] /= Par_SqrtPi*dnu;
  }

  return 0;
}

extern int profile2(double *W, int num, double dnu, double a, double *H, double *L){

  int i;
  double an=a/dnu;
  for(i=0;i<num;i++){
    Faddeeva(W[i]/dnu, an, H+i, L+i, 8);
    //Faddeeva916(W[i]/dnu, an, H+i, L+i, 6);
    H[i] /= Par_SqrtPi*dnu;
    L[i] /= Par_SqrtPi*dnu;
  }

  return 0;
}


/*--------------------------------------------------------------------------------*/

extern int GAUSS_PROFILE(double *W, int num, double dnu, double *Y){
   
    int i;
    for(i=0;i<num;i++){
      //Y[i] = exp(-W[i]*W[i]/dnu/dnu/2)/Par_sqrt2pi/dnu;
      Y[i] = exp(-W[i]*W[i]/dnu/dnu)/Par_SqrtPi/dnu;

    }
    
    return 0;
}

/*--------------------------------------------------------------------------------*/

extern int LORENTZ_PROFILE(double *W, int num, double a, double *Y){

    int i;    
    for(i=0;i<num;i++){
      Y[i] = a/Par_Pi/(W[i]*W[i]+a*a);
    }
    return 0;
}

/*--------------------------------------------------------------------------------*/
