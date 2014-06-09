#ifndef ATL_ztGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,174,232,290,348,406,464,522,696,1392,2784
 * N : 25,174,232,290,348,406,464,522,696,1392,2784
 * NB : 6,8,58,58,64,72,72,76,80,80,58
 */
#define ATL_ztGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 99) (nb_) = 6; \
   else if ((n_) < 203) (nb_) = 8; \
   else if ((n_) < 319) (nb_) = 58; \
   else if ((n_) < 377) (nb_) = 64; \
   else if ((n_) < 493) (nb_) = 72; \
   else if ((n_) < 609) (nb_) = 76; \
   else if ((n_) < 2088) (nb_) = 80; \
   else (nb_) = 58; \
}


#endif    /* end ifndef ATL_ztGetNB_geqrf */
