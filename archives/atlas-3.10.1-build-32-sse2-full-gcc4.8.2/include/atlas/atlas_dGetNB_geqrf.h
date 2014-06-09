#ifndef ATL_dGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,162,324,648,810,864,918,972,1350,1674,1728,1782,1836,2052,2754
 * N : 25,162,324,648,810,864,918,972,1350,1674,1728,1782,1836,2052,2754
 * NB : 4,54,54,54,54,54,24,78,60,60,54,108,108,108,108
 */
#define ATL_dGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 93) (nb_) = 4; \
   else if ((n_) < 891) (nb_) = 54; \
   else if ((n_) < 945) (nb_) = 24; \
   else if ((n_) < 1161) (nb_) = 78; \
   else if ((n_) < 1701) (nb_) = 60; \
   else if ((n_) < 1755) (nb_) = 54; \
   else (nb_) = 108; \
}


#endif    /* end ifndef ATL_dGetNB_geqrf */
