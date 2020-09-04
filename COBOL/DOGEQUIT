      */////////////////////////////////////////////////////////////// 
      * DOGE Coin CICS/KICKS Application
      * DOGEQUIT:
      *   Exits DOGE Bank.
      *
      * AUTHOR:
      *   Philip Young aka Soldier of FORTRAN
      *
      * 08/30/2020
      * License GPL v3
      */////////////////////////////////////////////////////////////// 
       IDENTIFICATION DIVISION.
       PROGRAM-ID.   DOGEQUIT.
       AUTHOR. SOLDIER OF FORTRAN.
       INSTALLATION. DOGE BANK.
       DATE-WRITTEN. 08/30/20.
       SECURITY. CONFIDENTIAL.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
       01  WTO-MESSAGE PIC X(38) VALUE SPACES.
       01  FACES.
           05  FACES-LIST.
               10  FACE01 PIC X(5) VALUE '(-_-)'.
               10  FACE02 PIC X(5) VALUE '(o_O)'.
               10  FACE03 PIC X(5) VALUE '(^_-)'.
               10  FACE04 PIC X(5) VALUE '(T_T)'.
               10  FACE05 PIC X(5) VALUE '(+_+)'.
               10  FACE06 PIC X(5) VALUE '(@_@)'.
               10  FACE07 PIC X(5) VALUE '(>_>)'.
               10  FACE08 PIC X(5) VALUE '(<_<)'.
               10  FACE09 PIC X(5) VALUE '(*_*)'.
               10  FACE10 PIC X(5) VALUE '(^-^)'.
           05  FACE-ARRAY REDEFINES FACES-LIST OCCURS 10 PIC X(05).
      * 
       01  EXIT-MSG.
           10  COMMAND          PIC X VALUE X'F5'.
           10  WRITE-CONTROL    PIC X VALUE X'C3'.
           10  FILLER PIC X(2)  VALUE X'1DF0'.
           10  FILLER PIC X(3)  VALUE X'284100'.
           10  YELLOW           PIC X(3) VALUE X'2842F6'.
           10  FILLER PIC X(17) VALUE 'DOGE HAS EXITED. '.
           10  DEEP-BLUE        PIC X(3) VALUE X'2842F9'.
           10  FILLER PIC X     VALUE 'G'.
           10  BLUE             PIC X(3) VALUE X'2842F1'.
           10  FILLER PIC X     VALUE 'O'.
           10  TURQ             PIC X(3) VALUE X'2842F5'.
           10  FILLER PIC X     VALUE 'O'.
           10  WHITE            PIC X(3) VALUE X'2842F7'.
           10  FILLER PIC X     VALUE 'D'.
           10  TURQ             PIC X(3) VALUE X'2842F5'.
           10  FILLER PIC X     VALUE 'B'.
           10  BLUE             PIC X(3) VALUE X'2842F1'.
           10  FILLER PIC X     VALUE 'Y'.
           10  DEEP-BLUE        PIC X(3) VALUE X'2842F9'.
           10  FILLER PIC X(3)  VALUE 'E. '.
           10  RED              PIC X(3) VALUE X'2842F2'.
           10  EXIT-FACE        PIC X(5) VALUE '(-_-)'.
           10  FILLER PIC X     VALUE X'13'.
      * vars for random-number from kookbook
       01  IA                   PIC S9(8) COMP VALUE +31337.
       01  IM                   PIC S9(8) COMP VALUE +32768.
       01  IC                   PIC S9(8) COMP VALUE +6925.
       01  FSEED                COMP-1.
       01  FIM                  COMP-1.
       01  IRNDM                PIC S9(8) COMP.
       01  ISEED                PIC S9(8) COMP.
       01  FACE                 PIC S9(8) COMP. 
       01  GARBAGE              PIC S9(8) COMP.
       PROCEDURE DIVISION.
      * Preseed the random number generator
           MOVE EIBTIME TO ISEED.
           PERFORM RANDOM-NUMBER.
           DIVIDE IRNDM BY 10 GIVING GARBAGE REMAINDER FACE.
           MOVE FACE-ARRAY (FACE) TO EXIT-FACE.
           MOVE 'Thank you for using DOGE Bank. Goodbye.' TO WTO-MESSAGE.
           PERFORM DOGE-WTO.

           EXEC CICS
             SEND TEXT FROM(EXIT-MSG) STRFIELD
           END-EXEC.

           EXEC CICS RETURN END-EXEC.
       RANDOM-NUMBER SECTION.
      *    simple LCG algorithm (lifted from Boillot fortran book)
      *    Source: KICKS Kookbook
           MULTIPLY ISEED BY IA GIVING ISEED.
           IF ISEED < 0 COMPUTE ISEED = -1 * ISEED.
           ADD IC, ISEED         GIVING ISEED.
           DIVIDE ISEED BY IM    GIVING IRNDM  REMAINDER ISEED.
           MOVE ISEED TO FSEED.
           MOVE IM    TO FIM.
           DIVIDE FSEED BY FIM   GIVING FIM.
           COMPUTE FSEED = 1000.0 * FIM.
           MOVE FSEED TO IRNDM.
       RANDOM-NUMBER-EXIT.
           EXIT.
      *
       DOGE-WTO.
           EXEC CICS WRITE OPERATOR
               TEXT(WTO-MESSAGE)
           END-EXEC.
           MOVE SPACES TO WTO-MESSAGE.