#include <stdio.h>
#include <stdlib.h>

typedef union {
	unsigned int ui;
	unsigned char b4;
} Dword;

void printPartInfo(unsigned char *part, int partNum)
{
	printf("Partition %d:\n", partNum);
	int i;
	for (i=0; i<16; i++)
	{
		printf("%02x", part[i]);
	}
	printf("\n");

	if (part[0] == 0x80){
		printf("Bootable: true\n");
	} else {
		printf("Bootable: false\n");
	}

		
	printf("CHS value of first sector: %02x %02x %02x\n", part[1], part[2], part[3]);
	printf("Partition type: %02x\n", part[4]);
	printf("CHS value of last sector: %02x %02x %02x\n", part[5], part[6], part[7]);
	printf("LBA of first sector: %02x %02x %02x %02x\n", part[8], part[9], part[10], part[11]);
	
	Dword totalSectors = {part[12], part[13], part[14], part[15]};
	printf("Total Number of Sectors: %u\n", totalSectors.ui);
	printf("\n");
}

int main()
{
	printf("Partition Table:\n\n");
	unsigned char sectorZero[512];

	FILE *image;
	image = fopen("sdb.mbr", "r");
	fread(sectorZero, 1, 512, image);

	int x = 0;
	int i;
	unsigned char first[16];
	for (i=0; i<16; i++) {
		first[i] = sectorZero[x+i];
	}

	x = 16; //beginning of second partition entry
	unsigned char second[16];
	for (i=0; i<16; i++) {
		second[i] = sectorZero[x+i];
	}

	x = 32; //beginning of third partition entry
	unsigned char third[16];
	for (i=0; i<16; i++) {
		third[i] = sectorZero[x+i];
	}

	x = 48; //beginning of fourth partition entry
	unsigned char fourth[16];
	for (i=0; i<16; i++) {
		fourth[i] = sectorZero[x+i];
	}

	printPartInfo(first, 1);
	printPartInfo(second, 2);
	printPartInfo(third, 3);
	printPartInfo(fourth, 4);
}
