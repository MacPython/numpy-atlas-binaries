#ifndef ATL_dtGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,96,144,192,240,288,384,432,528,672,816,960,1008,1056,1104,2208,4464
 * N : 25,96,144,192,240,288,384,432,528,672,816,960,1008,1056,1104,2208,4464
 * NB : 9,8,12,4,80,104,96,88,112,112,120,120,112,104,136,96,96
 */
#define ATL_dtGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 60) (nb_) = 9; \
   else if ((n_) < 120) (nb_) = 8; \
   else if ((n_) < 168) (nb_) = 12; \
   else if ((n_) < 216) (nb_) = 4; \
   else if ((n_) < 264) (nb_) = 80; \
   else if ((n_) < 336) (nb_) = 104; \
   else if ((n_) < 408) (nb_) = 96; \
   else if ((n_) < 480) (nb_) = 88; \
   else if ((n_) < 744) (nb_) = 112; \
   else if ((n_) < 984) (nb_) = 120; \
   else if ((n_) < 1032) (nb_) = 112; \
   else if ((n_) < 1080) (nb_) = 104; \
   else if ((n_) < 1656) (nb_) = 136; \
   else (nb_) = 96; \
}


#endif    /* end ifndef ATL_dtGetNB_geqrf */
