#ifndef ATL_zGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,96,144,192,432,864,1296,1728
 * N : 25,96,144,192,432,864,1296,1728
 * NB : 9,8,12,48,48,48,96,96
 */
#define ATL_zGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 60) (nb_) = 9; \
   else if ((n_) < 120) (nb_) = 8; \
   else if ((n_) < 168) (nb_) = 12; \
   else if ((n_) < 1080) (nb_) = 48; \
   else (nb_) = 96; \
}


#endif    /* end ifndef ATL_zGetNB_geqrf */
