#ifndef ATL_ztGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,144,192,240,288,336,384,432,480,672,1392,2784
 * N : 25,144,192,240,288,336,384,432,480,672,1392,2784
 * NB : 5,8,8,12,60,60,84,88,92,80,48,48
 */
#define ATL_ztGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 84) (nb_) = 5; \
   else if ((n_) < 216) (nb_) = 8; \
   else if ((n_) < 264) (nb_) = 12; \
   else if ((n_) < 360) (nb_) = 60; \
   else if ((n_) < 408) (nb_) = 84; \
   else if ((n_) < 456) (nb_) = 88; \
   else if ((n_) < 576) (nb_) = 92; \
   else if ((n_) < 1032) (nb_) = 80; \
   else (nb_) = 48; \
}


#endif    /* end ifndef ATL_ztGetNB_geqrf */
