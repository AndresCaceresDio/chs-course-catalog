#include "helpers.h"
#include <math.h>
#include <stdio.h>

int d = 0;
int e = 0;
int f = 0;
int g = 0;

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float n = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            n = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0;
            image[i][j].rgbtRed = round(n);
            image[i][j].rgbtGreen = round(n);
            image[i][j].rgbtBlue = round(n);
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float sepiaRed = 0;
    float sepiaGreen = 0;
    float sepiaBlue = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            sepiaRed = (.393 * image[i][j].rgbtRed) + (.769 * image[i][j].rgbtGreen) + (.189 * image[i][j].rgbtBlue);
            sepiaGreen = (.349 * image[i][j].rgbtRed) + (.686 * image[i][j].rgbtGreen) + (.168 * image[i][j].rgbtBlue);
            sepiaBlue = (.272 * image[i][j].rgbtRed) + (.534 * image[i][j].rgbtGreen) + (.131 * image[i][j].rgbtBlue);
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            image[i][j].rgbtRed = round(sepiaRed);
            image[i][j].rgbtGreen = round(sepiaGreen);
            image[i][j].rgbtBlue = round(sepiaBlue);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int a = 0;
    int b = 0;
    int c = 0;
    int x = 0;
    int y = 0;
    int z = 0;
    for (int i = 0; i < height; i++)
    {
        a = image[i][width - 1].rgbtRed;
        b = image[i][width - 1].rgbtGreen;
        c = image[i][width - 1].rgbtBlue;
        x = image[i][0].rgbtRed;
        y = image[i][0].rgbtGreen;
        z = image[i][0].rgbtBlue;
        image[i][0].rgbtRed = a;
        image[i][0].rgbtGreen = b;
        image[i][0].rgbtBlue = c;
        image[i][width - 1].rgbtRed = x;
        image[i][width - 1].rgbtGreen = y;
        image[i][width - 1].rgbtBlue = z;
        if (width > 3)
        {
            a = image[i][width - 2].rgbtRed;
            b = image[i][width - 2].rgbtGreen;
            c = image[i][width - 2].rgbtBlue;
            x = image[i][1].rgbtRed;
            y = image[i][1].rgbtGreen;
            z = image[i][1].rgbtBlue;
            image[i][1].rgbtRed = a;
            image[i][1].rgbtGreen = b;
            image[i][1].rgbtBlue = c;
            image[i][width - 2].rgbtRed = x;
            image[i][width - 2].rgbtGreen = y;
            image[i][width - 2].rgbtBlue = z;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j].rgbtRed = image[i][j].rgbtRed;
            copy[i][j].rgbtGreen = image[i][j].rgbtGreen;
            copy[i][j].rgbtBlue = image[i][j].rgbtBlue;
        }
    }
    for (int w = 0; w < height; w++)
    {
        for (int l = 0; l < width; l++)
        {
            for (int o = -1; o < 2; o++)
            {
                for (int p = -1; p < 2; p++)
                {
                    if ((w + o) >= 0 && (w + o) <= height && (l + p) >= 0 && (l + p) <= width)
                    {
                        d += copy[w + o][l + p].rgbtRed;
                        e += copy[w + o][l + p].rgbtGreen;
                        f += copy[w + o][l + p].rgbtBlue;
                        g++;
                    }
                }
            }
            image[w][l].rgbtRed = round((float) d / g);
            image[w][l].rgbtGreen = round((float) e / g);
            image[w][l].rgbtBlue = round((float) f / g);
            d = 0;
            e = 0;
            f = 0;
            g = 0;
        }
    }
    return;
}