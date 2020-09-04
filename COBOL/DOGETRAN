      */////////////////////////////////////////////////////////////// 
      * DOGE Coin CICS/KICKS Application
      * DOGETRAN:
      *   Displays historical transactions.
      *
      * AUTHOR:
      *   Philip Young aka Soldier of FORTRAN
      *
      * 08/30/2020
      * License GPL v3
      */////////////////////////////////////////////////////////////// 
       IDENTIFICATION DIVISION.
       PROGRAM-ID.   DOGETRAN.
       AUTHOR. SOLDIER OF FORTRAN.
       INSTALLATION. DOGE BANK.
       DATE-WRITTEN. 08/30/20.
       SECURITY. CONFIDENTIAL.
       ENVIRONMENT DIVISION.
       DATA DIVISION.
       WORKING-STORAGE SECTION.
      * VSAM Record Layout
       01  TRANSACTION.
           05  TDATE     PIC X(10).
           05  NUM-DATE  REDEFINES TDATE PIC 9(10).
           05  FILLER    PIC X VALUE SPACES.
           05  TADDRSS   PIC X(34).
           05  FILLER    PIC X VALUE SPACES.
           05  TLABEL    PIC X(10).
           05  FILLER    PIC X VALUE SPACES.
           05  TAMOUNT.
               10  TAMT-SIGN                PIC X.
                   88 TAMT-SIGN-POSITIVE    VALUE '+'.
                   88 TAMT-SIGN-NEGATIVE    VALUE '-'.
               10  TAMT-INTEGER-PART        PIC X(8).
               10  TAMT-DEC-POINT           PIC X.
               10  TAMT-DECIMAL-PART        PIC X(8).
      * Edit to display the amount         
       01  THE-AMOUNT                       PIC S9(8)V9(8).
       01  FILLER REDEFINES THE-AMOUNT.
           05  THE-AMOUNT-INTEGER           PIC X(8).
           05  THE-AMOUNT-DECIMAL           PIC S9(8).
       01  RECENT-COLOR                     PIC X.
       01  DISPLAY-TRAN.
           05  DDATE     PIC X(10).
           05  DTYPE     PIC X(10) VALUE 'RECV FROM'.
           05  DLABEL    PIC X(10).
           05  DSIGN     PIC X VALUE '+'.
           05  DAMOUNT   PIC Z(02),Z(03),Z(02)9.9(8).
       01  TEMP-DATE     PIC 9(15) COMP-3.
       01  SINCE-EPOCH   PIC S9(15) COMP-3 VALUE +2208988800000.
       01  RESPONSE-CODE  PIC S9(4) COMP.
       01  DOGECOMMS-AREA.
           05  START-RECORD-ID PIC 9(10) VALUE 0000000002.
       01  LINE-NUMBER PIC 9 VALUE 0.
       01  WTO-MESSAGE PIC X(38) VALUE SPACES.
       01  DONE-RECORDS PIC XXXX VALUE 'NOPE'.
      *
       COPY DOGETR.
       COPY DFHAID.
       COPY DFHBMSCA.
       LINKAGE SECTION.
      *
       01  DFHCOMMAREA                       PIC X(10).
      *
       PROCEDURE DIVISION.
       DOGE-MAIN.
      *
           IF EIBCALEN > ZERO THEN
               MOVE DFHCOMMAREA TO DOGECOMMS-AREA.

           IF EIBCALEN EQUAL TO ZERO
              MOVE 'Displaying first 7 Transactions' TO WTO-MESSAGE
              PERFORM DOGE-WTO
              PERFORM LET-ER-RIP
              PERFORM DOGE-LIST-TRANSACTIONS
      * MAP IS DFHMDI FROM THE MAPSET
      * MAPSET IS WHAT WE SET IN THE PCT (WITH CEDA)
              EXEC CICS SEND MAP('DOGETR1')
                  MAPSET('DOGETR') ERASE
              END-EXEC
           ELSE
           IF EIBAID EQUAL TO DFHPF8 AND
                           START-RECORD-ID NOT EQUAL TO '9999999999'
              MOVE 'Showing next screen' TO WTO-MESSAGE
              PERFORM DOGE-WTO
              PERFORM LET-ER-RIP
              PERFORM DOGE-LIST-TRANSACTIONS
              MOVE 'PF7 PREV -' TO PREVO
              EXEC CICS SEND MAP('DOGETR1')
                  MAPSET('DOGETR') ERASE
              END-EXEC
           ELSE
           IF EIBAID EQUAL TO DFHPF7
              MOVE 'Showing prev screen' TO WTO-MESSAGE
              PERFORM DOGE-WTO
              PERFORM LET-ER-RIP
              PERFORM BACK-IT-UP 15 TIMES
              PERFORM DOGE-LIST-TRANSACTIONS
              EXEC CICS SEND MAP('DOGETR1')
                  MAPSET('DOGETR') ERASE
              END-EXEC
           ELSE
           IF EIBAID EQUAL TO DFHPF3
               EXEC CICS XCTL 
                   PROGRAM('DOGEQUIT')
               END-EXEC
           ELSE
           IF EIBAID EQUAL TO DFHENTER
                   PERFORM RECEIVE-OPTION
                   PERFORM PARSE-OPTION.  
           EXEC CICS
               RETURN TRANSID('DTRN')
                      COMMAREA(DOGECOMMS-AREA)
           END-EXEC.
       DOGE-EXIT.
           GOBACK.
      *   
       LET-ER-RIP.
      *
           EXEC CICS STARTBR FILE('DOGEVSAM')
                RIDFLD(START-RECORD-ID)
           END-EXEC. 
       BACK-IT-UP.
      * Yes, this is a hack but i was too stupid to use READPREV
           MOVE 'PF7 PREV -' TO PREVO
           IF START-RECORD-ID NOT EQUAL TO '0000000002'
               EXEC CICS READPREV FILE('DOGEVSAM')
                   RIDFLD(START-RECORD-ID)
                   INTO(TRANSACTION)
               END-EXEC
           ELSE
      *         MOVE 'BACK TO ONE' TO WTO-MESSAGE
      *         PERFORM DOGE-WTO
               MOVE SPACES TO PREVO.
      *     MOVE 'BACK THAT THANG UP' TO WTO-MESSAGE.
      *     PERFORM DOGE-WTO.
      *    This does nothing but the compiler complains ending on an IF         
           MOVE 0 TO RESPONSE-CODE.
       DOGE-LIST-TRANSACTIONS.
      *   Skip the first record
           EXEC CICS READNEXT FILE('DOGEVSAM')
               RIDFLD(START-RECORD-ID)
               INTO(TRANSACTION)
           END-EXEC.
      *   Loop through and show 7 lines
           PERFORM DISPLAY-TRANS VARYING LINE-NUMBER
              FROM 1 BY 1 UNTIL LINE-NUMBER IS EQUAL TO 8 OR 
              DONE-RECORDS IS EQUAL TO 'DONE'. 

           IF DONE-RECORDS IS NOT EQUAL TO 'DONE'
               MOVE 'PF8 NEXT' TO NEXTO.
         
           EXEC CICS ENDBR 
               FILE('DOGEVSAM')
           END-EXEC.
      *    This does nothing but the compiler complains ending on an IF         
           MOVE 0 TO RESPONSE-CODE.
       CONVERT-AMOUNT-TO-DISPLAY.
      * Converts the number from VSAM to ##,###,###.########
           MOVE DFHGREEN TO RECENT-COLOR.
           MOVE TAMT-INTEGER-PART TO THE-AMOUNT-INTEGER.
           MOVE TAMT-DECIMAL-PART TO THE-AMOUNT-DECIMAL.
           MOVE 'RECV FROM' TO DTYPE.
           IF TAMT-SIGN-NEGATIVE
               MOVE DFHRED TO RECENT-COLOR
               MOVE 'SENT TO  ' TO DTYPE
               SUBTRACT THE-AMOUNT FROM ZERO GIVING THE-AMOUNT.
           MOVE THE-AMOUNT TO DAMOUNT.
           MOVE TAMT-SIGN TO DSIGN.
      *
       CONVERT-DATE.
      *
      * Converts Linux EPOCH to CICS Absolute Time
      * and places it in DISPLAY-TRAN:DDATE as MM/DD/YYYY
      *
           MOVE NUM-DATE TO TEMP-DATE.
           MULTIPLY 1000 BY TEMP-DATE.
           ADD SINCE-EPOCH TO TEMP-DATE.
           EXEC CICS FORMATTIME ABSTIME(TEMP-DATE)
                DATESEP('/')
                MMDDYYYY(DDATE)
           END-EXEC.
      *
       DOGE-WTO.
           EXEC CICS WRITE OPERATOR
               TEXT(WTO-MESSAGE)
           END-EXEC.
           MOVE SPACES TO WTO-MESSAGE.

       DISPLAY-TRANS.
           EXEC CICS READNEXT FILE('DOGEVSAM')
               RIDFLD(START-RECORD-ID)
               INTO(TRANSACTION)
           END-EXEC
           IF TDATE IS EQUAL TO '9999999999'                                
      *    We're done here 
               MOVE 'DONE' TO DONE-RECORDS
               MOVE SPACES TO NEXTO
               MOVE 'PF7 PREV' TO PREVO            
           ELSE  
               PERFORM CONVERT-DATE
               PERFORM CONVERT-AMOUNT-TO-DISPLAY
               MOVE TLABEL TO DLABEL
               PERFORM FILL-ROWS-WITH-DATA.
      *    This does nothing but the compiler complains ending on an IF         
           MOVE 0 TO RESPONSE-CODE.

       FILL-ROWS-WITH-DATA.
            IF LINE-NUMBER IS EQUAL TO 1 
                MOVE TDATE TO TRAN1KO
                MOVE DDATE TO TRAN1DO
                MOVE RECENT-COLOR TO TRAN1TC 
                MOVE DTYPE TO TRAN1TO
                MOVE DLABEL TO TRAN1LO
                MOVE RECENT-COLOR TO TRAN1SC
                MOVE DSIGN TO TRAN1SO
                MOVE THE-AMOUNT TO TRAN1AO
            ELSE
            IF LINE-NUMBER IS EQUAL TO 2 
                MOVE TDATE TO TRAN2KO
                MOVE DDATE TO TRAN2DO
                MOVE RECENT-COLOR TO TRAN2TC 
                MOVE DTYPE TO TRAN2TO
                MOVE DLABEL TO TRAN2LO
                MOVE RECENT-COLOR TO TRAN2SC
                MOVE DSIGN TO TRAN2SO
                MOVE THE-AMOUNT TO TRAN2AO
            ELSE
            IF LINE-NUMBER IS EQUAL TO 3 
                MOVE TDATE TO TRAN3KO
                MOVE DDATE TO TRAN3DO
                MOVE RECENT-COLOR TO TRAN3TC 
                MOVE DTYPE TO TRAN3TO
                MOVE DLABEL TO TRAN3LO
                MOVE RECENT-COLOR TO TRAN3SC
                MOVE DSIGN TO TRAN3SO
                MOVE THE-AMOUNT TO TRAN3AO
            ELSE
            IF LINE-NUMBER IS EQUAL TO 4 
                MOVE TDATE TO TRAN4KO
                MOVE DDATE TO TRAN4DO
                MOVE RECENT-COLOR TO TRAN4TC 
                MOVE DTYPE TO TRAN4TO
                MOVE DLABEL TO TRAN4LO
                MOVE RECENT-COLOR TO TRAN4SC
                MOVE DSIGN TO TRAN4SO
                MOVE THE-AMOUNT TO TRAN4AO
            ELSE
            IF LINE-NUMBER IS EQUAL TO 5 
                MOVE TDATE TO TRAN5KO
                MOVE DDATE TO TRAN5DO
                MOVE RECENT-COLOR TO TRAN5TC 
                MOVE DTYPE TO TRAN5TO
                MOVE DLABEL TO TRAN5LO
                MOVE RECENT-COLOR TO TRAN5SC
                MOVE DSIGN TO TRAN5SO
                MOVE THE-AMOUNT TO TRAN5AO
            ELSE
            IF LINE-NUMBER IS EQUAL TO 6 
                MOVE TDATE TO TRAN6KO
                MOVE DDATE TO TRAN6DO
                MOVE RECENT-COLOR TO TRAN6TC 
                MOVE DTYPE TO TRAN6TO
                MOVE DLABEL TO TRAN6LO
                MOVE RECENT-COLOR TO TRAN6SC
                MOVE DSIGN TO TRAN6SO
                MOVE THE-AMOUNT TO TRAN6AO
            ELSE
            IF LINE-NUMBER IS EQUAL TO 7 
                MOVE TDATE TO TRAN7KO
                MOVE DDATE TO TRAN7DO
                MOVE RECENT-COLOR TO TRAN7TC 
                MOVE DTYPE TO TRAN7TO
                MOVE DLABEL TO TRAN7LO
                MOVE RECENT-COLOR TO TRAN7SC
                MOVE DSIGN TO TRAN7SO
                MOVE THE-AMOUNT TO TRAN7AO.
      *    This does nothing but the compiler complains ending on an IF         
           MOVE 0 TO RESPONSE-CODE.
      *     
       RECEIVE-OPTION.
      * Get the option the user enters

           MOVE 'DTRN - Getting Input from User.' TO WTO-MESSAGE.
           PERFORM DOGE-WTO.
           EXEC CICS
               RECEIVE MAP('DOGETR1')
                       MAPSET('DOGETR')
                       INTO(DOGETR1I)
           END-EXEC.

       PARSE-OPTION.
      *    Parse the user entry 
           MOVE OPTIONI TO WTO-MESSAGE.          
           PERFORM DOGE-WTO.
           IF OPTIONI EQUAL TO 'T' OR OPTIONI EQUAL TO 'M'
               MOVE 'Opening Transaction History' TO WTO-MESSAGE
               PERFORM DOGE-WTO
      *         EXEC CICS XCTL 
      *             PROGRAM('DOGETRAN')
      *         END-EXEC
           ELSE
           IF OPTIONI EQUAL TO 'W'         
               MOVE 'DTRN - Opening Main Menu' TO WTO-MESSAGE
               PERFORM DOGE-WTO
               MOVE 'W' TO DOGECOMMS-AREA
               EXEC CICS XCTL 
                   PROGRAM('DOGECOIN')
                   COMMAREA(DOGECOMMS-AREA)
               END-EXEC
           ELSE
           IF OPTIONI EQUAL TO 'D'
               MOVE 'Opening Transaction Details' TO WTO-MESSAGE
               PERFORM DOGE-WTO
               EXEC CICS XCTL 
                   PROGRAM('DOGEDEET')
               END-EXEC
           ELSE
           IF OPTIONI EQUAL TO 'S'
               MOVE 'Opening Such Send' TO WTO-MESSAGE
               PERFORM DOGE-WTO
               EXEC CICS XCTL 
                   PROGRAM('DOGESEND')
               END-EXEC.
           MOVE SPACES TO WTO-MESSAGE.