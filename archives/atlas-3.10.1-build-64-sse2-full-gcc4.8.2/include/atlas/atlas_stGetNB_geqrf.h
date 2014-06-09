#ifndef ATL_stGetNB_geqrf

/*
 * NB selection for GEQRF: Side='RIGHT', Uplo='UPPER'
 * M : 25,128,192,256,320,384,448,640,1344,2752,4160,5568
 * N : 25,128,192,256,320,384,448,640,1344,2752,4160,5568
 * NB : 4,64,16,128,128,128,136,144,128,128,128,192
 */
#define ATL_stGetNB_geqrf(n_, nb_) \
{ \
   if ((n_) < 76) (nb_) = 4; \
   else if ((n_) < 160) (nb_) = 64; \
   else if ((n_) < 224) (nb_) = 16; \
   else if ((n_) < 416) (nb_) = 128; \
   else if ((n_) < 544) (nb_) = 136; \
   else if ((n_) < 992) (nb_) = 144; \
   else if ((n_) < 4864) (nb_) = 128; \
   else (nb_) = 192; \
}


#endif    /* end ifndef ATL_stGetNB_geqrf */
