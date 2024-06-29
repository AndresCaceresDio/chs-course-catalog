#include <stdint.h>
#include <stdio.h>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

#include "wav.h"

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        printf("Usage: ./reverse input.wav output.wav\n");
        return 1;
    }

    FILE *input_file = fopen(argv[1], "r");
    if (input_file == NULL)
    {
        printf("ERROR: invalid input file\n");
        return 1;
    }

    WAVHEADER input_header;
    fread(&input_header, sizeof(WAVHEADER), 1, input_file);

    if (check_format(input_header) == 1)
    {
        return 1;
    }

    FILE *output_file = fopen(argv[2], "w");
    if (output_file == NULL)
    {
        printf("ERROR: invalid output file\n");
        return 1;
    }

    fwrite(&input_header, sizeof(WAVHEADER), 1, output_file);

    int block_size = get_block_size(input_header);
    int data_size = 46000;
    int output_data[data_size];

    for (int i = data_size; i > -1; i--)
    {
        fread(&output_data[i], sizeof(int), 2, input_file);
    }

    for (int i = 0; i < data_size; i++)
    {
        fwrite(&output_data[i], sizeof(int), 2, output_file);
    }

    fclose(input_file);
    fclose(output_file);
    return 0;
}

int check_format(WAVHEADER header)
{
    if (header.format[0] == 'W' && header.format[1] == 'A' && header.format[2] == 'V' && header.format[3] == 'E')
    {
        return 0;
    }
    return 1;
}

int get_block_size(WAVHEADER header)
{
    int x = header.numChannels;
    int y = header.bitsPerSample / 8;
    return (x * y);
}
