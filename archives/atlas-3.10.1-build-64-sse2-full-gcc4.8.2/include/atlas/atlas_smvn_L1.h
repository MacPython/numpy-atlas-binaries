#ifndef ATLAS_SMVN_L1_H
#define ATLAS_SMVN_L1_H

#include "atlas_type.h"

#ifndef ATL_MVKERN_DEF
   #define ATL_MVKERN_DEF
   typedef void (*ATL_mvkern_t)
      (ATL_CINT, ATL_CINT, const float*, ATL_CINT, const float*, float*);

#endif
void ATL_smvnk__2(ATL_CINT, ATL_CINT, const float*, ATL_CINT, const float*, float*);
void ATL_smvnk__2_b0(ATL_CINT, ATL_CINT, const float*, ATL_CINT, const float*, float*);
void ATL_smvnk__900001(ATL_CINT, ATL_CINT, const float*, ATL_CINT, const float*, float*);
void ATL_smvnk__900001_b0(ATL_CINT, ATL_CINT, const float*, ATL_CINT, const float*, float*);

static ATL_mvkern_t ATL_GetMVNKern
   (ATL_CINT M, ATL_CINT N, const void *A, ATL_CINT lda,
    ATL_mvkern_t *mvk_b0, int *DOTBASED,
    int *mu, int *nu, int *minM, int *minN, int *alignX, int *ALIGNX2A,
    int *alignY, int *FNU, ATL_INT *CacheElts) 
{
   if ((((((ATL_MulBySize(lda)) >> 4)) << 4)) == ATL_MulBySize(lda))
   {
      *minM = 0;   *minN = 0;
      *mu = 8;     *nu = 4;
      *alignX = 4;  *alignY = 16;
      *ALIGNX2A = 1;
      *FNU = 0;
      *CacheElts = 6881;
      *mvk_b0 = ATL_smvnk__2_b0;
      *DOTBASED = 0;
      return(ATL_smvnk__2);
   } /* end if on lda multiple restriction */
   *minM = 1;   *minN = 8;
   *mu = 1;     *nu = 8;
   *alignX = 4;  *alignY = 4;
   *ALIGNX2A = 0;
   *FNU = 1;
   *CacheElts = 6881;
   *mvk_b0 = ATL_smvnk__900001_b0;
   *DOTBASED = 0;
   return(ATL_smvnk__900001);
}

#define ATL_GetPartMVN(A_, lda_, mb_, nb_) { *(mb_) = 381; *(nb_) = 8; }

#endif  /* end protection around header file contents */
