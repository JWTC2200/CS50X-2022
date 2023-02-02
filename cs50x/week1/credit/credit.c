#include <cs50.h>
#include <stdio.h>

long get_cardno(void);
int get_one(long cardno);
int get_two(long cardno);
int get_three(long cardno);
int get_four(long cardno);
int get_five(long cardno);
int get_six(long cardno);
int get_seven(long carndo);
int get_eight(long cardno);
int get_nine(long cardno);
int get_ten(long cardno);
int get_eleven(long cardno);
int get_twelve(long cardno);
int get_thirteen(long cardno);
int get_fourteen(long cardno);
int get_fifteen(long cardno);
int get_sixteen(long cardno);

int main(void)
{
    //ask cardnumber
    long cardno = get_cardno();
    //setting numbers 1-16 from input
    int one = get_one(cardno);
    int two = get_two(cardno);
    int three = get_three(cardno);
    int four = get_four(cardno);
    int five = get_five(cardno);
    int six = get_six(cardno);
    int seven = get_seven(cardno);
    int eight = get_eight(cardno);
    int nine = get_nine(cardno);
    int ten = get_ten(cardno);
    int eleven = get_eleven(cardno);
    int twelve = get_twelve(cardno);
    int thirteen = get_thirteen(cardno);
    int fourteen = get_fourteen(cardno);
    int fifteen = get_fifteen(cardno);
    int sixteen = get_sixteen(cardno);
    //double two and spliting numbers if answer is double digit
    int twox = two * 2;
    int twoxx = twox % 10;
    int twoxy = twox / 10;
    //double four and split
    int fourx = four * 2;
    int fourxx = fourx % 10;
    int fourxy = fourx / 10;
    //double six and split
    int sixx = six * 2;
    int sixxx = sixx % 10;
    int sixxy = sixx / 10;
    //double eight and split
    int eightx = eight * 2;
    int eightxx = eightx % 10;
    int eightxy = eightx / 10;
    //double 10 and split
    int tenx = ten * 2;
    int tenxx = tenx % 10;
    int tenxy = tenx / 10;
    //double 12 and split
    int twelvex = twelve * 2;
    int twelvexx = twelvex % 10;
    int twelvexy = twelvex / 10;
    //double 14 and split
    int fourteenx = fourteen * 2;
    int fourteenxx = fourteenx % 10;
    int fourteenxy = fourteenx / 10;
    //double 16 and split
    int sixteenx = sixteen * 2;
    int sixteenxx = sixteenx % 10;
    int sixteenxy = sixteenx / 10;

    //luhns check
    int luhns = one + twoxx + twoxy + three + fourxx + fourxy + five + sixxx + sixxy + seven + eightxx + eightxy + nine + tenxx + tenxy + eleven + twelvexx + twelvexy + thirteen + fourteenxx + fourteenxy + fifteen + sixteenxx + sixteenxy;
    //get remainder to get a single digit for use later when checking card numbers. If(luhnsx == 0 )
    int luhnsx = luhns % 10;
    printf("%i\n", luhnsx);

    //checking the numbers using card structure rules. Each also uses luhnsx == 0 to check for it meets that criteria as well

    //MASTERCARD always a 16 digit card 16th must be a 5 and 15th number between 1-5
    if (sixteen == 5 && (fifteen == 1 || fifteen == 2 || fifteen == 3 || fifteen == 4 || fifteen == 5) && luhnsx == 0)
    {
        printf("MASTERCARD\n");
    }
    //VISA starts with 4 on 16th or 13th digit. If its 13 digit card assume 14th to 16th digits is a 0.
    //384222222222222 would be a positive without excluding digits 15 & 14
    else if ((sixteen == 4 || (thirteen == 4 && sixteen == 0 && fifteen == 0 && fourteen == 0)) && luhnsx == 0)
    {
        printf("VISA\n");
    }
    //AMEX always 15th digit a 3 with 14th as 3 or 7
    //exclude 16th digit just in case
    else if (fifteen == 3 && (fourteen == 3 || fourteen == 7) && luhnsx == 0 && (sixteen == 0))
    {
        printf("AMEX\n");
    }
    //print INVALID if no above conditions are met
    else
    {
        printf("INVALID\n");
    }
}
//get cardnumber only if 0 or above
long get_cardno(void)
{
    long cardno;
    do
    {
        cardno = get_long("enter\n");

    }
    while (cardno <= 0);
    return cardno;
}
//reducing the card number into individual int
//get remainder with % then divide to get a single digit int
int get_one(long cardno)
{
    return cardno % 10;
}

int get_two(long cardno)
{
    return cardno % 100 / 10;
}

int get_three(long cardno)
{
    return cardno % 1000 / 100;
}

int get_four(long cardno)
{
    return cardno % 10000 / 1000;
}

int get_five(long cardno)
{
    return cardno % 100000 / 10000;
}

int get_six(long cardno)
{
    return cardno % 1000000 / 100000;
}

int get_seven(long cardno)
{
    return cardno % 10000000 / 1000000;
}

int get_eight(long cardno)
{
    return cardno % 100000000 / 10000000;
}

int get_nine(long cardno)
{
    return cardno % 1000000000 / 100000000;
}

int get_ten(long cardno)
{
    return cardno % 10000000000 / 1000000000;
}

int get_eleven(long cardno)
{
    return cardno % 100000000000 / 10000000000;
}

int get_twelve(long cardno)
{
    return cardno % 1000000000000 / 100000000000;
}

int get_thirteen(long cardno)
{
    return cardno % 10000000000000 / 1000000000000;
}

int get_fourteen(long cardno)
{
    return cardno % 100000000000000 / 10000000000000;
}

int get_fifteen(long cardno)
{
    return cardno % 1000000000000000 / 100000000000000;
}

int get_sixteen(long cardno)
{
    return cardno % 10000000000000000 / 1000000000000000;
}
