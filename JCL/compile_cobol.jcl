//DOGECOB  JOB  CLASS=A,MSGCLASS=H,MSGLEVEL=(1,1),NOTIFY=HERC01
//JOBPROC  DD DSN=HERC01.KICKSSYS.V1R5M0.PROCLIB,DISP=SHR    
//* MAIN DOGE SCREEN                                         
//DOGEMAIN EXEC K2KCOBCL                                     
//COPY.SYSUT1 DD DISP=SHR,DSN=HERC01.DOGECICS(DOGEMAIN)            
//LKED.SYSIN DD *                                            
 INCLUDE SKIKLOAD(KIKCOBGL)                                  
 ENTRY DOGECOIN                                              
 NAME DOGECOIN(R)                                            
//* DOGE TRANSACTION HISTORY                                 
//DOGETRAN EXEC K2KCOBCL                                     
//COPY.SYSUT1 DD DISP=SHR,DSN=HERC01.DOGECICS(DOGETRAN)            
//LKED.SYSIN DD *                                            
 INCLUDE SKIKLOAD(KIKCOBGL)                                  
 ENTRY DOGETRAN                                              
 NAME DOGETRAN(R)                                            
//* DOGE SEND MONEYS                                         
//DOGESEND EXEC K2KCOBCL                                     
//COPY.SYSUT1 DD DISP=SHR,DSN=HERC01.DOGECICS(DOGESEND)            
//LKED.SYSIN DD *                                            
 INCLUDE SKIKLOAD(KIKCOBGL)                                  
 ENTRY DOGESEND                                              
 NAME DOGESEND(R)                                            
//* DOGE TRANSACTION DETAILS                                 
//DOGEDEET EXEC K2KCOBCL                                     
//COPY.SYSUT1 DD DISP=SHR,DSN=HERC01.DOGECICS(DOGEDEET)            
//LKED.SYSIN DD *                                            
 INCLUDE SKIKLOAD(KIKCOBGL)                                  
 ENTRY DOGEDEET                                              
 NAME DOGEDEET(R)                                            
//* DOGE QUIT DOGE                                           
//DOGEQUIT EXEC K2KCOBCL                                     
//COPY.SYSUT1 DD DISP=SHR,DSN=HERC01.DOGECICS(DOGEQUIT)            
//LKED.SYSIN DD *                                            
 INCLUDE SKIKLOAD(KIKCOBGL)                                  
 ENTRY DOGEQUIT                                              
 NAME DOGEQUIT(R)       