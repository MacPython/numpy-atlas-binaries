#ifndef ATL_sGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,192,384,832,1280,1472,1728,3520
 * N : 25,192,384,832,1280,1472,1728,3520
 * NB : 9,64,64,64,64,64,128,128
 */
#define ATL_sGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 108) (nb_) = 9; \
   else if ((n_) < 1600) (nb_) = 64; \
   else (nb_) = 128; \
}


#endif    /* end ifndef ATL_sGetNB_geqrf */
