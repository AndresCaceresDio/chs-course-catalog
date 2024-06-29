-- Keep a log of any SQL queries you execute as you solve the mystery.

-- To look at all of the tables of information at my disposal

.tables

-- To look at what columns I can index into to find any crime scene report that matches the setting of this crime

.schema crime_scene_reports

-- To see if there are any crime scene reports that match the setting of this crime

SELECT *
    FROM crime_scene_reports
        WHERE year = 2021
        AND month = 7
        AND day = 28;

-- To see what columns I can index into to get more information about the bakery, which was mentioned in the witness
-- interview transcripts

.schema bakery_security_logs

-- To see if I can find a license plate that corresponds to the time and place of the crime

SELECT *
    FROM bakery_security_logs
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND hour = 10;

-- To see if the people table has a license plate column and any useful information to provide

.schema people

-- To get more information about my suspect including his/her name, number, and passport number

SELECT *
    FROM people
        WHERE license_plate = '13FNH73';

-- To see what columns I can index into to find out who Sophia, my suspect, has been calling

.schema phone_calls

-- To see who Sophia has been calling in order to maybe ascertain an accomplice

SELECT *
    FROM phone_calls
        WHERE caller = '(027) 555-1068'
        AND year = 2021
        AND month = 7;

-- To determine if a possible accomplice ever called Sophia

SELECT *
    FROM phone_calls
    WHERE caller = '(375) 555-8161'
    AND year = 2021
    AND month = 7;

-- To find out more about Sophia's possible accomplice

SELECT *
    FROM people
        WHERE phone_number = '(375) 55-8161';

-- To see if the interviews table has any info to provide

.schema interviews

-- To look at the transcripts of the three interviews that occurred after this crime

SELECT name, transcript
    FROM interviews
        WHERE year = 2021
        AND month = 7
        AND day = 28;

-- To find if anyone made any phone calls around the time that the interviewee mentioned

SELECT *
    FROM phone_calls
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND duration < 60;

-- To find who it is that the suspected accomplice (Robin) called that day after the crime

SELECT *
    FROM people
        WHERE phone_number = '(367) 555-5533';


-- To find out whether Bruce, the man Robin called, had been driving in the bakery and when

SELECT *
    FROM bakery_security_logs
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND license_plate = '94KL13X';

-- To find out what information the atm_transactions table offers

.schema atm_transactions

-- To find out which bank accounts made a transaction on the day of the crime at Leggett Street

SELECT *
    FROM atm_transactions
        WHERE year = 2021
        AND month = 7
        AND day = 28
        AND atm_location = 'Leggett Street';

-- To find out what types of columns are in bank_accounts

.schema bank_accounts

-- To find out the account number of Bruce

SELECT *
    FROM bank_accounts
        WHERE person_id =
            (SELECT id
                FROM people
                    WHERE license_plate = '94KL13X')

-- To find out who Bruce called on the day of the crime, if anyone

SELECT *
    FROM people
        WHERE phone_number IN
            (SELECT receiver
                FROM phone_calls
                    WHERE caller = '(367) 555-5533'
                    AND year = 2021
                    AND month = 7
                    AND day = 28);

-- To see what the passengers table can give me

.schema passengers

-- To see if Bruce was a passenger on any flight

SELECT *
    FROM passengers
        WHERE passport_number =
            (SELECT passport_number
                FROM people
                    WHERE license_plate = '94KL13X');

-- To see what the flights table can give me

.schema flights

-- To see whether the flight Bruce was in was the earliest flight out of Fiftyville on the 29th, per the interview transcripts

SELECT *
    FROM flights
        WHERE year = 2021
        AND month = 7
        AND day = 29;

-- To see what the airports table can give me

.schema airports

-- To see the destination of Bruce's flight

SELECT *
    FROM airports
        WHERE id = 4;
