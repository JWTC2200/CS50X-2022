#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{

    //for height h loop
    //for width w loop
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            //calculate average darkness
            float grayav = ((image[h][w].rgbtRed) + (image[h][w].rgbtGreen) + (image[h][w].rgbtBlue)) / 3.0;
            int grayint = round(grayav);

            image[h][w].rgbtRed = grayint;
            image[h][w].rgbtGreen = grayint;
            image[h][w].rgbtBlue = grayint;
        }
    }
    // image h w .red./green/blue = XYZ
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
            //apply formula
        {
            float sRedf = (0.393 * image[h][w].rgbtRed) + (0.769 * image[h][w].rgbtGreen) + (0.189 * image[h][w].rgbtBlue);
            int sRedi = round(sRedf);
            //cap value at 255
            if (sRedi >= 255)
            {
                sRedi = 255;
            }
            float sGreenf = (0.349 * image[h][w].rgbtRed) + (0.686 * image[h][w].rgbtGreen) + (0.168 * image[h][w].rgbtBlue);
            int sGreeni = round(sGreenf);
            if (sGreeni >= 255)
            {
                sGreeni = 255;
            }
            float sBluef = (0.272 * image[h][w].rgbtRed) + (0.534 * image[h][w].rgbtGreen) + (0.131 * image[h][w].rgbtBlue);
            int sBluei = round(sBluef);
            if (sBluei >= 255)
            {
                sBluei = 255;
            }
            image[h][w].rgbtRed = sRedi;
            image[h][w].rgbtGreen = sGreeni;
            image[h][w].rgbtBlue = sBluei;
        }
    }

    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width / 2; w++)
        {
            RGBTRIPLE refstore = image[h][w];
            image[h][w] = image[h][width - 1 - w];
            image[h][width - 1 - w] = refstore;
        }

    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    float float_red;
    float float_green;
    float float_blue;
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            //store copy for calculations
            copy[h][w] = image[h][w];
        }
    }
    for (int h = 0; h < height; h++)
    {
        for (int w = 0; w < width; w++)
        {
            //top left corner
            if (h == 0 && w == 0) //h+1 w+1 //4 inputs
            {
                float_red = (copy[h][w].rgbtRed + copy[h][w + 1].rgbtRed + copy[h + 1][w].rgbtRed + copy[h + 1][w + 1].rgbtRed) / 4.0;
                float_green = (copy[h][w].rgbtGreen + copy[h][w + 1].rgbtGreen + copy[h + 1][w].rgbtGreen + copy[h + 1][w + 1].rgbtGreen) / 4.0;
                float_blue = (copy[h][w].rgbtBlue + copy[h][w + 1].rgbtBlue + copy[h + 1][w].rgbtBlue + copy[h + 1][w + 1].rgbtBlue) / 4.0;
                image[h][w].rgbtRed = round(float_red);
                image[h][w].rgbtGreen = round(float_green);
                image[h][w].rgbtBlue = round(float_blue);
            }
            //top right corner
            else if (h == 0 && w == width - 1) //h+1 w-1 //4 inputs
            {
                float_red = (copy[h][w].rgbtRed + copy[h][w - 1].rgbtRed + copy[h + 1][w].rgbtRed + copy[h + 1] [w - 1].rgbtRed) / 4.0;
                float_green = (copy[h][w].rgbtGreen + copy[h][w - 1].rgbtGreen + copy[h + 1][w].rgbtGreen + copy[h + 1] [w - 1].rgbtGreen) / 4.0;
                float_blue = (copy[h][w].rgbtBlue + copy[h][w - 1].rgbtBlue + copy[h + 1][w].rgbtBlue + copy[h + 1] [w - 1].rgbtBlue) / 4.0;
                image[h][w].rgbtRed = round(float_red);
                image[h][w].rgbtGreen = round(float_green);
                image[h][w].rgbtBlue = round(float_blue);
            }
            //bottom left corner
            else if (h == height - 1 && w == 0) //h-1 w+1 // 4 inputs
            {
                float_red = (copy[h][w].rgbtRed + copy[h - 1][w].rgbtRed + copy[h - 1][w + 1].rgbtRed + copy[h][w + 1].rgbtRed) / 4.0;
                float_green = (copy[h][w].rgbtGreen + copy[h - 1][w].rgbtGreen + copy[h - 1][w + 1].rgbtGreen + copy[h][w + 1].rgbtGreen) / 4.0;
                float_blue = (copy[h][w].rgbtBlue + copy[h - 1][w].rgbtBlue + copy[h - 1][w + 1].rgbtBlue + copy[h][w + 1].rgbtBlue) / 4.0;
                image[h][w].rgbtRed = round(float_red);
                image[h][w].rgbtGreen = round(float_green);
                image[h][w].rgbtBlue = round(float_blue);
            }
            //bottom right corner
            else if (h == height - 1 && w == width - 1) //h-1 w-1 // 4 inputs
            {
                float_red = (copy[h][w].rgbtRed + copy[h][w - 1].rgbtRed + copy[h - 1][w].rgbtRed + copy[h - 1][w - 1].rgbtRed) / 4.0;
                float_green = (copy[h][w].rgbtGreen + copy[h][w - 1].rgbtGreen + copy[h - 1][w].rgbtGreen + copy[h - 1][w - 1].rgbtGreen) / 4.0;
                float_blue = (copy[h][w].rgbtBlue + copy[h][w - 1].rgbtBlue + copy[h - 1][w].rgbtBlue + copy[h - 1][w - 1].rgbtBlue) / 4.0;
                image[h][w].rgbtRed = round(float_red);
                image[h][w].rgbtGreen = round(float_green);
                image[h][w].rgbtBlue = round(float_blue);
            }
            //top middle
            else if (h == 0) //h+1 w+-1 /6 inputs
            {
                float_red = (copy[h][w].rgbtRed + copy[h][w - 1].rgbtRed + copy[h][w + 1].rgbtRed +
                             copy[h + 1][w - 1].rgbtRed + copy[h + 1][w].rgbtRed + copy[h + 1][w + 1].rgbtRed) / 6.0;
                float_green = (copy[h][w].rgbtGreen + copy[h][w - 1].rgbtGreen + copy[h][w + 1].rgbtGreen +
                               copy[h + 1][w - 1].rgbtGreen + copy[h + 1][w].rgbtGreen + copy[h + 1][w + 1].rgbtGreen) / 6.0;
                float_blue = (copy[h][w].rgbtBlue + copy[h][w - 1].rgbtBlue + copy[h][w + 1].rgbtBlue +
                              copy[h + 1][w - 1].rgbtBlue + copy[h + 1][w].rgbtBlue + copy[h + 1][w + 1].rgbtBlue) / 6.0;
                image[h][w].rgbtRed = round(float_red);
                image[h][w].rgbtGreen = round(float_green);
                image[h][w].rgbtBlue = round(float_blue);
            }
            //bottom middle
            else if (h == height - 1) //h-1 w+-1 / 6 inputs
            {
                float_red = (copy[h][w].rgbtRed + copy[h - 1][w - 1].rgbtRed + copy[h - 1][w].rgbtRed +
                             copy[h - 1][w + 1].rgbtRed + copy[h][w - 1].rgbtRed + copy[h][w + 1].rgbtRed) / 6.0;
                float_green = (copy[h][w].rgbtGreen + copy[h - 1][w - 1].rgbtGreen + copy[h - 1][w].rgbtGreen +
                               copy[h - 1][w + 1].rgbtGreen + copy[h][w - 1].rgbtGreen + copy[h][w + 1].rgbtGreen) / 6.0;
                float_blue = (copy[h][w].rgbtBlue + copy[h - 1][w - 1].rgbtBlue + copy[h - 1][w].rgbtBlue +
                              copy[h - 1][w + 1].rgbtBlue + copy[h][w - 1].rgbtBlue + copy[h][w + 1].rgbtBlue) / 6.0;
                image[h][w].rgbtRed = round(float_red);
                image[h][w].rgbtGreen = round(float_green);
                image[h][w].rgbtBlue = round(float_blue);
            }
            //left side
            else if (w == 0) //h+-1 w+1 // 6 inputs
            {
                float_red = (copy[h][w].rgbtRed + copy[h - 1][w].rgbtRed + copy[h - 1][w + 1].rgbtRed +
                             copy[h][w + 1].rgbtRed + copy[h + 1][w].rgbtRed + copy[h + 1][w + 1].rgbtRed) / 6.0;
                float_green = (copy[h][w].rgbtGreen + copy[h - 1][w].rgbtGreen + copy[h - 1][w + 1].rgbtGreen +
                               copy[h][w + 1].rgbtGreen + copy[h + 1][w].rgbtGreen + copy[h + 1][w + 1].rgbtGreen) / 6.0;
                float_blue = (copy[h][w].rgbtBlue + copy[h - 1][w].rgbtBlue + copy[h - 1][w + 1].rgbtBlue +
                              copy[h][w + 1].rgbtBlue + copy[h + 1][w].rgbtBlue + copy[h + 1][w + 1].rgbtBlue) / 6.0;
                image[h][w].rgbtRed = round(float_red);
                image[h][w].rgbtGreen = round(float_green);
                image[h][w].rgbtBlue = round(float_blue);
            }
            //right side
            else if (w == width - 1) //h+-1 w-1 // 6 inputs
            {
                float_red = (copy[h][w].rgbtRed + copy[h - 1][w - 1].rgbtRed + copy[h - 1][w].rgbtRed +
                             copy[h][w - 1].rgbtRed + copy[h + 1][w - 1].rgbtRed + copy[h + 1][w].rgbtRed) / 6.0;
                float_green = (copy[h][w].rgbtGreen + copy[h - 1][w - 1].rgbtGreen + copy[h - 1][w].rgbtGreen +
                               copy[h][w - 1].rgbtGreen + copy[h + 1][w - 1].rgbtGreen + copy[h + 1][w].rgbtGreen) / 6.0;
                float_blue = (copy[h][w].rgbtBlue + copy[h - 1][w - 1].rgbtBlue + copy[h - 1][w].rgbtBlue +
                              copy[h][w - 1].rgbtBlue + copy[h + 1][w - 1].rgbtBlue + copy[h + 1][w].rgbtBlue) / 6.0;
                image[h][w].rgbtRed = round(float_red);
                image[h][w].rgbtGreen = round(float_green);
                image[h][w].rgbtBlue = round(float_blue);
            }
            else
            {
                float_red = (copy[h][w].rgbtRed + copy[h - 1][w].rgbtRed + copy[h + 1][w].rgbtRed + copy[h][w + 1].rgbtRed +
                             copy[h][w - 1].rgbtRed + copy[h - 1][w - 1].rgbtRed + copy[h - 1][w + 1].rgbtRed +
                             copy[h + 1][w - 1].rgbtRed + copy[h + 1][w + 1].rgbtRed) / 9.0;
                float_green = (copy[h][w].rgbtGreen + copy[h - 1][w].rgbtGreen + copy[h + 1][w].rgbtGreen +
                               copy[h][w + 1].rgbtGreen + copy[h][w - 1].rgbtGreen + copy[h - 1][w - 1].rgbtGreen +
                               copy[h - 1][w + 1].rgbtGreen + copy[h + 1][w - 1].rgbtGreen + copy[h + 1][w + 1].rgbtGreen) / 9.0;
                float_blue = (copy[h][w].rgbtBlue + copy[h - 1][w].rgbtBlue + copy[h + 1][w].rgbtBlue +
                              copy[h][w + 1].rgbtBlue + copy[h][w - 1].rgbtBlue + copy[h - 1][w - 1].rgbtBlue +
                              copy[h - 1][w + 1].rgbtBlue + copy[h + 1][w - 1].rgbtBlue + copy[h + 1][w + 1].rgbtBlue) / 9.0;

                image[h][w].rgbtRed = round(float_red);
                image[h][w].rgbtGreen = round(float_green);
                image[h][w].rgbtBlue = round(float_blue);
            }

        }
    }
    return;
}
