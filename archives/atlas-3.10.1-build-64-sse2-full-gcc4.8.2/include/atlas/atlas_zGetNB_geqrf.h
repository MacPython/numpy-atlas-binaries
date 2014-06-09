#ifndef ATL_zGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,174,406,870,1740
 * N : 25,174,406,870,1740
 * NB : 6,58,58,58,58
 */
#define ATL_zGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 99) (nb_) = 6; \
   else (nb_) = 58; \
}


#endif    /* end ifndef ATL_zGetNB_geqrf */
