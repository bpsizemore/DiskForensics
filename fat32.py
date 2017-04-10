from tkinter import *

root = Tk()
T = Text(root, height=30, width=100)
T.pack()

def print_hex(d, s):
    print(d + ' '.join(map('{:02X}'.format, s)));


def print_dec(d, s):
    print(d + str(int.from_bytes(s, byteorder='little')))


def print_dir_entry(d, ):
    #print_hex('', d)
    if d[0] == 0x00: #If filename starts with 0x00 then then a file was never written there
        return

    elif d[0] == 0x05: #If file was previously deleted
        print("File previously deleted")
        print()
        return
    elif d[0] == 0x41:
        #print("Extended filename entry");
        #print();
        return

    T.insert(END, ('Filename: ' + str(d[0:8]) + '\n'))
    #print_hex('', d)
    T.insert(END, ("Starting cluster: " + str(int.from_bytes(d[26:28], byteorder='little')) + '\n'))
    T.insert(END, ("Filesize in Bytes: " + str(int.from_bytes(d[28:32], byteorder='little')) + '\n'))

    # iterate through fat entries
    fat_cluster = int.from_bytes(d[26:28], byteorder='little')
    file_start = root_dir + (fat_cluster - 2) * 512 - 64
    print(fat_cluster)
    while fat_cluster != 0:
        contents = data[file_start:file_start+512]
        i = 0
        while i < 512 and contents[i] != 0x00:
            i = i + 1

        T.insert(END, 'File Contents: ' + str(contents[0:i]))

        fat_cluster = 0;
    T.insert(END, '\n\n')
    # while data[(fat_start_offset + 4 * fat_cluster + 2)] != 0xFF:
    # swap to next fat cluster num and do stuff
    # print()

fat_partition = open("usb1.img", "rb")

data = fat_partition.read()
jump_instruction = data[0:3]
oem_name = data[3:11]
bytes_per_sector = data[11:13]
sectors_per_cluster = data[13]
reserved_sectors = data[14:16]
num_fats = data[16]
max_root_entries = data[17:19]
small_sectors = data[19:21]
media_type = data[21]
sectors_per_fat = data[22:24]
sectors_per_track = data[24:26]
num_heads = data[26:28]
hidden_sectors = data[28:32]
large_sectors = data[32:36]
disk_num = data[36]
curr_head = data[37] # not used in FAT
ex_sig = data[38]
volume_serial = data[39:43]
volume_label = data[43:54]
system_id = data[54:62]
sig = data[510:512]
fat_start_offset = reserved_sectors * 512

# found other document saying different info

sectors_per_fat = data[36:40]
root_dir_first_cluster = data[44:48]

print_hex("Jump instruction: ", jump_instruction)
print('Oem_name: ' + str(oem_name))
print_dec('Bytes per sector: ', bytes_per_sector)
print('Sectors per cluster: ', sectors_per_cluster)
print_dec('Reserved sectors: ', reserved_sectors)
print('Number of FATs: ', num_fats)
print_dec('Maximum number of Root Entries: ', max_root_entries)
print_dec('Sectors per FAT: ', sectors_per_fat)
print_dec('Sectors per track: ', sectors_per_track)
print_dec('Hidden sectors: ', hidden_sectors)
print_dec('Total number of sectors: ', large_sectors)
print_hex('Signature: ', sig)
print_dec('Root Dir starts at sector: ', root_dir_first_cluster)

root_dir = (520*2 + 32)*512 + 64
print()
T.insert(END, 'Directory listing follows... \n\n')
print()
print()

x = 0;
while data[root_dir+x] != 0x00:
    print_dir_entry(data[root_dir+x:root_dir+x+32])
    x = x + 32;

mainloop()




