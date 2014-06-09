#ifndef ATL_ctGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,144,216,360,792,1656,3384
 * N : 25,144,216,360,792,1656,3384
 * NB : 4,4,72,72,72,72,72
 */
#define ATL_ctGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 180) (nb_) = 4; \
   else (nb_) = 72; \
}


#endif    /* end ifndef ATL_ctGetNB_geqrf */
