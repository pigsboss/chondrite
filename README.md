# CHONDRITE - Chondrite Hands-ON Data Reduction Integrate Tools Ensemble
## Environment
### macOS with Apple silicon (M1/M2 chips)
#### Z shell
*Shell* 是用户或其他应用程序与计算机操作系统进行交互的功能界面，其本身也是一种计算机程序。
常用的 shell 程序包含 bash, csh, zsh 等命令行界面，
也包含 Windows 及 macOS 等操作系统的图形用户界面（GUI）。

过去，macOS 的默认 Shell 与 Linux 操作系统一样，均为 bash；
后来，由于授权等原因，macOS 改为使用 zsh.

用户通过硬件终端与 Shell 交互，并最终与计算机交互。终端包含键盘、显示器与鼠标三件套。
由于过去的用户终端仅支持显示固定行高、列宽的字母与数字，而无法显示高分辨率的图像内容，
鼠标也仅仅用于快速移动输入文字的光标，导致目前图形用户界面已经成为主流交互方式之后，
运行命令行 Shell 的计算机程序常常也被称为终端模拟器。

当用于通过桌面图标等方式，运行 macOS 的终端模拟器（默认为 Terminal 应用）时，
zsh 即自动运行，并提供当前用户登入的会话（Session）。
下文将终端模拟器简称为终端。

所谓会话（Session），是指被授权的用户通过特定的 Shell 与计算机的交互过程。
会话随着用户登入开始，用户注销后会话即结束。
与用户交互及应用软件运行的环境变量也将加载到会话中。
会话启动之后，将自动调用 `~/.zshrc` 脚本（`~/` 指当前用户的主目录）以加载本次会话的资源，包括环境变量。

我们可以创建一个跨 Shell 使用的配置文件 `~/.profile`
以便于在包含其他操作系统的局域网内面向跨操作系统的用户提供尽可能一致的环境变量，
并在 `~/.zshrc` 加载该文件。

```zsh
[[ -e ~/.profile ]] && emulate sh -c 'source ~/.profile'
```

初次启动终端，安装必要的工具（包括 git, bash 等等）：

```zsh
xcode-select --install
```


#### Homebrew, the missing package manager for macOS
由于 *Homebrew* 资源经常难以访问，或即便能够访问，也难以获得令人满意的体验，我们推荐通过镜像访问。
推荐的镜像是清华大学开源软件镜像站。
在 `~/.profile` 添加并设置以下环境变量，从而使得每次启动会话时，自动配置镜像。

```zsh
export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"
export HOMEBREW_PIP_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"
```

从镜像下载安装脚本并安装 Homebrew:

```zsh
git clone --depth=1 https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/install.git brew-install
/bin/bash brew-install/install.sh
rm -rf brew-install
```

安装完成后，将 brew 及其他相关程序的路径添加到环境变量，在 `~/.profile` 添加：

```zsh
eval "$(/opt/homebrew/bin/brew shellenv)"
```
