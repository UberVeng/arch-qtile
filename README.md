# Arch-qtile
<img src="https://i.imgur.com/otd883Q.png">

# Full installation guide
##### Check internet connection and update clock
```sh
ping 8.8.8.8
timedatectl set-ntp true
```
##### Find the disk you want to partition
```sh
fdisk -l
```
##### Patition the disk \[+4G non encrypted/+8G ecnrypted]
### First partition should be 'Linux swap / Solaris', second -  'Linux LVM' or 'Linux'
```sh
fdisk /dev/sda

>> o

>> n
>>
>>
>> +8G

>> n
>>
>>
>>

>> t
>> 1
>> 19

>> t
>> 2
>> 30

>>p
>> w
```
***
### 1) Method with encryption
##### Encrypt partition
```sh
cryptsetup -y --use-random luksFormat /dev/sda2
>> YES
>> password
>> password
cryptsetup open --type luks /dev/sda2 crypt_name
lsblk
pvcreate /dev/mapper/crypt_name
vgcreate crypt_vg_name /dev/mapper/crypt_name
lvcreate -n swap -L 4G crypt_vg_name
lvcreate -n root -l 100%FREE crypt_vg_name
mkfs.ext4 /dev/crypt_vg_name/root
mkswap /dev/crypt_vg_name/swap
swapon /dev/crypt_vg_name/swap
mount /dev/crypt_vg_name/root /mnt
```
***
### 2) Method with LVM 
```sh
pvcreate /dev/sda2
vgcreate vg /dev/sda2
lvcreate -n root -l +100%FREE vg
mkfs.ext4 /dev/sda2
mkswap /dev/sda1
swapon /dev/sda1
mount /dev/vg/root /mnt
```
***
### 3) Method without encryption or LVM
##### Make a swap
```sh
mkswap /dev/sda1
swapon /dev/sda1
```
##### set file system of sda2
```sh
mkfs.ext4 /dev/sda2
```
##### Mount the file system
```sh
mount /dev/sda2 /mnt
```
***
### Proceed after you setted up file system using one of 3 methods
##### Download some basic stuff
```sh
pacstrap /mnt base linux linux-firmware git vim lvm2
```
##### Fstab
```sh
genfstab -U /mnt >> /mnt/etc/fstab
```
##### Chroot
```sh
arch-chroot /mnt
```
##### Clone repository
```sh
git clone https://github.com/UberVeng/arch-qtile
cd arch-qtile
```
##### Edit one of this files
```sh
vim install-bios.sh
vim install-uefi.sh 
```
##### Add permistion to execute
```sh
chmod +x install-bios.sh
chmod +x install-uefi.sh
```
##### Execute one of this
```sh
cd /
/arch-basic/install-bios.sh
/arch-basic/install-uefi.sh
```
#####
```sh
lsblk -f
```
***
##### Copy UUID of sda2 (encrypted only)
```sh
vim /etc/default/grub
```
replace 'quiet' with:
```sh
GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 cryptdevice=UUID=*UUID GOES HERE*:luks:allow-discards"
```
```sh
cp /usr/share/locale/en\@quot/LC_MESSAGES/grub.mo /boot/grub/locale/en.mo
grub-mkconfig -o /boot/grub/grub.cfg
```
```sh
vim /etc/fstab
>> tmpfs    /tmp    tmpfs    defaults,noatime,mode=1777    0 0
```
***
##### Edit 
```sh
vim /etc/mkinitcpio.conf
>> MODULES=(nouveau)
>> HOOKS=(base systemd autodetect modconf block encrypt lvm2 filesystems...)
mkinitcpio -p linux
```

##### Exit, unmount and reboot
```sh
exit
umount -a
reboot
```
# Qtile
##### Login as root
```sh
root
password
```
##### Edit visudo file
```sh
pacman -S sudo
EDITOR=vim visudo
uber ALL=(ALL) ALL
exit
```
##### Change password
```sh
uber
password
passwd
```
##### Install qtile and other stuff
```sh
sudo pacman -S qtile xorg kitty nitrogen picom lightdm lightdm-gtk-greeter firefox pcmanfm lxappearance arc-gtk-theme arc-icon-theme
```
##### Enable lightdm on boot
```sh
sudo systemctl enable lightdm
```
##### Reboot
```sh
reboot
```

### Move config files to your home diercory
```sh
mv /arch-qtile/ ~/Documents/
cd ~/Documents/arch-qtile/qtile/
cp autostart.sh config.py ~/.config/qtile/
cd ..
cp kitty/kitty.conf ~/.config/kitty/
cp picom/picom.conf ~/.config/picom
cd
cd Pictures
mkdir wallpapers
cd Documents/arch-qtile/wallpapers
cp chitoge-yellow-2.jpg
reboot

```
