#ifndef ATL_stGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,160,320,400,480,560,640,1360,2800,5600
 * N : 25,160,320,400,480,560,640,1360,2800,5600
 * NB : 9,80,12,12,16,80,132,128,80,80
 */
#define ATL_stGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 92) (nb_) = 9; \
   else if ((n_) < 240) (nb_) = 80; \
   else if ((n_) < 440) (nb_) = 12; \
   else if ((n_) < 520) (nb_) = 16; \
   else if ((n_) < 600) (nb_) = 80; \
   else if ((n_) < 1000) (nb_) = 132; \
   else if ((n_) < 2080) (nb_) = 128; \
   else (nb_) = 80; \
}


#endif    /* end ifndef ATL_stGetNB_geqrf */
