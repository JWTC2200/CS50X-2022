#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
//byte data type
typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    //check one command line argument //return 1
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    //open file
    FILE *file = fopen(argv[1], "r");

    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 1;
    }
    //512 BYTE buffer
    BYTE buffer[512];
    //filename
    char imagebuffer[10];
    //file store
    FILE *img = NULL;
    //file count
    int count = 0;
    //read file
    while ((fread(&buffer, 512, 1, file)) == 1)
    {
        //search for jpeg start
        if (buffer[0] == 0xff & buffer[1] == 0xd8 & buffer[2] == 0xff & (buffer[3] & 0xf0) == 0xe0)
        {
            //first image check
            if (count > 0)
            {
                fclose(img); //close previous image
            }
            sprintf(imagebuffer, "%0.3i.jpg", count); //image number
            img = fopen(imagebuffer, "w");
            count++; //move on file number
        }
        if (count != 0) // >0 or else no header found
        {
            //continue writing to file
            fwrite(buffer, 512, 1, img);
        }
    }
    fclose(img);
    fclose(file);

    //if valid create file
    // 00n.jpg

    //sprintf(photos, "%03i.jpg", n?);
    //stop if next jpeg detected

    // FILE *img = fopen(filename, "w");
    // fwrite(data, size, 1, filename)
    //loop continues?


}