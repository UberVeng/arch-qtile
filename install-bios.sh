#!/bin/bash

ln -sf /usr/share/zoneinfo/Asia/Novosibirsk /etc/localtime
hwclock --systohc
sed -i '177s/.//' /etc/locale.gen
locale-gen
echo "LANG=en_US.UTF-8" >> /etc/locale.conf
echo "KEYMAP=us" >> /etc/vconsole.conf
echo "arch" >> /etc/hostname
echo "127.0.0.1 localhost" >> /etc/hosts
echo "::1       localhost" >> /etc/hosts
echo "127.0.1.1 arch.localdomain arch" >> /etc/hosts
echo root:password | chpasswd

# You can add xorg to the installation packages, I usually add it at the DE or WM install script
# You can remove the tlp package if you are installing on a desktop or vm

pacman -S --noconfirm grub efibootmgr networkmanager network-manager-applet dialog linux-headers xdg-user-dirs xdg-utils bash-completion cups firewalld openssh lvm2 dosfstools os-prober mtools

# pacman -S --noconfirm xf86-video-amdgpu
# pacman -S --noconfirm nvidia nvidia-utils nvidia-settings

grub-install --target=i386-pc /dev/sda
grub-mkconfig -o /boot/grub/grub.cfg

systemctl enable NetworkManager
systemctl enable cups.service
systemctl enable sshd
systemctl enable libvirtd
systemctl enable firewalld

useradd -m -g users -G wheel uber
echo uber:password | chpasswd

echo "uber ALL=(ALL) ALL" >> /etc/sudoers.d/uber
echo "%wheel ALL=(ALL) ALL" >> /etc/sudoers.d/uber


printf "\e[1;32mDone! Type exit, umount -a and reboot.\e[0m"
