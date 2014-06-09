#ifndef ATL_cGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,120,240,480,1020,2100
 * N : 25,120,240,480,1020,2100
 * NB : 9,60,60,60,60,60
 */
#define ATL_cGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 72) (nb_) = 9; \
   else (nb_) = 60; \
}


#endif    /* end ifndef ATL_cGetNB_geqrf */
