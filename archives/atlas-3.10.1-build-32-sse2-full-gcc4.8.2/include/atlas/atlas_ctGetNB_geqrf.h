#ifndef ATL_ctGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,180,420,840,900,1020,1080,1140,1260,1680,3360
 * N : 25,180,420,840,900,1020,1080,1140,1260,1680,3360
 * NB : 9,60,60,60,60,96,120,120,120,120,180
 */
#define ATL_ctGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 102) (nb_) = 9; \
   else if ((n_) < 960) (nb_) = 60; \
   else if ((n_) < 1050) (nb_) = 96; \
   else if ((n_) < 2520) (nb_) = 120; \
   else (nb_) = 180; \
}


#endif    /* end ifndef ATL_ctGetNB_geqrf */
