#ifndef ATL_dGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,144,240,288,336,672,1392,2832
 * N : 25,144,240,288,336,672,1392,2832
 * NB : 2,12,16,48,48,48,96,96
 */
#define ATL_dGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 84) (nb_) = 2; \
   else if ((n_) < 192) (nb_) = 12; \
   else if ((n_) < 264) (nb_) = 16; \
   else if ((n_) < 1032) (nb_) = 48; \
   else (nb_) = 96; \
}


#endif    /* end ifndef ATL_dGetNB_geqrf */
