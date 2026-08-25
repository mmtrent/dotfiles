## Arch Linux Config notes


## 4K Display
- Scaling set in .Xresources
    - xft.dpi of 192 is 200% scaling, 144 is 150%

## Managing dotfiles with git
- Current alias in .zshrc
    - alias config='/usr/bin/git --git-dir=$HOME/dotfiles/ --work-tree=$HOME'

- Starting from scratch:
    1. git init --bare $HOME/.cfg
    2. alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'
    3. config config --local status.showUntrackedFiles no
    4. echo "alias config='/usr/bin/git --git-dir=$HOME/.cfg/ --work-tree=$HOME'" >> $HOME/.bashrc
