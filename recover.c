#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[])
{
    FILE *img = 0;
    int n = 0;
    char filename[8] = {0};
    char *t = "000.jpg";
    strcpy(filename, t);
    FILE *file = fopen(argv[1], "r");
    typedef uint8_t BYTE;
    BYTE buffer[512];

    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }
    else if (argc == 2)
    {
        for (int i = 0; i < 1000; i++)
        {
            fread(buffer, 1, 512, file);
            if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
            {
                if (strcmp(filename, "000.jpg") == 0)
                {
                    img = fopen(filename, "w");
                    fwrite(buffer, 1, 512, img);
                    t = "999.jpg";
                    strcpy(filename, t);
                }
                else
                {
                    n++;
                    fclose(img);
                    sprintf(filename, "%03i.jpg", n);
                    img = fopen(filename, "w");
                    fwrite(buffer, 1, 512, img);
                }
            }
            else if (buffer[0] != 0xff && img != 0)
            {
                fwrite(buffer, 1, 512, img);
            }
        }
    }
    return 0;
    fclose(file);
}