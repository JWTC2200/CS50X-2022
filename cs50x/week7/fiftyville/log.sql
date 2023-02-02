-- Keep a log of any SQL queries you execute as you solve the mystery.

-- trying to discover more details about the crime

SELECT id, year, month, day, street, description
FROM crime_scene_reports;
-- ID 295, Year 2021, Month 7 (July), Day 28, Humphrey Street, took place at 10.15am. Bakery.
-- Three witnesses present at time. interview transcripts

SELECT id, name, year, month, day, transcript
FROM interviews
WHERE transcript
LIKE "%bakery%";
-- full results, Kiana doesn't seem to be a relevant entry?
-- 1. within 10 minutes theif drove off, up to 10.25am.
-- 2. Eugene recognised them before 10.15am. near ATM withdrawing money from Leggett street
-- 3. Raymond. Thief made 1 minute call. while leaving so 10.15 to 10.25am. earliest flight out of fiftyville next day (29th July?). helper purchases flight ticket. between 10.15am and flight time?

SELECT id, account_number, transaction_type, amount
FROM atm_transactions
WHERE year = 2021 AND month = 7 AND day = 28 AND atm_location = "Leggett Street";
-- list of atm information for that day.
-- get names of all people who used atm to withdraw
Select name
FROM people
JOIN bank_accounts
ON bank_accounts.person_id = people.id
WHERE id
    IN (SELECT person_id
    FROM bank_accounts
    WHERE account_number
        IN (SELECT account_number
        FROM atm_transactions
        WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street"
        )
);

-- check phone calls on the day that were < 60seconds
SELECT id, caller, receiver, duration
FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;
-- get names of people making calls
SELECT name
FROM people
WHERE phone_number
    IN(SELECT caller
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration <60);

-- check bakery security logs using time references
SELECT id, activity, license_plate, minute
FROM bakery_security_logs
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;
-- list of cars leaving bakery between 10.15 and 10.25
-- get owners of cars leaving
Select name
FROM people
WHERE license_plate
    IN (SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25);

-- combine 3 lists to see who used used ATM, owned a car that drove away and made a <60s phone call that day.
Select name
FROM people
WHERE license_plate
    IN (SELECT license_plate
    FROM bakery_security_logs
    WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)
INTERSECT
SELECT name
FROM people
WHERE phone_number
    IN(SELECT caller
    FROM phone_calls
    WHERE year = 2021 AND month = 7 AND day = 28 AND duration <60)
INTERSECT
SELECT name
FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
WHERE id
    IN (SELECT person_id
    FROM bank_accounts
    WHERE account_number
        IN (SELECT account_number
        FROM atm_transactions
        WHERE year = 2021 AND month = 7 AND day = 28 AND transaction_type = "withdraw" AND atm_location = "Leggett Street"
        )
    )
;
-- 2 results. Bruce and Diana.
-- check who went on a plane?

-- check earliest flight next day and destination
SELECT abbreviation, full_name, city
FROM airports
WHERE id =
    (SELECT destination_airport_id
    FROM flights
    WHERE year = 2021 AND month = 7 AND day = 29
    ORDER BY(hour)
    LIMIT 1)
;
-- earliest flight goes to LGA, laGuardia Airport, New York City.
--check Diana
select city
from airports
where id IN (select destination_airport_id
from flights
Where id IN (SELECT flight_id
FROM passengers
WHERE passport_number = (Select passport_number from people where name = "Diana")));
-- returns Dallas, Boston, Fiftyville - did not go to New York
-- check Bruce
select city
from airports
where id IN (select destination_airport_id
from flights
Where id IN (SELECT flight_id
FROM passengers
WHERE passport_number = (Select passport_number from people where name = "Bruce")));
--New York City - Bruce confirmed as thief

-- find accomplice search phone calls.
-- everyone Bruce called filtered for date and call duration. 
select name
from people
where phone_number
    IN(select receiver
from phone_calls
where caller
    IN (SELECT phone_number
    FROM people
    WHERE name = "Bruce")
AND year = 2021
AND month = 7
AND day = 28
AND duration < 60);
-- add constraints = Robin
