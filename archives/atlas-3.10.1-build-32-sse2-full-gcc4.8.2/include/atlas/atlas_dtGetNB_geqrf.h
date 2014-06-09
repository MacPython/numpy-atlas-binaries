#ifndef ATL_dtGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,270,324,378,540,1080,2214,3294,4428
 * N : 25,270,324,378,540,1080,2214,3294,4428
 * NB : 8,8,108,108,108,108,108,108,144
 */
#define ATL_dtGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 297) (nb_) = 8; \
   else if ((n_) < 3861) (nb_) = 108; \
   else (nb_) = 144; \
}


#endif    /* end ifndef ATL_dtGetNB_geqrf */
